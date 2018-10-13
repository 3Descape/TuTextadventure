class Mercenary:
    def __init__(self, kwargs):
        self.health = 100
        self.damage = 0
        self.

        self.__dict__.update(**kwargs)

    def attackEnemy(self, enemy, player):
        damage = self.damage
        enemy.health -= damage
        print(
            f"Your mercenary attacked {enemy.name} and dealt {damage} damage.")
        if(not enemy.alive()):
            reward = enemy.getReward()
            player.gold += reward
            print(f"{enemy.name} died. It dropped {reward} gold.")

        return enemy, player
