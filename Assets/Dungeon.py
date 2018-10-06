class Dungeon:
    # def __init__(self):

    def enter(self, player):
        print("You see...")

        input_required = True
        while input_required:
            print("What do you want to do?")
            print(
                "\t1) Inventory\t2) Look Around\t3) Attack\t4) Open chest\t5) Move\t0) Run away(leave dungeon)")

            option = int(input())

            if(option == 1):
                player.showInventory()
            elif(option == 2):
                pass
            elif(option == 3):
                pass
            elif(option == 4):
                pass
            elif(option == 5):
                pass
            elif(option == 0):
                input_required = False
        return player
