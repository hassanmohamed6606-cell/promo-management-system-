from dataclasses import dataclass
from datetime import datetime

@dataclass
class Sale:
    id: int
    staff_username: str
    customer_name: str
    product_id: int
    quantity: int
    original_total: float
    discount_total: float
    final_total: float
    promotion_id: int | None
    created_at: str

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def create(cls, sale_id, staff, customer, product_id, quantity, original, discount, final, promotion_id=None):
        return cls(sale_id, staff, customer, product_id, quantity, round(original,2), round(discount,2), round(final,2), promotion_id, datetime.now().isoformat(timespec="seconds"))

    @classmethod
    def from_dict(cls, data):
        return cls(**data)