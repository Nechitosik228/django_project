from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAdminUser, AllowAny

from . import ProductSerializer
from ..filters import ProductFilter
from shop.models import Product, Category


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
        description='**Get details about certain product** by **id**',
    ),
    create = extend_schema(
        description="""
        Create a product with this information: 

        - name: Product's name (required, max-length=100) 

        - description: Product's description (not required) 

        - entity: Product's entity. Must not be less than 0 (not required, default=0) 
        
        - price: Product's price (required, max-digits=7, decimal-places=2) 
        
        - available: Product's availability (True or False, default=True) 
        
        - nomenclature: Product's nomenclature (unique=True) 
        
        - rating: Product's rating (default=0.0) 
        
        - discount: Product's discount (default=0) 
        
        - attributes: Product's attributes (default=dict)"""
    ),
    update = extend_schema(
        description="""
        - id: Product's id

        Update a product with this information: 

        - name: New product's name (required, max-length=100) 

        - description: New product's description (not required) 

        - entity: New product's entity. Must not be less than 0 (not required, default=0) 
        
        - price: New product's price (required, max-digits=7, decimal-places=2) 
        
        - available: New product's availability (True or False, default=True) 
        
        - nomenclature: New product's nomenclature (unique=True) 
        
        - rating: New product's rating (default=0.0) 
        
        - discount: New product's discount (default=0) 
        
        - attributes: New product's attributes (default=dict)"""
    ),
    destroy = extend_schema(
        description='Delete a product by **id**',
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'rating']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAdminUser()]
        else:
          return [AllowAny()]  
