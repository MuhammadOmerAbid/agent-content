from shared.approval import send_for_approval, notify
from agent_content.db import save_draft, mark_idea_used
from agent_content.llm import draft_post


def process_idea(idea: dict) -> None:
    draft = draft_post(idea["text"])
    draft_id = save_draft(idea["id"], draft)
    mark_idea_used(idea["id"])
    msg = f"*New LinkedIn Draft*\n\nIdea: _{idea['text']}_\n\n---\n{draft}"
    import asyncio
    asyncio.run(send_for_approval(msg, str(draft_id)))
