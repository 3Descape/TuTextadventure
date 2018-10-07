from Assets.Room import Room
from Assets.Enemy import Enemy
from Assets.Chest import Chest
from Assets.InventoryItem import InventoryItem

from Globals import *


class Dungeon:
    def __init__(self):
        self.rooms = self.generateRooms(5)
        self.current_room = 0

    def enter(self, player):
        print("You see a door in front of you..")

        dungeon = True
        while dungeon:
            print("What do you want to do?\n")
            print(
                "\t1) Inventory\n\t2) Look Around\n\t3) Attack\n\t4) Open chest\n\t5) Move\n\t0) Run away (leave dungeon)\n")

            option = input("> ")
            try:
                option = int(option)
            except:
                pass

            if(option == 1):
                player.showInventory()
            elif(option == 2):
                # //TODO: Add meaningful description
                print("Some description in here")
            elif(option == 3):
                fight = True
                while fight:
                    print("You see the following enemies:")
                    room = self.rooms[self.current_room]
                    room.showEnemies()
                    print(f"\nYou have {player.health} health.")
                    selected_enemy = int(
                        input("Which enemy would you like to attack?\n >"))

                    if(0 < selected_enemy <= len(room.enemies)):
                        fighters = [player] + room.enemies
                        fighters = reversed(sorted(fighters,
                                                   key=lambda fighter: fighter.speed))

                        selected_enemy = room.enemies[selected_enemy-1]

                        print(selected_enemy.name)
                        for fighter in fighters:
                            if(isinstance(fighter, Enemy)):
                                player = fighter.attackPlayer(player)
                                if(not player.alive):
                                    fight = False
                                    dungeon = False
                                    break
                            else:
                                fighter = player.attackEnemy(selected_enemy)
                                room.updateEnemy(fighter)
                    else:
                        print(
                            f"Please input a positive integer between 1 and {len(room.enemies)}")
            elif(option == 4):
                pass
            elif(option == 5):
                pass
            elif(option == 0):
                dungeon = False
            else:
                print("Invalid choice. Please try again.")
        return player

    def generateRooms(self, count):
        rooms = []
        rat = Enemy("Rat", 30, 10, 15, 50, [1, 5])
        gnoll = Enemy("Gnoll", 60, 30, 40, 20, [5, 10])
        wolf = Enemy("Wolf", 40, 25, 30, 60, [10, 15])

        chest_empty = Chest([])
        chest = Chest([
            InventoryItem("Potion", 0, EFFECT_HEALTH, 10, "held")
        ])
        for i in range(count):
            if i % 2 == 0:
                rooms.append(Room([rat, gnoll], chest_empty))
            else:
                rooms.append(Room([wolf, rat], chest))
        return rooms
