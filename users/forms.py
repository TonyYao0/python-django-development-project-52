from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Имя"), required=True)
    last_name = forms.CharField(label=_("Фамилия"), required=True)


    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput,
        required=False
        )
    
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput,
        required=False
        )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        labels = {'username': _('Имя пользователя'),}