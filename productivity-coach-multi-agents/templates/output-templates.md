# Reusable Output Templates

## 1. Universal Output Contract (every output, every agent)

```markdown
## <Title — e.g., Weekly Plan: Jun 15–21>

**Objective:** <one sentence — what this output achieves>

**Inputs used:** <manual inputs listed; MCP data listed by service + exact data>

**Assumptions:** <everything inferred: capacity, estimates, energy, levels>

### Prioritized Actions
**Must-do** (≤3/day, ≤5/week)
- [ ] <action — verb + scope + when> (est. Xh)
**Should-do**
- [ ] ...
**Optional**
- ...

### Capacity Check
Nominal free hours: X · ×0.7 focus factor = Y usable · Planned: Z (N% of usable) · Buffer: B%

### Risks & Overload Warnings
- ⚠ <named day/item + why + suggested fix>

### Tradeoffs
- <what was deprioritized and why>

### Success Criteria
- <countable / observable conditions>
**Minimum viable:** <smallest outcome that still counts>

**Review checkpoint:** <when + which review cadence>

**Manual fallback:** <how to do/redo this with zero tools>

**Connector usage note:** <only if MCP used — full format below>
```

## 2. Connector Usage Note

```markdown
Services used:    <service (scope)>
Purpose:          <why>
Data accessed:    <exact fields, range, filters>
Data excluded:    <named exclusions>
Stored:           <none | what + where + approval ref>
Privacy risk:     <low|medium|high — reason>
Permission scope: <e.g., calendar.readonly, session-only>
Manual fallback:  <the paste that replaces this connector>
```

## 3. Weekly Plan Grid

```markdown
| Day | Meetings (h) | Planned tasks (h) | Capacity used | Flags |
|-----|--------------|-------------------|---------------|-------|
| Mon |              |                   |            %  |       |
...
```

## 4. Weekend Plan Block

```markdown
**Energy level:** n/5 · **Unstructured time:** ≥X% (allocated first)
| Block | Sat | Sun |
|-------|-----|-----|
| Morning | | |
| Afternoon | | |
| Evening | | |
**Not this weekend:** <deferred items>
**Monday prep (≤30 min Sun):** review calendar · write top 3 · <physical prep>
```

## 5. Daily Plan

```markdown
**Top 3:** 1) ___ 2) ___ 3) ___   **Minimum viable day:** ___
**Deep work block:** <time range> — <top-3 item #1>
**Parking lot:** (capture intrusions here)  **If interrupted:** <one-line restart rule>
<time-blocked schedule>
**End of day (3 min):** top-3 done? · win · friction · carry-overs · energy /5
```

## 6. 30/60/90 Skill Roadmap

```markdown
**Skill:** ___ · **Baseline:** <level + probe results> · **Target (day 90):** <observable capability + artifact>
| Phase | Focus | Practice | Feedback loop | Checkpoint | Artifact |
|-------|-------|----------|---------------|------------|----------|
| 1–30  | fundamentals | <n×/wk, m min> | | day-30 probes | |
| 31–60 | applied project | | | day-60 probes | |
| 61–90 | consolidate + teach | | | day-90 probes vs target | |
**Metrics:** sessions x/y · probe scores · artifacts shipped
```

## 7. Evidence Log Entry

```markdown
| Date | Project | Situation/Task | Action | Result (quantified) | Competencies | Corroboration |
|------|---------|----------------|--------|---------------------|--------------|---------------|
```

## 8. Review Templates

**Daily:** top-3 done? · 1 win · 1 friction · carry-overs (do/move/drop) · energy /5 · habit ticks

**Weekly:**
```markdown
Completion: must-dos x/y
Wins: · Misses (+cause: overcommitted|interrupted|underestimated|avoided):
Blockers (active? unblock action):
Habits: <habit x/y …> · Evidence capture: shipped? result? who benefited?
Process changes for next week (≤3): · Follow-ups to check next week:
```

**Monthly:** weekly roll-up → patterns → goal status (+changes w/ reason) →
skill checkpoint → start/stop/continue (≤2 each) → next month's 3 priorities.

**Quarterly:** goals retro → career checkpoint → 90-day skill probes → habit
system review → OS system review → next quarter's ≤3 goals.

## 9. Promotion Readiness Table

```markdown
| Competency (next level) | Current evidence | Gap | Next evidence-producing action |
|--------------------------|------------------|-----|--------------------------------|
```

## 10. Ledger Block (no-database persistence)

See database/mongodb-strategy.md §Manual Fallback — YAML records matching the
DB schemas 1:1, pasted back in future sessions.
