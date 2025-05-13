from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError("This email already exists")
        else:
            return new_email

    class Meta:
        model = User
        extra_fields = ['email']
        fields = ['username', 'password1', 'password2']
    

class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(required=True, label='Enter new email:')
    avatar = forms.ImageField(required=False, label='Upload an avatar:')

    def clean_email(self):
        new_email = self.cleaned_data.get('email')
        if User.objects.filter(email=new_email).exists():
            raise ValidationError('User with this email already exists')
        else:
            return new_email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Login:')
    password = forms.PasswordInput(required=True)