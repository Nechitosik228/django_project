import os
import pytest
from django.contrib.auth.models import User

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testusertestusertestuser", password="password_test_user"
    )
    