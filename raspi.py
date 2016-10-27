from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from credentials import *
import json
import time

import RPi.GPIO as GPIO

DEBUG = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
BLUE_LED = 23
RED_LED = 18
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

# Todo:
# add more hashtags


demotaglist = {"imwithher","clintonfoundation","amerikkka","drumpf", "strongertogether"}
repubtaglist = {"makeamericagreatagain","crookedhillary","votetrump","buildthewall","trumpforpresident"}

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        j = json.loads(data)
        d = 0
        r = 0
        i = 0
        #print(j["entities"]["hashtags"])
        #print(len(j["entities"]["hashtags"]))
        while (i < len(j["entities"]["hashtags"])):
            #print(j["entities"]["hashtags"][i-1])
            i = i + 1
            for tag in demotaglist:
                if j["entities"]["hashtags"][i-1]["text"].lower() == tag:
                    d += 1
                    #print(j["entities"]["hashtags"][i-1]["text"].lower())
            for tag in repubtaglist:
                if j["entities"]["hashtags"][i-1]["text"].lower() == tag:
                    r += 1
                    #print(j["entities"]["hashtags"][i-1]["text"].lower())
        if (d > r):
            print("d")
        elif (r > d):
            print("r")
            GPIO.output(BLUE_LED, False)
            GPIO.output(RED_LED, True)
        else:
            print("n")
            GPIO.output(BLUE_LED, True)
            GPIO.output(RED_LED, False)
        print("\n")
        time.sleep(0.1)
        GPIO.output(BLUE_LED, False)
        GPIO.output(RED_LED, False)
        return True
        #while (i < range(len(j["entities"]["hashtags"]))):
        #    print(i)
        #    print(j["entities"]["hashtags"][i])
            #i += 1
#            for tag in demotaglist:
#                if i["text"].lower() == tag:
#                    d += 1
#                    print(i["text"].lower())
#            for tag in repubtaglist:
#                if i["text"].lower() == tag:
#                    r += 1
#                    print(i["text"].lower())

#        print("d: " + str(d))
#	    print("r: " + str(r))
#	    print("\n")


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    try:
        l = StdOutListener()
        auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=['#imwithher', '#makeamericagreatagain', '#clintonfoundation', '#crookedhillary', '#amerikkka'])
    finally:
        GPIO.cleanup()
