from External.json_serialization import json_class


@json_class
class Item:
    def __init__(self, kwargs):
        self.name = ""
        self.price = 0
        self.effects = []
        self.usecase = ""

        self.__dict__.update(**kwargs)

    def prefix(self, effect):
        return "+" if effect["effect_amount"] > 0 else ""

    def effectDescription(self):
        last_index = len(self.effects) - 1
        effect_description = ""

        for (index, effect) in enumerate(self.effects):
            effect_description = effect_description + (self.prefix(effect) + str(effect["effect_amount"]) + " " + effect["effected_attribute"])
            if(index != last_index):
                effect_description = effect_description + ", "

        return effect_description
