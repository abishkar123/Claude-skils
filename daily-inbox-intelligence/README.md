# Daily Inbox Intelligence

A privacy-conscious Codex skill for reviewing recent Gmail messages, classifying actionable items, and preparing a daily inbox digest.

## What It Does

- Reviews recent Gmail messages.
- Identifies bills, renewals, meetings, interviews, recruiter outreach, and LinkedIn job alerts.
- Prepares proposed calendar actions for approval.
- Presents a digest in chat before taking external action.

## Safety Model

This skill is designed to avoid publishing or acting on private data by default:

- It does not send email without user approval.
- It does not create calendar events without user approval.
- It does not modify Gmail messages without user approval.
- It avoids sending full email bodies to third-party APIs unless explicitly approved.

See [SKILL.md](./SKILL.md) for the full workflow.
