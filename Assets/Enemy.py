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

    def attackPlayer(self, game):
        damage = floor((self.attack**2)/(self.attack + game.player.defense))
        game.player.health -= damage
        print(f"{self.name} attacked you and dealt {damage} damage.")

        if(game.player.health < 1):
            game = game.player.kill(game)
            print(f"You were killed by {self.name}.")

        return game

    def getReward(self):
        return randint(self.reward[0], self.reward[1])

    def alive(self):
        return self.health > 0

    def copy(self):
        return Enemy(self.name, self.health, self.attack, self.defense, self.speed, self.reward)
