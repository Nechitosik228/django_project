from django.urls import path
from .views import home, about, product_details, cart_add, cart_detail_view, cart_delete


app_name = "shop"

urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("product/<int:product_id>/", product_details, name="product_details"),
    path("cart_add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart_detail/", cart_detail_view, name="cart_detail"),
    path('cart_delete/<int:product_id>/', cart_delete, name="cart_delete")
]
