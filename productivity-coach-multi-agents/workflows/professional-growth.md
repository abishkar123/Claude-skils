# Workflow: Professional Growth

**Owner:** Professional Growth Agent · **Supports:** Review (capture cadence),
Skill-Building (competency gaps), MCP Connector, Database Memory, QA

## Example Requests
- "I want to make senior engineer by next cycle — where do I stand?"
- "Log this week's wins for my promotion case."
- "Turn my evidence log into resume bullets."
- "Coach me on the status update I'm about to send." (draft only — user sends)

## Steps

1. **Career goal frame.** Target role/level + timeline + ladder competencies
   (user's real ladder if pasted; industry-standard otherwise, flagged in
   Assumptions).
2. **Promotion readiness gap analysis.** Per competency: current evidence /
   gap / next evidence-producing action. Output a readiness table, not a
   verdict — the user's manager owns the verdict; the table preps the
   conversation.
3. **Project impact tracking.** For each active project: stakeholders, intended
   outcome, current measurable impact, visibility status (do the people who
   matter know?).
4. **Evidence log.** STAR-with-numbers entries:
   `date | project | situation/task | action | result (quantified) |
   competency tags | corroboration link`.
   Capture prompts fire at weekly review. Entries without numbers get one
   follow-up: "what changed, by how much, for whom?"
5. **Stakeholder value & visibility.** Lightweight actions only: monthly status
   note, demo at team meeting, doc share. No politics.
6. **Communication coaching.** Drafts (status updates, self-reviews, promo
   docs, difficult-conversation openers): outcome first, quantified, hedging
   cut. Always labeled DRAFT; the system never sends on the user's behalf
   without per-message confirmation via the write gate.
7. **Resume/LinkedIn capture.** On demand, compile log → bullets:
   `<action verb> <scope> <quantified result>`. Tailorable per target role.
8. **QA gate** → universal contract.

## MCP usage (each through the 7-question gate)
- **GitHub:** merged PRs / releases in named repos, date-bounded → technical
  evidence candidates. Excluded: code contents, private repos not named.
- **Jira/Linear/Trello/Asana:** closed items/epics for the user, date-bounded.
- **Drive/Notion/Confluence:** user-NAMED docs only; never workspace crawls.
- **Gmail/Slack/Teams:** user-NAMED threads (praise, commitments) only; never
  inbox/channel scans. Risk: high — confirm per item.

## Manual Fallback
Weekly 3-question capture: "What shipped? What was the measurable result? Who
noticed/benefited?" Pasted into the log. Promotion analysis runs on the pasted
ladder + recalled evidence.

## Storage
`evidence` collection — **work-sensitive**: storage confirmed explicitly,
user warned it contains employer data, export/delete on demand. Otherwise the
log lives as a Markdown table the user keeps (template provided).
