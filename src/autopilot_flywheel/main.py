import argparse
import sys
from autopilot_flywheel.orchestrator import AutopilotOrchestrator
from autopilot_flywheel.prompts.planner_agent import PlannerAgent

def main():
    parser = argparse.ArgumentParser(description="Autopilot Flywheel CLI")
    parser.add_argument("command", type=str, help="Command or request to process")
    parser.add_argument("--task-id", type=str, default="default", help="Task ID")
    parser.add_argument("--plan", action="store_true", help="Use PlannerAgent to generate tasks")
    args = parser.parse_args()

    if args.plan:
        print(f"🧠 Planning for request: {args.command}")
        agent = PlannerAgent()
        graph = agent.plan(args.command)
        print(f"✅ Created {len(graph.tasks)} tasks in the database.")
        for task in graph.tasks:
            print(f"  - {task.id}: {task.description} (blocks: {task.blocks})")
        sys.exit(0)
    else:
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
