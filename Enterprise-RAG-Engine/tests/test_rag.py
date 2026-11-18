import unittest
from rag import Index,Chunk,load
class Tests(unittest.TestCase):
    def setUp(self): self.i=Index(load('examples/docs'))
    def test_retrieve(self):
        r=self.i.answer('What is the retention period for audit logs?'); self.assertEqual(r['status'],'evidence_found'); self.assertEqual(r['evidence'][0]['source'],'security.txt'); self.assertIn('90 days',r['evidence'][0]['excerpt'])
    def test_abstain(self): self.assertEqual(self.i.answer('spacecraft launch date')['status'],'insufficient_evidence')
    def test_empty(self): self.assertEqual(Index([]).answer('hello')['status'],'insufficient_evidence')
    def test_stopwords(self): self.assertEqual(self.i.answer('what is the')['status'],'insufficient_evidence')
