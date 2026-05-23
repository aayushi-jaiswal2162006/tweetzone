import tweepy
from django.conf import settings

def post_tweet(status_text):
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    try:
        tweet = api.update_status(status=status_text)
        print("✅ Tweet posted successfully!")
        return tweet.id
    except Exception as e:
        print("❌ Tweet Error:", e)
        return None
