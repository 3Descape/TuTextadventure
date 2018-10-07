class Room:
    def __init__(self, enemies, chest):
        self.enemies = enemies
        self.chest = chest

    def showEnemies(self):
        for index, enemy in enumerate(self.enemies):
            print(f"\t{index+1}) {enemy.name.ljust(15, ' ')} ({enemy.health} HP)")
