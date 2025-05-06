from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from shop.models import Order


def send_confirmation_email(request, user, email, cofirm_view:str):
    confirm_url = request.build_absolute_uri(reverse(f"{cofirm_view}"))
    confirm_url += f"?user={user.id}&email={email}"
    subject = "Confirm email"
    message = f"Confirm your email on link: {confirm_url}"
    send_mail(
            subject, message, "no-reply", [email], fail_silently=False
        )
    messages.info(request, "Confirmation email has been sent")


def send_order_confirmation_email(order: Order, total_price):
    subject = f'Cofirmation {order}'
    context = {'order':order, 'total_price':total_price}
    text_content = render_to_string('email/confirm_order_email.txt', context=context)
    to_email = order.contact_email
    try: 
        send_mail(subject, text_content, settings.DEFAULT_EMAIL, [to_email, settings.ADMIN_EMAIL])
    except Exception as e:
        print(f'Error sending email:{e}')