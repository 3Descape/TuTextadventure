from Assets.Reseller import Reseller
from Assets.Store import Store
from Assets.Dungeon import Dungeon


def menu_inventory(game):
    game.player.showInventory()
    return game


def menu_merchant(game):
    merchant = Reseller("merchant")
    return merchant.enter(game)


def menu_blacksmith(game):
    blacksmith = Store.construt("blacksmith", game)
    return blacksmith.enter(game)


def menu_druid(game):
    druid = Store.construt("druid", game)
    return druid.enter(game)


def menu_dungeon(game):
    dungeon = Dungeon()
    return dungeon.enter(game)


def menu_save_game(game):
    game.save()
    return game


def menu_quit_game(game):
    print("Save before exiting? (Y/N)")
    should_save = input().lower()
    if(should_save == "y"):
        game.save()

    game.stop()

    return game


def menu_treasure_chest(game):
    game.player.showTreasureChest()
    return game


def menu_gravedigger(game):
    gravedigger = Store("gravedigger", game.gravedigger_items.copy(), removeAfterSelling=True)
    return gravedigger.enter(game)

    # def menu_mercenary(game):
    #     print("Mercenary")
    #     return game


def addBonusMenuItems():
    menu = village_menu
    quit_entry = village_menu.pop(0)

    menu[8] = {
        "name": "treasure chest",
        "execute": menu_treasure_chest
    }

    menu[9] = {
        "name": "gravedigger",
        "execute": menu_gravedigger
    }
    # menu[7] = {
    #     "name": "Mercenary",
    #     "execute": menu_mercenary
    # }

    menu[0] = quit_entry


village_menu = {
    1: {
        "name": "inventory",
        "execute": menu_inventory
    },
    2: {
        "name": "merchant",
        "execute": menu_merchant

    },
    3: {
        "name": "blacksmith",
        "execute": menu_blacksmith
    },
    4: {
        "name": "druid",
        "execute": menu_druid
    },
    5: {
        "name": "dungeon",
        "execute": menu_dungeon
    },
    6: {
        "name": "save game",
        "execute": menu_save_game
    },
    0: {
        "name": "quit game",
        "execute": menu_quit_game
    }


}
