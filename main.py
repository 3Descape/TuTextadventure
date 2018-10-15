import argparse
import os.path

from Assets.Player import Player
from Assets.Store import Store
from Game import Game
from Globals import EFFECT_ATTACK, EFFECT_SPEED, EFFECT_DEFENSE, USECASE_HELD
from Menus import village_menu, addBonusMenuItems


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--savefile', default="game.json",
                        help="The save file. default: 'game.json'")
    parser.add_argument("--new-game", dest="new_game", default=False,
                        action='store_true', help="Create a new save file.")
    parser.add_argument("-b", dest="bonus_tasks", default=False,
                        action="store_true", help='enable bonus tasks')
    parser.add_argument("--print-bonus", dest="print_bonus", default=False,
                        action="store_true", help='print bonus task list and exit')
    args = parser.parse_args()

    savefile = args.savefile
    new_game = args.new_game

    game = Game(savefile=savefile, bonus_tasks=args.bonus_tasks)

    if(not os.path.isfile(savefile)):
        new_game = True

    if(args.print_bonus):
        print("6,7,9")

    if(new_game):
        game.initialize()
    else:
        game.load(args.bonus_tasks)

    if(args.bonus_tasks):
        Store.addItem(store="blacksmith", item="war hammer", price=15, effects=[
                      [EFFECT_ATTACK, 7], [EFFECT_SPEED, -5]], usecase=USECASE_HELD)
        Store.addItem("blacksmith", "crystal sword", 10, [
                      [EFFECT_ATTACK, 8], [EFFECT_DEFENSE, -3]], USECASE_HELD)

        addBonusMenuItems()

    while game.gameloop:
        menu = True
        while menu:
            print("Welcome to Prog0 Village! \nWhat do you want to do?\n")

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
