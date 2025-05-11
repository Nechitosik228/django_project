from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from shop.models import Category
from . import CategorySerializer


@extend_schema_view(
    retrieve = extend_schema(
        description='**Get details about certain category** by **id**',
    ),
)

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer