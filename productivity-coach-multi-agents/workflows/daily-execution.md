# Workflow: Daily Execution

**Owner:** Planning Agent · **Supports:** Review Agent (end-of-day), MCP Connector, QA

## Example Requests
- "Plan my day. Meetings at 10 and 2, need to finish the design doc."
- "I keep getting distracted — structure my afternoon."
- "End-of-day review." (→ Review Agent, daily cadence)

## Steps

1. **Morning plan (≤5 min to produce).** Inputs: today's meetings (pasted or
   Calendar via MCP gate), open tasks (pasted or Tasks/tracker via gate),
   weekly plan if one exists, energy level.
2. **Top 3 priorities.** Exactly three, ranked. #1 is the one that, if it's the
   only thing done, makes the day a success. Tie daily top-3 to weekly must-dos
   when a weekly plan exists; flag drift ("none of today's top 3 serve this
   week's must-dos — intentional?").
3. **Calendar–task alignment.** Place each top-3 item into a specific time
   block. No block, no commitment — it moves to should-do.
4. **Deep work block.** One protected 90–120 min block in the largest free
   window, matched to peak energy (default: morning). On >4h-meeting days:
   no deep work block; top 3 become shallow tasks and the plan says so.
5. **Distraction handling.** A parking-lot note for intrusive thoughts/tasks;
   notifications off during the deep block; a named "if interrupted, then…"
   rule (e.g., "write down where I stopped, one-line restart note").
6. **Minimum viable day.** The single outcome that still counts if everything
   melts down. Stated up front, not as consolation.
7. **End-of-day review (3–5 min, Review Agent).** Top-3 done? One win, one
   friction, carry-over decisions (tomorrow / reschedule / drop), energy note.
   Feeds tomorrow's plan and the weekly review.
8. **QA gate** → universal contract (compact daily variant).

## Output specifics
- Time-blocked day with deep work + buffer visible
- Top 3 + minimum viable day
- Parking lot + interruption rule
- End-of-day review prompts

## Manual Fallback
Paste meeting times + task list, answer "peak energy: morning or afternoon?"
That's everything needed.

## Storage
Optional `plans` (type `daily`) and `reviews` (cadence `daily`); otherwise the
end-of-day review emits a 5-line ledger block.
