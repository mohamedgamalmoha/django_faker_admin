Django Faker Admin
==================

.. warning::
   This package is a work in progress, and not all features are implemented
   or tested intensively to make sure that it behaves as expected.

.. image:: _static/logo.png
   :target: https://test.pypi.org/simple/django-faker-admin
   :alt: PyPI Version

A Django admin extension for creating fake data directly from the admin interface.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   getting_started
   configuration
   views
   admin
   templates
   notes

Features
--------

* Create fake data for your models directly from the Django admin interface
* Customizable faker templates
* Batch creation of fake objects
* Custom admin views and templates

Installation
------------

You can install Django Faker Admin via pip:

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ django-faker-admin

Quick Start
-----------

1. Add ``django_faker_admin`` before ``django.contrib.admin`` to your ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'django_faker_admin',
          'django.contrib.admin',
          ...
      ]

2. Use the provided admin mixins in your ``admin.py``:

   .. code-block:: python

      from django.contrib import admin
      from django_faker_admin.mixins import FakerAdminMixin
      from .models import YourModel
      from .factories import YourModelFactory

      @admin.register(YourModel)
      class YourModelAdmin(FakerAdminMixin, admin.ModelAdmin):
          factory_class = YourModelFactory
