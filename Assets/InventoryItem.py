class InventoryItem:
    def __init__(self, name, price, effected_attribute, effect_amount, usecase):
        self.name = name
        self.price = price
        self.effected_attribute = effected_attribute
        self.effect_amount = effect_amount
        self.usecase = usecase
