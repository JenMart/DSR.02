class Boss:
    def __init__(self, name, theme, damage):
        self.name = name
        self.theme = theme
        self.damage = damage

    def talk(self):
        print("and you encounter a " + self.name)