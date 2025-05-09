from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from shop.models import Product, Category
from . import ProductSerializer

@extend_schema_view(
    list = extend_schema(
        description='**Get all products**',
        parameters=[
            OpenApiParameter(
                name='category',
                type = OpenApiTypes.STR,
                description='Filter by **category**',
                examples=[
                    OpenApiExample(
                        name=f'{category}',
                        value=f'{category}'
                    ) for category in Category.objects.all()
                ],
                default=''
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                description='Order products by **price and rating**',
                examples=[
                    OpenApiExample(
                        name='No filter'
                    ),
                    OpenApiExample(
                        name='Increasing Price',
                        value='price'
                    ),
                    OpenApiExample(
                        name='Decreasing Price',
                        value='-price'
                    ),
                    OpenApiExample(
                        name='Increasing Rating',
                        value='rating'
                    ),
                    OpenApiExample(
                        name='Decreasing Rating',
                        value='-rating'
                    )
                ],
                default=''
            )
        ]
    ),
    retrieve = extend_schema(
        description='Get deatils about certain product'
    ),
    create = extend_schema(
        description='Create a product'
    ),
    update = extend_schema(
        description='Update a product'
    ),
    destroy = extend_schema(
        description='Delete a product',
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['price', 'rating']
    search_fields = []
