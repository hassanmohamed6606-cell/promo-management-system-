"""Optional demo data. Run once if you want sample products/promotions."""
from services.product_service import ProductService
from services.promotion_service import PromotionService
p=ProductService()
if not p.products:
    a=p.add("Paper Cups 12oz","Packaging",5,1000)
    b=p.add("Cling Film","Packaging",350,40)
    c=p.add("Tomato Sauce Sachet","Food",650,25)
    PromotionService().add("Weekend Cup Blast",a.id,"percentage",10,"2026-01-01","2099-12-31")
    PromotionService().add("Cling Film Saver",b.id,"fixed",50,"2026-01-01","2099-12-31")
    print("Demo data added.")
else:
    print("Products already exist.")
