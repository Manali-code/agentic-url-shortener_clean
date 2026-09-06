# Orchestration

The executable entry point is `python run_orchestrator.py "Deliver a URL shortener"`.
It composes `WorkflowGraph`, `Workflow`, `StateStore`, `PolicyEngine`, `ApprovalGate`,
`WorkflowMetrics`, and all six agents through `orchestrator.Orchestrator`.

## Execution trace

1. Requirements and architecture run first, followed by implementation.
2. After implementation, documentation and testing are both dependency-ready. The
	runner records this as `parallel_batch_ready` and synchronizes before release.
3. Release is blocked when approval is absent. `approve_and_resume()` continues from
	the existing state instead of rerunning completed agents.
4. Every agent output is stored under its step name. Each event records step, event,
	and detail in `lineage`, providing an audit-grade decision trace.

Example output from the CLI includes:

```text
release: blocked
notes: Awaiting human approval
...
release: completed
notes: ready_for_release
```

## Failure controls

`Orchestrator.run(..., failure_plan={"implementation": 1})` injects one transient
failure for a deterministic demo. The failed attempt restores the pre-step state,
increments retry and rollback metrics, records `replanned`, and retries within the
retry limit held by the graph. A policy failure stops release after its bounded retry
budget and leaves the violation list in the snapshot.

Release policy requires passing tests, ready documentation, human approval, and a
security review. The optional OpenAI Responses API integration is enabled when
`OPENAI_API_KEY` is configured; without it, planning agents use deterministic local
behavior so the workflow remains runnable offline.
