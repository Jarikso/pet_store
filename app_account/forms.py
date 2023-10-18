from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

from django.utils.translation import gettext_lazy as _


class CreationUserForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('full_name', 'phone', 'email',)

    def clean_password2(self):
        cd = self.cleaned_data
        a = cd['password2'].isdigit()  # состоит из цифр
        b = cd['password2'].isalpha()  # состоит из букв
        if len(cd['password2']) < 8:
            raise forms.ValidationError("Слишком короткий пароль. Придумайте пароль минимум из 8 символов")
        elif a is not b:
            raise forms.ValidationError("Слишком простой пароль. Придумайте более сложный пароль (1-9, A-Z)")
        elif cd['password1'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']

    def clean_full_name(self):
        cd = self.cleaned_data
        result = cd['full_name'].split(' ')
        if not ''.join(result).isalpha():
            raise forms.ValidationError("В имени присутствует число")
        elif len(result) != 3:
            raise forms.ValidationError("Формат имени пользователя Фамилия Имя Отчество")
        return cd['full_name']


class PassimLoginForm(forms.Form):
    """форма контекст процессора для входав в аккаунт """
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={
        'autocomplete': 'email',
        'class': 'form-input',
        'placeholder': 'E-mail'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password',
        'class': 'form-input',
        'placeholder': 'Пароль'}), )


class ChangeUserForm(UserChangeForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'Profile-file form-input', 'id': 'avatar'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Здесь вы можете поменять пароль'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Подтвердите новый пароль'}))

    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'phone', 'email', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False
        self.fields['full_name'].required = False
        self.fields['phone'].required = False
        self.fields['email'].required = False
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean_full_name(self):
        cd = self.cleaned_data
        result = cd['full_name'].split(' ')
        if not ''.join(result).isalpha():
            raise forms.ValidationError("В имени присутствует число")
        elif len(result) != 3:
            raise forms.ValidationError("Формат имени пользователя Фамилия Имя Отчество")
        return cd['full_name']

    def clean_new_password2(self):
        cd = self.cleaned_data
        a = cd['new_password2'].isdigit()  # состоит из цифр
        b = cd['new_password2'].isalpha()  # состоит из букв
        if len(cd['new_password2']) == 0:
            return cd['new_password2']
        elif len(cd['new_password2']) < 8:
            raise forms.ValidationError("Слишком короткий пароль. Придумайте пароль минимум из 8 символов")
        elif a is not b:
            raise forms.ValidationError("Слишком простой пароль. Придумайте более сложный пароль (1-9, A-Z)")
        elif cd['new_password1'] != cd['new_password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['new_password2']
