import pytest
import uuid

from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User

from .fixtures import category, product_with_discount, product, order
from ..models import Product

@pytest.mark.django_db
def test_product_list(api_client):
    url = reverse('shop:product-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_product_list_2(api_client, product, product_with_discount):
    url = reverse('shop:product-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_product_one(api_client, product, product_with_discount):
    url = reverse('shop:products-detail', kwargs={'pk':product.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == product.name


@pytest.mark.django_db
def test_product_detail_not_found(api_client):
    url = reverse('shop:products-detail', kwargs={'pk':1435768})

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_product_update_not_authorized(api_client, product):
    url = reverse('shop:products-update', kwargs={'pk':product.id})

    response = api_client.patch(url, data={'price':200})

    assert response.status_code == 403


@pytest.mark.django_db
def test_product_update(api_client, product, super_user):
    api_client.force_authenticate(user=super_user)

    url = reverse('shop:products-update', kwargs={'pk':product.id})

    response = api_client.patch(url, data={'price':150})

    assert response.status_code == 200
    assert response.data.get('price') == 150
    assert product.price == 150


@pytest.mark.django_db
def test_product_create(api_client, category, super_user):
    api_client.force_authenticate(user=super_user)

    url = reverse('shop:products-list')

    data = {
        "name":"test-product", 
        "category":category.id,
        "nomenclature":uuid.uuid4()
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert response.data.get('name') == data.get('name')
    assert Product.objects.filter(id=response.data.get('id')).exists()


@pytest.mark.django_db
def test_product_create_not_authorized(api_client, category):
    url = reverse('shop:products-list')

    data = {
        "name":"test-product", 
        "category":category.id,
        "nomenclature":uuid.uuid4()
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 403

