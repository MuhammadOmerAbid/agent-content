"""agent-content CLI

Usage:
  python agent_content/main.py add "Your raw idea here"
  python agent_content/main.py run
  python agent_content/main.py list
"""
import sys
from agent_content.db import init_db, add_idea, list_ideas, get_unused_idea
from agent_content.telegram_bot import process_idea
from agent_content.scheduler import start_scheduler


def cmd_add(text: str) -> None:
    init_db()
    idea_id = add_idea(text)
    print(f"Idea added (id={idea_id}): {text}")


def cmd_run() -> None:
    init_db()
    idea = get_unused_idea()
    if idea is None:
        print("No unused ideas. Add one first.")
        return
    process_idea(idea)
    print("Draft sent to Telegram for approval.")


def cmd_list() -> None:
    init_db()
    ideas = list_ideas()
    if not ideas:
        print("No ideas yet.")
        return
    for i in ideas:
        status = "used" if i["used"] else "unused"
        print(f"[{i['id']}] ({status}) {i['text']}")


def cmd_schedule() -> None:
    init_db()
    start_scheduler()


COMMANDS = {"add": cmd_add, "run": cmd_run, "list": cmd_list, "schedule": cmd_schedule}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: python agent_content/main.py add \"your idea\"")
            sys.exit(1)
        cmd_add(sys.argv[2])
    else:
        COMMANDS[cmd]()
