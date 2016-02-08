import random
import time
import tweepy


ckey= '*'
csecret= '*'
atoken= '*'
asecret= '*'

class TwtPrinter:
    def printTweet(self, user, text):
        #Remember: You have exactly 123 characters to tell a story. Waste none in the struggle.
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        api = tweepy.API(auth)
        message = "@" + user  + " " + text
        for status in tweepy.Cursor(api.user_timeline).items():
            if status.text in message:
                try:
                    api.destroy_status(status.id)
                except:
                    pass
        # message = "@" + user  + " " + text
        time.sleep(random.randint(1,3))
        print(message)
        api.update_status(status=message)
        # return