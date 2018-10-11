from Globals import *
from Assets.Item import Item
from Utils.Helpers import *


class Store:
    stores = {
        "blacksmith": {
            "items": {
                "helmet": {
                    "price": 3,
                    "effected_attribute": EFFECT_DEFENSE,
                    "effect_amount": 2,
                    "usecase": USECASE_HELD
                },
                "chest plate": {
                    "price": 5,
                    "effected_attribute": EFFECT_DEFENSE,
                    "effect_amount": 4,
                    "usecase": USECASE_HELD
                },
                "sword": {
                    "price": 10,
                    "effected_attribute": EFFECT_ATTACK,
                    "effect_amount": 5,
                    "usecase": USECASE_HELD
                }
            }
        },
        "druid": {
            "items": {
                "potion": {
                    "price": 3,
                    "effected_attribute": EFFECT_DEFENSE,
                    "effect_amount": 10,
                    "usecase": USECASE_USE
                },
                "beer": {
                    "price": 2,
                    "effected_attribute": EFFECT_SPEED,
                    "effect_amount": -1,
                    "usecase": USECASE_USE
                },
                "coffee": {
                    "price": 5,
                    "effected_attribute": EFFECT_SPEED,
                    "effect_amount": 2,
                    "usecase": USECASE_USE
                },
                "antidote": {
                    "price": 15,
                    "effected_attribute": EFFECT_DEFENSE,
                    "effect_amount": 6,
                    "usecase": USECASE_USE
                },
                "milk": {
                    "price": 15,
                    "effected_attribute": EFFECT_ATTACK,
                    "effect_amount": 6,
                    "usecase": USECASE_USE
                },
            }
        }
    }

    def __init__(self, name, items):
        self.name = name
        self.items = items

    @staticmethod
    def construt(name):
        return Store(name, [Item({"name": item, **data}) for (item, data) in Store.stores[name]["items"].items()])

    def enter(self, player):
        while True:
            print(
                f"Welcome to the {self.name}\nYou have {player.gold} gold to spend. This is what I'm selling:")
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
                        print(f"You have chosen {found.name}.")
                        player.buyItem(found)
                        print(f"You have {player.gold} gold left.\n")

                    else:
                        print("Not enough gold.")

                else:
                    print(f"I do not sell '{user_input}'.")

        return player

    def listItems(self):
        for item in self.items:
            name = format_r(item.name.title(), 20)
            price = format_l(item.price, 4)
            effect_amount = ("+" if item.effect_amount >=
                             0 else "-") + str(item.effect_amount)
            print(
                f"\t* {name} for {price} gold ({effect_amount} {item.effected_attribute} when {item.usecase})")
