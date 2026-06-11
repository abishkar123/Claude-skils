"""Reusable output templates: the universal output frame and connector notes."""

# Every agent output must contain these sections, in this order. The QA Agent
# rejects outputs that are missing any of them (connector note only when MCP
# was used).
REQUIRED_SECTIONS = (
    "OBJECTIVE",
    "INPUTS USED",
    "ASSUMPTIONS",
    "PRIORITIZED ACTIONS",
    "CAPACITY CHECK",
    "RISKS & OVERLOAD",
    "TRADEOFFS",
    "SUCCESS CRITERIA",
    "REVIEW CHECKPOINT",
    "MANUAL FALLBACK",
)

OUTPUT_FRAME = """\
Format your answer with EXACTLY these section headers, in this order:

OBJECTIVE          - one sentence
INPUTS USED        - manual: ... | MCP: ... | memory: ...
ASSUMPTIONS        - explicit list; every assumption must be challengeable
PRIORITIZED ACTIONS - Must / Should / Optional tiers, each action with a "when"
CAPACITY CHECK     - planned Xh vs available Yh (Z%) and pass/warn verdict
RISKS & OVERLOAD   - flagged days, fragile dependencies, overload warnings
TRADEOFFS          - what was deliberately deprioritized and why
SUCCESS CRITERIA   - measurable, checkable at the review checkpoint
REVIEW CHECKPOINT  - when and what to assess
MANUAL FALLBACK    - how to run/update this plan with no tools at all
STATE              - a compact 5-10 line paste-back block the user can carry
                     into the next session (only for durable artifacts)
"""


def connector_usage_note(*, services: str, purpose: str, accessed: str,
                         excluded: str, stored: str, risk: str,
                         scope: str, fallback: str) -> str:
    return (
        "\n--- Connector Usage Note ---\n"
        f"Services used:    {services}\n"
        f"Purpose:          {purpose}\n"
        f"Data accessed:    {accessed}\n"
        f"Data excluded:    {excluded}\n"
        f"Stored:           {stored}\n"
        f"Privacy risk:     {risk}\n"
        f"Permission scope: {scope}\n"
        f"Manual fallback:  {fallback}\n"
    )
