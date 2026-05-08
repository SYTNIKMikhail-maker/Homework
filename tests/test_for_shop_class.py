import pytest
from testing_to_test import Product, Shop

@pytest.fixture
def product():
    return Product("Apple", 1.5, 100)


@pytest.fixture
def empty_shop():
    return Shop()

@pytest.fixture
def shop_with_product(product):
    return Shop(product)

def test_add_product(empty_shop, product):
    empty_shop.add_product(product)
    assert len(empty_shop.products) == 1

def test_sell_product(shop_with_product):
    receipt = shop_with_product.sell_product("Apple", 10)
    assert receipt == 15.0

def test_shop_money_after_sell(shop_with_product):
    shop_with_product.sell_product("Apple", 10)
    assert shop_with_product.money == 15.0

def test_product_removed_when_sold_out(shop_with_product):
    shop_with_product.sell_product("Apple", 100)
    assert len(shop_with_product.products) == 0

def test_sell_more_than_available(shop_with_product):
    with pytest.raises(ValueError):
        shop_with_product.sell_product("Apple", 999)

def test_sell_nonexistent_product(empty_shop):
    result = empty_shop.sell_product("Banana")
    assert result is None