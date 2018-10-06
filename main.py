import argparse
from Assets.Player import Player
from Assets.Reseller import Reseller
from Assets.Store import Store
from Assets.InventoryItem import InventoryItem
from Assets.Dungeon import Dungeon

import json

EFFECT_ATTACK = "attack"
EFFECT_DEFENSE = "defense"
EFFECT_SPEED = "speed"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--new-game',
                        help='Starts a new game', action='store_true', required=False)
    parser.add_argument('--savefile',
                        help='File to load game from', required=False)

    args = parser.parse_args()

    player = None
    savefile = "game.json"

    if(args.new_game):
        player = Player.character_setup()
    elif(args.savefile):
        savefile = args.savefile
        print(f"set savefile to {savefile}")

    game = True
    while game:
        selection = None
        input_required = True
        while input_required:
            print("Welcome to Prog0 Village! \nWhat do you want to do?")
            print("\t1) Inventory\n\t2) Merchant\n\t3) Blacksmith\n\t4) Druid\n\t5) Dungeon\n\t6) Save game\n\t0) Quit game")

            option = int(input())

            if(option in range(0, 7)):
                input_required = False
                selection = option
            else:
                print("Invalid choice. Try again.")

        if(selection == 0):
            print("> Save before exiting? (Y/N)")
            should_exit = input()
            if(should_exit.lower() == "y"):
                game = False
        elif(selection == 1):
            player.showInventory()
        elif(selection == 2):
            merchant = Reseller("merchant")
            player = merchant.enter(player)
        elif(selection == 3):
            blacksmith = Store("blacksmith", [
                InventoryItem('Helmet', 3, EFFECT_DEFENSE, 2, "held"),
                InventoryItem('Check plate', 5, EFFECT_DEFENSE, 4, "held"),
                InventoryItem('Sword', 10, EFFECT_ATTACK, 5, "held")
            ])
            player = blacksmith.enter(player)
        elif(selection == 4):
            druid = Store("druid", [
                InventoryItem('Potion', 3, EFFECT_DEFENSE, 10, "used"),
                InventoryItem('Beer', 2, EFFECT_SPEED, -2, "used"),
                InventoryItem('Coffee', 5, EFFECT_SPEED, 2, "used"),
                InventoryItem('Antidote', 15, EFFECT_DEFENSE, 6, "used"),
                InventoryItem('Milk', 15, EFFECT_ATTACK, 6, "used"),
            ])
            player = druid.enter(player)
        elif(selection == 5):
            dungeon = Dungeon()
            dungeon.enter(player)
        elif(selection == 6):
            file = open(savefile, "w")
            json.dump({"player": player.toDic()}, file)
            file.close()


if __name__ == "__main__":
    main()
