from Assets.Room import Room
from Assets.Enemy import Enemy
from Assets.Chest import Chest
from Assets.Item import Item
from Assets.Store import Store

import random


class Dungeon:
    def __init__(self):
        self.current_room = 0
        self.rooms = self.generateRooms(4)

    def enter(self, game):
        if(game.bonus_tasks):
            self.rooms = self.generateAdvancedRooms()
        else:
            self.rooms = self.generateRooms(4)

        player = game.player
        print("You see a door in front of you..")
        dungeon = True

        while dungeon:
            print("""What do you want to do?

    1) Inventory
    2) Look Around
    3) Attack
    4) Open chest
    5) Move
    0) Run away (leave dungeon)
                """)

            selected_action = input("> ")
            try:
                selected_action = int(selected_action)
            except:
                pass

            room = self.getRoom()
            if(selected_action == 1):
                player.showInventory()

            elif(selected_action == 2):
                print("You see a room.")

            elif(selected_action == 3):
                fight = True

                while fight:
                    print("You see the following enemies:")
                    room.showEnemies()

                    print(f"\nYou have {player.health} health.")
                    print("Which enemy would you like to attack?")

                    selected_enemy = int(input("> "))

                    if(0 < selected_enemy <= len(room.enemies)):
                        fighters = [player] + room.enemies
                        fighters = reversed(sorted(fighters, key=lambda fighter: fighter.speed))
                        selected_enemy = room.enemies[selected_enemy-1]

                        for fighter in fighters:
                            if(isinstance(fighter, Enemy)):

                                if(fighter.alive()):
                                    game.player = player
                                    game = fighter.attackPlayer(game)
                                    player = game.player

                                    if(not player.alive()):
                                        player.respawn()
                                        fight = False
                                        dungeon = False
                                        break

                            else:
                                room.updateEnemy(
                                    player.attackEnemy(selected_enemy))

                        if(not room.hasEnemies()):
                            print("All enemies defeated.\nYou are alone in this room.")
                            fight = False
                    else:
                        print(f"Please input a positive integer between 1 and {len(room.enemies)}")

            elif(selected_action == 4):
                if(not room.hasEnemies()):
                    player = room.chest.collectItems(player)
                else:
                    print("Monsters are blocking your way.")

            elif(selected_action == 5):
                self.move(game)

            elif(selected_action == 0):
                dungeon = False

            else:
                print("Invalid choice. Please try again.")
        game.player = player
        return game

    def getRoom(self):
        return self.rooms[self.current_room]

    def move(self, game):
        room = self.getRoom()

        if(not room.hasEnemies()):
            if(game.bonus_tasks):
                pass
            else:
                if(self.current_room == (len(self.rooms)-1)):
                    self.generateRooms(4)

                self.current_room += 1
                room = self.rooms[self.current_room]

                if(room.hasEnemies()):
                    print("Monsters are blocking your way.")

        else:
            print("Monsters are blocking your way.")

    def generateRooms(self, count):
        rooms = []
        rat = Enemy(name="Rat", health=30, attack=10, defense=15, speed=50, reward=[1, 5])
        gnoll = Enemy(name="Gnoll", health=60, attack=30, defense=40, speed=20, reward=[5, 10])
        wolf = Enemy(name="Wolf", health=40, attack=25, defense=30, speed=60, reward=[10, 15])

        chest_empty = Chest([])
        item = Item({"name": "potion", **(Store.stores["druid"]["items"]["potion"])})
        chest = Chest([item])

        for i in range(self.current_room, self.current_room + count):
            if (i % 2 == 0):
                rooms.append(Room([rat.copy(), gnoll.copy()], chest_empty))
            else:
                rooms.append(Room([wolf.copy(), rat.copy()], chest))
        return rooms

    def generateAdvancedRooms(self):
        rooms = []
        for row in range(5):
            rooms_row = []
            for col in range(5):
                if(random.randint(0, 100) < 70):
                    rooms_row.append("#")
                else:
                    rooms_row.append(" ")

            rooms.append(rooms_row)

        rooms[0][0] = "x"
        print(self.chechSoroundingRooms(rooms, 0, 0))
        # for y in range(len(rooms)-1):
        #     for x in range(len(rooms[y])-1):
        #         mask = self.chechSoroundingRooms(rooms, x, y)
        #         print(f"X: {x}, Y: {y}")
        #         print(mask)
        # rooms[x][y] = str(x) + ", " + str(y)

        for i in rooms:
            print(i)
        return rooms

    def chechSoroundingRooms(self, rooms, x, y):
        mask = 0b11111111

        #   8 1 2
        #   7 x 3
        #   6 5 4

        # 0 = start der bitmakse

        x_max = len(rooms[0])-1
        y_max = len(rooms)-1

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                x_ = x+j
                # 00 ist rechts oben
                y_ = y-i

                if(x_ < 0):
                    # left doesn't exist
                    mask = mask & 0b11111000
                elif(x_ > x_max):
                    # right doesn't exist
                    mask = mask & 0b10001111

                if(y_ < 0):
                    # bottom doesn't exist
                    mask = mask & 0b11100011
                elif(y_ > y_max):
                    # top don't exitst
                    mask = mask & 0b00111110

                if(x_ <= x_max and x_ >= 0):
                    if(y_ <= y_max and y_ >= 0):
                        if(rooms[y_][x_] != "#"):
                            if(j == 0 and i == 1):
                                mask = mask & 0b01111111
                            elif(j == 1 and i == 1):
                                mask = mask & 0b10111111
                            elif(j == 1 and i == 0):
                                mask = mask & 0b11011111
                            elif(j == 1 and i == -1):
                                mask = mask & 0b11101111
                            elif(j == 0 and i == -1):
                                mask = mask & 0b11110111
                            elif(j == -1 and i == -1):
                                mask = mask & 0b11111011
                            elif(j == -1 and i == 0):
                                mask = mask & 0b11111101
                            elif(j == -1 and i == 1):
                                mask = mask & 0b11111110

        return str(bin(mask))[2:].rjust(8, "0")
