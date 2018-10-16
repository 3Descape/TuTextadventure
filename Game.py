import json
from External.json_serialization import CustomDecoder, CustomEncoder, json_class
from Assets.Player import Player


class Game:
    def __init__(self, **kwargs):
        self.savefile = ""
        self.player = ""
        self.gameloop = True
        self.bonus_tasks = False
        self.__dict__.update(kwargs)

    def stop(self):
        self.gameloop = False

    def initialize(self):
        self.player = Player.character_setup()

    def load(self, bonus_tasks):
        decoder = CustomDecoder()
        data = open(self.savefile, "r").read()
        decoded = decoder.decode(data)
        self.player = decoded["player"]
        if("mercenary" in self.player.__dict__ and bonus_tasks == False):
            del self.player.mercenary

        if(bonus_tasks):
            self.enableBonusTasks()
            if("gravedigger_items" in decoded):
                self.gravedigger_items = decoded["gravedigger_items"]

    def save(self):
        file = open(self.savefile, "w")
        data = {
            "player": self.player.tojson(self.bonus_tasks)
        }

        if(self.bonus_tasks):
            encoder = CustomEncoder()
            if("gravedigger_items" in data):
                data["gravedigger_items"] = [encoder.default(
                    item) for item in self.gravedigger_items]

        json.dump(data, file)
        file.close()
        print(f"Game saved to {self.savefile}")

    def enableBonusTasks(self):
        self.bonus_tasks = True
        self.gravedigger_items = []
