import sqlite3

class Character:
    def __init__(self, name, job, health, marker=0, runs = 0):
        self.name = name
        self.job = job
        self.health = health
        self.marker = marker
        self.runs = runs

    def stats(self):
        return self.name + " - " + str(self.health) + "/100 Health"

    def numbered_stats(self, index):
        return str(index) + ". " + self.stats()

    def announce(self):
        print("I am " + self.name + " and I am a " + self.job  +"!!!")

    def hit(self, x):
        if self.health > x.damage:
            self.health -= x.damage

            conn = sqlite3.connect('DunSuciRun.sqlite')
            c = conn.cursor()
            c.execute("UPDATE CHARACTERS SET HEALTH=" + self.health + " WHERE NAME =" + self.name)
            conn.commit()
            conn.close()


        elif self.health <= x.damage:
            self.health = 0
           # self.alive = False
            print ("You have perished.")

            conn = sqlite3.connect('DunSuciRun.sqlite')
            c = conn.cursor()
            c.execute("UPDATE CHARACTERS SET HEALTH=0 WHERE NAME =" + self.name)
            conn.commit()
            conn.close()