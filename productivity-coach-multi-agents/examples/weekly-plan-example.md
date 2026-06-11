# Example: Weekly Plan (Hybrid Mode)

> **User request:** "Plan my week (Jun 15–21). Priorities: finish the API
> migration, draft the Q3 review deck, gym 3x. You can read my calendar for
> availability — times only. Roughly 8h workdays."

## Weekly Plan: Jun 15–21

**Objective:** Ship the API migration, get the Q3 deck to reviewable draft, and hold 3 gym sessions — without an overloaded midweek.

**Inputs used:** Manual: 3 stated priorities, 8h workdays. MCP: Google Calendar (read-only) — event times/durations Mon–Fri, primary calendar, no titles/attendees.

**Assumptions:** Focus factor 0.7. Migration estimate 10h and deck 4h are mine (you gave none) — already inflated ×1.5 from typical sizes. Gym sessions 1h, evenings. No weekend work.

### Prioritized Actions
**Must-do**
- [ ] API migration: finish + deploy behind flag (10h: Mon/Tue/Thu deep blocks)
- [ ] Q3 deck: reviewable draft, 10–12 slides (4h: Wed pm + Fri am)
- [ ] Gym ×3 (Mon, Wed, Fri 6pm)
**Should-do**
- [ ] Migration writeup for the team wiki (1h, Fri pm)
**Optional**
- Inbox zero pass

### Capacity Check
Free (non-meeting) hours Mon–Fri: 26 · ×0.7 = **18 usable** · Planned: 15h (83%) · Buffer: 17%

### Risks & Overload Warnings
- ⚠ **Wednesday has 5.5h of meetings** — no deep work scheduled there; only deck slide-sketching (shallow). If a migration issue erupts Wednesday, it waits for Thursday's block.

### Tradeoffs
Deck "final polish" deferred to next week — draft is enough for review; migration outranks it. Wiki writeup drops first under pressure.

### Success Criteria
Migration deployed behind flag by Thu EOD · deck draft shared by Fri noon · gym 3/3.
**Minimum viable week:** migration deployed, even if the deck slips.

**Review checkpoint:** Weekly review Fri 4:30pm (15 min).

**Manual fallback:** Paste meeting times for the week + the same 3 priorities; identical plan, no connector.

**Connector usage note:**
```
Services used:    Google Calendar (read-only)
Purpose:          availability + meeting load for weekly planning
Data accessed:    event start/end/duration, Mon Jun 15–Fri Jun 19, primary calendar
Data excluded:    titles, attendees, descriptions, locations, other calendars
Stored:           none
Privacy risk:     low — timing metadata only
Permission scope: calendar.readonly, this session, this purpose
Manual fallback:  paste weekly meeting times
```
