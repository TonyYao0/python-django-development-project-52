from django.apps import AppConfig
from django.contrib.auth import get_user_model

def users_get_full_name(self):
    full_name = f"{self.first_name} {self.last_name}".strip()
    return full_name if full_name else self.username


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    def ready(self):
        user_model = get_user_model()
        user_model.__str__ = users_get_full_name