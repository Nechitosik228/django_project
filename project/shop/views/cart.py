from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.shortcuts import get_object_or_404
from django.conf import settings


from shop.models import Cart, CartItem, Product
from . import CartItemSerializer, CartSerializer, ProductSerializer

@extend_schema_view(
    add=extend_schema(
        description="""
        Create a cart item
        
        - product_id: Product's id 
        """
    )
)

class CartViewSet(ViewSet):
    queryset = CartItem.objects.all()

    @action(detail=False, methods=['post'], url_path='cart-add/<int:product_id>')
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
            if _:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default = {})
            cart[str(product_id)] = cart.get(str(product_id), default=0) + 1
        return Response({'message':f'Product with id {product_id} has been added'}, status=200)

    @action(detail=False, methods=['get'], url_path='cart-items')
    def detail(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            return Response(CartSerializer(cart).data)
        else:
           cart = request.session.get(settings.CART_SESSION_ID, default = {}) 
           products = Product.objects.filter(id__in=cart.keys())
           cart_items = []
           cart_total = 0
           for product in products:
               data = ProductSerializer(product).data
               amount = cart.get(str(product.id))
               item_total = product.discount_price * amount

               cart_total += item_total
               cart_items.append({
                   'product': data,
                   'cart':None,
                   'item_total':item_total,
                   'amount':amount
               })

        return Response({
            'user':request.user,
            'items': cart_items,
            'created_at': None,
            'total': cart_total
        })