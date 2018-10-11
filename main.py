import argparse
from Assets.Player import Player
from Assets.Reseller import Reseller
from Assets.Store import Store
from Assets.Dungeon import Dungeon

from Utils.Game import saveGame, loadGame


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

        while True:
            print("Welcome to Prog0 Village! \nWhat do you want to do?")

            print(
                """
                1) Inventory
                2) Merchant
                3) Blacksmith
                4) Druid
                5) Dungeon
                6) Save game
                0) Quit game
                """)
            option = input("> ")

            try:
                option = int(option)
            except:
                pass

            if(option in range(0, 7)):
                selection = option
                break
            else:
                print("Invalid choice. Try again.")

        if(selection == 0):
            should_save = input("Save before exiting? (Y/N)").lower()
            if(should_save == "y"):
                saveGame(savefile, player)
                game = False

            elif(should_save == "n"):
                game = False

            return

        elif(selection == 1):
            player.showInventory()

        elif(selection == 2):
            merchant = Reseller("merchant")
            player = merchant.enter(player)

        elif(selection == 3):
            blacksmith = Store.construt("blacksmith")
            player = blacksmith.enter(player)

        elif(selection == 4):
            druid = Store.construt("druid")
            player = druid.enter(player)

        elif(selection == 5):
            dungeon = Dungeon()
            dungeon.enter(player)

        elif(selection == 6):
            saveGame(savefile, player)


if __name__ == "__main__":
    main()
