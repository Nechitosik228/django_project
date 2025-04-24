from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from .forms import RegisterForm, ProfileUpdateForm
from .models import Profile
from shop.models import Cart, CartItem, Product

# not a view
def send_confirmation_email(request, user, email, confirm_view:str):
    confirm_url = request.build_absolute_uri(reverse(f"accounts:{confirm_view}"))
    confirm_url += f"?user={user.id}&email={email}"
    subject = "Confirm email"
    message = f"Confirm your email on link: {confirm_url}"
    send_mail(
            subject, message, "no-reply", [email], fail_silently=False
        )
    messages.info(request, "Confirmation email has been sent")
    

#views:
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = form.save()
            send_confirmation_email(request, user, email, 'confirm_register')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form':form})


def confirm_register(request):
    user_id = request.GET.get('user')
    email = request.GET.get('email')

    if not user_id or not email:
        return HttpResponseBadRequest('BAD REQUEST: No user or email')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest('BAD REQUEST: No user or email')
    
    login(request, user)
    messages.info(request, 'You are registered')
    return redirect('accounts:profile')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            session_cart = request.session.get(settings.CART_SESSION_ID)
            if session_cart:
                cart = Cart.objects.get_or_create(user=user)
                for product_id, amount in session_cart.items():
                    product = Product.objects.get(id=product_id)
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                    if not created:
                        cart_item.amount += amount
                    else:
                        cart_item.amount = amount
                    
                    cart_item.save()
                request.session[settings.CART_SESSION_ID] = {}
            next_url = request.GET.get('next')
            return redirect(next_url or 'shop:home')
        else:
            return render(request, 'login.html', {'error': 'Incorrect login or password'})
    return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('shop:home')


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile':profile})


@login_required
def edit_profile_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")
            if new_email != user.email:
                send_confirmation_email(request, user, new_email, "confirm_email")
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(user=user)
    return render(
        request, "edit_profile.html", context={"form": form, "profile": profile}
    )


def confirm_email(request):
    user_id = request.GET.get('user')
    email = request.GET.get('email')

    if not user_id or not email:
        return HttpResponseBadRequest('BAD REQUEST: No user or email')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest('BAD REQUEST: No user or email')

    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest('This email is already taken')

    user.email = email
    user.save()

    return render(request, 'email_change_done.html', {'email': email})
