"""Run the delivery workflow and demonstrate its approval gate."""

import argparse
import json

from orchestrator import Orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="?", default="Deliver a reliable URL shortener")
    parser.add_argument("--approve", action="store_true", help="approve release immediately")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    initial = orchestrator.run(args.request, approve=args.approve)
    print(json.dumps(initial, indent=2))
    if initial["workflow"]["release"]["status"] == "blocked":
        print("\nApproval required. Resuming after human approval...\n")
        print(json.dumps(orchestrator.approve_and_resume(), indent=2))


if __name__ == "__main__":
    main()