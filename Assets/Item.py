from External.json_serialization import json_class


@json_class
class Item:
    def __init__(self, kwargs):
        self.name = ""
        self.price = 0
        self.effected_attribute = ""
        self.effect_amount = 0
        self.usecase = ""

        self.__dict__.update(**kwargs)
