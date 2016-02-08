import thread
import tweepy
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream

from game_manager import GameManager
from db_manager import DatabaseManager


ckey= '*'
csecret= '*'
atoken= '*'
asecret= '*'
    #Canekin GylRarkin the first Paladin & Thun Lenth the last Barbarian. The immortal lords.

class twtrManager(StreamListener):


    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    # """

    def on_status(self, status):

        self.db_manager = DatabaseManager(self)
        self.game_manager = GameManager()
        screenName = status.author.screen_name
        createDate = str(status.created_at)
        txt = status.text
        txt = txt.replace("@DunSuciRun","")
        print(txt)
        try:
            thread.start_new_thread(self.handleChoice,(txt, screenName,createDate,))
        except:
            print("unable to start thread")
    def on_error(self, status):
        print(status)

    def handleChoice(self, input, userName,createDate):
        # self.db_manager = DatabaseManager(self)
        # self.db_manager.setup()
        check = self.db_manager.checkTweets(userName,input,createDate)
        if (check): #If not, add to DB
            self.db_manager.storeTweets(userName,input,createDate)

        choice = input.lower()

        while True:
            if "new" in choice:
                reslt = self.game_manager.new_game(userName)
            elif "continue" in choice:
                reslt = self.game_manager.dungeon_pick(userName)
            elif "about" in choice:
                reslt = self.game_manager.instructions(userName)
            elif "who" in choice:
                reslt = self.game_manager.player_stats(userName)
            else:
                reslt = self.game_manager.player_options(userName)
            try:

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







