import argparse
from Assets.Player import Player
from Assets.Reseller import Reseller
from Assets.Store import Store
from Assets.InventoryItem import InventoryItem
from Assets.Dungeon import Dungeon

from Utils.Game import saveGame, loadGame

from Globals import *

import json


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--savefile', default="game.json",
                        help="The save file. default: 'game.json'")
    parser.add_argument("--new-game", dest="new_game", default=False, action='store_true',
                        help="Create a new save file.")
    parser.add_argument("-b", dest="bonus_tasks", default=False,
                        action="store_true", help='enable bonus tasks')
    parser.add_argument("--print-bonus", dest="print_bonus", default=False,
                        action="store_true", help='print bonus task list and exit')
    args = parser.parse_args()
    args = parser.parse_args()

    player = None
    savefile = args.savefile

    if(args.new_game):
        player = Player.character_setup()
    else:
        data = loadGame(savefile)
        player = data['player']

    game = True
    while game:
        selection = None
        input_required = True
        while input_required:
            print("Welcome to Prog0 Village! \nWhat do you want to do?")

            print(
                "\t1) Inventory\n\t2) Merchant\n\t3) Blacksmith\n\t4) Druid\n\t5) Dungeon\n\t6) Save game\n\t0) Quit game\n")
            option = input("> ")

            try:
                option = int(option)
            except:
                pass

            if(option in range(0, 7)):
                input_required = False
                selection = option
            else:
                print("Invalid choice. Try again.")

        if(selection == 0):
            should_save = input("Save before exiting? (Y/N)").lower()
            if(should_save == "y"):
                saveGame(savefile, player)
                game = False
            elif(should_save == "n"):
                game = False
            else:
                print("Invalid choice. Try again.")
            return

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
            saveGame(savefile, player)


if __name__ == "__main__":
    main()
