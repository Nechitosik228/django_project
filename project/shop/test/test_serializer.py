import pytest

from shop.serializers.product import ProductSerializer
from shop.serializers.order import OrderItemSerializer, OrderSerializer
from shop.serializers.category import CategorySerializer


from .fixtures import category, product_with_discount, product, order


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
        "entity": -3,
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
    assert "category" not in serializer.data.keys()



@pytest.mark.django_db
def test_product_serializer_method_field(product_with_discount):
    serializer = ProductSerializer(product_with_discount)

    assert serializer.data['discount_price'] == product_with_discount.discount_price
    assert serializer.data['discount_price'] == 90


@pytest.mark.django_db
def test_order_serializer_read_only(order, user):
    data = {
        'user':user.id,
        'contact_name':'TEST_NAME',
        'contact_email':'TEST@gmail.com',
        'contact_phone':'+49027499127',
        'address':'TEST_ADDRESS',
        }
    

    serializer_d = OrderSerializer(data=data)

    assert serializer_d.is_valid()
    assert 'items' not in serializer_d.data

    serializer = OrderSerializer(order)

    assert 'items' in serializer.data


@pytest.mark.django_db
def test_order_serializer_items(order, product, product_with_discount):
    serializer = OrderSerializer(order)
    items = serializer.data['items']

    assert len(items) == 2