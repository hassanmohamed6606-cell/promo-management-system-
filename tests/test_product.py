from models.product import Product

def test_product_to_dict():
    p=Product(1,"Paper Cups","Packaging",5,100)
    assert p.to_dict()["name"] == "Paper Cups"
    assert p.stock == 100