class RequirementsAgent:
    def capture_requirements(self, request: str) -> dict:
        return {
            "source": "requirements_agent",
            "request": request,
            "status": "approved",
        }
