import unittest
from dataclasses import replace
from energy import Scenario,estimate
class Tests(unittest.TestCase):
    def setUp(self): self.s=Scenario('test',10,.1,.5,.5,2,100,1.2,.1,.5)
    def test_calculation(self):
        r=estimate(self.s); self.assertAlmostEqual(r['facility_kwh'],600); self.assertAlmostEqual(r['electricity_cost_usd'],60); self.assertAlmostEqual(r['operational_tonnes_co2e'],.3)
    def test_pue(self): self.assertLess(estimate(replace(self.s,pue=1))['facility_kwh'],estimate(self.s)['facility_kwh'])
    def test_invalid(self):
        for x in [replace(self.s,pue=.8),replace(self.s,utilization=1.1),replace(self.s,hours=float('nan')),replace(self.s,accelerators=-1)]:
            with self.assertRaises(ValueError): estimate(x)
