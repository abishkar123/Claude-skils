# Example: Monthly Review (Manual Mode, ledger-based)

> **User request:** "Monthly review for May. Here are my four weekly ledger
> blocks: [pasted]."

## Monthly Review: May 2026

**Objective:** Find the patterns across May's four weeks and set June's three priorities, adjusting goals where May's evidence says to.

**Inputs used:** Manual: 4 pasted weekly ledger blocks (W18–W21). No MCP, no database.

**Assumptions:** Ledger blocks are complete for must-dos and habits; daily detail unavailable, so energy patterns are weekly-grain only.

### Roll-up
| Week | Must-dos | Gym | Reading | Notable |
|------|----------|-----|---------|---------|
| W18 | 5/5 | 3/3 | 1/5 | migration kickoff |
| W19 | 3/5 | 3/3 | 0/5 | prod incident ate Tue–Wed |
| W20 | 4/5 | 2/3 | 2/5 | deck shipped |
| W21 | 3/5 | 3/3 | 1/5 | 2 misses both "underestimated" |
**Totals:** must-dos 15/20 (75%) · gym 11/12 (92%) · reading 4/20 (20%)

### Patterns (the actual point)
1. **Underestimation is your dominant miss cause** — 4 of 5 misses across W19–W21, all on writing/document tasks, not coding. Coding estimates are fine; writing estimates need ×2, not ×1.5.
2. **Reading habit is failing structurally, not motivationally** — scheduled for evenings, and evenings consistently lose. Gym survives evenings because it has a fixed time and a place; reading has neither.
3. **One incident (W19) cost two weeks of momentum** — W19's misses cascaded into W20 carry-overs. There was no buffer to absorb it.

### Wins
Migration shipped (W20, on the rescoped date) · gym is now effectively automatic (92%, no friction notes since W18) · deck praised by manager → **evidence-log candidate, want me to draft the entry?**

### Goal Changes
- "Read 20 books this year" → **rescoped**: 10 books, mornings. Reason: 20% adherence over 8 weeks is data, not a slump.
- Migration goal → **done**, replaced by stabilization goal for June.

### Start / Stop / Continue
**Start:** writing tasks estimated ×2 · 15-min reading at breakfast (fixed time + place, like gym). **Stop:** scheduling reading after 8pm · carrying >2 items week-to-week (3rd carry-over gets dropped or rescoped, deliberately). **Continue:** gym slotting exactly as is.

### June Priorities (3)
1. Migration stabilization: zero P1s by Jun 30.
2. Q3 planning doc — first writing task under the ×2 rule.
3. Reading habit relocated to mornings: ≥50% adherence by month end (target is the *new slot working*, not the book count).

### Capacity Check
Three priorities + one habit redesign — within monthly threshold (≤3 goals, ≤1 habit change). No new commitments added on top.

### Risks & Overload Warnings
- ⚠ June has the Q3 planning cycle; if planning meetings spike past 4h/day in W24, priority 3 pauses rather than silently failing. Decided now.

### Tradeoffs
Book-count goal halved — adherence at a sustainable slot beats a number you resent.

### Success Criteria
June review shows: zero P1s · planning doc shipped with actual-vs-estimate logged · reading ≥50% in the morning slot · misses tagged "underestimated" < 2.

**Review checkpoint:** Weekly reviews check the ×2 rule and the morning slot; monthly review Jun 30.

**Manual fallback:** This *is* the fallback — ledger blocks in, review out, new ledger block emitted below for your notes file.

```yaml
type: monthly_review
month: 2026-05
must_do_rate: 15/20
patterns: [writing-underestimation, evening-habits-fail, no-incident-buffer]
goal_changes: [{goal: "20 books", change: "rescoped to 10, mornings", reason: "20% adherence"}]
june_priorities: ["zero P1s", "Q3 doc (x2 estimate)", "morning reading >=50%"]
follow_ups: [{commitment: "x2 writing estimates", check: weekly}, {commitment: "evidence entry for deck praise", check: 2026-W23}]
```
