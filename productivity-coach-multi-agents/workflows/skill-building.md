# Workflow: Skill-Building

**Owner:** Skill-Building Agent · **Supports:** Knowledge & Search (resources),
Planning (calendar reality), Professional Growth (evidence), Database Memory, QA

## Example Requests
- "I want to get good at system design — build me a plan."
- "I have 30 minutes a day. Help me learn Spanish / Rust / public speaking."
- "Day-30 check-in on my SQL roadmap."

## Steps

1. **Skill selection.** If multiple candidates: score impact (career/goals) ×
   interest × opportunity-to-practice (does daily life provide reps?). Pick ONE
   primary; park the rest with a revisit date.
2. **Baseline assessment.** 3–5 concrete capability probes ("explain X cold",
   "build Y without docs", "record 2-min talk") → level: novice /
   advanced-beginner / competent / proficient. Self-rating alone is insufficient.
3. **Target capability.** Observable and dated: "By day 90: <do specific thing>
   <under specific conditions>, evidenced by <artifact>."
4. **30/60/90 roadmap.**
   - **1–30 Fundamentals:** small near-daily reps (20–40 min), core concepts,
     first micro-artifact. Day-30 probe re-test.
   - **31–60 Application:** one realistic project forcing the skill under
     pressure; feedback loop active. Day-60 probe + project checkpoint.
   - **61–90 Consolidation:** production-grade artifact + teach/expose
     (writeup, talk, PR review, demo). Day-90 probe vs. target.
5. **Weekly practice plan.** Sessions sized to *actual* capacity (cross-check
   the Planning Agent's numbers; beginners cap at 5 sessions/week). Each
   session: objective, activity, output.
6. **Feedback loops.** Name the mechanism + frequency: mentor/peer review,
   automated tests, recordings, spaced-repetition stats, community critique.
7. **Progress metrics.** Countable only: sessions done/planned, probe scores at
   30/60/90, artifacts shipped, feedback rounds completed.
8. **Evidence artifacts.** One per phase, minimum. Offer handoff to the
   Professional Growth evidence log.
9. **Resources.** If current resources needed → Knowledge & Search with a
   GENERIC query (skill name + level + year; zero personal/employer context).
10. **QA gate** → universal contract.

## Check-ins (day 30/60/90)
Re-run probes, compare metrics, adjust roadmap (intensify / extend / pivot /
gracefully stop — stopping a low-value skill is a valid outcome, said plainly).

## Manual Fallback
Entire workflow is conversation-native. Resources without search: rely on
standard canonical materials with a "verify currency" disclaimer.

## Storage
Optional `skills` collection (roadmap + session log + probe results); otherwise
a copy-pasteable progress tracker table is emitted with the plan.
