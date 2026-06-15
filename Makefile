.PHONY: install run-once schedule test lint

install:
	pip install -r requirements.txt

run-once:
	python agent_content/main.py run

schedule:
	python agent_content/main.py schedule

test:
	pytest tests/ -v

lint:
	python -m py_compile agent_content/main.py agent_content/db.py agent_content/llm.py
	add-idea:
		python agent_content/main.py add "$(IDEA)"
