from External.json_serialization import json_class, CustomDecoder, CustomEncoder

from math import floor


@json_class
class Player:
    def __init__(self, name, attack, defense, speed, gold, inventory, health):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.gold = gold
        self.inventory = inventory
        self.health = health

    @staticmethod
    def attribute_input_handler(text, used):
        valid = False
        value = None
        while not valid:
            value = input(text)

            try:
                value = int(value)
                if(value > 0):
                    valid = True
#                    if(100-used-value != 0):
#                        print(f"You only have {100-used-value} points left.")
                else:
                    print("Please input a positive integer.")
            except ValueError:
                print("Please input a positive integer.")
        return value

    def buyItem(self, item):
        self.inventory.append(item)
        self.gold -= item.price

    @staticmethod
    def character_setup():
        name = ""
        attack = ""
        defense = ""
        speed = ""

        require_confirmation = True
        while require_confirmation:

            input_required = True

            while input_required:
                print(
                    "Welcome to P0 Dungeon Quest character creator!")

                name = input("Enter your name: ")
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
                    print("Attributes:")
                    print("\t * Attack:", attack)
                    print("\t * Defense:", defense)
                    print("\t * Speed:", speed)

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
                        "Sorry, it seems like you spend more than 100 ability points on your charater... \nTry that again!")

        return Player(name, attack, defense, speed, 100, [], 100)

    def showInventory(self):
        require_input = True
        while require_input:
            if(len(self.inventory)):
                print(
                    f"Welcome to your inventory {self.name}!\nThese are your items:")
                for item in self.inventory:
                    prefix = "+" if item.effect_amount >= 0 else "-"
                    print(
                        f"\t* {item.name.ljust(20, ' ')} ({prefix}{item.effect_amount} {item.effected_attribute} when {item.usecase})")

                print("Type 'quit' or the name of the item you want to use/drop:")
                user_input = input().lower()

                if(user_input == "quit"):
                    require_input = False
                else:
                    inventory_item = None
                    for item in self.inventory:
                        if(item.name.lower() == user_input):
                            inventory_item = item
                    if(inventory_item != None):

                        action = input(
                            f"> Do you want to 'use' or 'drop' {inventory_item.name}? Else 'quit'.\n").lower()

                        if(action == "drop"):
                            self.inventory.remove(inventory_item)
                            print(f"> You dropped {inventory_item.name}.")
                            require_input = False
                        elif(action == "use"):
                            if(inventory_item.usecase == "used"):
                                setattr(self, inventory_item.effected_attribute, getattr(
                                    self, inventory_item.effected_attribute) + inventory_item.effect_amount)
                                self.inventory.remove(inventory_item)
                                print(f"> You used {inventory_item.name}.")
                                print(
                                    f"It increased your {inventory_item.effected_attribute} by {inventory_item.effect_amount}.")
                                print(
                                    f"You now have {getattr(self, inventory_item.effected_attribute)} {inventory_item.effected_attribute}.")
                                require_input = False
                            else:
                                print("> You cannot use this item.")
                                require_input = False
                        elif(action == "quit"):
                            require_input = False
                        else:
                            print("Nothing done.")
                    else:
                        print("Item does not exist.")

            else:
                print("Your inventory is empty.")
                require_input = False

    def killed(self):
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
            print(f"You killed {enemy.name} and earned {reward} gold.")
            self.gold += reward
            print(f"{enemy.name} died. It dropped {reward} gold.")
        return enemy

    def tojson(self):
        encoder = CustomEncoder()
        json = encoder.default(self)
        json["inventory"] = [encoder.default(item) for item in self.inventory]
        return json
