from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category
from . import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer