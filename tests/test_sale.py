from models.product import Product
from models.promotion import Promotion
from services.sale_service import SaleService

def test_sale_calculation(tmp_path, monkeypatch):
    import services.sale_service as ss
    monkeypatch.setattr(ss, "save_json", lambda *args, **kwargs: None)
    service=SaleService(); service.sales=[]
    p=Product(1,"Cups","Packaging",5,100)
    promo=Promotion(1,"10% Off",1,"percentage",10,"2026-01-01","2099-01-01")
    sale=service.create("staff","Ahmed",p,10,promo)
    assert sale.original_total == 50
    assert sale.discount_total == 5
    assert sale.final_total == 45
    assert p.stock == 90