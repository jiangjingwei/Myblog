from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class RegisterForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    username = forms.CharField(
        required=True,
        min_length=4,
        max_length=12,
        strip=True,
        error_messages={'required': '用户名不能为空', 'min_length': '用户名最少为4个字符', 'max_length': '用户名最多不超过12个字符'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名为4-12个字符', 'autofocus': 'autofocus'}))

    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '密码不能为空', 'min_length': '密码最少6为字符', 'max_length': '密码最长不超过12个字符'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control password', 'placeholder': '密码为6-12个字符'})
    )

    rePassword = forms.CharField(
        required=True,
        strip=True,
        error_messages={'required': '请再次输入密码', 'min_length': '密码最少6为字符', 'max_length': '密码最长不超过12个字符'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control password', 'placeholder': '请再次输入密码'})
    )

    email = forms.EmailField(
        required=True,
        strip=True,
        error_messages={'required': '邮箱不能为空', 'invalid': '请输入正确的邮箱格式'},
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))

    phone = forms.CharField(
        required=True,
        strip=True,
        error_messages={'required': '手机号不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'})
    )

    captcha = forms.CharField(
        required=True,
        strip=True,
        error_messages={'required': '验证码不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control captcha', 'placeholder': '验证码'})
    )

    def clean_password(self):
        if self.cleaned_data.get('password').isdigit() or self.cleaned_data.get('password').isalpha():
            raise ValidationError('密码不能是纯数字或纯字母')

        return self.cleaned_data.get('password')

    def clean_captcha(self):
        if self.cleaned_data.get('captcha').upper() != self.request.session.get('captcha_code').upper():
            raise ValidationError('验证码错误')
        else:
            return self.cleaned_data.get('captcha')

    def clean_phone(self):
        if len(self.cleaned_data.get('phone')) != 11:
            raise ValidationError('手机号码长度为11位')
        elif not self.cleaned_data.get('phone').isdigit() or not self.cleaned_data.get('phone').startswith('1'):
            raise ValidationError('手机号码格式不正确')

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('rePassword') and 6 <= len(self.cleaned_data.get('rePassword')) <= 12:
            raise ValidationError('密码不一致')
        return self.cleaned_data




