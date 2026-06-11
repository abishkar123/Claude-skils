# Quality Assurance Checklists

Operated by the QA Agent on every output. Verdicts: approve / annotate / bounce
(once max, then annotate-and-ship).

## 1. Realism & Overload Detection

Hard thresholds (any TWO trips = bounce; one = annotate):

| Check | Threshold |
|---|---|
| Planned work vs. usable capacity | > 85% of (nominal × 0.7) |
| Buffer | < 15% unallocated |
| Must-dos per day / per week | > 3 / > 5 |
| Deep work on meeting-heavy day | any deep block on a > 4h-meeting day |
| Back-to-back depth | > 2 consecutive deep-work blocks without break |
| Estimates | user estimates not inflated ×1.5 (no track record) |
| Weekend | unstructured time < 30% of waking hours |
| New habits started simultaneously | > 1 |
| Beginner skill practice | > 5 sessions/week or > 60 min/session |
| Plan fragility | fails if ONE surprise meeting or sick day occurs |
| Missing minimum-viable day/week | absent |

## 2. Privacy Review

Automatic bounce:
- Any personal/employer/email/document/calendar/database content found in a
  web search query (also: incident note to Orchestrator).
- MCP used but Connector Usage Note missing or inaccurate.
- Data stored without a recorded user approval.
- Data from one connector pushed to another without separate approval.
- An external write (email, event, post, comment) without per-action
  confirmation.

Annotate:
- More data accessed than the workflow needed (note for next time, tighten).
- Sensitive content echoed back verbosely in the output when a summary would do.

## 3. Assumptions Audit
- Every inferred value (capacity, energy, focus factor, career ladder,
  estimate inflation) appears in **Assumptions**. Hidden assumption → annotate.
- Conflicts between sources (calendar vs. user statement) resolved in the
  user's favor and flagged.
- No fabricated history: missing review data is declared, recall-based answers
  are marked.

## 4. Actionability
- Each action = verb + scope + when. ("Work on deck" → bounce; "Draft 5 slides
  for Q3 review, Tue 9:00–10:30" → pass.)
- Each action has an estimate; top-3/must-dos have a calendar slot or an
  explicit "unscheduled — needs a block" flag.
- Next actions from reviews have owners and dates.

## 5. Success Criteria & Checkpoints
- Success criteria countable/observable; "be more productive" fails.
- Minimum viable day/week present in plans.
- Review checkpoint names a time and cadence.
- Review outputs include follow-up commitments checked at next review.

## 6. Contract Completeness
All 10 universal-contract sections present (11 with Connector Usage Note when
MCP used). Missing manual fallback = bounce — it is the system's load-bearing
guarantee.

## Worked Rejection Examples

**Bounced (overload):** Weekly plan with 9 must-dos, 38h planned on 40 nominal
hours, deep work Wed with 5h meetings. → Fix: cap must-dos at 5, replan to
~25h, move deep work to Tue/Thu, add minimum viable week.

**Bounced (privacy):** Skill agent requested search "negotiation course for
upcoming Acme reorg conversation with my manager Dana". → Rewritten:
"negotiation fundamentals course 2026 reviews".

**Annotated (user-forced):** User insists on 6 must-dos before a launch. Ship
with: "⚠ 6 must-dos exceeds the 5/week threshold; launch week justifies it
once. Pre-agree which 2 drop first if Tuesday slips."
