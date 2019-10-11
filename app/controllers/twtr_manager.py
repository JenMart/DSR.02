import threading
import time
import random
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream
from app.controllers.db_manager import DatabaseManager
from app.controllers.game_manager import GameManager

##RUN THE APP FROM HERE, STUPID.
######
ckey= '*****'
csecret= '*****'
atoken= '*****'
asecret= '*****'

print("test commit")

class twtrManager(StreamListener):
    # def __init__(self):
    #     self.db_manager = DatabaseManager(self)
    #     self.game_manager = GameManager()

    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    # """

    def on_status(self, status):
        self.db_manager = DatabaseManager(self)
        self.game_manager = GameManager()
        # Status object holds all twitter user info objects
        screenName = status.author.screen_name
        createDate = str(status.created_at)
        txt = status.text
        txt = txt.replace("@DunSuRu","")
        print(txt)
        try:
            # Takes data and starts new thread.
            th = threading.Thread(target=self.handleChoice(txt, screenName,createDate,))
            th.start()
        except:
            print("unable to start thread")
    def on_error(self, status):
        print(status)

    def handleChoice(self, input, userName,createDate):
        check = self.db_manager.checkTweets(userName,input,createDate)
        if (check): #If not, add to DB
            self.db_manager.storeTweets(userName,input,createDate)

        choice = input.lower()

        while True:
            if "new" in choice or "begin" in choice or "start" in choice:
                reslt = self.game_manager.new_game(userName)
            elif "about" in choice or "info" in choice or "information" in choice or "what" in choice:
                reslt = self.game_manager.instructions(userName)
            elif "who" in choice:
                reslt = self.game_manager.player_stats(userName)
            elif "continue" in choice:
                rndchoice = random.randint(0,4)
                if rndchoice == 0:
                    reslt = self.game_manager.dungeon_pick(userName)
                elif rndchoice == 1:
                    reslt = self.game_manager.ruins_people(userName)
                elif rndchoice == 2:
                    reslt = self.game_manager.ruins_monster(userName)
                elif rndchoice == 3:
                    reslt = self.game_manager.the_road_monster(userName)
                else:
                    reslt = self.game_manager.the_road_people(userName)
            elif "test0" in choice:
                reslt = self.game_manager.dungeon_pick(userName)
            elif "test1" in choice:
                reslt = self.game_manager.ruins_people(userName)
            elif "test2" in choice:
                reslt = self.game_manager.ruins_monster(userName)
            elif "test3" in choice:
                reslt = self.game_manager.the_road_monster(userName)
            elif "test4" in choice:
                reslt = self.game_manager.the_road_people(userName)
            else:
                reslt = self.game_manager.player_options(userName)
            try:

                return reslt
                break
            except:
                pass



if __name__ == '__main__':
    l = twtrManager()
    #Starts twitter scrape
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    stream = Stream(auth, l)
    #Filters results to only display @DunSuciRun
    try:
        th = threading.Thread(stream.filter(track=['@DunSuRu']))
        th.start()
    except:
        print("process failed at: " + time.ctime())
        time.sleep(5)
        th = threading.Thread(stream.filter(track=['things']))
        th.start()







