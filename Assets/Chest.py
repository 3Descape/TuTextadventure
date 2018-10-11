from Globals import *


class Chest:
    def __init__(self, item):
        self.items = item

    def collectItems(self, player):
        if(len(self.items)):
            for item in self.items:
                print(f"You collected {item.name} from the chest.")
                if(item.usecase == USECASE_HELD):
                    player = player.applyEffect(
                        item.effected_attribute, item.effect_amount)

            return player.inventory.append(self.items)
        else:
            print("The chest is empty.")
            return player
