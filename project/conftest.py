import os
import pytest


import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testusertestusertestuser", password="password_test_user"
    )
    

@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        username='Admin', 
        password='Adminpasword123', 
        email='admin@gmail.com'
    )