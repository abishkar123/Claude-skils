# Example: 30/60/90-Day Skill-Building Plan (Manual + sanitized search)

> **User request:** "I want to get good at system design for senior interviews
> and real work. I can do ~45 min on weekdays. Currently I can build CRUD
> services but freeze on open-ended design questions."

## Skill Plan: System Design — Jun 15 → Sep 13

**Objective:** Go from freezing on open-ended design questions to confidently designing and defending a mid-size system in 45 minutes.

**Inputs used:** Manual: goal, 45 min/weekday capacity, self-described baseline. Web search (sanitized): current resource check.

**Assumptions:** Baseline ≈ advanced-beginner, pending probes below. Weekends off — sustainability beats intensity.

**Baseline probes (do these first, ~45 min total; results calibrate the plan):**
1. Whiteboard a URL shortener in 20 min — where do you stall?
2. Explain consistent hashing cold, 3 min.
3. Name the failure modes of a system you've actually worked on.

**Target (day 90):** Design a mid-size system (e.g., notification service, rate limiter at scale) in a 45-min mock: requirements → estimation → high-level → deep-dive → tradeoffs, recorded, defensible under follow-up questions.

| Phase | Focus | Practice (5×45 min/wk) | Feedback loop | Checkpoint | Artifact |
|-------|-------|------------------------|---------------|------------|----------|
| **1–30** Fundamentals | storage, caching, queues, replication, partitioning, estimation | Mon/Wed/Fri concept study + notes; Tue/Thu one back-of-envelope estimation drill | self-test: re-explain yesterday's concept cold each morning (5 min) | day-30: redo probes 1–2 | concept notes repo + 10 estimation drills |
| **31–60** Application | full designs, one per week | 3 sessions design a system on paper; 2 sessions critique it against reference solutions | weekly: compare your design vs. a published reference; log deltas | day-60: one 45-min self-timed mock, recorded | 4 complete design docs |
| **61–90** Consolidation + teach | mocks + teaching | 2 mocks/wk (1 recorded solo, 1 with a peer if available); 1 session writing | peer or recording review — watching yourself stall is the highest-signal feedback available | day-90: full mock vs. target, scored on the 5 stages | 1 published design writeup + recorded mock |

**Progress metrics:** sessions x/25 per phase · probe scores at 30/60/90 · designs completed 0→4→8 · stall count per mock (should trend down).

### Capacity Check
5×45 min = 3.75h/week — fits inside your stated capacity with zero weekend creep. Beginner cap (≤5 sessions/wk) respected.

### Risks & Overload Warnings
- ⚠ Phase 2 is where these plans die (novelty gone, difficulty up). The week-31 session is pre-committed to the calendar NOW, and the weekly review tracks sessions x/5 from day 1.

### Tradeoffs
Breadth sacrificed for the interview-shaped core: no Kubernetes/infra-ops detours during these 90 days — parked, revisit at day-90 review.

### Success Criteria
Day-90 mock hits all 5 stages without freezing · ≥80% session adherence · 8 designs + 1 writeup shipped.

**Review checkpoint:** Weekly (sessions + one delta) inside your weekly review; formal probe re-tests at day 30/60/90.

**Manual fallback:** Fully manual. Resource list below came from search; without search, canonical texts (DDIA, the open system-design primers) apply with a "verify currency" note.

**Connector usage note:**
```
Services used:    Web search (Knowledge & Search Agent)
Purpose:          current learning resources for system design (2026)
Data accessed:    public web results for generic queries:
                  "best system design interview resources 2026",
                  "system design practice with feedback"
Data excluded:    all personal/employer context — none appeared in queries
Stored:           none
Privacy risk:     low — generic queries only
Permission scope: search-only, no writes
Manual fallback:  canonical resource list from model knowledge + currency disclaimer
```
