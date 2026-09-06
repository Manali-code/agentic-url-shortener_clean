from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class WorkflowStep:
    name: str
    status: str = "pending"
    notes: str = ""
    retry_count: int = 0
    approved: bool = False
    last_error: Optional[str] = None


@dataclass
class Workflow:
    steps: List[WorkflowStep] = field(default_factory=list)

    def add_step(self, name: str) -> None:
        self.steps.append(WorkflowStep(name=name))

    def get_step(self, name: str) -> Optional[WorkflowStep]:
        for step in self.steps:
            if step.name == name:
                return step
        return None

    def set_status(self, name: str, status: str, notes: str = "", error: Optional[str] = None) -> None:
        step = self.get_step(name)
        if step is None:
            self.add_step(name)
            step = self.get_step(name)
        step.status = status
        if notes:
            step.notes = notes
        if error:
            step.last_error = error

    def mark_approved(self, name: str) -> None:
        step = self.get_step(name)
        if step is not None:
            step.approved = True

    def snapshot(self) -> Dict[str, Any]:
        return {
            step.name: {
                "status": step.status,
                "notes": step.notes,
                "retry_count": step.retry_count,
                "approved": step.approved,
                "last_error": step.last_error,
            }
            for step in self.steps
        }

    def record_retry(self, name: str) -> None:
        step = self.get_step(name)
        if step is not None:
            step.retry_count += 1

    def execute(self, graph: Any, executor: Callable[[str], str], approval: Optional[Any] = None) -> Dict[str, Any]:
        for step_name in graph.build():
            if self.get_step(step_name) is None:
                self.add_step(step_name)

            step = self.get_step(step_name)
            if step is None:
                continue

            if graph.get_step(step_name)["requires_approval"] and approval is not None:
                if not approval.is_approved():
                    step.status = "blocked"
                    step.notes = "Awaiting human approval"
                    continue

            try:
                result = executor(step_name)
                step.status = "completed"
                step.notes = result
            except Exception as exc:  # pragma: no cover - defensive runtime guard
                step.status = "failed"
                step.last_error = str(exc)
                step.retry_count += 1
                if step.retry_count > 2:
                    step.status = "stopped"
                    raise

        return self.snapshot()
