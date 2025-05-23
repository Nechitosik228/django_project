from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django.core.exceptions import ValidationError

from shop.models import Product


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