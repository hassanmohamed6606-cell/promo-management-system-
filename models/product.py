from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    stock: int

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(int(data["id"]), data["name"], data.get("category", "General"), float(data["price"]), int(data["stock"]))