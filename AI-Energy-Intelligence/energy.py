from dataclasses import dataclass
import argparse,json,math
@dataclass(frozen=True)
class Scenario:
    name: str
    accelerators: int
    idle_kw: float
    peak_kw: float
    utilization: float
    other_it_kw: float
    hours: float
    pue: float
    usd_per_kwh: float
    kg_co2e_per_kwh: float

def estimate(s: Scenario):
    numbers=[s.idle_kw,s.peak_kw,s.utilization,s.other_it_kw,s.hours,s.pue,s.usd_per_kwh,s.kg_co2e_per_kwh]
    if not all(math.isfinite(x) and x>=0 for x in numbers) or type(s.accelerators) is not int or s.accelerators<0 or s.utilization>1 or s.pue<1 or s.peak_kw<s.idle_kw or s.hours>8784:
        raise ValueError('Invalid scenario assumptions')
    avg=s.idle_kw+s.utilization*(s.peak_kw-s.idle_kw)
    it_kw=s.accelerators*avg+s.other_it_kw
    it_kwh=it_kw*s.hours
    facility=it_kwh*s.pue
    return {'name':s.name,'average_it_kw':it_kw,'it_kwh':it_kwh,'facility_kwh':facility,'electricity_cost_usd':facility*s.usd_per_kwh,'operational_tonnes_co2e':facility*s.kg_co2e_per_kwh/1000}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('scenarios'); a=parser.parse_args()
    with open(a.scenarios,encoding='utf8') as f: data=json.load(f)
    print(json.dumps([estimate(Scenario(**x)) for x in data],indent=2))
