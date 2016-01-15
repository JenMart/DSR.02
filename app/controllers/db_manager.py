import sqlite3
import os

from app.models.monDAO import monDAO
from app.models.charDAO import CharDAO
from app.models.dunDAO import DunDAO



#
#   DatabaseManager
#
#   Controls data storage and reading.
#

class DatabaseManager:
    #
    #   Init
    #
    #   Should call self.setup() if the DB isn't found in the same folder as main.py.
    #   To rebuild the DB, delete the file and run main.py again.
    #
    def __init__(self, game_manager):
        self.game_manager = game_manager

        if not os.path.isfile('DunSuciRun.sqlite'):
            self.setup()

    #
    #   Deletes the database. Used for testing.
    #
    def delete(self):
        #delete the database to test new additions
        print('deleting database')
        if os.path.isfile('DunSuciRun.sqlite'):
           os.remove('DunSuciRun.sqlite')

    #
    #   Sets up the database for the first time, then seeds it.
    #
    def setup(self):
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()

        print("Creating database")

        char = """ CREATE TABLE CHARACTERS (
            PLAYER VARCHAR(255),
            NAME VARCHAR(255) NOT NULL,
            JOB VARCHAR(255) NOT NULL,
            HEALTH INT NOT NULL,
            GOLD INT NOT NULL)"""

        dungeons = """ CREATE TABLE DUNGEONS (
            NAME VARCHAR(255) NOT NULL,
            THEME VARCHAR(255) NOT NULL,
            DIFFICULTY INT NOT NULL )"""

        bosses = """ CREATE TABLE BIGSCARIES (
            NAME VARCHAR(255) NOT NULL,
            THEME VARCHAR(255) NOT NULL,
            DAMAGE INT NOT NULL)"""
        players = """ CREATE TABLE PLAYERS (
            USERNAME VARCHAR(255) NOT NULL,
                STEP VARCHAR(255) NOT NULL,
                DATESTAMP VARCHAR(255) NOT NULL )"""

        c.execute(char)
        c.execute(dungeons)
        c.execute(bosses)
        c.execute(players)
        # c.execute(playerActions)

        conn.commit()
        conn.close()

        # self.seed()

    #
    #   Fills the database with seed data.
    #   TODO: Add more data!
    #
    def seed(self):
        # Starting information
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        print("seeding now")
        monsters = ['Dragon', 'Slime', 'Wolf','Ghost', 'Zombie','Spider', 'Bat', 'Rat','Ghoul','Vampire', 'Bear', 'Cyclops', 'Witch', 'Warlock', 'Mummy', 'Werewolf', 'Harpy', 'Hydra', 'Griffon', 'Crab', 'Roc','Mermaid', 'Nymph', 'Ifrit', 'Phoenix']
        types = ['earth', 'air', 'earth', 'undead', 'undead','earth', 'earth', 'earth', 'undead', 'undead', 'earth', 'earth', 'earth', 'earth', 'undead', 'undead', 'air', 'water', 'air', 'water', 'air', 'water', 'water', 'air', 'air']
        health = [10,2,5,2,4,1,1,1,5,8,4,2,6,4,3,7,5,8,3,1,1,4,2,3,1]
        for i in range(len(monsters)):
            print ("Add " + monsters[i] + " to database")
            c.execute("INSERT INTO BIGSCARIES VALUES (?, ?, ?)", (monsters[i], types[i], health[i]))

        dungeonname = ['Dungeon of Death', 'Scary Eyrie', 'Julies Crypt', 'Bastion Hold', 'Caverns of Remorse', 'The Whispering Maze', 'Grizzly Vale','Chambers of Red Viper', 'The White Abyss', 'The Wading Seas', 'Pheia Bay' 'Zephyrs Bluff', 'Heavens Toilet']
        theme = ['earth', 'air', 'undead', 'earth', 'undead', 'undead', 'earth', 'air', 'water', 'water','water', 'air', 'air']
        difficulty = [3,2,1,1,2,2,3,3,1,2,3,1,2]
        for d in range(len(dungeonname)):
            print ("Add " + dungeonname[d] + " to database")
            c.execute("INSERT INTO DUNGEONS VALUES (?,?,?)", (dungeonname[d], theme[d], difficulty[d]))


        conn.commit()
        conn.close()
        return

    #
    #   Test function.
    #


    def storeTweets(self,name,text,date):
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        p = conn.cursor()
        p.execute("SELECT * FROM PLAYERS WHERE USERNAME = ?",(name,))
        check = p.fetchall()
        if check == 0:
            print("Adding user data to Database")
            c.execute("INSERT INTO PLAYERS VALUES (?, ?, ?)", (name,text,date))
        else:
            print("Updating current player data")
            c.execute("UPDATE PLAYERS SET USERNAME = ? AND STEP = ? AND DATESTAMP = ?", (name, text, str(date)))
        conn.commit()
        conn.close()
        return

    def checkTweets(self, name, text, date):

        conn = sqlite3.connect('DunSuciRun.sqlite')
        t = conn.cursor()
        # self.setup()
        # t.execute("DELETE FROM PLAYERS") #MAKE SURE TO REMOVE THIS AFTER TESTING!! -jm
        t.execute("""SELECT * FROM PLAYERS WHERE USERNAME = ? AND STEP = ? AND DATESTAMP = ?""", (name, text, str(date)))
        tweets = t.fetchall()
        conn.commit()
        conn.close()
        if len(tweets) < 1:
            return True
        else:
            return False
    def test(self):
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        d = conn.cursor()
        a = conn.cursor()
        print("Run test")

        d.execute("SELECT * FROM DUNGEONS")
        c.execute("SELECT * FROM BIGSCARIES")
        a.execute("SELECT * FROM CHARACTERS")

        dungeons = d.fetchall()
        bosses = c.fetchall()
        characters = a.fetchall()

        # Make bosses
        for boss in bosses:
            print(boss)
            b = monDAO(boss[0], boss[1], boss[2])
            b.talk()

        for dungeon in dungeons:
            print(dungeon)
            d = DunDAO(dungeon[0], dungeon[1], dungeon[2])
            d.sign()

        for character in characters:
            print(character)
            a = CharDAO(character[0], character[1], character[2])
            a.announce()
        conn.close()