from django.contrib import admin
from django_faker_admin import FakerModelAdminMixin

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(FakerModelAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
