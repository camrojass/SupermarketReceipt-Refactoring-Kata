from sre_constants import ASSERT
import pytest 

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller

from tests.fake_catalog import FakeCatalog

def test_SingleProduct_NoDiscount():
    qty = 5
    price = 2.99
    #ARRANGE
    catalog = FakeCatalog()
    oranges = Product("oranges", ProductUnit.KILO)
    catalog.add_product(oranges, price)
    teller = Teller(catalog)
    

    #ACT
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, oranges, 5.0)
    
    cart = ShoppingCart()
    cart.add_item_quantity(oranges,qty)
    
    receipt = teller.checks_out_articles_from(cart)
    receipt_item = receipt.items[0]
    ResponseExpected = qty*price

    #ASSERT
    assert ResponseExpected == pytest.approx(receipt_item.total_price, 0.01)
    assert oranges == receipt_item.product 


def test_ten_percent_discount():
    #ARRANGE
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)   
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    teller = Teller(catalog)
    cart = ShoppingCart()

    #ACT
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    cart.add_item_quantity(apples, 3)
    receipt = teller.checks_out_articles_from(cart)
    receipt_item = receipt.items[0]
    TotalPriceExpected = 3 * 1.99

    #ASSERT
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    assert apples == receipt_item.product
    assert TotalPriceExpected == pytest.approx(receipt.total_price(), 0.01)
    assert TotalPriceExpected == pytest.approx(receipt_item.total_price, 0.01)
    
def test_teller_qty():
    #ARRANGE
    catalog = FakeCatalog()
    apples = Product("apples", ProductUnit.KILO) 
    catalog.add_product(apples, 1.99)
    cart = ShoppingCart()

    #ACT
    teller = Teller(catalog)
    cart.add_item_quantity(apples, 3)
    receipt = teller.checks_out_articles_from(cart)
    Receipt_item = receipt.items[0]
    ReceiptExpected = 3

    #ASSERT
    assert ReceiptExpected == Receipt_item.quantity