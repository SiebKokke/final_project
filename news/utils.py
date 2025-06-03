import tweepy
from django.conf import settings


def post_to_twitter(status):
    """Posts a status to Twitter using Tweepy."""
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    api = tweepy.API(auth)
    try:
        api.update_status(status)
        return True
    except Exception as e:
        print("Error posting to Twitter:", e)
        return False
