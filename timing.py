from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from credentials import *
import json
import time

# Todo:
# add more hashtags
# add serial communication
# port to raspi

demotaglist = {"imwithher","placeholder","placeholder2"}
repubtaglist = {"makeamericagreatagain","placeholderasdf","placeholderfoobar"}

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
	j = json.loads(data)
	print(str(int(j["timestamp_ms"]) / 100))
	return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#imwithher', '#makeamericagreatagain'])
