from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices={
            "liqpay": "With LiqPay",
            "monopay": "With MonoPay",
            "googlepay": "With Google Pay",
            "cash": "With cash",
        },
        label="Payment method",
    )

    class Meta:
        model = Order
        fields = [
            "contact_name",
            "contact_email",
            "address",
            "contact_phone",
            "payment_method",
        ]
        labels = {
            "contact_name": "Enter your contact name",
            "contact_email": "Enter your contact email",
            "address": "Enter your address",
            "contact_phone": "Enter your contact phone",
        }
