import sqlite3

class CharDAO:
    # player|name|job|health|gold|runs|org|weapon|map|RARM|LARM|RLEG|LLEG|HEAD 14 in total
    def __init__(self, user, name, job, health, gold,runs,org,weapon,map,rarm,larm,rleg,lleg,head):
        self.user = user
        self.name = name
        self.job = job
        self.health = health
        self.gold = gold
        self.runs = runs
        self.org = org
        self.weapon = weapon
        self.map = map
        self.rarm = rarm
        self.larm = larm
        self.rleg = rleg
        self.lleg = lleg

        # self.runs = runs


