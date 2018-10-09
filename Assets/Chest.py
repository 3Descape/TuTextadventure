class Chest:
    def __init__(self, item):
        self.items = item

    def collectItems(self, player):
        if(len(self.items)):
            for item in self.items:
                print(f"You collected {item.name} from the chest.")
            return player.inventory.append(self.items)
        else:
            print("The chest is empty.")
            return player
