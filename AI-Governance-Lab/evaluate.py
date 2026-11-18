import argparse,json,re
EMAIL=re.compile(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}')

def evaluate(case):
    text=case['response']; folded=text.casefold()
    required=case.get('required',[]); forbidden=case.get('forbidden',[])
    if any(not isinstance(x,str) or not x.strip() for x in required+forbidden): raise ValueError('Empty or invalid rule')
    checks={'required_phrases':all(x.casefold() in folded for x in required),'forbidden_phrases':all(x.casefold() not in folded for x in forbidden)}
    if case.get('no_email',False): checks['email_pattern_absent']=EMAIL.search(text) is None
    return {'id':case['id'],'passed':all(checks.values()),'checks':checks}

def report(cases):
    ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate case ID')
    results=[evaluate(c) for c in cases]; stats={}
    for r in results:
        for name,passed in r['checks'].items():
            s=stats.setdefault(name,{'passed':0,'total':0});s['total']+=1;s['passed']+=int(passed)
    passed=sum(r['passed'] for r in results)
    return {'total':len(results),'passed':passed,'pass_rate':passed/len(results) if results else None,'rules':stats,'cases':results}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cases');p.add_argument('--strict',action='store_true');a=p.parse_args()
    with open(a.cases,encoding='utf8') as f: r=report(json.load(f))
    print(json.dumps(r,indent=2))
    if a.strict and (not r['total'] or r['passed']!=r['total']): raise SystemExit(1)
