# Architecture & Routing Logic

## System Overview

```
                          ┌─────────────────────────┐
   User request ────────► │   ORCHESTRATOR AGENT    │ ◄── final answer assembly
                          └───────────┬─────────────┘
                                      │ classify → route → coordinate
        ┌──────────┬──────────┬───────┴──────┬─────────────┐
        ▼          ▼          ▼              ▼             ▼
   ┌─────────┐ ┌────────┐ ┌─────────┐ ┌───────────┐ ┌──────────┐
   │PLANNING │ │ SKILL- │ │ PROF.   │ │  REVIEW   │ │KNOWLEDGE │
   │  AGENT  │ │BUILDING│ │ GROWTH  │ │  AGENT    │ │ & SEARCH │
   └────┬────┘ └───┬────┘ └────┬────┘ └─────┬─────┘ └────┬─────┘
        │          │           │            │            │
        └──────────┴─────┬─────┴────────────┘            │
                         ▼                               │
   support layer  ┌──────────────┐   ┌────────────────┐  │
                  │MCP CONNECTOR │   │DATABASE MEMORY │  │
                  │    AGENT     │   │     AGENT      │  │
                  └──────────────┘   └────────────────┘  │
                         │                   │           │
                         ▼                   ▼           ▼
                  [authorized MCP]    [approved DB]  [web search]
                                      
   gate (always)  ┌─────────────────────────────────────────┐
                  │       QUALITY ASSURANCE AGENT           │
                  │ realism · overload · privacy · action-  │
                  │ ability · assumptions · success criteria│
                  └─────────────────────────────────────────┘
```

Three layers:

1. **Coordination layer** — Orchestrator only. The single entry and exit point.
2. **Specialist layer** — Planning, Skill-Building, Professional Growth, Review, Knowledge & Search. Each owns its workflows end-to-end.
3. **Support layer** — MCP Connector (external tool access), Database Memory (persistence), Quality Assurance (output gate). Specialists never call MCP tools or the database directly; they request data through the support agents, which enforce permission and privacy boundaries.

## Routing Logic (Orchestrator)

### Step 1 — Classify intent

| Signals in request | Route to | Workflow |
|---|---|---|
| "plan my week", commitments, priorities, capacity | Planning | Weekly Planning |
| "weekend", rest, errands, Saturday/Sunday | Planning | Weekend Planning |
| "today", "this morning", top 3, deep work | Planning | Daily Execution |
| "learn", "get better at", roadmap, practice | Skill-Building | Skill-Building |
| promotion, career, resume, LinkedIn, impact, evidence | Professional Growth | Professional Growth |
| "review", retro, "how did I do", wins/misses, habits | Review | Personal Review (pick cadence: daily/weekly/monthly/quarterly) |
| "what tools can you use", connector setup | MCP Connector | Connector discovery |
| "remember this", "save", "show my history" | Database Memory | Storage (requires approval) |
| "find resources", "what's the current best…" | Knowledge & Search | Search (privacy-filtered) |

Multi-intent requests ("plan my week and check my promotion progress") fan out to
multiple specialists; the Orchestrator merges results into one answer with one
combined capacity check.

Ambiguous requests: ask **one** clarifying question with concrete options, never an
open-ended interview.

### Step 2 — Mode decision (Manual / MCP-Assisted / Hybrid)

```
needs_external_data?
├─ no  → Manual Mode. Proceed with what the user provided.
└─ yes → for each candidate service, ask MCP Connector Agent:
         1. Is the service AVAILABLE?          (discovered, not assumed)
         2. Is it NECESSARY?                   (does it change the output materially?)
         3. Has the user AUTHORIZED it?        (this session, this purpose)
         4. What EXACT data will be accessed?  (fields, date range, filters)
         5. What data is EXCLUDED?             (named explicitly)
         6. Will anything be STORED?           (default: no)
         7. Can it be done MANUALLY instead?   (always yes — offer it)
         ├─ all pass → use connector, attach Connector Usage Note
         └─ any fail → fall back: ask user for a manual paste of just the
                       missing data ("paste your meeting list for next week")
```

The Orchestrator never blocks on a connector. If authorization is pending or
denied, it produces the best output possible from manual input and lists what
extra data would improve it.

### Step 3 — Coordinate specialists

- Sequential when output feeds output (Review of last week → Weekly Plan).
- Parallel when independent (Skill roadmap + Growth evidence log).
- Shared context passed between agents is **minimized**: the Planning Agent gets
  calendar *availability windows*, not meeting titles/attendees, unless titles are
  needed and authorized.

### Step 4 — QA gate (mandatory)

Every candidate output passes through the Quality Assurance Agent before reaching
the user. QA can: approve, annotate (add warnings), or bounce (return to the
specialist with a named defect: overloaded, vague, privacy leak, missing fallback,
unstated assumption, no success criteria). One bounce maximum; after that, QA
annotates and ships with warnings rather than looping forever.

### Step 5 — Assemble final answer

The Orchestrator formats the result in the [universal output contract](templates/output-templates.md),
merges Connector Usage Notes if MCP was used, and includes the manual fallback.

## Inter-Agent Message Contract

Agents exchange structured handoffs, not free text:

```yaml
handoff:
  from: orchestrator
  to: planning
  workflow: weekly-planning
  mode: hybrid                  # manual | mcp-assisted | hybrid
  inputs:
    manual: { priorities: [...], capacity_hours: 30, notes: "..." }
    mcp:                        # only authorized, minimized data
      - service: google-calendar
        data: availability_windows   # NOT raw events
        range: 2026-06-15..2026-06-21
  constraints: [no_storage, exclude_personal_calendar]
  prior_context: { last_week_review_summary: "..." }   # optional, summarized
expected_return:
  draft_output: <universal contract>
  open_questions: []            # max 1, only if blocking
```

## Privacy Boundaries by Design

- **Specialists are sandboxed**: only the MCP Connector Agent touches external
  tools; only the Database Memory Agent touches storage; only the Knowledge &
  Search Agent touches the internet. This makes "no private data in search
  queries" structurally enforceable: the Search Agent receives only generic,
  pre-sanitized queries from the Orchestrator and rejects queries containing
  names, employers, email fragments, document excerpts, or calendar content.
- **Data minimization at handoff**: support agents return derived summaries
  (availability windows, task counts, overdue lists) instead of raw records
  wherever the workflow allows.
- **Storage is explicit**: nothing reaches the Database Memory Agent without a
  user-approved storage request naming the collection, fields, and retention.

## Failure & Degradation Modes

| Failure | Behavior |
|---|---|
| MCP server unavailable mid-workflow | Continue with data already retrieved; mark gaps; offer manual paste |
| User declines authorization | Manual Mode for that data; never re-ask in the same session |
| Database unavailable / not approved | Emit a copy-pasteable "manual ledger" block the user can keep in their own notes (see database strategy) |
| Search unavailable | Answer from existing knowledge with a freshness disclaimer |
| QA bounce loop | Ship after one revision with explicit warnings attached |
| Conflicting inputs (calendar vs. user statement) | User statement wins; flag the conflict in Assumptions |

## Reusability

The system is implementation-agnostic. Each agent file is a self-contained system
prompt + decision rules, usable as:

- Claude Code / Claude API subagents (each `agents/*.md` is a subagent definition)
- A single-model "virtual multi-agent" pattern (one model role-switching through
  the same contracts) when subagents aren't available
- Any framework with tool-permission scoping (the MCP Connector Agent's checklist
  maps to allow-lists)
