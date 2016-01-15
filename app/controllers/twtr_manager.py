import tweepy
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream

from app.controllers.game_manager import GameManager
from db_manager import DatabaseManager


ckey= 'rlee33vXmHIlmR5tQljIX0ucD'
csecret= 'cUiIFESIXSSin9YJHYwLnVwnHpS64Ytj7csY9yFqshvAlkcaPg'
atoken= '2836017980-DxYDsgHqGMyRIq1yH3Uf3Ar63eYCFhqawJAWGOw'
asecret= 'SruNXYjh0BpY4GQhiflXaxbB2XUhrCMslBrmrH2ViULnu'


class twtrManager(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    # """

    def on_status(self, status):
        self.db_manager = DatabaseManager(self)
        self.game_manager = GameManager(self)

        screenName = status.author.screen_name
        createDate = str(status.created_at)
        txt = status.text
        txt = txt.replace("@DunSuciRun","")
        respnse = ""
        # self.db_manager.storeTweets(screenName,txt,createDate)
        check = self.db_manager.checkTweets(screenName,txt,createDate)


        if (check): #If not, add to DB
            self.db_manager.storeTweets(screenName,txt,createDate)
            self.printTweet(screenName,self.handleChoice(txt, screenName))



        # print(status.author.screen_name)
        # print(str(status.created_at))
        print(txt)
        # return True


    def on_error(self, status):
        print(status)

    def printTweet(self, user, text):
        #Remember: You have exactly 123 characters to tell a story. Waste none in the struggle.
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        api = tweepy.API(auth)
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
            except:
                pass

        # api.update_status("@" + usr + " " + text)
        message = "@" + user  + " " + text
        api.update_status(status=message)
        print "demo!"
        # print ("@" + usr + " " + text)
        # print text
        return

    def handleChoice(self, input, userName):

        choice = input.lower()
        reslt = ""
        while True:
            if "new" in choice:
                reslt = self.game_manager.new_game(userName)
            elif "continue" in choice:
                reslt = self.game_manager.dungeon_pick(userName)
            elif "about" in choice:
                reslt = self.game_manager.instructions()
            elif "who" in choice:
                reslt = self.game_manager.player_stats(userName)
            else:
                reslt = self.game_manager.player_options()
                # self.twtr_manager.printTweet("That is not a valid choice.")
                # self.prompt('main_menu')
            try:
                # int(choice)
                # self.menus['main_menu'][int(choice) -
                return reslt
                break
            except:
                pass



if __name__ == '__main__':
    l = twtrManager()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    stream = Stream(auth, l)
    stream.filter(track=['@DunSuciRun'])




############################################## NO MANS LAND

# __author__ = 'Jen Mart'
# import tweepy, time, sys, json
# # from tweepy
# # import OAuthHandler
#
# __author__ = 'Jen Mart'
# import tweepy, time, sys, json
# from tweepy import OAuthHandler
#
#
# class twtrManager:
#     def __init__(self):
#         self.db_manager = DatabaseManager(self)
#         self.main()
#
#     def main(self):
#
#
#         auth = tweepy.OAuthHandler(ckey, csecret)
#         auth.set_access_token(atoken, asecret)
#         api = tweepy.API(auth)
#         # auth = OAuthHandler(ckey, csecret)
#     def homeTimeline(self):
#         while True:
#             # auth = tweepy.OAuthHandler(ckey, csecret)
#             # auth.set_access_token(atoken, asecret)
#             # api = tweepy.API(auth)
#             # auth = OAuthHandler(ckey, csecret)
#             # timeline=api.home_timeline(COUNT=0)
#             # try:
#             #     for tweet in timeline:
#             #         user=tweet.user
#             #         name=tweet.user.name.encode('utf-8')
#             #         text=tweet.text.encode('utf-8')
#             #         date=tweet.created_at
#             #
#             #         if "@DunSuciRun" in text: #checks if special text in field
#             #             text = text[11:]
#             #             check = self.db_manager.checkTweets(name, text, date)
#             #             if (check): #If not, add to DB
#             #                 self.db_manager.storeTweets(name, text, date)
#             #                 return text
#             #                 break
#             #             else:
#             #                 print "wait a minute"
#             #                 time.sleep(60)
#             #                 pass
#             #
#             #         else:
#             #             print "nothing valid. Waiting"
#             #             time.sleep(60)
#             #             pass
#             # except Exception, e:
#             #     print "not valid. Lets wait a minute!"
#             #     time.sleep(60)
#             #     pass
#         return text
#          # return text
#
#         # self.mainMenu(ckey,csecret,atoken,asecret,auth,api)
#
#         # self.db_manager.storeTweets(name, text, date)
#
#     def printTweet(self,text): #Works perfectly!
#         auth = tweepy.OAuthHandler(ckey, csecret)
#         auth.set_access_token(atoken, asecret)
#
#         # conn = sqlite3.connect('DunSuciRun.sqlite')
#         # t = conn.cursor()
#         # t.execute("DELETE FROM PLAYERS") #MAKE SURE TO REMOVE THSI AFTER TESTING!! -jm
#         # t.execute("""SELECT * FROM PLAYERS""")
#         # usr = t.fetchall()
#         # usr = usr[0][0]
#         # conn.commit()
#         # conn.close()
#
#
#         # api.update_status("@" + usr + " " + text)
#         print "demo!"
#         # print ("@" + usr + " " + text)
#         print text
#         return
#
#
#



