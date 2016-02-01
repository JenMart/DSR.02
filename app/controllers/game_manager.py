import sqlite3
import random
from app.models.monDAO import monDAO
from app.models.charDAO import CharDAO
from app.models.dunDAO import DunDAO
from app.controllers.twt_print import TwtPrinter







class GameManager:
    def __init__(self):
        self.twt_print = TwtPrinter()

    def testDB(self):
        print("hello world")
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()

        this = """SELECT * FROM CHARACTERS"""
        c.execute(this)
        getStuff = c.fetchall()

        charTuple = getStuff[0]
        cha = CharDAO(charTuple[0], charTuple[1],charTuple[2],charTuple[3],charTuple[4])
        print(cha.name.split(' ')[0])


    def new_game(self, userName):
        firstHalf = "Ger Sym Hugh Ger Bysh Riff Vin Heg Gile Gau Ewl Gyl Van Syn Gath Par" \
                  "Rar Helm Thu Coel Erf Cane Fol Knet Leth Dene Hav Tun Thun Ara Bur".split() #24

        seconHalf = "y ey te nah ney ley walt wort man der dar dor da ness ke fin son kin wyn mir".split() #18

        nickName1 = "Silent Horse Iron Grim Shadow Warrior Cold Queen King Prince Princess" \
                    " Mumble Quick  Flame".split() #14

        nickName2 = "Tongue Preserver Mouth Phantom Wonder Guardian Watcher Fist " \
                    "Slayer Hammer Sword Arrow".split() #12

        nickName3 = "Big Small Flamming Last First Great Final Burning Smug".split()

        nickName = ""
        while True:
            # Total of 456 first name combinations
            if (random.randint(0,1) == 0): #Flips coin, determins if name will have one or two syllables
                firstName = random.choice(firstHalf) + random.choice(seconHalf)
            else:
                firstName = random.choice(firstHalf)

            if (random.randint(0,1) == 0):#Flips coin, determins if name will have one or two syllables
                secondName = random.choice(firstHalf) + random.choice(seconHalf)
            else:
                secondName = random.choice(firstHalf)
            while(firstName == secondName): #If first and last name are both the same, remakes last name.
                if (random.randint(0,1) == 0):
                    secondName = random.choice(firstHalf) + random.choice(seconHalf)
                else:
                    firstName = random.choice(firstHalf)
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
            fullName = name #Getting rid of nicknames for the moment.

            chkName = self.checkName(fullName)
            if chkName is not "not available":
                break


        gold = random.randint(1,5)
        job = ["Warrior", "Thief","Rager","War Priest","Knight","Paladin","Nomad"]
        youJob =  random.choice(job)

        sharpWeapons = ["sword","axe","spear","lance","saber","shield"]
        bluntWeapons = ["mace","hammer","flail","staff"]
        otherWeapons = ["twin axes","daggers","knife","whip", "fists"]

        elementMods = ['flaming', 'icy','electric','bright','shadow','black','dark']
        godMod = ["rightous","holy","unholy","divine","vile","depraved","pious"]
        oddMod = ["odd","quick","fierce","strange","great","quiet",'stone','golden','silver','steel','bloodied','ancient']


        health = random.randint(80,400)
        #The longest sentence possible is a max of 123 characters to avoid going over twitters char limit
        if gold > 1:
            text ="You are " + fullName + ". You are a " + youJob + ". You begin your adventure with only " + str(gold) + " coins."
        else:
            text = "You're " + fullName + ". You are a " + youJob + ". You begin your adventure with only a single coin."

        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        ch= conn.cursor()

        ch.execute("SELECT PLAYER FROM CHARACTERS WHERE PLAYER = ?",(userName,))
        check = ch.fetchall()
        if len(check) == 0: #Checks if user already has a character and replaces current character if yes
            c.execute('INSERT INTO CHARACTERS VALUES (?,?,?,?,?)', (userName, fullName, youJob, health, gold))
        else:
            text = "You already possess a character"

        conn.commit()
        conn.close()


        self.twt_print.printTweet(userName,text)

    def checkName (self, name): # FINISH THIS!
        conn = sqlite3.connect('DunSuciRun.sqlite')
        c = conn.cursor()
        numerals = ['II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX']
        checkName = '%'+name+'%'
        c.execute('SELECT NAME FROM CHARACTERS WHERE NAME LIKE ?,',(checkName,))

        chk = c.fetchall()
        count = 0
        secondCount = 0

        while count < len(chk):
            if chk[count] in name:
                name = name + " The " + numerals[secondCount]
                secondCount += 1
                if secondCount > 18:
                    return "not available"
            else:
                count += 1
        return name

        conn.commit()
        conn.close()


    def instructions(self,userName):
        #A story in 123 characters.
        text = 'You are one of the Last to resist against The End. There is no rest, each struggle calls you closer to death. Now fight on.'
        self.twt_print.printTweet(userName,text)



    def player_stats(self, userName):
        conn = sqlite3.connect('DunSuciRun.sqlite')
        p = conn.cursor()
        p.execute("SELECT * FROM CHARACTERS WHERE PLAYER = ?", (userName,))
        charData = p.fetchall()
        if len(charData) == 0:
            text = "You do not possess a character!"
        else:
            charTuple = charData[0]

            cha = CharDAO(charTuple[0], charTuple[1],charTuple[2],charTuple[3],charTuple[4])
            text = "You are " + str(cha.name) + " a " + str(cha.job) + ". You possess " + str(cha.gold) + \
                   " gold and your health is " + str(cha.health) + "."
        self.twt_print.printTweet(userName,text)


    def player_options(self,userName):
        text = "Your options are: make a [new] character, " \
               "learn about [who] you are or [continue] on. You may also learn [about] this world"
        self.twt_print.printTweet(userName,text)

    def dungeon_pick(self, userName):

            try:
                level = 1

                if 1 <= level <= 3:
                    conn = sqlite3.connect('DunSuciRun.sqlite')
                    c = conn.cursor()
                    m = conn.cursor()
                    n = conn.cursor()
                    p = conn.cursor()
                    c.execute('SELECT * FROM DUNGEONS WHERE DIFFICULTY =' + str(level))
                    dungeons = c.fetchall()
                    p.execute('SELECT * FROM CHARACTERS WHERE PLAYER = ?', (userName,))
                    getData = p.fetchall()
                    if len(getData) == 0:
                        return "You have no character!"
                    else:
                        charTuple = getData[0]
                        cha = CharDAO(charTuple[0], charTuple[1],charTuple[2],charTuple[3],charTuple[4])
                        randomNum= random.randint(0, len(dungeons)-1)
                        newTuple = dungeons[randomNum]
                        dun = DunDAO(newTuple[0], newTuple[1], newTuple[2]) #
                        dun.sign()
                        m.execute('SELECT * FROM BIGSCARIES WHERE THEME =?',(dun.theme,))
                        monsters = m.fetchall()
                        randoMon = random.randint(0, len(monsters)-1)
                        monsterTuple = monsters[randoMon]
                        mob = monDAO(monsterTuple[0], monsterTuple[1], int(monsterTuple[2]))
                        horde = random.randint(0,(level*dun.difficulty)) + cha.gold
                        #Updates character date with new health and treasure
                        n.execute('UPDATE CHARACTERS SET HEALTH = ?, GOLD = ? WHERE PLAYER = ?',(str((cha.health - (mob.damage*dun.difficulty))), horde, userName))
                        conn.commit()
                        conn.close()
                        entersAdj= 'runs into,traverses,stalks,enters,charges,assaults'.split(",")
                        # gathfath enters the whispering maze. With a slice, gathfath slew a mermaid. You find 00 gold but are hurt for 00

                        # text = ("You slay a " + mob.name + " and collect " + str(horde) + " gold! but hurts you for " + str((mob.damage*dun.difficulty)) + " damage.")
                        text = cha.name.split(' ')[0] + " " + random.choice(entersAdj) + " " + dun.name + " and slew a " + mob.name + \
                               " with a mighty cleave. They find " + str(dun.difficulty*random.randint(1,5)) + " gold but take " + str((mob.damage*dun.difficulty)) + " wound"

                        # return text
                        self.twt_print.printTweet(userName,text)
                else:
                    print("You shouldn't be able to get here")
                    self.dungeon_pick(userName)

            except StandardError as e:
                print('Try/catch error occured: ' + e)
                self.dungeon_pick(userName)
