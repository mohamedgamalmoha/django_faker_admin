Configuration
=============

Django Faker Admin can be configured through several settings in your Django project's ``settings.py`` file.

Default Settings
----------------

Django Faker Admin comes with the following default configuration:

.. code-block:: python

    DEFAULTS = {
        'FAKER_ADMIN_MAX_LIMIT': 100,
        'FAKER_ADMIN_URL': 'populate-dummy-data/',
        'FAKER_ADMIN_TEMPLATE_NAME': 'admin/faker_admin.html',
        'FAKER_ADMIN_CHANGE_LIST_TEMPLATE': 'admin/faker_admin_change_list.html',
    }

Configuration Options
---------------------

FAKER_ADMIN_MAX_LIMIT
~~~~~~~~~~~~~~~~~~~~~

**Default:** ``100``

The maximum number of fake objects that can be created in a single batch operation. This limit helps prevent accidental creation of too many database records.

**Validation:** Must be a positive integer (greater than 0).

Example:

.. code-block:: python

    # In settings.py
    FAKER_ADMIN_MAX_LIMIT = 500  # Allow creation of up to 500 objects in one batch

FAKER_ADMIN_URL
~~~~~~~~~~~~~~~

**Default:** ``'populate-dummy-data/'``

The URL path segment used for the faker admin view. This URL will be appended to your model's admin URL.

**Validation:** Must end with a forward slash (``'/'``).

Example:

.. code-block:: python

    # In settings.py
    FAKER_ADMIN_URL = 'generate-fake-data/'  # Changes the URL pattern

With the above setting, if your model admin URL is ``/admin/myapp/customer/``, the faker admin URL would be ``/admin/myapp/customer/generate-fake-data/``.

FAKER_ADMIN_TEMPLATE_NAME
~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``'admin/faker_admin.html'``

The template used for the faker admin view. This template contains the form for generating fake data.

**Validation:** Must end with the ``.html`` extension.

Example:

.. code-block:: python

    # In settings.py
    FAKER_ADMIN_TEMPLATE_NAME = 'admin/custom_faker_form.html'  # Use a custom template

FAKER_ADMIN_CHANGE_LIST_TEMPLATE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default:** ``'admin/faker_admin_change_list.html'``

The template used for the change list view that includes the faker admin functionality. This template extends the standard Django admin change list template.

**Validation:** Must end with the ``.html`` extension.

Example:

.. code-block:: python

    # In settings.py
    FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'admin/custom_change_list.html'

Applying Configuration
----------------------

To override the default settings, add your custom values to your project's ``settings.py`` file:

.. code-block:: python

    # settings.py

    # Django Faker Admin settings
    FAKER_ADMIN_MAX_LIMIT = 200
    FAKER_ADMIN_URL = 'create-fake-data/'
    FAKER_ADMIN_TEMPLATE_NAME = 'admin/custom_faker.html'
    FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'admin/custom_faker_list.html'

Validation Checks
-----------------

Django Faker Admin performs validation checks on your configuration values during Django's system check framework execution. If any of your configuration values don't meet the validation requirements, Django will raise a warning.

The following checks are performed:

1. ``FAKER_ADMIN_MAX_LIMIT`` must be an integer greater than 0
2. ``FAKER_ADMIN_URL`` must end with a forward slash (``'/'``)
3. ``FAKER_ADMIN_TEMPLATE_NAME`` must end with the ``.html`` extension
4. ``FAKER_ADMIN_CHANGE_LIST_TEMPLATE`` must end with the ``.html`` extension

For example, if you set ``FAKER_ADMIN_MAX_LIMIT = 0``, you'll see a warning like:

.. code-block:: text

    System check identified some issues:

    WARNINGS:
    ?: (django_faker_admin.W001)' FAKER_ADMIN_MAX_LIMIT' should be a positive integer.
         HINT: Set 'FAKER_ADMIN_MAX_LIMIT' to a positive integer in your settings.
