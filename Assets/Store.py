from Globals import *
from Assets.Item import Item
from Utils.Helpers import *


class Store:
    stores = {
        "blacksmith": {
            "items": {
                "helmet": {
                    "price": 3,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_DEFENSE,
                            "effect_amount": 2,
                        }
                    ],
                    "usecase": USECASE_HELD
                },
                "chest plate": {
                    "price": 5,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_DEFENSE,
                            "effect_amount": 4,
                        }
                    ],
                    "usecase": USECASE_HELD
                },
                "sword": {
                    "price": 10,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_ATTACK,
                            "effect_amount": 5,
                        }
                    ],
                    "usecase": USECASE_HELD
                }
            }
        },
        "druid": {
            "items": {
                "potion": {
                    "price": 3,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_DEFENSE,
                            "effect_amount": 10,
                        }
                    ],
                    "usecase": USECASE_USE
                },
                "beer": {
                    "price": 2,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_SPEED,
                            "effect_amount": -1,
                        }
                    ],
                    "usecase": USECASE_USE
                },
                "coffee": {
                    "price": 5,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_SPEED,
                            "effect_amount": 2,
                        }
                    ],
                    "usecase": USECASE_USE
                },
                "antidote": {
                    "price": 15,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_DEFENSE,
                            "effect_amount": 6
                        },
                    ],
                    "usecase": USECASE_USE
                },
                "milk": {
                    "price": 15,
                    "effects": [
                        {
                            "effected_attribute": EFFECT_ATTACK,
                            "effect_amount": 6,
                        }
                    ],
                    "usecase": USECASE_USE
                },
            }
        }
    }

    def __init__(self, name, items, removeAfterSelling=False):
        self.name = name
        self.items = items
        self.removeAfterSelling = removeAfterSelling

    @staticmethod
    def addStore(name):
        Store.stores[name] = {
            "items": {

            }
        }
        return

    @staticmethod
    def construt(name, game):
        return Store(name, [Item({"name": item, **data}) for (item, data) in Store.stores[name]["items"].items()])

    @staticmethod
    def addItem(store, item, price, effects, usecase):
        effects_arr = []
        for e in effects:
            effects_arr.append({
                "effected_attribute": e[0],
                "effect_amount": e[1]
            })

        Store.stores[store]["items"][item] = {
            "price": price,
            "effects": effects_arr,
            "usecase": usecase
        }

    def enter(self, game):
        player = game.player
        while True:
            print(f"Welcome to the {self.name}\nYou have {player.gold} gold to spend. This is what I'm selling:")

            if(DEBUG):
                print(f"attack: {player.attack}, speed: {player.speed}, defense: {player.defense}")

            self.listItems()
            print("Type 'quit' or the name of the item you want to buy.")

            user_input = input("> ").lower()

            if(user_input == "quit"):
                break

            else:
                found = None
                for item in self.items:
                    if(item.name.lower() == user_input):
                        found = item

                if(found != None):
                    if(player.gold >= found.price):
                        print(f"You have chosen {found.name.capitalize()}.")
                        player.buyItem(found)
                        if(self.removeAfterSelling):
                            if(game.bonus_tasks):
                                if(self.name == "gravedigger"):
                                    game.gravedigger_items.remove(found)
                            self.items.remove(found)

                        print(f"You have {player.gold} gold left.\n")

                    else:
                        print("Not enough gold.")

                else:
                    print(f"I do not sell '{user_input}'.")

        game.player = player
        return game

    def listItems(self):
        print("")
        if(len(self.items)):
            for item in self.items:
                name = format_r(item.name.title(), 20)
                price = format_l(item.price, 4)
                print(f"\t* {name} for {price} gold ({item.effectDescription()} when {item.usecase})")

        else:
            print("I don't have any items currently. Please come back later again!")

        print("")
