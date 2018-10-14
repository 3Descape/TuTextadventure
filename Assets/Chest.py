from Globals import *


class Chest:
    def __init__(self, items):
        self.items = items

    def collectItems(self, player):
        if(len(self.items)):
            for item in self.items:
                print(f"You collected {item.name} from the chest.")
                if(item.usecase == USECASE_HELD):
                    player = player.applyItemEffect(item)
                player.inventory.append(item)

            return player
        else:
            print("The chest is empty.")
            return player
