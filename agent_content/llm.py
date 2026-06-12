import os
from shared.llm import ask

_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")


def _read(filename: str) -> str:
    with open(os.path.join(_CONFIG_DIR, filename)) as f:
        return f.read()


def draft_post(idea: str) -> str:
    voice = _read("voice.txt")
    template = _read("star_prompt.txt")
    prompt = template.replace("{idea}", idea)
    system = f"Voice profile:\n{voice}"
    return ask(system=system, user=prompt, max_tokens=512)
