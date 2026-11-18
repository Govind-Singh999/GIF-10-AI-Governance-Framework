# AI Governance Framework — Portfolio Workspace

This repository currently hosts an AI-assisted educational prototype for evaluating AI-generated responses. It is a demonstration of governance engineering, not a published definition or implementation of the GIF-10 framework, an official standard, or a compliance certification.

## AI Governance Lab

- [Evaluation harness and architecture](AI-Governance-Lab/README.md)
- [Python evaluator](AI-Governance-Lab/evaluate.py)
- [Synthetic evaluation cases](AI-Governance-Lab/examples/cases.json)
- [Automated tests](AI-Governance-Lab/tests/test_evaluate.py)

**Scope:** deterministic checks for required and forbidden phrases and simple email-pattern privacy indicators. Local evaluation only; no production or customer data.

## Quick start

Requires Python 3.10 or newer (standard library only).

```bash
cd AI-Governance-Lab
python evaluate.py examples/cases.json
python -m unittest discover -s tests -v
```

The sample intentionally includes both passing and failing responses.

**Attribution:** AI-assisted code and documentation prepared for portfolio learning, review, and experimentation. No claim of independent authorship or production validation.
