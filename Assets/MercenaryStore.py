from Assets.Player import Player
from random import randint


class MercenaryStore:
    def __init__(self):
        self.mercenaries = []
        self.generateMercenaries()

    def generateMercenaries(self):
        mercenaries = {
            "herman": {
                "speed": 20,
                "attack": 10,
                "defense": 3,
                "gold": 5
            },
            "endres": {
                "speed": 10,
                "attack": 7,
                "defense": 10,
                "gold": 3
            },
            "erhardt": {
                "speed": 15,
                "attack": 4,
                "defense": 14,
                "gold": 4
            },
            "steffan": {
                "speed": 20,
                "attack": 20,
                "defense": 7,
                "gold": 7
            },
            "thomas": {
                "speed": 3,
                "attack": 10,
                "defense": 30,
                "gold": 5
            }
        }

        for (mercenary, data) in mercenaries.items():
            temp = Player({"name": mercenary, "speed": data["speed"], "attack": data["attack"], "defense": data["defense"], "gold": data["gold"]})
            self.mercenaries.append(temp)

    def enter(self, game):
        player = game.player

        while True:
            if(not player.hasMercenary()):

                print(f"Welcome to the mercenary store\nYou have {player.gold} gold to spend. These are the mercenaries that you can lent:")

                for m in self.mercenaries:
                    print(f"{m.name.title().ljust(10, ' ')}, for {str(m.gold).rjust(2, ' ')} gold per fight. Speed: {str(m.speed).rjust(2, ' ')}, \
                          Attack: {str(m.attack).rjust(2, ' ')}, Defense: {str(m.defense).rjust(2, ' ')}")

                print("\nType the name of the mercenary you want to hire or 'quit'.")
                name = input("> ").lower()

                if(name == "quit"):
                    break

                found = None

                for m in self.mercenaries:
                    if(m.name == name):
                        found = m
                if(found == None):
                    print("We could not find a mercenary with that name. Try it again!")
                else:
                    player.hireMercenary(found)
                    break

            else:
                print(f"You have already lented {game.player.mercenary.name.title()}.")
                print("Do you want to bring him back? Yes/No")
                user_input = input(">").lower()

                if(user_input == "yes"):
                    player.returnMercenary()
                else:
                    break
        return game
