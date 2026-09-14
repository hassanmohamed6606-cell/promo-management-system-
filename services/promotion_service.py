from datetime import date
from models.promotion import Promotion
from utils.storage import load_json, save_json
from utils.validators import non_empty, positive_float, percentage

class PromotionService:
    FILE="promotions.json"
    def __init__(self): self.promotions=[Promotion.from_dict(x) for x in load_json(self.FILE)]
    def _save(self): save_json(self.FILE,[p.to_dict() for p in self.promotions])
    def next_id(self): return max([p.id for p in self.promotions], default=0)+1
    def add(self,name,product_id,dtype,value,start,end):
        if dtype == "percentage": value=percentage(value)
        else: value=positive_float(value,"Discount")
        if start > end: raise ValueError("Start date must be before end date.")
        p=Promotion(self.next_id(),non_empty(name,"Promotion name"),int(product_id),dtype,value,start,end,True)
        self.promotions.append(p); self._save(); return p
    def get(self,pid): return next((p for p in self.promotions if p.id==int(pid)),None)
    def active_for_product(self, product_id):
        today=date.today().isoformat()
        return [p for p in self.promotions if p.product_id==int(product_id) and p.active and p.start_date<=today<=p.end_date]
    def toggle(self,pid):
        p=self.get(pid)
        if not p: raise ValueError("Promotion not found.")
        p.active=not p.active; self._save(); return p
    def delete(self,pid):
        p=self.get(pid)
        if not p: raise ValueError("Promotion not found.")
        self.promotions.remove(p); self._save()