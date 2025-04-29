from typing import Dict

from django.utils.functional import LazyObject
from django.core.signals import setting_changed


type SettingType = str | int
type SettingsType = Dict[str, SettingType]


DEFAULTS = {
    'FAKER_ADMIN_MAX_LIMIT': 100,
    'FAKER_ADMIN_URL': 'populate-dummy-data/',
    'FAKER_ADMIN_TEMPLATE_NAME': 'admin/faker_admin.html',
    'FAKER_ADMIN_CHANGE_LIST_TEMPLATE': 'admin/faker_admin_change_list.html',
}


class Settings:
    """
    A class to manage settings for the Django Faker Admin app.
    It allows for default settings and overridden settings to be accessed in a consistent manner.
    """

    def __init__(
            self,
            defaults: SettingsType,
            explicit_overridden_settings: SettingsType = None
    ) -> None:
        """
        Initialize the Settings class with default settings and any explicitly overridden settings.

        Args:
            - defaults: A dictionary of default settings.
            - explicit_overridden_settings: A dictionary of explicitly overridden settings.
        """
        self.defaults = defaults
        self.explicit_overridden_settings = explicit_overridden_settings or {}

    def __getattr__(self, name: str) -> SettingType:
        """
        Get the value of a setting by its name.
            - If the setting has been explicitly overridden, return that value.
            - If the setting is not found, return the default value.
            - If the setting is not found in either, raise an AttributeError.

        Args:
            - name: The name of the setting to retrieve.

        Returns:
            - The value of the setting.

        Raises:
            - AttributeError: If the setting is not found in either the defaults or overridden settings.
        """
        if name in self.explicit_overridden_settings:
            return self.explicit_overridden_settings[name]

        if name in self.defaults:
            return self.defaults[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, key: str, value: SettingType) -> None:
        """
        Set the value of a setting by its name.
            - If the setting is in the defaults, set the overridden value.
            - If the setting is not found, set it as an instance attribute.

        Args:
            - key: The name of the setting to set.
            - value: The value to set for the setting.
        """
        if key in ('defaults', 'explicit_overridden_settings'):
            # Set class attributes directly
            super().__setattr__(key, value)
        elif key in self.defaults:
            # Set overridden value for a setting
            self.explicit_overridden_settings[key] = value
        else:
            # Set regular instance attribute
            super().__setattr__(key, value)

    def update_setting(self, key: str, value: SettingType) -> None:
        """
        Update a single setting value.

        Args:
            - key: The name of the setting to update.
            - value: The new value for the setting.
        """
        if key in self.defaults:
            self.explicit_overridden_settings[key] = value


class LazySettings(LazyObject):
    """
    A lazy object that wraps the Settings class.
    It initializes the Settings class with default settings and any explicitly overridden settings.
    """

    def _setup(self, explicit_overridden_settings: SettingsType = None) -> None:
        """
        Set up the LazySettings object by initializing the Settings class.
        This method is called when the LazySettings object is first accessed.

        Args:
            - explicit_overridden_settings: A dictionary of explicitly overridden settings.
        """
        self._wrapped = Settings(DEFAULTS.copy(), explicit_overridden_settings)


settings = LazySettings()


def reload_api_settings(*args, **kwargs) -> None:
    """
    Reload the settings when they are changed.
    This function is connected to the setting_changed signal.
    It updates the settings with the new values.

    Args:
        - args: Positional arguments.
        - kwargs: Keyword arguments containing the setting name and value.
    """
    setting = kwargs['setting']
    value = kwargs['value']

    if setting in DEFAULTS.keys():
        if not settings._wrapped:
            settings._setup()

        # Update the existing settings object instead of recreating it
        settings._wrapped.update_setting(setting, value)


setting_changed.connect(reload_api_settings)
