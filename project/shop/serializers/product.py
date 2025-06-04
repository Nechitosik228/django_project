from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django.core.exceptions import ValidationError

from shop.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "entity",
            "price",
            "available",
            "category",
            "nomenclature",
            "created_at",
            "rating",
            "discount",
            "attributes",
            "discount_price",
        ]

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_discount_price(self, obj):
        return obj.discount_price
    
    def clean_price(self, value):
        if value <= 0:
            return ValidationError('The price should be higher than 0')
        else:
            return value
            
    def clean_stock(self, value):
        if value < 0:
            return serializers.ValidationError('The stock should be higher than 0')
        else:
            return value
    
    def clean_description(self, value):
        if isinstance(value,str):
            return value
        else:
            return serializers.ValidationError('Description must be text')
    
    def clean_category(delf, value):
        if not (isinstance(value, int)) or not (isinstance(value, Category)):
            return serializers.ValidationError("Category must be int or Category instance")