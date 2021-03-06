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
                    if(not room.hasEnemies()):
                        fight = False

                    print("You see the following enemies:")
                    room.showEnemies()

                    print(f"\nYou have {player.health} health.")
                    print("Which enemy would you like to attack?")

                    selected_enemy = input("> ")

                    try:
                        selected_enemy = int(selected_enemy)
                    except:
                        pass

                    if(isinstance(selected_enemy, int)):
                        if(0 < selected_enemy <= len(room.enemies)):
                            external_fighters = [player]

                            if(game.bonus_tasks and game.player.hasMercenary()):
                                external_fighters.append(game.player.mercenary)

                            fighters = external_fighters + room.enemies
                            fighters = reversed(sorted(fighters, key=lambda fighter: fighter.speed))
                            selected_enemy = room.enemies[selected_enemy-1]

                            for fighter in fighters:

                                if(isinstance(fighter, Enemy)):
                                    if(fighter.alive()):
                                        if(game.bonus_tasks):

                                            player = game.player
                                            if(player.hasMercenary()):
                                                if(player.health < player.mercenary.health and player.mercenary.alive()):
                                                    game = fighter.attackMercenary(game)
                                                else:
                                                    game = fighter.attackPlayer(game)
                                            else:
                                                game = fighter.attackPlayer(game)
                                        else:
                                            game = fighter.attackPlayer(game)

                                        player = game.player

                                        if(not player.alive()):
                                            player.respawn()
                                            fight = False
                                            dungeon = False
                                            break

                                else:
                                    if(fighter == game.player):
                                        room.updateEnemy(
                                            player.attackEnemy(selected_enemy))

                                    else:
                                        enemy = room.getFirstEnemy()

                                        if(enemy != None and game.player.hasMercenary() and game.player.mercenary.alive()):
                                            enemy, player = fighter.mercenaryAttackEnemy(enemy, player)
                                            room.updateEnemy(enemy)

                            if(not room.hasEnemies()):
                                print("All enemies defeated.\nYou are alone in this room.")
                                fight = False
                    else:
                        print(f"Please input a positive integer between 1 and {len(room.enemies)}")

                if(game.bonus_tasks and "mercenary" in player.__dict__ and player.mercenary != None):
                    player.gold -= player.mercenary.gold
                    print(f"You paid {player.mercenary.name.title()} a wage of {player.mercenary.gold} gold.")

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
            if(self.current_room == (len(self.rooms)-1)):
                self.rooms.extend(self.generateRooms(4))

            self.current_room += 1

            if(self.getRoom().hasEnemies()):
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

    # def generateAdvancedRooms(self):
    #     rooms = []
    #     for row in range(5):
    #         rooms_row = []
    #         for col in range(5):
    #             if(random.randint(0, 100) < 70):
    #                 rooms_row.append("#")
    #             else:
    #                 rooms_row.append(" ")

    #         rooms.append(rooms_row)

    #     # rooms[2][2] = "x"
    #     # print(self.chechSoroundingRooms(rooms, 2, 2))
    #     for y in range(len(rooms)):
    #         for x in range(len(rooms[y])):
    #             mask = self.chechSoroundingRooms(rooms, x, y)

    #             valid_masks = [
    #                 0b10000000,
    #                 0b00100000,
    #                 0b00001000,
    #                 0b00000010,
    #             ]

    #             has_neighbour = 0

    #             for position in valid_masks:
    #                 if(mask & position == position):
    #                     has_neighbour += 1

    #             print(f"X: {x}, Y: {y} : {has_neighbour}")
    #             # print(mask)

    #     for i in rooms:
    #         print(i)
    #     return rooms

    # def chechSoroundingRooms(self, rooms, x, y):
    #     mask = 0b11111111

    #     #   8 1 2
    #     #   7 x 3
    #     #   6 5 4

    #     # 0 = start der bitmakse

    #     x_max = len(rooms[0])-1
    #     y_max = len(rooms)-1

    #     for i in [-1, 0, 1]:
    #         for j in [-1, 0, 1]:
    #             x_ = x+j
    #             # 00 ist rechts oben
    #             y_ = y-i
    #             if(x_ < 0):
    #                 # left doesn't exist
    #                 mask = mask & 0b11111000
    #             elif(x_ > x_max):
    #                 # right doesn't exist
    #                 mask = mask & 0b10001111

    #             if(y_ < 0):
    #                 # bottom doesn't exist
    #                 mask = mask & 0b00111110
    #             elif(y_ > y_max):
    #                 # top don't exitst
    #                 mask = mask & 0b11100011

    #             if(x_ <= x_max and x_ >= 0):
    #                 if(y_ <= y_max and y_ >= 0):
    #                     if(rooms[y_][x_] != "#"):
    #                         if(j == 0 and i == 1):
    #                             mask = mask & 0b01111111
    #                         elif(j == 1 and i == 1):
    #                             mask = mask & 0b10111111
    #                         elif(j == 1 and i == 0):
    #                             mask = mask & 0b11011111
    #                         elif(j == 1 and i == -1):
    #                             mask = mask & 0b11101111
    #                         elif(j == 0 and i == -1):
    #                             mask = mask & 0b11110111
    #                         elif(j == -1 and i == -1):
    #                             mask = mask & 0b11111011
    #                         elif(j == -1 and i == 0):
    #                             mask = mask & 0b11111101
    #                         elif(j == -1 and i == 1):
    #                             mask = mask & 0b11111110

    #     # return str(bin(mask))[2:].rjust(8, "0")
    #     return mask
