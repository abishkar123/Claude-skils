# Workflow: Weekend Planning

**Owner:** Planning Agent · **Supports:** QA

## Example Requests
- "Plan my weekend — I have errands, want to study, and I'm exhausted."
- "Help me have a weekend that doesn't feel wasted but isn't another workweek."

## Design Principle
A weekend is not two bonus workdays. The plan balances **seven buckets** —
rest, errands, admin, learning, social time, personal projects, Monday prep —
and rest is allocated FIRST, not from leftovers.

## Steps
1. **Capture fixed commitments** (social events, appointments) and energy level
   (1–5, asked or inferred from user's words — log in Assumptions).
2. **Allocate rest first.** Low energy (≤2): ≥50% of waking weekend time stays
   unstructured. Normal: ≥30%. Never below 30%.
3. **Cap the rest:**
   - Errands + admin: batch into ONE block (e.g., Sat morning), ≤3h total.
   - Learning / personal projects: 1–2 blocks of 60–120 min, never both days
     fully booked; skip entirely if energy ≤2.
   - Social: as committed; protect at least one unscheduled evening.
   - Monday prep: ≤30 min Sunday early evening (review calendar, set top 3,
     lay out anything physical) — never Sunday night work sessions.
4. **Overload check:** if requested items exceed caps, force-rank with the
   user's stated priorities and move the rest to "next weekend / weekday /
   drop" — explicitly.
5. **Define success criteria:** e.g., "errands done by Sat 1pm, one 90-min
   project block happened, Sunday felt restful, Monday top-3 written."
6. **QA gate** → universal contract.

## Output specifics
- Two-day block layout with unstructured time visibly marked
- The "not this weekend" list (deferred items, named)
- Monday-prep micro-checklist

## Manual Fallback
Fully manual by nature. Optional MCP: Calendar (weekend events only,
availability + titles of user-named events) after the 7-question gate.

## Storage
Optional `plans` collection, type `weekend`; otherwise manual ledger block.
