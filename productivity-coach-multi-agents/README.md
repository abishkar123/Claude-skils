# Productivity Coach — Multi-Agent Productivity Operating System

A reusable, privacy-aware multi-agent system for weekly planning, weekend planning,
daily execution, skill-building, professional growth, habit improvement, and
daily/weekly/monthly/quarterly reviews.

This is **not** a generic coaching assistant. It is a structured operating system:
every request is routed to specialist agents, every output follows a strict template,
every plan is capacity-checked, and every external integration is opt-in with a
manual fallback.

## Operating Modes

| Mode | Data source | When to use |
|------|-------------|-------------|
| **Manual Mode** | User pastes tasks, calendar summaries, goals, notes, project updates, review inputs | Default. No connectors available or user prefers no tool access |
| **MCP-Assisted Mode** | MCP tools (calendar, email, tasks, GitHub, etc.) used **only after explicit per-service user authorization** | Connectors exist, user authorizes, data access saves real effort |
| **Hybrid Mode** | Manual input + approved MCP data with strict data minimization | Most common in practice: e.g., user pastes goals, system reads calendar availability |

The system is fully functional in Manual Mode. MCP is an accelerant, never a dependency.

## Core Rules (non-negotiable)

1. **Never assume a connector exists.** No MCP server, API, database, or service is used unless discovered as available or confirmed by the user.
2. **Every MCP workflow has a manual fallback**, documented in the workflow file and in every output.
3. **Least privilege.** Each connector gets the narrowest scope that does the job (read-only before read-write, single calendar before all calendars, date-bounded queries always).
4. **Minimum information.** Ask only for what the workflow needs. Don't collect "context" speculatively.
5. **No storage without approval.** Nothing is persisted (database, notes, files) unless the user explicitly approves what, where, and for how long.
6. **No private data in search queries.** Never send personal, employer, email, document, calendar, or database content into internet search. Search queries are generic ("best spaced-repetition tools 2026"), never specific ("resources for [employer]'s migration to X").

## Agents

| Agent | Responsibility |
|-------|----------------|
| [Orchestrator](agents/orchestrator.md) | Routes requests, selects workflows, decides if MCP is needed, coordinates agents, assembles the final answer |
| [Planning](agents/planning-agent.md) | Weekly, weekend, and daily planning |
| [Skill-Building](agents/skill-building-agent.md) | Skill focus, baseline assessment, 30/60/90-day roadmaps, practice plans, feedback loops, progress tracking |
| [Professional Growth](agents/professional-growth-agent.md) | Career goals, promotion readiness, project impact, evidence logs, communication coaching, resume/LinkedIn achievements |
| [Review](agents/review-agent.md) | Daily/weekly/monthly/quarterly reviews; patterns, blockers, wins, misses, improvement actions |
| [MCP Connector](agents/mcp-connector-agent.md) | Discovers available MCP tools, maps tools to workflows, enforces permission boundaries, writes connector usage notes |
| [Database Memory](agents/database-memory-agent.md) | MongoDB (or approved DB) for user-approved plans, reviews, habit logs, skill progress, evidence logs |
| [Knowledge & Search](agents/knowledge-search-agent.md) | Web/documentation search only when current external information is needed |
| [Quality Assurance](agents/quality-assurance-agent.md) | Checks every output for realism, overload risk, privacy, assumptions, actionability, success criteria |

Architecture and routing logic: [ARCHITECTURE.md](ARCHITECTURE.md)

## Workflows

- [Weekly Planning](workflows/weekly-planning.md)
- [Weekend Planning](workflows/weekend-planning.md)
- [Daily Execution](workflows/daily-execution.md)
- [Skill-Building](workflows/skill-building.md)
- [Professional Growth](workflows/professional-growth.md)
- [Personal Review](workflows/personal-review.md) (daily / weekly / monthly / quarterly)

## MCP & Data

- [MCP Integration Strategy](mcp/integration-strategy.md) — connector catalog, authorization protocol, privacy levels, connector usage note format
- [Database Strategy](database/mongodb-strategy.md) — MongoDB collections, schemas, retention, manual fallback ledger

## Templates & Examples

- [Output Templates](templates/output-templates.md) — the universal output contract every agent must follow
- Examples: [weekly plan](examples/weekly-plan-example.md) · [weekend plan](examples/weekend-plan-example.md) · [daily plan](examples/daily-plan-example.md) · [30/60/90 skill roadmap](examples/skill-roadmap-example.md) · [monthly review](examples/monthly-review-example.md) · [growth evidence log](examples/growth-evidence-log-example.md)
- [QA Checklists](quality/qa-checklists.md) — overload detection, privacy review, realism checks

## Universal Output Contract

Every output from this system includes:

1. **Objective** — what this output achieves
2. **Inputs used** — exactly what data informed it (manual + MCP)
3. **Assumptions** — anything inferred rather than provided
4. **Prioritized actions** — must-do / should-do / optional
5. **Capacity check** — estimated hours vs. available hours
6. **Risks & overload warnings** — flagged explicitly
7. **Tradeoffs** — what was deprioritized and why
8. **Success criteria** — how the user knows it worked
9. **Review checkpoint** — when and how to revisit
10. **Manual fallback** — how to do this without any tools
11. **Connector usage note** — only if MCP was used (services, purpose, data accessed/excluded, storage, risk level, scope, fallback)

## Acceptance Checklist

The system is complete only if it can produce all of the following (verified by examples and templates in this repo):

- [x] A realistic weekly plan — [example](examples/weekly-plan-example.md)
- [x] A realistic weekend plan — [example](examples/weekend-plan-example.md)
- [x] A daily execution plan — [example](examples/daily-plan-example.md)
- [x] A 30/60/90-day skill-building plan — [example](examples/skill-roadmap-example.md)
- [x] A monthly review — [example](examples/monthly-review-example.md)
- [x] A professional growth evidence log — [example](examples/growth-evidence-log-example.md)
- [x] MCP connector recommendations with privacy notes — [mcp/integration-strategy.md](mcp/integration-strategy.md)
- [x] MongoDB / database storage strategy — [database/mongodb-strategy.md](database/mongodb-strategy.md)
- [x] Manual fallback workflows — every workflow file, "Manual Fallback" section
- [x] Reusable output templates — [templates/output-templates.md](templates/output-templates.md)
- [x] Example user requests — each workflow file, "Example Requests" section
- [x] Example outputs — [examples/](examples/)
- [x] Quality checks for unrealistic or overloaded plans — [quality/qa-checklists.md](quality/qa-checklists.md)

## Quick Start (Manual Mode)

> **You:** "Plan my week. Here are my meetings: [paste]. My priorities: ship the API migration, prep the Q3 review deck, gym 3x. I have roughly 6 focused hours/day."

The Orchestrator routes to the Planning Agent, which runs the Weekly Planning workflow, the QA Agent checks for overload, and you get a capacity-checked plan in the universal output format. No connectors, no storage, nothing leaves the conversation.
