# Connector Guidance

Use connectors only when the user asks for them or when explicitly available in the current environment. Never assume access. Always offer a manual fallback.

## Permission Boundaries

General rules:
- Request read-only access where possible.
- Do not send, delete, archive, edit, publish, commit, or share without explicit confirmation.
- Summarize sensitive records instead of reproducing them.
- Prefer date ranges and labels over broad account access.
- Explain what data is needed and why.

## Calendar

Useful for:
- Capturing fixed commitments
- Finding focus blocks
- Flagging overloaded days
- Monday preparation

Minimum data:
- Event title, time, duration, optional location
- Avoid attendee details unless needed

Manual fallback:
- Ask the user to paste a day/week schedule or list fixed commitments.

## Email

Useful for:
- Finding commitments, waiting-for items, deadlines, and follow-ups

Minimum data:
- Search queries, sender/category, subject, dates, snippets
- Avoid full email bodies unless needed

Manual fallback:
- Ask for a short list: pending replies, promised deliverables, waiting-for items, deadlines.

## Task Manager

Useful for:
- Backlog triage
- Due-date review
- Daily Top 3 selection
- Weekly capacity planning

Minimum data:
- Task title, due date, project, priority, status

Manual fallback:
- Ask user to paste task list grouped by project or urgency.

## Notes

Useful for:
- Reviewing goals, meeting notes, project plans, reflections, habit logs

Minimum data:
- Relevant page titles and summaries first

Manual fallback:
- Ask for the current goals, notes excerpts, or decisions.

## Documents

Useful for:
- Performance reviews
- Resume/LinkedIn updates
- Project briefs
- Evidence extraction

Minimum data:
- Specific document or excerpt

Manual fallback:
- Ask user to paste accomplishments, feedback, or project summaries.

## GitHub

Useful for:
- Engineering impact tracking
- Project evidence
- Pull request and issue review
- Release and contribution summaries

Minimum data:
- Repo, PR/issue titles, dates, merged status, review comments only when needed

Manual fallback:
- Ask for shipped projects, PR links, issue summaries, metrics, and stakeholder outcomes.

## Collaboration Tools

Examples: Slack, Teams, Linear, Jira, Notion, Asana.

Useful for:
- Commitments made in messages
- Project status
- Stakeholder asks
- Decision history

Minimum data:
- Channel/project, date range, message snippets or ticket metadata

Manual fallback:
- Ask for decisions, blockers, asks, and promised follow-ups in bullet form.

## Connector Recommendation Output

For each recommended connector include:
- Purpose
- Minimum permission
- Data read
- Actions requiring confirmation
- Privacy risk
- Manual fallback
