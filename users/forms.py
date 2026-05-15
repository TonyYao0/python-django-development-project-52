from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), required=True)
    last_name = forms.CharField(label=_("Фамилия"), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name",)
        labels = {'username': _('Имя пользователя'),}


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Имя"), required=True)
    last_name = forms.CharField(label=_("Фамилия"), required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        labels = {'username': _('Имя пользователя'),}