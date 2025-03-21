import tweepy
import logging
from typing import Optional
from tweepy import Response

from helper import REQUIRED_VARS

logger = logging.getLogger(__name__)  

class TwitterBot:

    def __init__(self, *args, **kwargs):
        missing_keys = [key for key in REQUIRED_VARS if not kwargs.get(key)]
        if missing_keys:
            raise ValueError(f"Missing required credentials: {', '.join(missing_keys)}")
            
        self.api_key = kwargs.get('API_KEY')
        self.api_secret = kwargs.get('API_SECRET')
        self.access_token = kwargs.get('ACCESS_TOKEN')
        self.access_secret = kwargs.get('ACCESS_SECRET')

        self.bearer_token = kwargs.get("BEARER_TOKEN")

        self.client = None

    def __call__(self, *args, **kwargs):

        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret
        )

        resp = self.client.get_me()

        logger.warning("Logged in as : %s",resp.data.name )        

    def make_tweet(self, tweet: str) -> Optional[Response]:
        """
        Post a tweet to Twitter.
        
        Args:
            tweet (str): The text content of the tweet
            
        Returns:
            tweepy.responses.Response: Response from Twitter API
            
        Raises:
            ValueError: If tweet is empty or exceeds character limit
            RuntimeError: If client is not initialized
            tweepy.TweepyException: If tweet posting fails
        """
        if self.client is None:
            raise RuntimeError("Twitter client not initialized")
            
        if not tweet or len(tweet) > 280:
            raise ValueError("Tweet must be between 1 and 280 characters")
            
        try:
            resp = self.client.create_tweet(
                text=tweet,
                user_auth=True
            )
            logger.info("[+] Tweet successfully posted: %s", tweet)
            return resp
        except tweepy.TweepyException as e:
            logger.error("Failed to post tweet: %s", str(e))
            raise