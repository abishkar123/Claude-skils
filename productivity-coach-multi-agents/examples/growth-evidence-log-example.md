# Example: Professional Growth Evidence Log (Hybrid Mode)

> **User request:** "Build my evidence log for Q2. You can read merged PRs in
> acme/payments-service under my handle. I'll paste the rest. Target: senior
> engineer this cycle."

## Evidence Log: Q2 2026 — toward Senior Engineer

**Objective:** A corroborated, quantified evidence base for the senior promotion conversation, mapped to ladder competencies.

**Inputs used:** Manual: pasted ladder competencies (technical execution, project leadership, cross-team impact, communication), recalled wins, manager feedback quotes. MCP: GitHub — merged PR titles/links/stats, repo `acme/payments-service`, author = user, Apr 1–Jun 11.

**Assumptions:** Ladder text pasted is current. Impact numbers below are yours as stated — I flagged the two that need a source before they go in a promo doc.

### Evidence Log
| Date | Project | Situation/Task | Action | Result (quantified) | Competencies | Corroboration |
|------|---------|----------------|--------|---------------------|--------------|---------------|
| Apr 18 | payments retry rework | duplicate-charge incidents recurring | designed + shipped idempotency-key scheme, led rollout across 3 services | duplicate charges 12/wk → 0 over 6 wks | tech execution, project leadership | PR #482, #491; incident dashboard ⚠needs link |
| May 09 | API migration | legacy v1 blocking partner onboarding | drove migration plan, coordinated 2 teams, cut over with zero downtime | 14 partners migrated, 0 downtime, 3 wks early | project leadership, cross-team | PR #510–#524; migration doc |
| May 22 | onboarding runbook | new hires taking ~3 wks to first PR | wrote runbook + paired with 2 new hires | first-PR time ~3 wks → 1 wk (n=2) | communication, mentorship | runbook doc; ⚠small n — frame as "early signal" |
| Jun 05 | Q3 planning deck | leadership needed payments roadmap view | authored deck, presented to director | adopted as Q3 plan of record; direct quote from manager: "clearest roadmap we've had" | communication, cross-team | deck link; manager Slack quote (you pasted) |

### Promotion Readiness (vs. pasted ladder)
| Competency | Current evidence | Gap | Next evidence-producing action |
|---|---|---|---|
| Technical execution | strong (retry rework, migration) | none material | keep cadence |
| Project leadership | strong (migration, 2 teams) | single-quarter sample | lead Q3 stabilization visibly |
| Cross-team impact | moderate | mostly within payments org | take the partner-API consult that platform team requested |
| Communication | moderate→strong | written artifacts thin before May | publish migration retrospective internally |

### Sample resume bullets (from this log)
- Eliminated recurring duplicate-charge incidents (12/wk → 0) by designing an idempotency scheme adopted across 3 services.
- Led a zero-downtime API migration of 14 partner integrations across 2 teams, landing 3 weeks early.

### Capacity Check
Next-evidence actions: 2 items, both attachable to existing Q3 work — no new workload invented for the promo case.

### Risks & Overload Warnings
- ⚠ Two results lack a verifiable source (incident dashboard link, n=2 onboarding). Fix before this goes in a promo packet — unsourced numbers get challenged.

### Tradeoffs
Excluded 6 smaller PRs (routine fixes) — a log of everything persuades no one; 4 strong entries beat 10 mixed ones.

### Success Criteria
Every entry has a quantified result + corroboration link by end of Q2 · readiness table reviewed with manager at the next 1:1 · weekly capture keeps running (3 questions at weekly review).

**Review checkpoint:** Weekly review evidence prompt; full readiness re-check at quarterly review (Sep).

**Manual fallback:** Without GitHub access: paste PR titles/links yourself, or answer the weekly 3 questions ("what shipped? measurable result? who benefited?") — the log builds identically.

**Storage:** Not stored — emitted as this Markdown table for your own notes. Say the word and the Database Memory Agent will propose the `evidence` collection schema for approval (sensitivity: work; delete/export on demand).

**Connector usage note:**
```
Services used:    GitHub (read-only)
Purpose:          technical evidence candidates for promotion log
Data accessed:    merged PR titles, links, dates, line stats; repo acme/payments-service;
                  author = user; Apr 1–Jun 11 2026
Data excluded:    code contents, review comments, other repos, other authors' activity
Stored:           none
Privacy risk:     medium — employer project metadata; kept out of any search queries
Permission scope: repo read on one named repo, this session
Manual fallback:  paste PR titles/links or describe shipped work
```
