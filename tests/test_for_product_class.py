import pytest
from testing_to_test import Product

@pytest.fixture
def product():
    return Product("Apple",1.5,100)

def test_subtract_quantity(product):
    product.subtract_quantity(10)
    assert product.quantity == 90

def test_add_quantity(product):
    product.add_quantity(50)
    assert product.quantity == 150

def test_change_price(product):
    product.change_price(2.0)
    assert product.price == 2.0

