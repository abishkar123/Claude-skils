# productivity-coach Multi Agents

A privacy-first, multi-agent productivity operating system built on the
Anthropic Python SDK. It handles weekly planning, weekend planning, daily
execution, 30/60/90-day skill-building, professional growth & evidence logs,
and daily/weekly/monthly/quarterly reviews — fully manually by default, with
opt-in MCP connectors and opt-in MongoDB memory.

## Architecture

```
user request ─▶ Orchestrator ─▶ domain agent ─▶ QA gate ─▶ final answer
                   │                │
                   │                ├─ Planning Agent (weekly / weekend / daily / habits)
                   │                ├─ Skill-Building Agent (30/60/90 roadmaps)
                   │                ├─ Professional Growth Agent (evidence logs, promotion readiness)
                   │                ├─ Review Agent (daily/weekly/monthly/quarterly)
                   │                └─ Knowledge & Search Agent (sanitized queries only)
                   │
                   ├─ MCP Connector Agent  (registry + 7-question safety gate + usage notes)
                   ├─ Database Memory Agent (MongoDB, opt-in; paste-back STATE otherwise)
                   └─ Quality Assurance Agent (deterministic checks + model review)
```

Three modes fall out of the permission model rather than a switch:

- **Manual** — default. No connector registered/authorized → agents work
  only from what you type.
- **MCP-Assisted** — a host registers real MCP calls
  (`MCPConnectorAgent.register`) *and* the user authorizes them
  (`--authorize calendar,tasks`). Every MCP-assisted output carries a
  Connector Usage Note (services, purpose, data accessed/excluded, stored,
  risk, scope, manual fallback).
- **Hybrid** — manual input plus approved connector data, strict data
  minimization (least-privilege scopes are hard-coded per connector).

## Hard rules enforced in code

- The 7-question pre-flight gate (`mcp_connector.gate`) blocks any connector
  that is unavailable, unnecessary, or unauthorized.
- `privacy.sanitize_search_query` **rejects** (never "cleans") search queries
  containing emails, phone numbers, deep URLs, or private-context markers.
- Storage is opt-in (`--enable-storage` + `MONGODB_URI`); without it the
  system stays stateless and emits paste-back `STATE` blocks.
- The QA Agent enforces the universal output frame, the ≤80% capacity rule,
  must-do/deep-work caps, and the presence of connector notes — with one
  automatic repair round before the answer is returned.

## Usage

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

python cli.py "Plan my week: ~30 focused hours. Ship the auth feature, prep
Thursday's design review, 3 gym sessions. Last week I overcommitted badly."

python cli.py "Build a 90-day plan to get good at system design, 5h/week,
I'm a mid-level backend dev."

python cli.py "Run my monthly review: shipped payments retry layer, missed
the blog post again, gym streak broke in week 3."

python cli.py "Which connectors would help my productivity system?"
```

As a library (e.g. to wire in real MCP calls):

```python
from productivity_coach import Orchestrator

orch = Orchestrator()
orch.connectors.register("calendar", fetch=my_calendar_mcp_call)
orch.connectors.authorize("calendar")   # only after the user said yes
print(orch.handle("Plan tomorrow around my meetings"))
```

## Layout

```
cli.py                              CLI entry point
productivity_coach/
  config.py                         model + capacity + storage settings
  privacy.py                        query sanitizer, permission ledger
  templates.py                      universal output frame, connector notes
  prompts.py                        all agent system prompts (workflow logic)
  orchestrator.py                   routing, MCP decision, QA gate, pipelines
  agents/
    base.py                         Anthropic API wrapper (streaming, adaptive thinking)
    workers.py                      Planning / Skill-Building / Growth / Review
    knowledge.py                    sanitized search agent
    mcp_connector.py                connector registry + safety gate
    memory.py                       MongoDB memory (opt-in) + graceful fallback
    qa.py                           deterministic + model QA gates
```
