import sqlite3
import random

from app.controllers.db_manager import DatabaseManager
from app.models.boss import Boss
from app.models.character import Character
from app.models.dungeon import Dungeon


class GameManager:

    def __init__(self, db_manager):
        self.db_manager = DatabaseManager(self)

    def test(self):
        testing = "testing"
        return testing
    #
    #   Continue
    #
    def new_game(self):
        text = ""
        firstHalf = "Ger Sym Hugh Ger Byssh Riff Vin Heg Gile Gau Ewl Gyl" \
                  "Rar Helm Thu Coel Erf Cane folke Knet Lenth Dene Hav Tun Thun".split() #24

        seconHalf = "y ey te nah ney ley walt wort man der dar dor da ness ke fin son kin".split() #18

        nickName1 = "Silent Horse Iron Grim Shadow Warrior Cold Queen King Prince Princess" \
                    " Mumble Quick  Flame".split() #14

        nickName2 = "Tongue Preserver Mouth Phantom Wonder Guardian Watcher Fist " \
                    "Slayer Hammer Sword Arrow".split() #12

        nickName3 = "Big Small Flamming Last First Great Final Burning Smug".split()

        nickName = ""

        # Total of 456 first name combinations
        if (random.randint(0,1) == 0): #Flips coin, determins if name will have one or two syllables
            firstName = firstHalf[random.randint(0,23)] + seconHalf[random.randint(0,17)]
        else:
            firstName = firstHalf[random.randint(0,23)]

        if (random.randint(0,1) == 0):#Flips coin, determins if name will have one or two syllables
            secondName = firstHalf[random.randint(0,23)] + seconHalf[random.randint(0,17)]
        else:
            secondName = firstHalf[random.randint(0,23)]
        while(firstName == secondName): #If first and last name are both the same, remakes last name.
            if (random.randint(0,1) == 0):
                secondName = firstHalf[random.randint(0,24)] + seconHalf[random.randint(0,17)]
            else:
                secondName = firstHalf[random.randint(0,24)]
        name = firstName + " " + secondName

        if (random.randint(0,1) == 0):

            if (random.randint(0,1) == 0):
                nickName += nickName1[random.randint(0,13)] + " " + nickName2[random.randint(0,11)]
            else:
                nickName += nickName2[random.randint(0,11)] + " " + nickName1[random.randint(0,13)]
        else: #Big Small Flamming Last First Great Final Burning
            if (random.randint(0,1) == 0):
                nickName = nickName1[random.randint(0,13)]
            else:
                nickName = nickName2[random.randint(0,11)]
            if (random.randint(0,1) == 0): #If Nickname appears as only one word then there is another flip to add another word
                nickName = nickName3[random.randint(0,6)] + " " + nickName

        if (random.randint(0,1) == 0 or nickName == "Tongue" or nickName == "Silent"or nickName == "Big"or nickName == "Small"
          or nickName == "Princess"):
            nickName = "the " + nickName
        else:
            nickName = "of the " + nickName + "s"
        fullName = name + " " + nickName
        gold = random.randint(1,5)
        job = ["Warrior", "Thief","Barbarian","Warrior Priest","Knight","Paladin"]
        youJob =  job[random.randint(1,5)]
        health = random.randint(80,400)
        #The longest sentence possible is a max of 122 characters to avoid going over twitters char limit
        if gold > 1:
            text ="You are " + fullName + ". You are a " + youJob + ". You begin your adventure with only " + str(gold) + " coins."
        else:
            text = "You're " + fullName + ". You are a " + youJob + ". You begin your adventure with only a single coin."

        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        p = conn.cursor()
        ch= conn.cursor()
        p.execute("SELECT USERNAME FROM PLAYERS")
        getUser = p.fetchall()
        userName = getUser[0][0]
        ch.execute("SELECT PLAYER FROM CHARACTERS WHERE PLAYER = ?",(userName,))
        check = ch.fetchall()
        if len(check) > 1: #Checks if user already has a character and replaces current character if yes
            c.execute('INSERT INTO CHARACTERS VALUES (?,?,?,?,?)', (userName, fullName, youJob, health, gold))
        else:
            c.execute('UPDATE CHARACTERS SET NAME = ?, JOB = ?, HEALTH = ?,  GOLD = ? WHERE PLAYER = ?', (fullName, youJob, health, gold, userName))

        conn.commit()
        conn.close()

        new_char = Character(fullName, youJob, health)
        return text

    def continue_game(self):
        self.printTweet(self.menu_manager.title('Continue Game'))
        player = self.player_game()
        self.dungeon_pick(player)
        self.menu_manager.continue_prompt()
        self.menu_manager.title_screen()

    def instructions(self):
        self.twtr_manager.printTweet('You are an adventurer tasked with rid the world of evil. There is no rest. Every battle brings you closer to death.')

        self.menu_manager.continue_prompt()
        self.menu_manager.title_screen()


    def player_stats(self, user):
        print "stuff later"

    def dungeon_pick(self, name):

            try:
                self.twtr_manager.printTweet("What level of dungeon would you like? (Easy, Medium or Hard)")
                level = self.twtr_manager.homeTimeline()
                level = level.lower()
                #Changed to text.
                level = 1
                # if "easy" in level: #keeps getting stuck in try/catch error
                #     self.twtr_manager.printTweet("You selected: Easy")
                #     level = 1
                # elif "medium" in level:
                #     self.twtr_manager.printTweet("You selected: Medium")
                #     level = 2
                # elif "hard" in level:
                #     self.twtr_manager.printTweet("You selected: Hard")
                #     level = 3
                # else:
                #     self.twtr_manager.printTweet('Level not recognized. Please choose Easy, Medium or Hard.')
                #     self.dungeon_pick(name)


                if 1 <= level <= 3:
                    conn = sqlite3.connect('DunSuciRun.sqlite')
                    c = conn.cursor()
                    m = conn.cursor()
                    n = conn.cursor()
                    p = conn.cursor()
                    c.execute('SELECT * FROM DUNGEONS WHERE DIFFICULTY =' + str(level))
                    dungeons = c.fetchall()
                    p.execute('SELECT * FROM PLAYERS')
                    getDate = p.fetchall()
                    useName = getDate[0][0]
                    gold = getDate[4][0] #I could have this backwards

                    randomNum= random.randint(0, len(dungeons)-1)
                    newTuple = dungeons[randomNum]
                    dun = Dungeon(newTuple[0],newTuple[1],newTuple[2]) #
                    dun.sign()
                    m.execute('SELECT * FROM BIGSCARIES WHERE THEME =?',(dun.theme,))
                    monsters = m.fetchall()
                    randoMon = random.randint(0, len(monsters)-1)
                    monsterTuple = monsters[randoMon]
                    mob = Boss(monsterTuple[0], monsterTuple[1], int(monsterTuple[2]))
                    horde = random.randint(0,(level*dun.difficulty))
                    #Updates character date with new health and treasure
                    n.execute('UPDATE CHARACTERS SET HEALTH = ?, GOLD = ? WHERE NAME = ?',(str((name.health - (mob.damage*dun.difficulty))), horde, useName))
                    conn.commit()
                    conn.close()

                    self.twtr_manager.printTweet("You slay a " + mob.name + " and collect " + str(horde) + " gold! " "It hurt you for " + str((mob.damage*dun.difficulty)) + " damage.")
                else:
                    self.twtr_manager.printTweet('Level not recognized. Please choose 1, 2, or 3.')
                    self.dungeon_pick(name)

            except StandardError as e:
                self.twtr_manager.printTweet('Level not recognized. Please choose Easy, Medium or Hard.')
                # self.menu_manager.write('Level not recognized. Please choose Easy, Medium or Hard.')
                self.dungeon_pick(name)
