from typing import Any, Dict, List


class PolicyEngine:
    """Checks workflow-specific constraints before release and enforces controlled autonomy."""

    def __init__(self):
        self.policies: Dict[str, Any] = {
            "require_tests": True,
            "require_docs": True,
            "require_approval": True,
            "max_retries": 2,
            "require_security_review": True,
        }

    def validate(self, workflow_state: Dict[str, Any]) -> bool:
        if workflow_state.get("tests_passed") is not True:
            return False
        if workflow_state.get("docs_ready") is not True:
            return False
        if workflow_state.get("approved") is not True:
            return False
        if workflow_state.get("security_reviewed") is not True:
            return False
        if workflow_state.get("retry_count", 0) > self.policies["max_retries"]:
            return False
        return True

    def evaluate(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        violations: List[str] = []
        if workflow_state.get("tests_passed") is not True:
            violations.append("tests_missing")
        if workflow_state.get("docs_ready") is not True:
            violations.append("docs_missing")
        if workflow_state.get("approved") is not True:
            violations.append("approval_missing")
        if workflow_state.get("security_reviewed") is not True:
            violations.append("security_review_missing")
        if workflow_state.get("retry_count", 0) > self.policies["max_retries"]:
            violations.append("retry_limit_exceeded")
        return {"valid": not violations, "violations": violations}
