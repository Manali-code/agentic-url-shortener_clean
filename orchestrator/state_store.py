from typing import Any, Dict, Optional


class StateStore:
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.history: Dict[str, list] = {}

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value
        self.history.setdefault(key, []).append(value)

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def get_history(self, key: str) -> list:
        return list(self.history.get(key, []))

    def update(self, updates: Dict[str, Any]) -> None:
        for key, value in updates.items():
            self.set(key, value)

    def reset(self) -> None:
        self.state.clear()
        self.history.clear()

    def snapshot(self) -> Dict[str, Any]:
        return dict(self.state)

    def fork(self) -> "StateStore":
        clone = StateStore()
        clone.state = dict(self.state)
        clone.history = {key: list(values) for key, values in self.history.items()}
        return clone
