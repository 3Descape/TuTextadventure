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
        print("gravedigger_items" in decoded)
        print(bonus_tasks)
        if(bonus_tasks):
            self.enableBonusTasks()
            if("gravedigger_items" in decoded):
                self.gravedigger_items = decoded["gravedigger_items"]

    def save(self):
        file = open(self.savefile, "w")
        data = {
            "player": self.player.tojson()
        }

        if(self.bonus_tasks):
            encoder = CustomEncoder()
            data["gravedigger_items"] = [encoder.default(item) for item in self.gravedigger_items]

        json.dump(data, file)
        file.close()
        print(f"Game saved to {self.savefile}")

    def enableBonusTasks(self):
        self.bonus_tasks = True
        self.gravedigger_items = []
