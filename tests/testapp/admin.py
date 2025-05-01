from django.contrib import admin
from django_faker_admin import FakerModelAdminMixin

from .models import TestModel
from .factory import TestModelFactory


@admin.register(TestModel)
class TestModelAdmin(FakerModelAdminMixin, admin.ModelAdmin):
    factory_class = TestModelFactory
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
