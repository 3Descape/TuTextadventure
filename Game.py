import json
from External.json_serialization import CustomDecoder
from Assets.Player import Player


class Game:
    def __init__(self, **kwargs):
        self.savefile = ""
        self.player = ""
        self.gameloop = True

        self.__dict__.update(kwargs)

    def stop(self):
        self.gameloop = False

    def initialize(self):
        self.player = Player.character_setup()

    def load(self):
        decoder = CustomDecoder()
        data = open(self.savefile, "r").read()
        decoded = decoder.decode(data)
        self.player = decoded["player"]

    def save(self):
        file = open(self.savefile, "w")
        json.dump({"player": self.player.tojson()}, file)
        file.close()
        print(f"Game saved to {self.savefile}")
