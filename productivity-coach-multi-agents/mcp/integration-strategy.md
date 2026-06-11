# MCP Integration Strategy

Owned by the MCP Connector Agent. Governing principles: discover before use,
authorize per service *and purpose*, least privilege, data minimization, manual
fallback always, no chained authorization, no private data in search queries.

## Authorization Protocol

1. **Discover:** enumerate actually-available tools at session start or first
   need. Build the session inventory. A service in this catalog that isn't
   discovered is treated as nonexistent.
2. **Propose:** when a workflow would benefit, present the user a choice:
   `[service] could provide [exact data] for [purpose]. Alternative: paste it
   manually. Use the connector? (read-only, nothing stored)`
3. **Scope:** authorization = service + purpose + session. Purpose change →
   re-ask. Writes (send, create, post) → confirmed individually, every time.
4. **Record:** every use produces a Connector Usage Note (format in
   agents/mcp-connector-agent.md) attached to the output.

## Connector Catalog

For each connector: what it's used for, exact data accessed, what's always
excluded, default scope, privacy risk, and manual fallback.

### Gmail / Email
- **Workflows:** weekly planning (commitments/deadlines from flagged threads), professional growth (user-named praise/commitment threads), communication drafts.
- **Access:** user-flagged or user-named threads only; subject + sender + date + the specific commitment lines. Date-bounded searches with user-approved query terms.
- **Excluded always:** inbox scans, full bodies unless the user names the thread, attachments, contacts.
- **Scope:** read-only; drafts created only on request and never auto-sent.
- **Risk:** HIGH (third-party content). Per-item confirmation.
- **Fallback:** "paste the 2–3 emails or commitments you want handled."

### Google Calendar / Calendar
- **Workflows:** weekly/daily planning (availability, meeting load, overloaded days, deep-work placement), weekend planning (fixed events).
- **Access:** event start/end/duration for a bounded range on user-named calendar(s). Titles only if needed for prioritization and approved.
- **Excluded by default:** titles, attendees, descriptions, locations, other calendars.
- **Scope:** read-only. Event creation (e.g., blocking deep work) is a write → per-event confirmation.
- **Risk:** LOW (times only) → MEDIUM (with titles).
- **Fallback:** "paste your meeting times for the week."

### Google Tasks / task managers
- **Workflows:** weekly/daily planning (open tasks, overdue items, prioritization).
- **Access:** task titles, due dates, status from user-named lists.
- **Excluded:** notes/descriptions unless needed, completed history beyond the review window.
- **Scope:** read-only default; completing/creating tasks confirmed per action.
- **Risk:** LOW–MEDIUM.
- **Fallback:** paste the task list.

### Google Drive / documents
- **Workflows:** planning notes, project updates, evidence capture.
- **Access:** user-NAMED files only — never folder/workspace crawls, never search across the drive without an approved, specific query.
- **Excluded:** everything not named; permissions/sharing metadata.
- **Scope:** read-only; document creation on request only.
- **Risk:** MEDIUM–HIGH depending on content.
- **Fallback:** paste the relevant section.

### GitHub
- **Workflows:** professional growth (PRs, commits, releases as evidence), skill-building (project artifacts).
- **Access:** merged PRs / commits / releases authored by the user in NAMED repos, date-bounded; titles + links + stats.
- **Excluded:** code contents, other people's activity, repos not named, issues/discussions unless requested.
- **Scope:** read-only. Comments/PRs are writes → per-action confirmation.
- **Risk:** LOW–MEDIUM (employer code metadata).
- **Fallback:** paste PR titles/links or describe shipped work.

### Internet search (web / docs)
- **Workflows:** skill-building resources, current documentation, tool research. Routed ONLY through the Knowledge & Search Agent.
- **Access:** generic queries only. Hard rule: zero personal/employer/email/document/calendar/database content in any query — taint check before every search.
- **Risk:** LOW *if hygiene holds*; query leakage is the threat model.
- **Fallback:** canonical-resource suggestions from model knowledge + freshness disclaimer.

### MongoDB / database MCP
- **Workflows:** persistence for plans, reviews, habit logs, skill progress, evidence (Database Memory Agent only). Full strategy: database/mongodb-strategy.md.
- **Access:** the dedicated productivity database/collections only; schema-validated writes; scoped reads.
- **Excluded:** any other databases/collections on the same server.
- **Scope:** readWrite on one database, ideally a dedicated DB user.
- **Risk:** MEDIUM (aggregated personal data) — mitigated by minimization + retention rules.
- **Fallback:** manual ledger blocks (pasteable YAML/Markdown records).

### Notes tools (Notion as notes, Obsidian, Apple Notes via MCP, etc.)
- **Workflows:** reflections, learning notes, planning history.
- **Access:** user-named pages/notes; append-only writes to a dedicated "Productivity" page/section with approval.
- **Excluded:** vault/workspace scans.
- **Risk:** MEDIUM.
- **Fallback:** outputs are Markdown — user pastes them into their own notes.

### Collaboration tools (Slack, Teams, Jira, Linear, Trello, Asana, Notion-as-PM, ClickUp, Confluence)
- **Workflows:** weekly planning (assigned tickets, blockers), professional growth (closed epics, stakeholder feedback the user names).
- **Access:** items assigned to the user, status + title + due date, bounded to current sprint/cycle; user-named threads/messages only for feedback capture.
- **Excluded always:** channel/message scans, other people's items, DM content, full ticket comment histories.
- **Scope:** read-only; posting updates is a per-message confirmed write.
- **Risk:** HIGH (employer + third-party content). Most conservative defaults of any connector.
- **Fallback:** "paste your sprint board / the blockers you want addressed."

## Recommended Connector Sets (privacy-ranked)

| Profile | Connectors | Why |
|---|---|---|
| **Minimal (recommended start)** | none — Manual Mode | Full functionality, zero exposure |
| **Planner** | Calendar (read-only, times only) + Tasks (read-only) | Biggest planning payoff per unit of risk; both LOW risk |
| **Builder** | Planner + GitHub (read-only, named repos) + web search (sanitized) | Adds evidence + resources at LOW–MEDIUM risk |
| **Full** | Builder + DB + named-item access to email/docs/collab tools | Maximum assistance; HIGH-risk items stay per-item confirmed |

Escalate one profile at a time, only when the user feels the manual friction.

## Threat Model Summary
1. **Over-collection** → exact-data specification + exclusions before every call.
2. **Purpose creep** → authorization bound to purpose; re-ask on change.
3. **Search leakage** → single search agent + taint check + generic-query rule.
4. **Cross-service exfiltration** → no chained authorization between connectors.
5. **Silent persistence** → storage only via Database Memory Agent's gate.
6. **Write surprises** → every external write individually confirmed.
