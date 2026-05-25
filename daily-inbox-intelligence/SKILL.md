---
name: daily-inbox-intelligence
description: >
  A privacy-conscious daily inbox triage skill that reviews recent Gmail messages,
  classifies actionable items such as bills, renewals, meetings, interviews,
  recruiter outreach, and job alerts, then prepares a digest and proposed calendar
  actions for the user to approve. Trigger this skill when the user asks to run a
  daily inbox check, triage their inbox, summarize recent email, check for bills
  or job opportunities, or prepare a daily digest.
compatibility: "Requires Gmail MCP and optionally Google Calendar MCP. LLM-based classification is optional."
---

# Daily Inbox Intelligence Skill

Review recent Gmail messages, classify actionable items, prepare a digest, and propose calendar actions for user approval.

## Privacy And Safety Rules

- Do not send emails, create calendar events, archive messages, delete messages, label messages, or mark messages as read without explicit user approval.
- Do not forward full email bodies to third-party APIs unless the user has explicitly approved that for this run.
- Prefer local reasoning over external classification when the available message metadata and snippet are enough.
- If external classification is approved, send the minimum necessary content: subject, sender domain, snippet, and only the relevant body excerpt.
- Redact account numbers, addresses, phone numbers, access codes, payment card details, and other sensitive identifiers before including content in prompts or digests.
- Treat the digest as private. Prepare it for the user in chat first unless they explicitly ask for an email draft or approve sending it.

## Overview

1. Fetch recent Gmail threads from the last 24 hours.
2. Classify relevant messages into actionable categories.
3. Extract dates, amounts, organizations, and concise notes where available.
4. Prepare proposed calendar actions for bills, renewals, meetings, and interviews.
5. Present a daily digest and ask for approval before taking any external action.

## Step 1 - Fetch Gmail Threads

Use the Gmail MCP tool to search for recent emails.

Search queries to run, in parallel when possible:

- `newer_than:1d`
- `(invoice OR bill OR payment OR due OR statement OR renewal OR subscription) newer_than:7d`
- `(interview OR meeting OR appointment OR calendar) newer_than:7d`
- `(recruiter OR hiring OR "job opportunity" OR "application update") newer_than:7d`
- `from:linkedin.com newer_than:7d`

Extract this metadata per email:

- `id`
- `threadId`
- `subject`
- `from`
- `snippet`
- `date`
- relevant body excerpt only when needed

Avoid fetching full bodies for messages that are clearly irrelevant from metadata and snippet.

## Step 2 - Classify Emails

Classify each relevant email into exactly one category:

- `BILL`: payment due, invoice, account statement, utility bill, phone bill, internet bill, rent, loan, or credit card payment.
- `SUBSCRIPTION`: renewal notice, membership renewal, trial ending, price change, or auto-renewal.
- `MEETING`: meeting invite, interview scheduled, appointment confirmation, or calendar invitation.
- `JOB`: recruiter outreach, hiring manager contact, job opportunity, application update, or interview process update.
- `LINKEDIN`: LinkedIn job alerts, job recommendations, profile views, recruiter messages, or connection requests.
- `IGNORE`: promotions, newsletters, spam, receipts with no action needed, and unrelated social notifications.

Return structured data in this shape:

```json
{
  "category": "BILL | SUBSCRIPTION | MEETING | JOB | LINKEDIN | IGNORE",
  "confidence": 0.0,
  "extracted": {
    "title": "short title or null",
    "date": "YYYY-MM-DD or null",
    "time": "HH:MM or null",
    "amount": "amount or null",
    "organization": "organization or sender name",
    "notes": "one-line private summary"
  }
}
```

Skip messages where `confidence < 0.6` or the category is `IGNORE`, unless the message looks financially or time sensitive.

## Step 3 - Prepare Calendar Proposals

Do not create calendar events immediately. Build a list of proposed actions for user approval.

For `BILL` and `SUBSCRIPTION`:

- If a clear date is available, propose an all-day event on that date.
- Propose a reminder action 3 days before the date.
- Use generic event titles such as `Pay [organization]` or `[organization] renewal`.
- Include the amount only if it is useful and not sensitive.
- For Google Calendar all-day events, set the `end.date` to the day after `start.date`.

For `MEETING`:

- If a clear date and time are available, propose a timed event.
- Default to 1 hour only when no duration is available.
- Preserve timezone details when present in the email.

For `JOB` and `LINKEDIN`:

- Do not propose calendar events unless there is a concrete interview, deadline, or follow-up date.
- Include concise summaries in the digest.

## Step 4 - Present Digest

Present a digest in chat with these sections when relevant:

```text
Daily Inbox Digest - [Date]

Actions proposed
- [calendar/email/label actions that need approval]

Bills and subscriptions
- [organization] - [amount if useful] - [date or "date not found"] - [status]

Meetings and interviews
- [title] - [date/time] - [status]

Job opportunities
- [sender or company] - [role or summary]

LinkedIn alerts
- [summary of relevant job alerts]

Needs attention
- [items missing dates, unclear instructions, or low-confidence but important]

Summary
- [number] emails scanned
- [number] relevant
- [number] ignored
```

After presenting the digest, ask the user which proposed actions they want to approve.

## Handling Missing Dates

If a bill, subscription, meeting, or interview email does not contain a clear date:

1. Do not guess the date.
2. Include it in the `Needs attention` section.
3. Say that the date could not be extracted and the user should check manually.

## Error Handling

| Situation | Action |
|---|---|
| Gmail fetch returns 0 emails | Say no recent emails matched the search window. |
| Calendar event proposal cannot be built | Include the item in `Needs attention`. |
| Classification confidence is below 0.6 | Skip unless the message appears financially or time sensitive. |
| Due date already passed | Flag as overdue in the digest. |
| Possible duplicate action | Search existing calendar events or prior digest context before proposing creation. |

## Approval Checklist

Before taking action outside the chat, confirm:

- Which calendar events to create.
- Which reminder events or notifications to create.
- Whether to draft or send a digest email.
- Whether to label, archive, or otherwise modify any Gmail messages.
