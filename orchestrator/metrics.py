from dataclasses import dataclass, field
from time import perf_counter
from typing import Dict, List


@dataclass
class WorkflowMetrics:
    tasks_completed: int = 0
    tasks_failed: int = 0
    retries: int = 0
    rollbacks: int = 0
    latency_samples: List[float] = field(default_factory=list)
    start_time: float = field(default_factory=lambda: perf_counter())

    def record_success(self) -> None:
        self.tasks_completed += 1

    def record_failure(self) -> None:
        self.tasks_failed += 1

    def record_retry(self) -> None:
        self.retries += 1

    def record_rollback(self) -> None:
        self.rollbacks += 1

    def observe_latency(self, seconds: float) -> None:
        self.latency_samples.append(seconds)

    def success_rate(self) -> float:
        total = self.tasks_completed + self.tasks_failed
        return (self.tasks_completed / total) if total else 0.0

    def average_latency(self) -> float:
        return sum(self.latency_samples) / len(self.latency_samples) if self.latency_samples else 0.0

    def mttr_seconds(self) -> float:
        if self.tasks_failed == 0:
            return 0.0
        return self.average_latency() * self.tasks_failed

    def snapshot(self) -> Dict[str, float | int]:
        return {
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "retries": self.retries,
            "rollbacks": self.rollbacks,
            "success_rate": self.success_rate(),
            "average_latency_seconds": self.average_latency(),
            "mttr_seconds": self.mttr_seconds(),
        }
