
def test_all_settings_valid(check_settings_function):
    """
    Test when all settings are valid, no warnings should be returned.
    """
    warnings = check_settings_function(None)
    assert len(warnings) == 0


def test_max_limit_invalid_type(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_MAX_LIMIT is not an integer.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = "100"
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W001'


def test_max_limit_negative(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_MAX_LIMIT is negative.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W001'


def test_max_limit_zero(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_MAX_LIMIT is zero.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = 0
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W001'


def test_admin_url_invalid_type(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_URL is not a string.
    """
    mock_settings.FAKER_ADMIN_URL = 123
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W002'


def test_admin_url_no_trailing_slash(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_URL doesn't end with a slash.
    """
    mock_settings.FAKER_ADMIN_URL = 'faker-admin'
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W002'


def test_template_name_invalid_type(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_TEMPLATE_NAME is not a string.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 123
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W003'


def test_template_name_no_html_extension(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_TEMPLATE_NAME doesn't end with .html.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W003'


def test_change_list_template_invalid_type(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_CHANGE_LIST_TEMPLATE is not a string.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 123
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W004'


def test_change_list_template_no_html_extension(mock_settings, check_settings_function):
    """
    Test when FAKER_ADMIN_CHANGE_LIST_TEMPLATE doesn't end with .html.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'faker_change_list.txt'
    warnings = check_settings_function(None)
    assert len(warnings) == 1
    assert warnings[0].id == 'django_faker_admin.W004'


def test_multiple_invalid_settings(mock_settings, check_settings_function):
    """
    Test when multiple settings are invalid.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    mock_settings.FAKER_ADMIN_URL = 'faker-admin'
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'
    warnings = check_settings_function(None)

    assert len(warnings) == 3
    warning_ids = [warning.id for warning in warnings]
    assert 'django_faker_admin.W001' in warning_ids
    assert 'django_faker_admin.W002' in warning_ids
    assert 'django_faker_admin.W003' in warning_ids


def test_warning_message_contents(mock_settings, check_settings_function):
    """
    Test that warning messages contain expected content.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    warnings = check_settings_function(None)

    assert len(warnings) == 1
    warning = warnings[0]

    assert warning.id == 'django_faker_admin.W001'
    assert "FAKER_ADMIN_MAX_LIMIT" in warning.msg
    assert "positive integer" in warning.msg
    assert "FAKER_ADMIN_MAX_LIMIT" in warning.hint
