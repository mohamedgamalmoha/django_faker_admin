![Alt text](assets/logo.png)

[![Run Tests](https://github.com/mohamedgamalmoha/django_faker_admin/actions/workflows/run_tests.yml/badge.svg)](https://github.com/mohamedgamalmoha/django_faker_admin/actions/workflows/run_tests.yml)
[![Deploy to TestPyPI](https://github.com/mohamedgamalmoha/django_faker_admin/actions/workflows/deploy_pypi.yml/badge.svg)](https://github.com/mohamedgamalmoha/django_faker_admin/actions/workflows/deploy_pypi.yml)

# Django Faker Admin

A Django app that adds fake data generation capabilities to your Django admin interface, making it easy to populate your database with realistic test data.

## Installation

You can install Django Faker Admin via pip:

```bash
pip install -i https://test.pypi.org/simple/ django-faker-admin
```

Add `django_faker_admin` before `django.contrib.admin` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'django_faker_admin',
    'django.contrib.admin',
    # ...
]
```

## Getting Started

### Create Database Model

First, define your Django model in your app's `models.py` file:

```python
# myapp/models.py
from django.db import models

class Customer(models.Model):
    MEMBERSHIP_CHOICES = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_CHOICES,
        default='bronze'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']
```

After defining your model, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a Model Factory

Next, create a factory for your model using `factory_boy`. This factory will be used by Django Faker Admin to generate fake data:

```python
# myapp/factories.py
import factory
import factory.fuzzy
from datetime import datetime, timedelta
from .models import Customer

class CustomerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )
    phone_number = factory.Faker('phone_number')
    birth_date = factory.Faker(
        'date_between',
        start_date='-70y',
        end_date='-18y'
    )
    membership = factory.fuzzy.FuzzyChoice(
        [choice[0] for choice in Customer.MEMBERSHIP_CHOICES]
    )
    is_active = factory.Faker('boolean', chance_of_getting_true=80)
    created_at = factory.LazyFunction(datetime.now)

    class Meta:
        model = Customer
```

### Set up the Admin Interface

Finally, register your model with the Django admin and incorporate the Django Faker Admin mixin:

```python
# myapp/admin.py
from django.contrib import admin
from django_faker_admin.mixins import FakerAdminMixin
from .models import Customer
from .factories import CustomerFactory

@admin.register(Customer)
class CustomerAdmin(FakerAdminMixin, admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'membership', 'is_active', 'created_at')
    list_filter = ('membership', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    date_hierarchy = 'created_at'

    # Configure the factory to use for generating fake data
    factory_class = CustomerFactory
```

## Usage

Once configured, you'll see additional options in your Django admin interface to generate fake data for your models. 
This makes it simple to populate your database with realistic test data for development and testing purposes.