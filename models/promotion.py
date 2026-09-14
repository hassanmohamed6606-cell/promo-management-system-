from dataclasses import dataclass
from .discount import discount_from_dict

@dataclass
class Promotion:
    id: int
    name: str
    product_id: int
    discount_type: str
    discount_value: float
    start_date: str
    end_date: str
    active: bool = True

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(int(data["id"]), data["name"], int(data["product_id"]), data["discount_type"], float(data["discount_value"]), data["start_date"], data["end_date"], data.get("active", True))

    def discount(self):
        return discount_from_dict({"type": self.discount_type, "value": self.discount_value})