class Dungeon:
    def __init__(self, name, theme, difficulty):
        self.name = name
        self.theme = theme
        self.difficulty = difficulty

    def sign(self):
        print('You are now entering ' + self.name)