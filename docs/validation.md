# Proposed validation plan

Source: white paper, pp. 12–13 and 16. No experiments have been conducted or results reported here.

Compare three configurations in an isolated synthetic test environment: (A) prompt-only restrictions; (B) scoped identities and typed tool enforcement; (C) B plus independent monitoring, revocation and delegation limits. Keep a hard outer sandbox for all configurations. Use mock tools and synthetic records only.

Pre-register 50 task templates with five fixed variations and at least 250 runs per configuration per model. Record actual external effects, authorization decisions, legitimate task completion, revocation time, audit completeness, false holds, latency and cost. Report denominators, uncertainty and failures.

Illustrative pilot gates: zero observed critical unauthorized effects, 100% mediation coverage in managed test scope, at least 90% authorized task success and no more than five percentage points below baseline, p95 revocation time no greater than five seconds for mock tools, 100% privileged-action audit completeness and false hold rate no greater than 5%. These are proposed targets, not results or certification criteria. Zero observed failures is not proof of zero risk.

A critical authorization bypass, unexplained telemetry gap, inability to revoke or insufficient review blocks release. A bounded pilot cannot establish control over hypothetical superintelligence.

## Roadmap

1. Scope a reversible workflow and agree evaluation protocol.
2. Build mock broker, action contracts, revocation and audit ledger.
3. Run matched configurations and adversarial tests.
4. Obtain independent review and document limitations.
5. Publish permitted results and decide whether to proceed.
