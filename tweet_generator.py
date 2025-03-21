import logging
from typing import Optional, Type

from config import AIConfig
from groq import Groq
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class LLMHelper:

    @abstractmethod
    def generate_content(self, topic: str) -> str:
        pass


class GroqHelper(LLMHelper):

    def __init__(self, model="llama-3.3-70b-versatile", api_key=None):
        self.model = model
        self.client = Groq(api_key=api_key)
        pass

    def generate_content(self, topic: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": topic
                }],
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
            )
            resp = ""
 
            for choice in completion.choices:
                msg = choice.message.content
                resp += msg if msg else ""
            return resp
        except Exception as e:
            logger.error("Failed to generate content: %s", str(e))
            raise

class GptHelper(LLMHelper):

    def __init__(self):
        self.model = None
        self.client = None

    def generate_content(self, topic: str) -> str:
        raise NotImplementedError("Not implemented yet.")

class TweetGenerator:
    """
    Generates tweets using various LLM providers.
    
    Args:
        config (AIConfig): Configuration for tweet generation
        llm (str): LLM provider name ('groq' or 'gpt')
    
    Raises:
        ValueError: If LLM provider is not supported
    """
    def __init__(self, config: AIConfig, llm: str = 'groq') -> None:

        self.config: AIConfig = config

        self.llm_instance: LLMHelper
        llm_class_name = llm.capitalize() + "Helper"
        llm_class = globals().get(llm_class_name)
        
        if llm_class is None:
            raise ValueError(f"LLM '{llm}' is not supported")
        
        self.llm_instance = llm_class()
        
    def generate_tweet(self, topic: str = "technology") -> str:
        prompt = self.config.prompt_template.format(
            topic=topic,
            tone=self.config.tone
        )
        
        tweet = self.llm_instance.generate_content(topic=prompt)
        
        if len(tweet) > self.config.max_tokens:
            tweet = tweet[:self.config.max_tokens]
        
        return tweet.strip()
