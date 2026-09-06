class ArchitectureAgent:
    def propose_architecture(self, requirements: dict) -> dict:
        return {
            "source": "architecture_agent",
            "requirements": requirements,
            "design": "FastAPI + SQLAlchemy + LangGraph orchestration",
            "status": "ready",
        }
