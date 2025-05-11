Getting Started
===============

This guide will walk you through the process of setting up Django Faker Admin for your project in three steps:

1. Creating a database model
2. Creating a model factory
3. Setting up the admin interface

Prerequisites
-------------

* Django 5.2 or higher
* Python 3.12 or higher
* Installed packages:
  * ``django-faker-admin``
  * ``factory_boy``

Create Database Model
---------------------

First, define your Django model in your app's ``models.py`` file:

.. code-block:: python

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

After defining your model, create and apply migrations:

.. code-block:: bash

    python manage.py makemigrations
    python manage.py migrate

Create a Model Factory
----------------------

Next, create a factory for your model using ``factory_boy``. This factory will be used by Django Faker Admin to generate fake data:

.. code-block:: python

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


Set up the Admin Interface
--------------------------

Finally, register your model with the Django admin and incorporate the Django Faker Admin mixin:

.. code-block:: python

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

Make sure Django Faker Admin is included in your ``INSTALLED_APPS``:

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        # ... other Django apps
        'django_faker_admin',
        # ... your apps
    ]

Using the Admin Interface
-------------------------

Once you've completed these steps:

1. Start your development server:

   .. code-block:: bash

      python manage.py runserver

2. Navigate to your admin site (typically http://127.0.0.1:8000/admin/)

3. Log in with your admin credentials

4. Go to the Customer admin page

5. You'll see additional options provided by Django Faker Admin:

   * A "Populate Dummy Data" button in the change list view
   * Options to specify how many fake objects to create
   * Configuration for specific field values

6. Click "Generate" to create fake customer records based on your factory configuration
