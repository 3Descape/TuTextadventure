class Room:
    def __init__(self, enemies, chest):
        self.enemies = enemies
        self.chest = chest

    def getFirstEnemy(self):
        if(len(self.enemies)):
            return self.enemies[0]

        return None

    def hasEnemies(self):
        return len(self.enemies) > 0

    def showEnemies(self):
        for index, enemy in enumerate(self.enemies):
            print(f"\t{index+1}) {enemy.name.ljust(15, ' ')} ({enemy.health} HP)")

    def updateEnemy(self, enemy):
        for index, e in enumerate(self.enemies):
            if e == enemy:
                if(enemy.alive()):
                    self.enemies[index] = enemy
                else:
                    del self.enemies[index]
                break
