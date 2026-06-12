from apscheduler.schedulers.blocking import BlockingScheduler
from agent_content.config.schedule import SCHEDULE_DAYS, SCHEDULE_HOUR, SCHEDULE_MINUTE
from agent_content.db import get_unused_idea
from agent_content.telegram_bot import process_idea
from shared.approval import notify


def run_job() -> None:
    idea = get_unused_idea()
    if idea is None:
        notify("No unused ideas left. Add more with: python agent_content/main.py add \"your idea\"")
        return
    process_idea(idea)


def start_scheduler() -> None:
    sched = BlockingScheduler()
    sched.add_job(
        run_job,
        trigger="cron",
        day_of_week=",".join(SCHEDULE_DAYS),
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
    )
    print(f"Scheduler started: {SCHEDULE_DAYS} at {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}")
    sched.start()
