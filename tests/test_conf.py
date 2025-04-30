
def test_valid_max_limit(mock_settings, check_settings_function):
    """
    Test that a positive integer value for FAKER_ADMIN_MAX_LIMIT passes validation.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = 50
    warnings = check_settings_function(None)
    assert not any(w.id == 'django_faker_admin.W001' for w in warnings)


def test_non_integer_max_limit(mock_settings, check_settings_function):
    """
    Test that a non-integer value for FAKER_ADMIN_MAX_LIMIT fails validation.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = "100"
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W001' for w in warnings)


def test_zero_max_limit(mock_settings, check_settings_function):
    """
    Test that a zero value for FAKER_ADMIN_MAX_LIMIT fails validation.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = 0
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W001' for w in warnings)


def test_negative_max_limit(mock_settings, check_settings_function):
    """
    Test that a negative value for FAKER_ADMIN_MAX_LIMIT fails validation.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -10
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W001' for w in warnings)


def test_valid_admin_url(mock_settings, check_settings_function):
    """
    Test that a string value ending with '/' for FAKER_ADMIN_URL passes validation.
    """
    mock_settings.FAKER_ADMIN_URL = 'custom-admin/'
    warnings = check_settings_function(None)
    assert not any(w.id == 'django_faker_admin.W002' for w in warnings)


def test_non_string_admin_url(mock_settings, check_settings_function):
    """
    Test that a non-string value for FAKER_ADMIN_URL fails validation.
    """
    mock_settings.FAKER_ADMIN_URL = 123
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W002' for w in warnings)


def test_admin_url_without_trailing_slash(mock_settings, check_settings_function):
    """
    Test that a string value not ending with '/' for FAKER_ADMIN_URL fails validation.
    """
    mock_settings.FAKER_ADMIN_URL = 'faker-admin'
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W002' for w in warnings)


def test_empty_admin_url(mock_settings, check_settings_function):
    """
    Test that an empty string for FAKER_ADMIN_URL fails validation.
    """
    mock_settings.FAKER_ADMIN_URL = ''
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W002' for w in warnings)


def test_valid_template_name(mock_settings, check_settings_function):
    """
    Test that a string value ending with '.html' for FAKER_ADMIN_TEMPLATE_NAME passes validation.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'custom_template.html'
    warnings = check_settings_function(None)
    assert not any(w.id == 'django_faker_admin.W003' for w in warnings)


def test_non_string_template_name(mock_settings, check_settings_function):
    """
    Test that a non-string value for FAKER_ADMIN_TEMPLATE_NAME fails validation.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 123
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W003' for w in warnings)


def test_template_name_without_html_extension(mock_settings, check_settings_function):
    """
    Test that a string value not ending with '.html' for FAKER_ADMIN_TEMPLATE_NAME fails validation.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W003' for w in warnings)


def test_valid_change_list_template(mock_settings, check_settings_function):
    """
    Test that a string value ending with '.html' for FAKER_ADMIN_CHANGE_LIST_TEMPLATE passes validation.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'custom_change_list.html'
    warnings = check_settings_function(None)
    assert not any(w.id == 'django_faker_admin.W004' for w in warnings)


def test_non_string_change_list_template(mock_settings, check_settings_function):
    """
    Test that a non-string value for FAKER_ADMIN_CHANGE_LIST_TEMPLATE fails validation.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 123
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W004' for w in warnings)


def test_change_list_template_without_html_extension(mock_settings, check_settings_function):
    """
    Test that a string value not ending with '.html' for FAKER_ADMIN_CHANGE_LIST_TEMPLATE fails validation.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'faker_change_list.txt'
    warnings = check_settings_function(None)
    assert any(w.id == 'django_faker_admin.W004' for w in warnings)


def test_all_settings_valid(mock_settings, check_settings_function):
    """
    Test that valid values for all settings pass validation with no warnings.
    """
    warnings = check_settings_function(None)
    assert len(warnings) == 0


def test_all_settings_invalid(mock_settings, check_settings_function):
    """
    Test that invalid values for all settings generate appropriate warnings.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    mock_settings.FAKER_ADMIN_URL = 'faker-admin'
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'faker_list'

    warnings = check_settings_function(None)
    assert len(warnings) == 4

    warning_ids = [warning.id for warning in warnings]
    assert 'django_faker_admin.W001' in warning_ids
    assert 'django_faker_admin.W002' in warning_ids
    assert 'django_faker_admin.W003' in warning_ids
    assert 'django_faker_admin.W004' in warning_ids


def test_some_settings_invalid(mock_settings, check_settings_function):
    """
    Test that invalid values for some settings generate appropriate warnings.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'

    warnings = check_settings_function(None)
    assert len(warnings) == 2

    warning_ids = [warning.id for warning in warnings]
    assert 'django_faker_admin.W001' in warning_ids
    assert 'django_faker_admin.W003' in warning_ids


def test_max_limit_warning_details(mock_settings, check_settings_function):
    """
    Test that the warning for FAKER_ADMIN_MAX_LIMIT has correct details.
    """
    mock_settings.FAKER_ADMIN_MAX_LIMIT = -5
    warnings = check_settings_function(None)

    warning = next(w for w in warnings if w.id == 'django_faker_admin.W001')
    assert warning.id == 'django_faker_admin.W001'
    assert "'FAKER_ADMIN_MAX_LIMIT'" in warning.msg
    assert "positive integer" in warning.msg
    assert "'FAKER_ADMIN_MAX_LIMIT'" in warning.hint


def test_admin_url_warning_details(mock_settings, check_settings_function):
    """
    Test that the warning for FAKER_ADMIN_URL has correct details.
    """
    mock_settings.FAKER_ADMIN_URL = 'faker-admin'
    warnings = check_settings_function(None)

    warning = next(w for w in warnings if w.id == 'django_faker_admin.W002')
    assert warning.id == 'django_faker_admin.W002'
    assert "'FAKER_ADMIN_URL'" in warning.msg
    assert "end with a '/'" in warning.msg
    assert "'FAKER_ADMIN_URL'" in warning.hint


def test_template_name_warning_details(mock_settings, check_settings_function):
    """
    Test that the warning for FAKER_ADMIN_TEMPLATE_NAME has correct details.
    """
    mock_settings.FAKER_ADMIN_TEMPLATE_NAME = 'faker_admin.txt'
    warnings = check_settings_function(None)

    warning = next(w for w in warnings if w.id == 'django_faker_admin.W003')
    assert warning.id == 'django_faker_admin.W003'
    assert "'FAKER_ADMIN_TEMPLATE_NAME'" in warning.msg
    assert "end with '.html'" in warning.msg
    assert "'FAKER_ADMIN_TEMPLATE_NAME'" in warning.hint


def test_change_list_template_warning_details(mock_settings, check_settings_function):
    """
    Test that the warning for FAKER_ADMIN_CHANGE_LIST_TEMPLATE has correct details.
    """
    mock_settings.FAKER_ADMIN_CHANGE_LIST_TEMPLATE = 'faker_list.txt'
    warnings = check_settings_function(None)

    warning = next(w for w in warnings if w.id == 'django_faker_admin.W004')
    assert warning.id == 'django_faker_admin.W004'
    assert "'FAKER_ADMIN_CHANGE_LIST_TEMPLATE'" in warning.msg
    assert "end with '.html'" in warning.msg
    assert "'FAKER_ADMIN_CHANGE_LIST_TEMPLATE'" in warning.hint
