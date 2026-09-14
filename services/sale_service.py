from models.sale import Sale
from utils.storage import load_json, save_json

class SaleService:
    FILE="sales.json"
    def __init__(self): self.sales=[Sale.from_dict(x) for x in load_json(self.FILE)]
    def _save(self): save_json(self.FILE,[s.to_dict() for s in self.sales])
    def next_id(self): return max([s.id for s in self.sales], default=0)+1
    def create(self,staff,customer,product,quantity,promotion=None):
        original=product.price*quantity
        discount=promotion.discount().calculate(product.price,quantity) if promotion else 0
        final=max(0,original-discount)
        product.stock -= quantity
        sale=Sale.create(self.next_id(),staff,customer,product.id,quantity,original,discount,final,promotion.id if promotion else None)
        self.sales.append(sale); self._save(); return sale
    def total_revenue(self): return round(sum(s.final_total for s in self.sales),2)
    def total_discounts(self): return round(sum(s.discount_total for s in self.sales),2)