class Store:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def enter(self, player):
        input_required = True
        while input_required:
            print(
                f"> Welcome to the {self.name}\nYou have {player.gold} gold to spend. This is what I'm selling:")
            self.list_items()
            print("Type 'quit' or the name of the item you want to buy.")

            user_input = input().lower()

            if(user_input == "quit"):
                input_required = False
            else:
                found = None
                for item in self.items:
                    if(item.name.lower() == user_input):
                        found = item
                if(found != None):
                    if(player.gold >= item.price):
                        print(f"> You have chosen {found.name}.")
                        player.buyItem(found)
                        print(f"You have {player.gold} gold left.\n")

                    else:
                        print("Not enough gold.")
                else:
                    print(f"I do not sell '{user_input}'.")
        return player

    def list_items(self):
        for item in self.items:
            print(
                f"\t* {self.format_attr_r(item.name, 20)} for {self.format_attr_l(item.price, 4)} gold (" + ("+" if item.effect_amount >= 0 else "-") + f"{item.effect_amount} {item.effected_attribute} when {item.usecase})")

    def format_attr_r(self, attribute, len):
        return str(attribute).ljust(len, " ")

    def format_attr_l(self, attribute, len):
        return str(attribute).rjust(len, " ")
