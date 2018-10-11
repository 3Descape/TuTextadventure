from External.json_serialization import json_class, CustomDecoder, CustomEncoder
from math import floor

from Globals import *

@json_class
class Player:
    def __init__(self, kwargs):
        self.name = ""
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.gold = 100
        self.inventory = []
        self.health = 100
        self.__dict__.update(**kwargs)

    @staticmethod
    def attribute_input_handler(text, used):
        value = None
        while True:
            value = input(text)

            try:
                value = int(value)
                if(value > 0):
                    break

                else:
                    print("Please input a positive integer.")

            except ValueError:
                print("Please input a positive integer.")

        return value

    def buyItem(self, item):
        self.inventory.append(item)
        if(item.usecase == USECASE_HELD):
            self.applyEffect(item.effected_attribute, item.effect_amount)

        self.gold -= item.price

    def applyEffect(self, effected_attribute, effect_amount):
        setattr(self, effected_attribute, getattr(
            self, effected_attribute) + effect_amount)

    @staticmethod
    def character_setup():
        name = ""
        attack = ""
        defense = ""
        speed = ""
        require_confirmation = True

        while require_confirmation:
            print(
                "Welcome to P0 Dungeon Quest character creator!")
            name = input("Enter your name: ")

            input_required = True
            while input_required:
                print("You have 100 points to assign to your character.")
                print(
                    "Start now to assign those Points to your characters attack, defense and speed.")

                used = 0

                attack = Player.attribute_input_handler("Attack: ", used)
                used += attack

                defense = Player.attribute_input_handler("Defense: ", used)
                used += defense

                speed = Player.attribute_input_handler("Speed: ", used)
                used += speed

                if(used <= 100):
                    input_required = False
                    print(
                        "Before you store your character please confirm your stats!")
                    print("Name:", name)
                    print("Attributes:\n")
                    print("\t * Attack:", attack)
                    print("\t * Defense:", defense)
                    print("\t * Speed:", speed, "\n")

                    valid_input = False

                    while not valid_input:
                        confirm = input("Is this correct? (Y/N) ")
                        confirm = confirm.lower()
                        if(confirm in ["y", "n"]):
                            valid_input = True
                            if(confirm == "y"):
                                require_confirmation = False
                        else:
                            print("Please enter Y/y for yes and N/n for no!")

                else:
                    print(
                        "Sorry, it seems like you spent more than 100 ability points on your character... Try that again!")

        return Player({"name": name, "attack": attack, "defense": defense, "speed": speed, "gold": 100, "inventory": [], "health": 100})

    def showInventory(self):
        while True:
            if(len(self.inventory)):
                print(
                    f"Welcome to your inventory {self.name}!\nThese are your items:\n")
                for item in self.inventory:
                    prefix = "+" if item.effect_amount >= 0 else "-"
                    print(
                        f"\t* {item.name.capitalize().ljust(20, ' ')} ({prefix}{item.effect_amount} {item.effected_attribute} when {item.usecase})")

                print("\nType 'quit' or the name of the item you want to use/drop:")

                user_input = input("> ").lower()

                if(user_input == "quit"):
                    break

                else:
                    inventory_item = None
                    for item in self.inventory:
                        if(item.name == user_input):
                            inventory_item = item

                    if(inventory_item != None):
                        print(
                            f"Do you want to 'use' or 'drop' {inventory_item.name.capitalize()}? Else 'quit'.\n")

                        action = input("> ").lower()

                        if(action == "drop"):
                            if(inventory_item.usecase == USECASE_HELD):
                                self.applyEffect(
                                    inventory_item.effected_attribute, -inventory_item.effect_amount)

                            self.inventory.remove(inventory_item)
                            print(f"You dropped {inventory_item.name.capitalize()}.")
                            break

                        elif(action == "use"):
                            if(inventory_item.usecase == USECASE_USE):
                                self.applyEffect(inventory_item.effected_attribute, inventory_item.effect_amount)
                                self.inventory.remove(inventory_item)

                                print(f"You used {inventory_item.name.capitalize()}.")
                                print(
                                    f"It increased your {inventory_item.effected_attribute} by {inventory_item.effect_amount}.")
                                print(
                                    f"You now have {getattr(self, inventory_item.effected_attribute)} {inventory_item.effected_attribute}.")
                                break

                            else:
                                print("You cannot use this item.")
                                break

                        elif(action == "quit"):
                            break
                        else:
                            print("Nothing done.")
                    else:
                        print("Item does not exist.")

            else:
                print("Your inventory is empty.")
                break

    def kill(self):
        for item in self.inventory:
            if(item.usecase == "held"):
                self.applyEffect(item.effected_attribute, -item.effect_amount)
        self.inventory = []

    def respawn(self):
        self.health = 100

    def alive(self):
        return self.health > 0

    def attackEnemy(self, enemy):
        damage = floor((self.attack**2)/(self.attack + enemy.defense))
        enemy.health -= damage
        print(f"You attacked {enemy.name} and dealt {damage} damage.")
        if(not enemy.alive()):
            reward = enemy.getReward()
            self.gold += reward
            print(f"{enemy.name} died. It dropped {reward} gold.")

        return enemy

    def tojson(self):
        encoder = CustomEncoder()
        json = encoder.default(self)
        json["inventory"] = [encoder.default(item) for item in self.inventory]
        return json
