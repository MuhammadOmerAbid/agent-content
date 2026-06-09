# Agent 1 â€” LinkedIn Content Agent

![CI](https://github.com/MuhammadOmerAbid/agent-content/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/github/license/MuhammadOmerAbid/agent-content) ![Python](https://img.shields.io/badge/python-3.11+-blue)


Turns your rough notes and wins into polished, STAR-structured LinkedIn posts. Sends drafts to your Telegram for approval before anything is published.

**Part of:** [AI Outreach System](../ai-outreach-system/)

---

## What It Does

1. You add raw ideas or wins to a content bank (SQLite table or via CLI command)
2. On a schedule (Mon/Wed/Fri morning by default) it picks one unused idea
3. Claude rewrites it into a STAR-format post â€” Situation, Task, Action, Result â€” with a strong hook, short lines, soft CTA, 3â€“4 hashtags, ~150â€“200 words
4. Draft is sent to you on Telegram
5. You reply `approve` or `edit` (with notes â†’ it redrafts)
6. Approved post is saved to a `ready` table and optionally queued in Taplio (or saved as a file to copy-paste manually)

**It never auto-posts. You always approve first.**

---

## Post Format (STAR Structure)

```
[Hook line 1 â€” bold statement or question]
[Hook line 2 â€” expand the hook]

Situation: ...
Task: ...
Action: ...
Result: ...

[Soft CTA â€” e.g. "What's your experience with X?"]

#hashtag1 #hashtag2 #hashtag3 #hashtag4
```

---

## Setup

```bash
# Inside ai-outreach-system/
pip install -r requirements.txt
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and TELEGRAM_BOT_TOKEN in .env
```

---

## Usage

```bash
# Add a new idea to the content bank
python agent_content/main.py add "Won a project for a US startup â€” built their landing page in 3 days"

# Run the scheduler (Mon/Wed/Fri it picks an idea and sends to Telegram)
python agent_content/main.py run

# List all ideas in the bank
python agent_content/main.py list
```

---

## Configuration

Edit `agent_content/config/voice.txt` to set your personal voice/niche:

```
I am a freelance full-stack web developer specializing in fast, modern sites for startups.
My audience: startup founders, tech leads, and CTOs.
Tone: confident, practical, no jargon.
```

Edit `agent_content/config/star_prompt.txt` to customize the STAR rewriting prompt sent to Claude.

---

## Environment Variables Needed

```
ANTHROPIC_API_KEY=       # https://console.anthropic.com
TELEGRAM_BOT_TOKEN=      # Create bot via @BotFather on Telegram
TELEGRAM_CHAT_ID=        # Your personal Telegram chat ID
TAPLIO_API_KEY=          # Optional â€” https://taplio.com (leave blank to use file output)
```

---

## Schedule

Default: Monday, Wednesday, Friday at 9:00 AM (your local time).
Configurable in `agent_content/config/schedule.py`.

---

## Database

SQLite file: `data/content.db`

Tables:
- `ideas` â€” raw ideas you add
- `drafts` â€” Claude-generated drafts pending approval
- `ready` â€” approved posts waiting to publish
- `published` â€” history of published posts

---

## Safety

- Never posts automatically â€” Telegram approval required every time
- Never accesses LinkedIn account directly
- You copy-paste the final post yourself (or Taplio queues it via official API)
