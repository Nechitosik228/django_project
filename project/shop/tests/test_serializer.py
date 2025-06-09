import pytest

import pytest_check as check
from shop.serializers.product import ProductSerializer

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
    