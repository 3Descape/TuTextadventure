import argparse
from Assets.Player import Player
from Game import Game

from Menus import *


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

    savefile = args.savefile

    game = Game(savefile=savefile)

    if(args.new_game):
        game.initialize()

    else:
        game.load()

    while game.gameloop:
        menu = True
        while menu:
            print("Welcome to Prog0 Village! \nWhat do you want to do?")

            for (option, data) in village_menu.items():
                print(f"\t{option}) {data['name'].capitalize()}")

            option = input("> ")

            try:
                option = int(option)
            except:
                pass

            found = False
            for (option_iter, data) in village_menu.items():
                if(option_iter == option):
                    game = data["execute"](game)
                    found = True
                    menu = False
                    break

            if(not found):
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
