import unittest
from agentforge import Task,run,demo
class Tests(unittest.TestCase):
    def test_gate(self):
        self.assertEqual(demo()['results']['publish']['status'],'approval_required')
        self.assertEqual(demo(['publish'])['results']['publish']['status'],'ok')
    def test_cycle(self):
        with self.assertRaises(ValueError): run([Task('a','x',('a',))],{'x':lambda _:0})
    def test_retry(self):
        calls=[]
        def flaky(_):
            calls.append(1)
            if len(calls)==1: raise RuntimeError()
            return 3
        r=run([Task('a','x',retries=1)],{'x':flaky})
        self.assertEqual(r['results']['a']['value'],3)
        self.assertEqual(len(r['audit']),2)
    def test_block(self):
        r=run([Task('a','x',approval=True),Task('b','x',('a',))],{'x':lambda _:0})
        self.assertEqual(r['results']['b']['status'],'blocked_dependency')
    def test_unknown_tool(self):
        with self.assertRaises(ValueError): run([Task('a','missing')],{})
