"""Executable orchestration runtime for the agentic delivery workflow."""

from copy import deepcopy
from time import perf_counter
from typing import Any, Dict, Optional

from .approval_gate import ApprovalGate
from .graph import WorkflowGraph
from .metrics import WorkflowMetrics
from .policy_engine import PolicyEngine
from .state_store import StateStore
from .workflow import Workflow
from .agents.architecture_agent import ArchitectureAgent
from .agents.docs_agent import DocsAgent
from .agents.implementation_agent import ImplementationAgent
from .agents.release_agent import ReleaseAgent
from .agents.requirements_agent import RequirementsAgent
from .agents.testing_agent import TestingAgent


class Orchestrator:
    """Coordinates agents, shared state, governance, and auditable execution."""

    def __init__(self, approval_gate: Optional[ApprovalGate] = None) -> None:
        self.graph = WorkflowGraph()
        self.workflow = Workflow()
        self.state = StateStore()
        self.policy = PolicyEngine()
        self.approval_gate = approval_gate or ApprovalGate()
        self.metrics = WorkflowMetrics()
        self.lineage: list[Dict[str, Any]] = []
        self.agents = {
            "requirements": RequirementsAgent(),
            "architecture": ArchitectureAgent(),
            "implementation": ImplementationAgent(),
            "testing": TestingAgent(),
            "documentation": DocsAgent(),
            "release": ReleaseAgent(),
        }
        self._failure_plan: Dict[str, int] = {}

    def run(
        self,
        request: str,
        *,
        approve: bool = False,
        failure_plan: Optional[Dict[str, int]] = None,
        security_reviewed: bool = True,
    ) -> Dict[str, Any]:
        """Run until completion or the first governance gate that blocks progress."""
        if approve:
            self.approval_gate.approve("Approved by run option")
        self._failure_plan = dict(failure_plan or {})
        self.state.set("request", request)
        self.state.set("security_reviewed", security_reviewed)
        self._execute_ready_steps()
        return self.snapshot()

    def approve_and_resume(self, reason: str = "Approved by human reviewer") -> Dict[str, Any]:
        self.approval_gate.approve(reason)
        self._execute_ready_steps()
        return self.snapshot()

    def _execute_ready_steps(self) -> None:
        completed = {
            name for name, details in self.workflow.snapshot().items() if details["status"] == "completed"
        }
        while True:
            ready = self.graph.next_ready_steps(completed)
            if not ready:
                return
            if len(ready) > 1:
                self._record("workflow", "parallel_batch_ready", list(ready))
            progressed = False
            for step_name in ready:
                if self._run_step(step_name):
                    completed.add(step_name)
                    progressed = True
            if not progressed:
                return

    def _run_step(self, step_name: str) -> bool:
        step = self.workflow.get_step(step_name)
        if step is None:
            self.workflow.add_step(step_name)
            step = self.workflow.get_step(step_name)
        assert step is not None
        metadata = self.graph.get_step(step_name)
        if metadata["requires_approval"] and not self.approval_gate.is_approved():
            self.workflow.set_status(step_name, "blocked", "Awaiting human approval")
            self._record(step_name, "blocked", "approval_required")
            return False

        checkpoint = deepcopy(self.state.snapshot())
        started = perf_counter()
        max_retries = metadata["retries"]
        while True:
            try:
                if self._failure_plan.get(step_name, 0) > 0:
                    self._failure_plan[step_name] -= 1
                    raise RuntimeError("planned transient failure")
                result = self._invoke_agent(step_name)
                if step_name == "release":
                    policy_result = self.policy.evaluate(self.state.snapshot())
                    if not policy_result["valid"]:
                        raise PermissionError("policy violations: " + ", ".join(policy_result["violations"]))
                self.workflow.set_status(step_name, "completed", result["status"])
                self.metrics.record_success()
                self.metrics.observe_latency(perf_counter() - started)
                self._record(step_name, "completed", result)
                return True
            except Exception as exc:
                self.state.restore(checkpoint)
                self.metrics.record_failure()
                self._record(step_name, "failed", str(exc))
                if step.retry_count >= max_retries:
                    self.workflow.set_status(step_name, "stopped", error=str(exc))
                    self.metrics.observe_latency(perf_counter() - started)
                    return False
                step.retry_count += 1
                self.metrics.record_retry()
                self.metrics.record_rollback()
                self._record(step_name, "replanned", {"retry": step.retry_count})

    def _invoke_agent(self, step_name: str) -> Dict[str, Any]:
        if step_name == "requirements":
            result = self.agents[step_name].capture_requirements(self.state.get("request", ""))
        elif step_name == "architecture":
            result = self.agents[step_name].propose_architecture(self.state.get("requirements", {}))
        elif step_name == "implementation":
            result = self.agents[step_name].implement(self.state.get("architecture", {}))
        elif step_name == "testing":
            result = self.agents[step_name].validate(self.state.get("implementation", {}))
            self.state.set("tests_passed", result.get("status") == "tests_passed")
        elif step_name == "documentation":
            result = self.agents[step_name].draft_docs(self.state.get("architecture", {}))
            self.state.set("docs_ready", result.get("status") == "documentation_ready")
        else:
            self.state.set("approved", self.approval_gate.is_approved())
            result = self.agents[step_name].prepare_release(self.state.get("testing", {}))
        self.state.set(step_name, result)
        return result

    def _record(self, step: str, event: str, detail: Any) -> None:
        self.lineage.append({"step": step, "event": event, "detail": detail})

    def snapshot(self) -> Dict[str, Any]:
        return {
            "workflow": self.workflow.snapshot(),
            "state": self.state.snapshot(),
            "approval": self.approval_gate.status(),
            "policy": self.policy.evaluate(self.state.snapshot()),
            "metrics": self.metrics.snapshot(),
            "lineage": list(self.lineage),
        }