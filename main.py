"""
Twitter Bot Application Entry Point

This module initializes and runs the Twitter bot application.
It handles environment configuration, logging setup, and bot initialization.

Environment Variables Required:
    - API_KEY: Twitter API Key
    - API_SECRET: Twitter API Secret
    - ACCESS_TOKEN: Twitter Access Token
    - ACCESS_SECRET: Twitter Access Secret
    - BEARER_TOKEN: Twitter Bearer Token
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from bot import TwitterBot
from logging_config import setup_logging
from config import (
    Config,
    AIConfig
)
from helper import validate_env_vars
from tweet_generator import AITweetGenerator

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)

logger.info("Loading environment variables...")
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)



# OUATH 1
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

if __name__ == "__main__":
    try:
        validate_env_vars()
        
        kwargs = {
            "API_KEY": API_KEY, 
            "API_SECRET": API_SECRET,
            "ACCESS_TOKEN": ACCESS_TOKEN,
            "ACCESS_SECRET": ACCESS_SECRET,
            "BEARER_TOKEN": BEARER_TOKEN
        }
        
        logger.info("Initializing TwitterBot...")
        bot = TwitterBot(**kwargs)
        bot()
        
        # Initialize configuration
        config = Config(
            ai_config=AIConfig(
                tones=["humourous"],
                topics=["QOTD i.e Quote of the day", "Indian demographics"]
            )
        )

        # set log level as per config
        logger.setLevel(config.log_level)


        # # Try to read from from tweets.txt first
        # tweet_file_path = Path(__file__).parent / 'tweets.txt'

        # if tweet_file_path.exists():
        #     with open(tweet_file_path, 'r') as f:
        #         lines = f.readlines()
        #         if lines:
        #             tweet = lines[0].strip()
        #             # Remove the used tweet from file
        #             with open(tweet_file_path, 'w') as f:
        #                 f.writelines(lines[1:])
        # else:
        #     logger.warning("please check the source file.")


        # Use AI to generate tweet
        tweety = AITweetGenerator(config=config.ai_config, llm='gpt')
        tweet = tweety.generate_tweet()


        # for future scope the tweets will be picked from a queue service (redis or rabbitmq)
        config.tweet_text = tweet

        logger.info("Tweeting this [+] ", tweet, " [+]")

        # If twiiter let's, we'll have valid tweet data to process
        # in future pipelines.. (aggregation or just checks)
        tweet_response = bot.make_tweet(config.tweet_text)

        logger.info("Tweet posted successfully. ID: %s", tweet_response.data['id'])
    
    except Exception as e:
        logger.error("Application failed: %s", str(e))
        raise
