# Database Strategy (MongoDB or approved alternative)

Owned by the Database Memory Agent. A database is **optional**: the system runs
indefinitely on manual ledger blocks. Use MongoDB (or any approved store) only
when the user wants longitudinal features (trend detection, multi-week
reviews, evidence compilation) without re-pasting history.

## Setup Principles
- Dedicated database, e.g. `productivity_coach`. Never touch other databases
  on a shared server.
- Least-privilege DB user: `readWrite` on `productivity_coach` only.
- The user approves the schema once before first write; sensitive collections
  (`evidence`, free-text `notes`) are confirmed per write or via an explicit
  standing rule the user grants.
- Every record: `user_approved: true`, `created_at`, `source` (`manual` |
  `mcp:<service>`), `sensitivity` (`routine` | `work` | `personal`).
- Store **summaries and structured outcomes** — never email bodies, document
  contents, calendar event details, message transcripts, or credentials.

## Collections & Schemas

### `plans`
```js
{
  _id, type: "weekly"|"weekend"|"daily",
  period: { start: ISODate, end: ISODate },          // or date for daily
  must_do:   [{ item, estimate_h, scheduled, done: null|true|false }],
  should_do: [{ item, estimate_h, done }],
  optional:  [String],
  capacity:  { nominal_h, focus_factor, planned_h, buffer_pct },
  overload_flags: [String],
  success_criteria: [String],
  minimum_viable: String,
  user_approved: true, created_at, source, sensitivity: "routine"
}
```

### `reviews`
```js
{
  _id, cadence: "daily"|"weekly"|"monthly"|"quarterly",
  period: { start, end },
  completion: { must_do_done: Int, must_do_total: Int },
  wins: [String],
  misses: [{ item, cause: "overcommitted"|"interrupted"|"underestimated"|"avoided" }],
  blockers: [{ desc, active: Bool, unblock_action }],
  patterns: [String],                                 // monthly+
  lessons: [String],
  goal_changes: [{ goal, change, reason }],
  next_actions: [{ action, due }],
  follow_up_commitments: [{ commitment, check_at }],
  energy_avg: Number,
  user_approved, created_at, source, sensitivity: "routine"
}
```

### `habits`
```js
{ _id, habit, target_per_week: Int, week: "2026-W24",
  ticks: [ISODate], adherence: Number, friction_note: String,
  user_approved, created_at, source, sensitivity: "routine" }
```

### `skills`
```js
{
  _id, skill, status: "active"|"parked"|"done"|"stopped",
  baseline: { level, probes: [{ probe, result }] , date },
  target: { capability, by: ISODate },
  roadmap: { d30: [String], d60: [String], d90: [String] },
  sessions: [{ date, minutes, objective, output }],
  checkpoints: [{ day: 30|60|90, probes: [...], decision }],
  artifacts: [{ desc, link }],
  user_approved, created_at, source, sensitivity: "routine"
}
```

### `evidence`  (work-sensitive — confirm writes)
```js
{
  _id, date, project,
  situation: String, action: String,
  result: { description, metric, value },             // quantified
  competency_tags: [String],
  corroboration: [String],                            // links only, no contents
  user_approved, created_at, source, sensitivity: "work"
}
```

### `goals`
```js
{ _id, horizon: "quarter"|"year", goal, success_criteria: [String],
  status: "on_track"|"at_risk"|"off_track"|"rescoped"|"dropped",
  checkpoints: [{ date, note }], user_approved, created_at, source, sensitivity }
```

## Indexes
`plans`: `{type:1, "period.start":-1}` · `reviews`: `{cadence:1, "period.start":-1}` ·
`habits`: `{habit:1, week:-1}` · `evidence`: `{date:-1}`, `{competency_tags:1}` ·
`skills`: `{status:1}`.

## Read Scoping
Weekly review → that week's `plans` + `reviews(daily)`. Monthly → that month's
weeklies. Quarterly → monthlies + `goals` + `skills` checkpoints. Evidence
compilation → `evidence` filtered by date/tags. Never "load everything."

## Retention & User Rights
- Default retention: `plans`/`reviews(daily)` 6 months; `reviews(weekly+)`,
  `habits`, `skills`, `goals` 2 years; `evidence` until the user deletes it
  (it's their career record). User can change any of these.
- **Delete on demand** (per collection or all), confirmed with counts.
- **Export on demand**: any collection as JSON or Markdown.
- No analytics, no sharing, no secondary use. Ever.

## Manual Fallback: the Ledger
Without a database, every storable output ends with a ledger block:

```yaml
# productivity-ledger · paste back in any future session
type: weekly_review
week: 2026-W24
must_do_completed: 4/5
wins: ["shipped API migration", "3/3 gym"]
misses: [{item: "Q3 deck draft", cause: underestimated}]
habits: {gym: 3/3, reading: 2/5}
next_week_changes: ["estimate deck work at 2x", "move reading to mornings"]
follow_ups: [{commitment: "send status note", check: 2026-W25 review}]
```

Users keep these in a notes file (`productivity-ledger.md`). The schema matches
the DB collections 1:1, so a later migration to MongoDB is a straight import.
