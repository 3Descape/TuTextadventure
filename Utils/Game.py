import json

from External.json_serialization import CustomDecoder


def saveGame(savefile, player):
    file = open(savefile, "w")
    json.dump({"player": player.tojson()}, file)
    file.close()


def loadGame(savefile):
    decoder = CustomDecoder()
    data = open(savefile, "r").read()
    return decoder.decode(data)
