from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from shop.models import Order, OrderItem
from .product import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only = True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_total(self, obj):
        return getattr(obj, "total", None)
