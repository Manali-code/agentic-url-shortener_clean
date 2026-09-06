class ApprovalGate:
    """Represents a gate that blocks release and high-impact actions until approved."""

    def __init__(self, required: bool = True):
        self.required = required
        self.approved = False
        self.reason = "Pending approval"

    def approve(self, reason: str = "Approved by human reviewer") -> None:
        self.approved = True
        self.reason = reason

    def reject(self, reason: str = "Rejected by human reviewer") -> None:
        self.approved = False
        self.reason = reason

    def reset(self) -> None:
        self.approved = False
        self.reason = "Pending approval"

    def is_approved(self) -> bool:
        return self.approved if self.required else True

    def status(self) -> dict:
        return {"required": self.required, "approved": self.approved, "reason": self.reason}
