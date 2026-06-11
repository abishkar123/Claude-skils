# Workflow: Weekly Planning

**Owner:** Planning Agent · **Supports:** Review Agent (previous week), MCP Connector, QA

## Example Requests
- "Plan my week. Here are my meetings and priorities: …"
- "I'm overwhelmed — help me figure out what actually matters this week."
- "Plan next week using my calendar." (→ MCP gate for calendar)

## Steps

1. **Capture commitments.**
   - Manual: user pastes meetings, deadlines, recurring obligations.
   - MCP (authorized): Calendar → availability windows + meeting-hours/day for
     the week; Tasks/Jira/Linear → open + overdue items; Gmail → only
     user-flagged threads containing commitments.
2. **Review previous week** (skip gracefully if no data): must-do completion
   rate, top miss + cause, one process change to carry forward. Uses stored
   weekly review if approved, else 3 recall questions max.
3. **Identify priorities.** From user goals + carry-overs + deadlines, draft
   candidate priorities; user-stated priorities always outrank inferred ones.
4. **Estimate capacity.** Nominal free hours × 0.7 focus factor − already-
   committed task time. Show the math.
5. **Create the plan.** Must-do (≤5/week, ≤3/day) / should-do / optional.
   Deep work mapped to the largest free blocks. Estimates ×1.5 unless user has
   accurate-estimate history.
6. **Flag overloaded days.** Any day where planned + meetings > capacity, or
   meetings > 4h with deep work scheduled → name the day, name the fix.
7. **Define success criteria.** "Week succeeds if: all must-dos done + ≥2
   should-dos + Friday review completed." Plus minimum viable week.
8. **Produce weekly execution checklist.** Day-by-day, checkbox format.
9. **QA gate** → assemble in universal contract.

## Output (universal contract + these specifics)
- Day-by-day grid: meetings hours, planned task hours, capacity %, flags
- Must/should/optional lists with estimates
- Minimum viable week
- Weekly execution checklist

## Manual Fallback
Everything above works from three pastes: (1) meeting times for the week,
(2) task/priority list, (3) rough free-hours estimate. If the user has none of
these, build the plan from 3 questions: biggest deadline? meeting-heaviest
days? realistic focused hours per day?

## Storage (optional, approved only)
`plans` collection, type `weekly` — see database/mongodb-strategy.md. Otherwise
emit a manual ledger block.
