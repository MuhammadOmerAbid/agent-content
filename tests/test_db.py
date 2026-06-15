import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_init_db(tmp_path, monkeypatch):
    import agent_content.db as db_mod
    test_db = str(tmp_path / "content.db")
    monkeypatch.setattr(db_mod, "DB_PATH", test_db)
    db_mod.init_db()
    conn = sqlite3.connect(test_db)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    conn.close()
    assert {"ideas", "drafts", "ready", "published"}.issubset(tables)


def test_add_and_list_ideas(tmp_path, monkeypatch):
    import agent_content.db as db_mod
    test_db = str(tmp_path / "content.db")
    monkeypatch.setattr(db_mod, "DB_PATH", test_db)
    db_mod.init_db()
    db_mod.add_idea("Won a project for a US startup")
    ideas = db_mod.list_ideas()
    assert len(ideas) == 1
    assert ideas[0]["text"] == "Won a project for a US startup"
    assert ideas[0]["used"] == 0
