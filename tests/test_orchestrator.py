from orchestrator import Orchestrator


def test_release_blocks_until_approval_then_resumes():
    orchestrator = Orchestrator()
    blocked = orchestrator.run("Deliver a URL shortener")

    assert blocked["workflow"]["release"]["status"] == "blocked"
    assert blocked["workflow"]["testing"]["status"] == "completed"
    assert blocked["policy"]["violations"] == ["approval_missing"]

    released = orchestrator.approve_and_resume()

    assert released["workflow"]["release"]["status"] == "completed"
    assert released["policy"]["valid"] is True
    assert released["metrics"]["tasks_completed"] == 6
    assert any(event["event"] == "blocked" for event in released["lineage"])


def test_transient_failure_retries_and_rolls_back():
    orchestrator = Orchestrator()
    result = orchestrator.run(
        "Deliver a URL shortener", approve=True, failure_plan={"implementation": 1}
    )

    implementation = result["workflow"]["implementation"]
    assert implementation["status"] == "completed"
    assert implementation["retry_count"] == 1
    assert result["metrics"]["retries"] == 1
    assert result["metrics"]["rollbacks"] == 1
    assert any(event["event"] == "failed" for event in result["lineage"])


def test_policy_violation_stops_release():
    orchestrator = Orchestrator()
    result = orchestrator.run(
        "Deliver a URL shortener", approve=True, security_reviewed=False
    )

    release = result["workflow"]["release"]
    assert release["status"] == "stopped"
    assert "security_review_missing" in result["policy"]["violations"]
    assert "policy violations" in release["last_error"]