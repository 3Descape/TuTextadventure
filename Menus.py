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
    blacksmith = Store.construt("blacksmith")
    return blacksmith.enter(game)


def menu_druid(game):
    druid = Store.construt("druid")
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


village_menu = {
    1: {
        "name": "inventory",
        "key": 1,
        "execute": menu_inventory
    },
    2: {
        "name": "merchant",
        "key": 2,
        "execute": menu_merchant

    },
    3: {
        "name": "blacksmith",
        "key": 3,
        "execute": menu_blacksmith
    },
    4: {
        "name": "druid",
        "key": 4,
        "execute": menu_druid
    },
    5: {
        "name": "dungeon",
        "key": 5,
        "execute": menu_dungeon
    },
    6: {
        "name": "save game",
        "key": 6,
        "execute": menu_save_game
    },
    0: {
        "name": "quit game",
        "key": 0,
        "execute": menu_quit_game
    }
}
