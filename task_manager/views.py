from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'


    def get_success_message(self, cleaned_data):
        return 'Вы успешно аутентифицированы'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')


    def post(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().post(request, *args, **kwargs)