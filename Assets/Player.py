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
        self.chest = []
        self.health = 100
        self.__dict__.update(**kwargs)

    def buyItem(self, item):
        self.inventory.append(item)
        if(item.usecase == USECASE_HELD):
            self.applyItemEffect(item)
        self.gold -= item.price

    def applyItemEffect(self, item):
        for effect in item.effects:
            self.applyEffect(effect["effected_attribute"], effect["effect_amount"])

    def removeItemEffect(self, item):
        for effect in item.effects:
            self.applyEffect(effect["effected_attribute"], -effect["effect_amount"])

    def applyEffect(self, effected_attribute, effect_amount):
        setattr(self, effected_attribute, getattr(
            self, effected_attribute) + effect_amount)

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
                print("Start now to assign those Points to your characters attack, defense and speed.")

                used = 0

                attack = Player.attribute_input_handler("Attack: ", used)
                used += attack

                defense = Player.attribute_input_handler("Defense: ", used)
                used += defense

                speed = Player.attribute_input_handler("Speed: ", used)
                used += speed

                if(used <= 100):
                    input_required = False
                    print("Before you store your character please confirm your stats!")
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
                    print("Sorry, it seems like you spent more than 100 ability points on your character... Try that again!")

        return Player({"name": name, "attack": attack, "defense": defense, "speed": speed, "gold": 100, "inventory": [], "health": 100})

    def findInventoryItem(self, name):
        inventory_item = None
        for item in self.inventory:
            if(item.name == name):
                inventory_item = item
        if(inventory_item == None):
            print("Item does not exist.")

        return inventory_item

    def findChestItem(self, name):
        chest_item = None
        for item in self.chest:
            if(item.name == name):
                chest_item = item
        if(chest_item == None):
            print("Item does not exist.")

        return chest_item

    def showInventory(self):
        while True:
            if(len(self.inventory)):
                print(f"Welcome to your inventory {self.name}!\nThese are your items:\n")

                for item in self.inventory:
                    print(f"\t* {item.name.capitalize().ljust(20, ' ')} ({item.effectDescription()} when {item.usecase})")

                print("\nType 'quit' or the name of the item you want to use/drop:")

                user_input = input("> ").lower()

                if(user_input == "quit"):
                    break

                else:
                    inventory_item = self.findInventoryItem(user_input)

                    if(inventory_item != None):
                        print(f"Do you want to 'use' or 'drop' {inventory_item.name.capitalize()}? Else 'quit'.\n")

                        action = input("> ").lower()

                        if(action == "drop"):
                            if(inventory_item.usecase == USECASE_HELD):
                                self.removeItemEffect(inventory_item)

                            self.inventory.remove(inventory_item)
                            print(f"You dropped {inventory_item.name.capitalize()}.")
                            break

                        elif(action == "use"):
                            if(inventory_item.usecase == USECASE_USE):
                                self.applyItemEffect(inventory_item)
                                self.inventory.remove(inventory_item)

                                print(f"You used {inventory_item.name.capitalize()}.")
                                message = ""
                                last_index = len(inventory_item.effects)-1

                                for (index, effect) in enumerate(inventory_item.effects):
                                    message = message + effect["effected_attribute"] + " by " + inventory_item.prefix(effect) + str(effect["effect_amount"])
                                    if(index != last_index):
                                        message = message + ", "

                                print(f"It increased your {message}.")

                                stats = ""

                                for (index, effect) in enumerate(inventory_item.effects):
                                    stats = stats + str(getattr(self, effect["effected_attribute"])) + " " + effect["effected_attribute"]
                                    if(index != last_index):
                                        stats = stats + ", "

                                print(f"You now have {stats}.")
                                break

                            else:
                                print("You cannot use this item.")
                                break

                        elif(action == "quit"):
                            break
                        else:
                            print("Nothing done.")

            else:
                print("Your inventory is empty.")
                break

    def kill(self, game):
        for item in self.inventory:
            if(item.usecase == USECASE_HELD):
                self.removeItemEffect(item)
            if(game.bonus_tasks):
                item.price = int(item.price/2)
                game.gravedigger_items.append(item)

        self.inventory = []
        return game

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

    def showTreasureChest(self):
        while True:
            if(len(self.inventory)):
                print("You have the following items in your inventory:")

                for item in self.inventory:
                    print(f"\t* {item.name.capitalize().ljust(20, ' ')} ({item.effectDescription()} when {item.usecase})")
                print("")
            else:
                print("Your inventory is empty.\n")

            if(len(self.chest)):
                print("You have the following items in your chest.")
                for item in self.chest:
                    print(f"\t* {item.name.capitalize().ljust(20, ' ')} ({item.effectDescription()} when {item.usecase})")
                print("")
            else:
                print("Your treasure chest is empty.\n")

            print("Type 'chest' or 'inventory' to exchange items. Type 'quit' to exit")

            action = input("> ").lower()

            if(action == "chest"):
                print("Type the name of the item you want to put back into your inventory.")
                item_name = input(">").lower()
                print(item_name)
                item = self.findChestItem(item_name)

                if(item != None):
                    self.inventory.append(item)
                    if(item.usecase == USECASE_HELD):
                        self.applyItemEffect(item)
                    self.chest.remove(item)

            elif(action == "inventory"):
                print("Type the name of the item you want to put into your treasure chest.")
                item_name = input(">").lower()
                item = self.findInventoryItem(item_name)

                if(item != None):
                    self.chest.append(item)
                    if(item.usecase == USECASE_HELD):
                        self.removeItemEffect(item)
                    self.inventory.remove(item)
            elif(action == "quit"):
                break
            else:
                print("Invalid choice. Try again!")

    def tojson(self):
        encoder = CustomEncoder()
        json = encoder.default(self)
        json["inventory"] = [encoder.default(item) for item in self.inventory]
        json["chest"] = [encoder.default(item) for item in self.chest]
        return json
