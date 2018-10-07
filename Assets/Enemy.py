from math import floor
from random import randint


class Enemy:
    def __init__(self, name, health, attack, defense, speed, reward):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.reward = reward
        self.alive = True

    def attackPlayer(self, player):
        damage = floor((self.attack**2)/(self.attack + player.defense))
        player.health -= damage
        print(f"{self.name} attacked you and dealt {damage} damage.")
        if(player.health < 1):
            print(f"You were killed by {self.name}")
            player.killed()
        return player

    def getReward(self):
        return randint(self.reward[0], self.reward[1])

    def killed(self):
        self.alive = False
