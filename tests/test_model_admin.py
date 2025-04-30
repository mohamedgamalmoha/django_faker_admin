from contextlib import contextmanager

from django.urls import reverse_lazy
from django.test import LiveServerTestCase
from django.test.selenium import SeleniumTestCase
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.utils.translation import gettext as _

from .testapp.models import TestModel


User = get_user_model()


class BaseSeleniumTestCase(SeleniumTestCase, LiveServerTestCase):
    static_handler = StaticFilesHandler
    browser = "chrome"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username='admin',
            password='password',
            is_staff=True,
            is_superuser=True
        )

    def wait_until(self, callback, timeout=10):
        from selenium.webdriver.support.wait import WebDriverWait

        WebDriverWait(self.selenium, timeout).until(callback)

    def wait_page_ready(self, timeout=10):
        """
        Block until the  page is ready.
        """
        self.wait_until(
            lambda driver: driver.execute_script("return document.readyState;")
            == "complete",
            timeout,
        )

    @contextmanager
    def wait_page_loaded(self, timeout=10):
        """
        Block until a new page has loaded and is ready.
        """
        from selenium.common.exceptions import WebDriverException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as ec

        old_page = self.selenium.find_element(By.TAG_NAME, "html")

        yield

        try:
            self.wait_until(ec.staleness_of(old_page), timeout=timeout)
        except WebDriverException:
            ...
        self.wait_page_ready(timeout=timeout)

    def admin_login(self, username, password, login_url="/admin/"):
        from selenium.webdriver.common.by import By

        self.selenium.get("%s%s" % (self.live_server_url, login_url))
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)
        login_text = _("Log in")
        with self.wait_page_loaded():
            self.selenium.find_element(
                By.XPATH, '//input[@value="%s"]' % login_text
            ).click()

    def find_dummy_data_href(self, model_list_url):
        from selenium.webdriver.common.by import By
        self.selenium.get("%s%s" % (self.live_server_url, model_list_url))
        return self.selenium.find_element(By.CLASS_NAME, 'dummy-data-href')


class FakerModelAdminMixinSeleniumTestCase(BaseSeleniumTestCase):

    def setUp(self):
        super().setUp()
        self.admin_login("admin", "password")

        info = TestModel._meta.app_label, TestModel._meta.model_name
        self.dummy_data_url = reverse_lazy('admin:%s_%s_populate_dummy_data' % info)
        self.model_list_url = reverse_lazy('admin:%s_%s_changelist' % info)

    def test_dummy_data_href_exists(self):
        """
        Test if the dummy data href exists in the model list page.
        """
        dummy_data_href = self.find_dummy_data_href(self.model_list_url)
        self.assertIsNotNone(dummy_data_href, "Dummy data href should exist.")

    def test_dummy_data_href_redirects(self):
        """
        Test if the dummy data href redirects to the correct URL.
        """
        dummy_data_href = self.find_dummy_data_href(self.model_list_url)
        dummy_data_href.click()

        # Wait for the page to load
        with self.wait_page_loaded():
            self.assertEqual(
                self.selenium.current_url,
                "%s%s" % (self.live_server_url, self.dummy_data_url),
                "Dummy data href should redirect to the correct URL."
            )

    def test_dummy_data_form(self):
        """
        Test if the dummy data form is displayed correctly.
        """
        from selenium.webdriver.common.by import By

        dummy_data_href = self.find_dummy_data_href(self.model_list_url)
        dummy_data_href.click()

        # Wait for the page to load
        with self.wait_page_loaded():
            form = self.selenium.find_element(By.TAG_NAME, 'form')
            self.assertIsNotNone(form, "Dummy data form should be present.")
