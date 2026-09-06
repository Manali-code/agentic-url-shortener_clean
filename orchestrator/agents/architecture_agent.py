import json
import os
from typing import Any, Optional


class ArchitectureAgent:
    def __init__(self, client: Optional[Any] = None) -> None:
        self.client = client

    def propose_architecture(self, requirements: dict) -> dict:
        if self.client is not None or os.getenv("OPENAI_API_KEY"):
            client = self.client
            if client is None:
                from openai import OpenAI

                client = OpenAI()
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                input=(
                    "Return JSON with keys source, requirements, design, "
                    "data_flow, risks, and status. Design a pragmatic URL shortener "
                    "architecture for these requirements: " + json.dumps(requirements)
                ),
            )
            result = json.loads(response.output_text)
            result["source"] = "architecture_agent"
            result["requirements"] = requirements
            result["status"] = "ready"
            return result
        return {
            "source": "architecture_agent",
            "requirements": requirements,
            "design": "FastAPI + SQLAlchemy + LangGraph orchestration",
            "status": "ready",
        }
