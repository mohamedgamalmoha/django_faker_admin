from django.apps import AppConfig
from django.utils.text import gettext_lazy as _


class DjangoFakerAdminConfig(AppConfig):
    name = 'django_faker_admin'
    verbose_name = _("Django Faker Admin")

    def ready(self):
        from .checks import check_settings
