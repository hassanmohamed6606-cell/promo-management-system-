from abc import ABC, abstractmethod

class Discount(ABC):
    def __init__(self, value):
        self.value = float(value)

    @abstractmethod
    def calculate(self, price, quantity=1):
        pass

    @abstractmethod
    def to_dict(self):
        pass

class PercentageDiscount(Discount):
    def calculate(self, price, quantity=1):
        return round(price * quantity * (self.value / 100), 2)

    def to_dict(self):
        return {"type": "percentage", "value": self.value}

class FixedDiscount(Discount):
    def calculate(self, price, quantity=1):
        return round(min(price * quantity, self.value), 2)

    def to_dict(self):
        return {"type": "fixed", "value": self.value}

def discount_from_dict(data):
    if data["type"] == "percentage":
        return PercentageDiscount(data["value"])
    return FixedDiscount(data["value"])