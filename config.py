from dataclasses import dataclass
from typing import Optional, List

@dataclass
class AIConfig:
    prompt_template: str = "Generate a tweet about {topic} in a {tone} tone"
    temperature: float = 0.7
    max_tokens: int = 255
    topics: List[str] = None
    tone: str = "professional but catchy"

@dataclass
class Config:
    tweet_text: Optional[str] = "Well this got triggered somehow.. suspicious ?"
    ai_config: AIConfig = AIConfig()
    log_level: str = "DEBUG"
    log_file: str = "twitter_bot.log"
    env_file: str = ".env"
    max_tweet_length: int = 255