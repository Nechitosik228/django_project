from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contact_name', 'contact_email', 'address', 'contact_phone']
        labels = {'contact_name' : 'Enter your contact name',
                   'contact_email' : 'Enter your contact email', 
                   'address' : 'Enter your address', 
                   'contact_phone' : 'Enter your contact phone',}