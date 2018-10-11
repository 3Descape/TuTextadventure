from Assets.Room import Room
from Assets.Enemy import Enemy
from Assets.Chest import Chest
from Assets.Item import Item
from Assets.Store import Store


class Dungeon:
    def __init__(self):
        self.current_room = 0
        self.rooms = self.generateRooms(4)

    def enter(self, player):
        print("You see a door in front of you..")
        dungeon = True

        while dungeon:
            print("What do you want to do?\n")
            print("""
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

            room = self.rooms[self.current_room]
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
                        fighters = reversed(sorted(fighters,
                                                   key=lambda fighter: fighter.speed))
                        selected_enemy = room.enemies[selected_enemy-1]

                        for fighter in fighters:
                            if(isinstance(fighter, Enemy)):

                                if(fighter.alive()):
                                    player = fighter.attackPlayer(player)

                                    if(not player.alive()):
                                        player.respawn()
                                        fight = False
                                        dungeon = False
                                        break
                            else:
                                room.updateEnemy(
                                    player.attackEnemy(selected_enemy))

                        if(not room.hasEnemies()):
                            print(
                                "All enemies defeated.\nYou are alone in this room.")
                            fight = False
                    else:
                        print(
                            f"Please input a positive integer between 1 and {len(room.enemies)}")

            elif(selected_action == 4):
                if(not room.hasEnemies()):
                    player = room.chest.collectItems(player)

                else:
                    print("Monsters are blocking your way.")
            elif(selected_action == 5):
                if(not room.hasEnemies()):

                    if(self.current_room == (len(self.rooms)-1)):
                        self.generateRooms(4)

                    self.current_room += 1
                    room = self.rooms[self.current_room]
                    if(room.hasEnemies()):
                        print("Monsters are blocking your way.")
                else:
                    print("Monsters are blocking your way.")

                pass
            elif(selected_action == 0):
                dungeon = False

            else:
                print("Invalid choice. Please try again.")

        return player

    def generateRooms(self, count):
        rooms = []
        rat = Enemy(name="Rat", health=30, attack=10,
                    defense=15, speed=50, reward=[1, 5])
        gnoll = Enemy(name="Gnoll", health=60, attack=30,
                      defense=40, speed=20, reward=[5, 10])
        wolf = Enemy(name="Wolf", health=40, attack=25,
                     defense=30, speed=60, reward=[10, 15])

        item = Item({"name": "potion", **(Store.stores["druid"]["items"]["potion"])})
        chest_empty = Chest([])
        chest = Chest([item])

        for i in range(self.current_room, self.current_room + count):
            if (i % 2 == 0):
                rooms.append(Room([rat.copy(), gnoll.copy()], chest_empty))
            else:
                rooms.append(Room([wolf.copy(), rat.copy()], chest))
        return rooms
