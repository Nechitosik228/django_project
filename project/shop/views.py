from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_name = request.GET.get("category")
    filter = request.GET.get("filter")
    search = request.GET.get("search")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if search:
        products = products.filter(name__icontains=search)

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if start_date:
        products = products.filter(created_at__gte=start_date)
    if end_date:
        products = products.filter(created_at__lte=end_date)

    if filter == "decrease_price":
        products = products.order_by("-price")
    elif filter == "increase_price":
        products = products.order_by("price")
    elif filter == "increase_rating":
        products = products.order_by("rating")
    elif filter == "decrease_rating":
        products = products.order_by("-rating")

    length = len(products)

    return render(
        request,
        "index.html",
        {"products": products, "categories": categories, "length": length},
    )


def about(request):
    return render(request, "about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "product_detail.html", {"product": product})
