import argparse, json, os, urllib.request
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Task:
    id: str
    tool: str
    dependencies: tuple[str, ...] = ()
    approval: bool = False
    retries: int = 0


def run(tasks: list[Task], tools: dict[str, Callable], approved=()):
    by_id = {t.id: t for t in tasks}
    if len(by_id) != len(tasks):
        raise ValueError('Duplicate task ID')
    for t in tasks:
        if not 0 <= t.retries <= 3 or t.tool not in tools or any(d not in by_id for d in t.dependencies):
            raise ValueError(f'Invalid task: {t.id}')
    pending, order = dict(by_id), []
    while pending:
        ready = [t for t in pending.values() if all(d not in pending for d in t.dependencies)]
        if not ready:
            raise ValueError('Cyclic dependencies')
        for t in ready:
            order.append(t); pending.pop(t.id)
    results, audit = {}, []
    for t in order:
        if any(results[d]['status'] != 'ok' for d in t.dependencies):
            results[t.id] = {'status': 'blocked_dependency'}
        elif t.approval and t.id not in approved:
            results[t.id] = {'status': 'approval_required'}
        else:
            for attempt in range(1, t.retries + 2):
                try:
                    value = tools[t.tool]({d: results[d]['value'] for d in t.dependencies})
                    results[t.id] = {'status': 'ok', 'value': value}
                    audit.append({'task': t.id, 'attempt': attempt, 'status': 'ok'})
                    break
                except Exception as exc:
                    # Avoid recording potentially sensitive exception text.
                    results[t.id] = {'status': 'failed', 'error_type': type(exc).__name__}
                    audit.append({'task': t.id, 'attempt': attempt, 'status': 'failed'})
        if results[t.id]['status'].startswith(('blocked', 'approval')):
            audit.append({'task': t.id, 'status': results[t.id]['status']})
    return {'results': results, 'audit': audit}


def chat_draft(context):
    url, model = os.environ['AI_CHAT_URL'], os.environ['AI_MODEL']
    if not url.startswith(('https://', 'http://localhost:', 'http://127.0.0.1:')):
        raise ValueError('Use HTTPS or a local HTTP endpoint')
    headers = {'Content-Type': 'application/json'}
    if os.environ.get('AI_API_KEY'):
        headers['Authorization'] = 'Bearer ' + os.environ['AI_API_KEY']
    body = {'model': model, 'messages': [{'role': 'system', 'content': 'Draft a brief using only the supplied synthetic facts. Label unknowns.'}, {'role': 'user', 'content': json.dumps(context)}]}
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read(1000000))
    return result['choices'][0]['message']['content']


def demo(approved=(), use_model=False):
    tasks = [Task('research', 'research'), Task('risk', 'risk'), Task('brief', 'draft', ('research','risk'), retries=1), Task('publish','marker',('brief',),approval=True)]
    tools = {'research': lambda _: ['Synthetic client needs document search and audit logs'],
             'risk': lambda _: ['Privacy review required; pilot metrics not yet known'],
             'draft': chat_draft if use_model else lambda c: '\n'.join(c['research'] + c['risk']),
             'marker': lambda c: {'draft_ready': True, 'content': c['brief']}}
    return run(tasks, tools, approved)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--approve', action='append', default=[])
    parser.add_argument('--model', action='store_true')
    args = parser.parse_args()
    print(json.dumps(demo(args.approve,args.model), indent=2))
