from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

from ..forms import RegisterForm, LoginForm
from ...utils.email import send_confirmation_email
from ...shop.models import Product, CartItem

class AccountViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            send_confirmation_email(request, user, user.email)
            return Response({'message':'User was registered'}, status=201)
        else:
            return Response({'errors':form.errors}, status=400)

    @action(detail=True, methods=['post'])
    def user_login(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                session_cart = request.session.get(settings.CART_SESSION_ID, default={})
                if session_cart:
                    cart = request.user.cart
                    for p_id, a in session_cart.items():
                        product = Product.objects.get(id=p_id)
                        cart_item, created = CartItem.objects.get_or_create(
                            cart = cart,
                            product = product
                        )
                        cart_item.amount = cart_item.amount + a if not created else a 
                        cart_item.save()
                    session_cart.clear()
                return Response({'message':'successful login'}, status=200)
            
            return Response({'error': 'Incorrect login or password'}, status=400)