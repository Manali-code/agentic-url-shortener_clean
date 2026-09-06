from collections import defaultdict, deque
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


class WorkflowGraph:
    """Dependency-aware workflow graph for requirements -> architecture -> implementation -> testing -> release."""

    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Set[str]] = defaultdict(set)
        self._register_step(
            "requirements",
            dependencies=[],
            requires_approval=False,
            retries=1,
            stage="planning",
            description="Capture and normalize product intent",
        )
        self._register_step(
            "architecture",
            dependencies=["requirements"],
            requires_approval=False,
            retries=1,
            stage="design",
            description="Translate requirements into design and sequencing",
        )
        self._register_step(
            "implementation",
            dependencies=["architecture"],
            requires_approval=False,
            retries=2,
            stage="build",
            description="Implement the URL shortener and orchestrator runtime",
        )
        self._register_step(
            "testing",
            dependencies=["implementation"],
            requires_approval=False,
            retries=2,
            stage="validation",
            description="Validate behavior, regression risk, and reliability",
        )
        self._register_step(
            "documentation",
            dependencies=["architecture", "implementation"],
            requires_approval=False,
            retries=1,
            stage="governance",
            description="Produce architecture and operational documentation",
        )
        self._register_step(
            "release",
            dependencies=["testing", "documentation"],
            requires_approval=True,
            retries=1,
            stage="release",
            description="Release candidate approved for deployment",
        )

    def _register_step(
        self,
        name: str,
        dependencies: Optional[Iterable[str]] = None,
        requires_approval: bool = False,
        retries: int = 0,
        stage: str = "general",
        description: str = "",
    ) -> None:
        self.nodes[name] = {
            "name": name,
            "dependencies": list(dependencies or []),
            "requires_approval": requires_approval,
            "retries": retries,
            "stage": stage,
            "description": description,
        }
        for dependency in dependencies or []:
            self.edges[dependency].add(name)

    def build(self) -> List[str]:
        indegree: Dict[str, int] = {name: 0 for name in self.nodes}
        for name, node in self.nodes.items():
            for dependency in node["dependencies"]:
                indegree[name] += 1

        queue = deque(sorted(name for name, degree in indegree.items() if degree == 0))
        ordered: List[str] = []
        while queue:
            item = queue.popleft()
            ordered.append(item)
            for child in sorted(self.edges.get(item, set())):
                indegree[child] -= 1
                if indegree[child] == 0:
                    queue.append(child)

        if len(ordered) != len(self.nodes):
            raise ValueError("Workflow graph contains a cycle or unresolved dependency")
        return ordered

    def next_ready_steps(self, completed: Iterable[str], skipped: Iterable[str] = ()) -> List[str]:
        completed_set = set(completed)
        skipped_set = set(skipped)
        ready: List[str] = []
        for name, node in self.nodes.items():
            if name in completed_set or name in skipped_set:
                continue
            dependencies = node["dependencies"]
            if all(dep in completed_set for dep in dependencies):
                ready.append(name)
        return sorted(ready)

    def get_step(self, name: str) -> Dict[str, Any]:
        return self.nodes[name]

    def status(self) -> Dict[str, Any]:
        return {
            "graph": list(self.nodes.keys()),
            "ready": True,
            "entry_points": [name for name, node in self.nodes.items() if not node["dependencies"]],
            "exit_points": [name for name, node in self.nodes.items() if not self.edges.get(name)],
        }

    def parallel_paths(self) -> Dict[str, List[str]]:
        groups: Dict[str, List[str]] = {}
        for name, node in self.nodes.items():
            groups.setdefault(node["stage"], [])
            groups[node["stage"]].append(name)
        return groups
