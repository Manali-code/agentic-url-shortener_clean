import json
import os
from typing import Any, Optional


class RequirementsAgent:
    def __init__(self, client: Optional[Any] = None) -> None:
        self.client = client

    def capture_requirements(self, request: str) -> dict:
        if self.client is not None or os.getenv("OPENAI_API_KEY"):
            client = self.client
            if client is None:
                from openai import OpenAI

                client = OpenAI()
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                input=(
                    "Return JSON with keys source, request, acceptance_criteria, "
                    "risks, and status. Normalize this software request: " + request
                ),
            )
            result = json.loads(response.output_text)
            result["source"] = "requirements_agent"
            result["request"] = request
            result["status"] = "approved"
            return result
        return {
            "source": "requirements_agent",
            "request": request,
            "status": "approved",
        }
