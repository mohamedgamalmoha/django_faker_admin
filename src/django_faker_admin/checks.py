from typing import List

from django.core.checks import Tags, Warning, register


@register(Tags.compatibility)
def check_settings(app_configs, **kwargs) -> List[Warning]:
    """
    Check the settings for the Django Faker Admin app.
    This function verifies that the settings used by the Django Faker Admin app are correctly configured.

    It checks for the following:
        - FAKER_ADMIN_MAX_LIMIT: Should be a positive integer.
        - FAKER_ADMIN_URL: Should be a string and should end with a '/'.
        - FAKER_ADMIN_TEMPLATE_NAME: Should be a string and should end with '.html'.
        - FAKER_ADMIN_CHANGE_LIST_TEMPLATE: Should be a string and should end with '.html'.

    Args:
        - app_configs: A list of app configurations.
        - kwargs: Additional keyword arguments.

    Returns:
        - list: A list of Warning objects if any settings are misconfigured.
    """
    from django_faker_admin.conf import settings

    errors = []

    if not isinstance(settings.FAKER_ADMIN_MAX_LIMIT, int) \
            or settings.FAKER_ADMIN_MAX_LIMIT <= 0:
        errors.append(
            Warning(
                msg="'FAKER_ADMIN_MAX_LIMIT' should be a positive integer.",
                id='django_faker_admin.W001',
                hint="Set 'FAKER_ADMIN_MAX_LIMIT' to a positive integer in your settings."
            )
        )

    if not isinstance(settings.FAKER_ADMIN_URL, str) \
            or not settings.FAKER_ADMIN_URL.endswith('/'):
        errors.append(
            Warning(
                msg="'FAKER_ADMIN_URL' should be a string and should end with a '/'",
                id='django_faker_admin.W002',
                hint="Set 'FAKER_ADMIN_URL' to a valid string in your settings."
            )
        )

    if not isinstance(settings.FAKER_ADMIN_TEMPLATE_NAME, str) \
            or not settings.FAKER_ADMIN_TEMPLATE_NAME.endswith('.html'):
        errors.append(
            Warning(
                msg="'FAKER_ADMIN_TEMPLATE_NAME' should be a string and should end with '.html'",
                id='django_faker_admin.W003',
                hint="Set 'FAKER_ADMIN_TEMPLATE_NAME' to a valid string in your settings."
            )
        )

    if not isinstance(settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE, str) \
        or not settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE.endswith('.html'):
        errors.append(
            Warning(
                msg="'FAKER_ADMIN_CHANGE_LIST_TEMPLATE' should be a string and should end with '.html'",
                id='django_faker_admin.W004',
                hint="Set 'FAKER_ADMIN_CHANGE_LIST_TEMPLATE' to a valid string in your settings."
            )
        )

    return errors
