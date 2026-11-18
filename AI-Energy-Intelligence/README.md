# AI-Energy-Intelligence
Scenario-based AI data center operational energy, electricity cost and emissions estimates.

```mermaid
flowchart LR
 A[Hardware and load assumptions] --> B[IT energy]
 B --> C[Apply PUE]
 C --> D[Facility kWh]
 D --> E[Cost and operational emissions]
```

## Quick start
```sh
python energy.py examples/scenarios.json
```
Inputs are synthetic and editable. Average accelerator power = idle power + utilization × (peak − idle). Facility energy = total IT kW × hours × PUE. Electricity cost = facility kWh × tariff. Operational emissions = facility kWh × grid intensity / 1,000 in tonnes CO2e. Excludes embodied emissions, demand charges, water use and energy outside the modeled hours. Not live metering, a hardware benchmark or a lifecycle assessment.

## Project status
AI-assisted educational portfolio prototype; synthetic examples only. Review and adapt before claiming expertise. Not production-ready. Python 3.10+, standard library only.
Run tests from this project folder: `python -m unittest discover -s tests -v`.
