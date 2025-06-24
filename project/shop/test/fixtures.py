import pytest

from shop.models import Category, Product, Order, OrderItem


@pytest.fixture
def category():
    return Category.objects.create(
        name="test_category"
    )

@pytest.fixture
def product(category):
    return Product.objects.create(
        name="test-product", 
        category=category,
        nomenclature="test_nomenclature", 
        price=100, 
    )

@pytest.fixture
def product_with_discount(category):
    return Product.objects.create(
        name="test_product", 
        category=category,
        nomenclature="test-nomenclature", 
        price=100,
        discount=10
    )

@pytest.fixture
def order(product_with_discount, product):
    order_ = Order.objects.create(
        contact_name="test_name", 
        contact_email="example@example.com",
        contact_phone="+380663831118", 
        address="5 Avenue",
    )

    OrderItem.objects.create(
        order = order_,
        product = product_with_discount,
        price = product_with_discount.discount_price
    )

    OrderItem.objects.create(
        order = order_,
        product = product,
        price = product.discount_price
    )

    return order_