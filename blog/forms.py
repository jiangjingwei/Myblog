from django import forms


class RegisterForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField()
    rePassword = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    avatar = forms.FileField()
