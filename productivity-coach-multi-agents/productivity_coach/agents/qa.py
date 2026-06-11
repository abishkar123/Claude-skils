"""Quality Assurance Agent.

Two layers:
1. Deterministic checks (cheap, always run): required sections present,
   capacity utilization parseable and within limits, connector note present
   when MCP was used.
2. Model review (one call): realism, overload, assumptions, actionability,
   success criteria — returns PASS or FAIL with reasons.

The QA agent never patches outputs; failures go back to the owning agent.
"""

import re
from dataclasses import dataclass, field

from .. import prompts
from ..config import settings
from ..templates import REQUIRED_SECTIONS
from .base import BaseAgent

CAPACITY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*h[^0-9]{0,20}(\d+(?:\.\d+)?)\s*h", re.I)
PERCENT_RE = re.compile(r"(\d{1,3})\s*%")


@dataclass
class QAResult:
    passed: bool
    failures: list = field(default_factory=list)

    def report(self) -> str:
        return "PASS" if self.passed else "FAIL:\n- " + "\n- ".join(self.failures)


class QAAgent(BaseAgent):
    name = "qa"
    system_prompt = prompts.QA_REVIEW

    def deterministic_checks(self, output: str, mcp_used: bool) -> QAResult:
        failures = []
        for section in REQUIRED_SECTIONS:
            if section not in output:
                failures.append(f"missing required section: {section}")
        if mcp_used and "Connector Usage Note" not in output:
            failures.append("MCP was used but no Connector Usage Note is present")

        # Capacity: prefer an explicit percentage; fall back to Xh vs Yh.
        utilization = None
        pct = PERCENT_RE.search(output.split("CAPACITY CHECK")[-1][:300]) \
            if "CAPACITY CHECK" in output else None
        if pct:
            utilization = int(pct.group(1)) / 100
        else:
            hours = CAPACITY_RE.search(output)
            if hours and float(hours.group(2)) > 0:
                utilization = float(hours.group(1)) / float(hours.group(2))
        if utilization is not None:
            if utilization > settings.hard_capacity_limit:
                failures.append(
                    f"plan exceeds 100% of capacity ({utilization:.0%}) — re-triage"
                )
            elif utilization > settings.max_capacity_utilization:
                failures.append(
                    f"plan exceeds the 80% capacity rule ({utilization:.0%})"
                )
        return QAResult(passed=not failures, failures=failures)

    def model_review(self, output: str) -> QAResult:
        verdict = self.run(f"Draft output to review:\n\n{output}")
        first = verdict.strip().splitlines()[0].strip().upper() if verdict.strip() else ""
        if first.startswith("PASS"):
            return QAResult(passed=True)
        reasons = [ln.strip("- ").strip()
                   for ln in verdict.strip().splitlines()[1:] if ln.strip()]
        return QAResult(passed=False, failures=reasons or ["model review failed"])

    def gate(self, output: str, mcp_used: bool, deep: bool = True) -> QAResult:
        result = self.deterministic_checks(output, mcp_used)
        if not result.passed or not deep:
            return result
        return self.model_review(output)
