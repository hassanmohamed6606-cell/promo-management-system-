from models.product import Product
from utils.storage import load_json, save_json
from utils.validators import non_empty, positive_float, non_negative_int

class ProductService:
    FILE = "products.json"
    def __init__(self):
        self.products = [Product.from_dict(x) for x in load_json(self.FILE)]
    def _save(self): save_json(self.FILE, [p.to_dict() for p in self.products])
    def next_id(self): return max([p.id for p in self.products], default=0) + 1
    def add(self, name, category, price, stock):
        p = Product(self.next_id(), non_empty(name,"Name"), non_empty(category,"Category"), positive_float(price,"Price"), non_negative_int(stock,"Stock"))
        self.products.append(p); self._save(); return p
    def get(self, pid): return next((p for p in self.products if p.id == int(pid)), None)
    def update(self, pid, name, category, price, stock):
        p = self.get(pid)
        if not p: raise ValueError("Product not found.")
        p.name=non_empty(name,"Name"); p.category=non_empty(category,"Category"); p.price=positive_float(price,"Price"); p.stock=non_negative_int(stock,"Stock"); self._save(); return p
    def delete(self, pid):
        p=self.get(pid)
        if not p: raise ValueError("Product not found.")
        self.products.remove(p); self._save()