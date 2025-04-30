import os

import pytest
import django


# Ensure tests use test-specific settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.testproject_settings'

# Initialize Django before fixtures
django.setup()


@pytest.fixture
def mock_settings(monkeypatch):
    """
    Fixture to mock django_faker_admin settings with valid defaults.
    """

    class MockSettings:
        FAKER_ADMIN_MAX_LIMIT = 100
        FAKER_ADMIN_URL = 'faker-admin/'
        FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.html'
        FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'faker_change_list.html'

    mock_settings_obj = MockSettings()
    monkeypatch.setattr('django_faker_admin.conf.settings', mock_settings_obj)
    return mock_settings_obj


@pytest.fixture
def check_settings_function(mock_settings):
    """
    Import the check_settings function after mocking settings.
    """
    from django_faker_admin.checks import check_settings
    return check_settings
