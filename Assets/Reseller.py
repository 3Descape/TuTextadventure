class Reseller:
    def __init__(self, name):
        self.name = name

    def enter(self, game):
        player = game.player

        while True:
            if(len(player.inventory)):
                print(f"Welcome to the {self.name}!\nYou have {player.gold} gold. This is what I would pay for your items:")
                for item in player.inventory:
                    print(f"\t* {item.name.capitalize().ljust(20, ' ')} for{str(int(item.price/2)).rjust(5, ' ')} gold")

                print("Type 'quit' or the name of the item you want to sell.")

                input_item = input("> ").lower()

                if(input_item == "quit"):
                    break
                else:
                    item_to_sell = None
                    for item in player.inventory:
                        if(input_item == item.name.lower()):
                            item_to_sell = item

                    if(item_to_sell != None):
                        print(f"You have chosen {item_to_sell.name.capitalize()}.")
                        player.gold += int(item_to_sell.price/2)
                        player.inventory.remove(item_to_sell)
                        print(f"You now have {player.gold} gold left.")
                        print("Removed item from inventory.")
                    else:
                        print(f"Sorry, you don't own the item {input_item}")
            else:
                print("Sorry, you have nothing to sell.\nThanks for visiting!")
                break

        game.player = player

        return game
