# app/core/prompt_loader.py

from pathlib import Path


PROMPT_DIR = (
    Path(__file__).resolve().parents[2]
    / "prompts"
)


def load_prompt(name: str) -> str:
    """
    加载 prompts 目录下的提示词文件。
    """

    prompt_path = PROMPT_DIR / f"{name}.prompt"

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    return prompt_path.read_text(
        encoding="utf-8"
    )