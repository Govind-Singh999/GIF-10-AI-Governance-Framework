import unittest,json
from evaluate import report,evaluate
class Tests(unittest.TestCase):
    def test_fixture(self):
        with open('examples/cases.json') as f: r=report(json.load(f))
        self.assertEqual(r['passed'],2);self.assertEqual(r['pass_rate'],.5)
    def test_casefold(self): self.assertTrue(evaluate({'id':'a','response':'YES','required':['yes']})['passed'])
    def test_empty(self): self.assertIsNone(report([])['pass_rate'])
    def test_duplicate(self):
        with self.assertRaises(ValueError): report([{'id':'a'},{'id':'a'}])
    def test_email(self): self.assertFalse(evaluate({'id':'b','response':'demo@example.invalid','no_email':True})['passed'])
