import pytest

import pytest_check as check
from shop.serializers.product import ProductSerializer

from .test.fixtures import category, product_with_discount, product, order
from .models import Product, CartItem, Category, OrderItem

@pytest.mark.django_db
def test_product_serializer_valid(category):
    data = {
        "name": "test_name",
        "description": "test_description",
        "stock":3,
        "price":100,
        "available": True,
        "category": category,
        "nomenclature":"test_nomenclature",
        "rating":2,
        "discount":10,
        "attributes": {}
    }
    
    serializer = ProductSerializer(data=data)
    
    assert serializer.is_valid()
    
@pytest.mark.django_db
def test_product_serializer_invalid(category):
    data = {
        "name": "*"*101,
        "description": {},
        "stock": -3,
        "price":-100,
        "available": 2,
        "nomenclature":"*"*101,
        "rating":"*",
        "discount":-10,
        "attributes": "*"
    }
    
    

    serializer = ProductSerializer(data=data)
    
    
    assert not serializer.is_valid()
    assert serializer.errors
    assert 'Ensure this field has no more than 100 characters.' in serializer.errors["name"]
    assert 'Must be a valid boolean.' in serializer.errors["available"]
    assert 'Ensure this field has no more than 50 characters.' in serializer.errors["nomenclature"]
    assert 'A valid number is required.' in serializer.errors["rating"]
    for field in data.keys():
        assert field in serializer.errors
    

@pytest.mark.django_db
def test_product_serializer_read_only(category):
    data = {
        "name": "test_name",
        "description": {},
        "stock": 3,
        "price":100,
        "available": 1,
        "category" : category,
        "nomenclature":"nomenclature",
        "rating":4.9,
        "discount":10,
        "attributes": []
    }

    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()
    assert "category" not in serializer.data


AMOUNT = 10

@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(
        name="test_category"
    )
    product = Product.objects.create(
        name="test_product", 
        category=category,
        nomenclature="test_nomenclature", 
        price=100, 
        discount=10
    )
    
    assert product.discount_price == 90
    assert product.category.name == "test_category"
    
@pytest.mark.django_db
def test_cart_model_one_product(user, product):
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product,
    )
    
    assert user.cart.total == product.price
    assert cart_item.item_total == product.price
        
@pytest.mark.django_db
def test_cart_model_multiple_products(user, product):
    
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product,
        amount=10,
    )
    
    assert user.cart.total == product.price * AMOUNT
    assert cart_item.item_total == product.price * AMOUNT
    
@pytest.mark.django_db
def test_cart_model_discount_product(user, product_with_discount):
    
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_with_discount,
    )
    
    assert user.cart.total == product_with_discount.discount_price
    assert cart_item.item_total == product_with_discount.discount_price
    
@pytest.mark.django_db
def test_cart_model_discount_multiple_products(user, product_with_discount):
    
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_with_discount,
        amount=10,
    )
    
    assert user.cart.total == product_with_discount.discount_price * AMOUNT
    assert cart_item.item_total == product_with_discount.discount_price * AMOUNT
    
@pytest.mark.django_db
def test_cart_model_diffrent_products(user, product_with_discount, product):
    
    cart_item = CartItem.objects.create(
        cart=user.cart,
        product=product_with_discount,
    )
    
    cart_item_2 = CartItem.objects.create(
        cart=user.cart,
        product=product,
    )
    
    assert user.cart.total == 190

@pytest.mark.django_db
def test_order_model_one_item(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, price=product.price
    )

    assert order_item.amount == 1
    assert order_item.item_total == product.price


@pytest.mark.django_db
def test_order_model_multiple_items(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, amount=10, price=product.price
    )

    assert order_item.amount == 10
    assert order_item.item_total == product.price * 10


@pytest.mark.django_db
def test_order_model_discount_item(order, product_with_discount):
    order_item = OrderItem.objects.create(
        order=order, product=product_with_discount, price=product_with_discount.price
    )

    assert order_item.item_total == 90


@pytest.mark.django_db
def test_order_model_different_items(order, product_with_discount, product):

    order_item_1 = OrderItem.objects.create(
        order=order, product=product, price=product.price
    )

    order_item_2 = OrderItem.objects.create(
        order=order, product=product_with_discount, price=product_with_discount.price
    )

    assert order_item_1.item_total + order_item_2.item_total == 190