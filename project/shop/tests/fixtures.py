import pytest

from shop.models import Category, Product, Order


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
def order():
    return Order.objects.create(
        contact_name="test_name", 
        contact_email="example@example.com",
        contact_phone="+380663831118", 
        address="5 Avenue",
    )