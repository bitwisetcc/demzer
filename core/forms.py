# core/forms.py
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    code = forms.IntegerField(required=True)
    user_id = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = CaptchaField(
        error_messages={'invalid': 'Texto do CAPTCHA incorreto.'}
    )
