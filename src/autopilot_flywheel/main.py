import argparse
import sys
from autopilot_flywheel.orchestrator import AutopilotOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Autopilot Flywheel CLI")
    parser.add_argument("command", type=str, help="Command to process")
    parser.add_argument("--task-id", type=str, default="default", help="Task ID")
    args = parser.parse_args()

    orchestrator = AutopilotOrchestrator()
    allowed = orchestrator.process_command(task_id=args.task_id, command=args.command)
    
    if allowed:
        print(f"✅ Command allowed: {args.command}")
        sys.exit(0)
    else:
        print(f"❌ Command blocked: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
