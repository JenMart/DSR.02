import sqlite3

class CharDAO:
    def __init__(self, user, name, job, health, gold):
        self.user = user
        self.name = name
        self.job = job
        self.health = health
        self.gold = gold

        # self.runs = runs

