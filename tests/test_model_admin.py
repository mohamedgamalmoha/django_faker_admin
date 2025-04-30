from django.urls import reverse_lazy
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.test import RequestFactory, TestCase
from bs4 import BeautifulSoup

from tests.testapp.models import TestModel
from tests.testapp.admin import TestModelAdmin


User = get_user_model()

FAKER_ADMIN_URL = 'populate-dummy-data/'


class DateHierarchyTests(TestCase):
    factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        call_command('migrate')
        
        super().setUpClass()

        info = TestModel._meta.app_label, TestModel._meta.model_name
        cls.add_perm_codename = "add_%s" % info[1]
        cls.list_url = reverse_lazy('admin:%s_%s_changelist' % info)
        cls.dummy_data_url = reverse_lazy('admin:%s_%s_populate_dummy_data' % info)

        cls.model_admin = TestModelAdmin(TestModel, site)

    @classmethod
    def setUpTestData(cls):        
        cls.superuser = User.objects.create_superuser(
            username="super", email="a@b.com", password="xxx"
        )
        cls.orduser = User.objects.create(
            username='ord', email='b@a.com', password='yyy', is_staff=True
        )

        permissions = cls.get_permissions_for_model(TestModel)
        cls.orduser.user_permissions.add(
            *permissions
        )

    @staticmethod
    def get_permissions_for_model(model):
        ct = ContentType.objects.get_for_model(model)

        permissions = Permission.objects.filter(
            content_type=ct
        )
        
        return permissions
    
    @staticmethod
    def get_permission_from_codename(codename):
        permission = Permission.objects.get(
            codename=codename
        )

        return permission

    def test_href_exisit(self):
        request = self.factory.get(self.list_url)
        request.user = self.superuser
        
        cl = self.model_admin.changelist_view(request=request)
        cl.render()

        soup = BeautifulSoup(cl.content, 'html.parser')

        add_tags = soup.find_all('a', class_='addlink')
        
        self.assertEqual(cl.status_code, 200)
        self.assertTrue(self.superuser.has_perm(self.add_perm_codename))
        self.assertTrue(
            any(tag['href'] == FAKER_ADMIN_URL for tag in add_tags)
        )

    def test_no_href_exisit(self):
        permission = self.get_permission_from_codename(self.add_perm_codename)
        self.orduser.user_permissions.remove(permission)
  
        request = self.factory.get(self.list_url)
        request.user = self.orduser
        
        cl = self.model_admin.changelist_view(request=request)
        cl.render()

        soup = BeautifulSoup(cl.content, 'html.parser')

        add_tags = soup.find_all('a', class_='addlink')
        
        self.assertEqual(cl.status_code, 200)
        self.assertFalse(self.orduser.has_perm(self.add_perm_codename))
        self.assertFalse(
            any(tag['href'] == FAKER_ADMIN_URL for tag in add_tags)
        )
