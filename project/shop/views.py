from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages

from .models import Product, Category, Cart, CartItem, OrderItem, Order, Payment
from .forms import OrderCreateForm
from utils import send_order_confirmation_email


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


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = request.user.cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect("shop:cart_detail")


def cart_detail_view(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        total_price = 0
        for product in products:
            amount = cart[str(product.id)]
            if product.discount:
                raw_price = product.discount_price
            else:
                raw_price = product.price
            price = amount * raw_price
            total_price += price
            cart_items.append({"product": product, "amount": amount, "price": price})
    else:
        try:
            cart = request.user.cart

        except Cart.DoesNotExist:
            cart = None

        if not cart or not cart.items.count():
            cart_items = []
            total_price = 0
        else:
            cart_items = cart.items.select_related("product").all()
            total_price = 0
            for item in cart_items:
                product = item.product
                total_price += item.item_total

    return render(
        request,
        "cart_detail.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def checkout(request):
    if (request.user.is_authenticated and not getattr(request.user, "cart", None)) or (
        not request.user.is_authenticated
        and not request.sesion.get(settings.CART_SESSION_ID)
    ):
        messages.error(request, "Carty is empty")
        return redirect("shop:cart_detail")
    if request.method == "GET":
        form = OrderCreateForm()
        if request.user.is_authenticated:
            form.initial["contact_email"] = request.user.email
    elif request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            if request.user.is_authenticated:
                cart = getattr(request.user, "cart")
                cart_items = cart.items.select_related("product").all()
            else:
                cart = request.session.get(settings.CART_SESSION_ID)
                cart_items = []
                for product_id, amount in cart.items():
                    product = Product.objects.get(id=product_id)
                    cart_items.append({"product": product, "amount": amount})
            items = OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=item.product,
                        amount=item.amount,
                        price=item.product.discount_price
                    )
                    for item in cart_items
                ]
            )
            total_price = sum(i.product.discount_price*i.amount for i in items)
            method = form.cleaned_data.get('payment_method')
            if method != 'cash':
                Payment.objects.create(order=order, provider=method, amount=total_price)
            order.status = 2
            order.save()

            if request.user.is_authenticated:
                cart.items.all().delete()
            else:
                request.session[settings.CART_SESSION_ID] = {}

            send_order_confirmation_email(order, total_price)
            messages.success(request, 'You have completed your order!') 
            return redirect('shop:home')
    return render(request, "checkout.html", {"form": form})


def cart_delete(request, product_id:int):
    product = get_object_or_404(Product, id=product_id)
    product_key = str(product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        cart[product_key] -= 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = request.user.cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount -= 1
            if cart_item.amount == 0:
                cart_item.delete()
            else:
                cart_item.save()
    return redirect("shop:cart_detail")



