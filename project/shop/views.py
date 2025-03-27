from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    category_name = request.GET.get("category")
    filter = request.GET.get("filter")
    categories = Category.objects.all()

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)

    if filter == "decrease_price":
        products=products.order_by("-price")
    elif filter == "increase_price":
        products=products.order_by("price")
    elif filter == "increase_rating":
        products = products.order_by("rating")
    elif filter == "decrease_rating":
        products = products.order_by("-rating")

    return render(request,"index.html", {"products":products,"categories": categories})


def about(request):
    return render(request, "about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "product_detail.html", {"product":product})
