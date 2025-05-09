from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.product import ProductViewSet
from .views.category import CategoryViewSet
from .views.cart import CartViewSet
from .views.views import (
    home,
    about,
    product_details,
    cart_add,
    cart_detail_view,
    cart_delete,
    checkout,
)


app_name = "shop"


router = DefaultRouter()

router.register(prefix=r'products', viewset=ProductViewSet)
router.register(prefix=r'categories', viewset=CategoryViewSet)
router.register(prefix=r'cart', viewset=CartViewSet)


urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("product/<int:product_id>/", product_details, name="product_details"),
    path("cart/cart-add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart_detail/", cart_detail_view, name="cart_detail"),
    path("cart_delete/<int:product_id>/", cart_delete, name="cart_delete"),
    path("order/checkout/", checkout, name="checkout"),
]

urlpatterns += router.urls
