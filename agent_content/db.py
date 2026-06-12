import os
import sqlite3
from shared.db import execute, fetchall, fetchone

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "content.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                used INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id INTEGER,
                content TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS ready (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                draft_id INTEGER,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS published (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ready_id INTEGER,
                published_at TEXT DEFAULT (datetime('now'))
            );
        """)


def add_idea(text: str) -> int:
    execute(DB_PATH, "INSERT INTO ideas (text) VALUES (?)", (text,))
    row = fetchone(DB_PATH, "SELECT last_insert_rowid() AS id")
    return row["id"]


def get_unused_idea() -> dict | None:
    return fetchone(DB_PATH, "SELECT * FROM ideas WHERE used = 0 ORDER BY id LIMIT 1")


def mark_idea_used(idea_id: int) -> None:
    execute(DB_PATH, "UPDATE ideas SET used = 1 WHERE id = ?", (idea_id,))


def save_draft(idea_id: int, content: str) -> int:
    execute(DB_PATH, "INSERT INTO drafts (idea_id, content) VALUES (?, ?)", (idea_id, content))
    row = fetchone(DB_PATH, "SELECT last_insert_rowid() AS id")
    return row["id"]


def list_ideas() -> list[dict]:
    return fetchall(DB_PATH, "SELECT * FROM ideas ORDER BY id DESC")
