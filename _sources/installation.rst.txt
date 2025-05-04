Installation
============

You can install Django Faker Admin via pip:

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ django-faker-admin


Add ``django_faker_admin`` before ``django.contrib.admin`` to your ``INSTALLED_APPS``:

   .. code-block:: python

      INSTALLED_APPS = [
          ...
          'django_faker_admin',
          'django.contrib.admin',
          ...
      ]
