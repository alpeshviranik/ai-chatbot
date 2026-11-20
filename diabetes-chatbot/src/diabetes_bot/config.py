import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "claude-sonnet-5-5")
    top_k: int = int(os.getenv("TOP_K", "3"))
    max_history_turns: int = int(os.getenv("MAX_HISTORY_TURNS", "6"))
    knowledge_dir: str = os.getenv("KNOWLEDGE_DIR", "data/knowledge")


settings = Settings()
