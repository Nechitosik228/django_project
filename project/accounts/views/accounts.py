from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.conf import settings

from ..forms import RegisterForm, LoginForm, ProfileUpdateForm
from ..serializers import ProfileSerializer, UserSerializer
from ...utils.email import send_confirmation_email
from ...shop.models import Product, CartItem


class AccountViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def user_register(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            send_confirmation_email(request, user, user.email)
            return Response({"message": "User was registered"}, status=201)
        else:
            return Response({"errors": form.errors}, status=400)

    @action(detail=True, methods=["post"])
    def user_login(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )

            if user:
                login(request, user)
                session_cart = request.session.get(settings.CART_SESSION_ID, default={})
                
                if session_cart:
                    cart = request.user.cart
                    
                    for p_id, a in session_cart.items():
                        product = Product.objects.get(id=p_id)
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=cart, product=product
                        )
                        cart_item.amount = cart_item.amount + a if not created else a
                        cart_item.save()
                    
                    session_cart.clear()
                
                return Response({"message": "successful login"}, status=200)

            return Response({"error": "Incorrect login or password"}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def user_logout(self, request):
        logout(request)
        return Response({"message": "Successfuly loged out"})

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def user_profile(self, request):
        profile = request.user.profile
        data = ProfileSerializer(profile).data
        return Response({"result": data})

    @action(detail=True, methods=["put"], permission_classes=[IsAuthenticated])
    def user_update(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(request.data, request.FILES, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data.get("email")

            if new_email != request.user.email:
                send_confirmation_email(request, request.user, new_email)

            avatar = form.cleaned_data.get("avatar")

            if avatar:
                profile.avatar = avatar

            profile.save()

            return Response({"result": ProfileSerializer(profile).data})
        else:
            return Response({"errors": form.errors}, status=400)

    @action(detail=True, methods=["get"])
    def user_confirm_email(self, request):
        user_id = request.GET.get("user")
        new_email = request.GET.get("new_email")

        if not user_id or not new_email:
            return Response({"error": "Invalid URL"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.is_active and User.objects.filter(email=new_email).exists():
            return Response({"error": "This email si already used"}, status=400)

        user.email = new_email
        user.is_active = True
        user.save()

        return Response({"result": UserSerializer(user).data})
