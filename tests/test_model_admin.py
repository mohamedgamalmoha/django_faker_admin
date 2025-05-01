from django.urls import reverse_lazy
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from bs4 import BeautifulSoup

from django_faker_admin.conf import settings

from tests.testapp.models import TestModel
from tests.testapp.admin import TestModelAdmin
from tests.testapp.factory import TestModelFactory


User = get_user_model()


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

        cls.size = 5
        cls.init_data = {'name': 'Test'}

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

    @staticmethod
    def create_model_instance(**kwargs):
        instance = TestModelFactory.build(**kwargs)
        data = instance.__dict__
        data.pop('_state')
        data.pop('id')
        return data

    def test_href_exist(self):
        request = self.factory.get(self.list_url)
        request.user = self.superuser
        
        cl = self.model_admin.changelist_view(request=request)
        cl.render()

        soup = BeautifulSoup(cl.content, 'html.parser')

        add_tag = soup.find('a', class_='dummy-data-href')
        
        self.assertEqual(cl.status_code, 200)
        self.assertTrue(self.superuser.has_perm(self.add_perm_codename))
        self.assertIsNotNone(add_tag)
        self.assertEqual(add_tag['href'], settings.FAKER_ADMIN_URL)

    def test_no_href_exist(self):
        permission = self.get_permission_from_codename(self.add_perm_codename)
        self.orduser.user_permissions.remove(permission)
  
        request = self.factory.get(self.list_url)
        request.user = self.orduser
        
        cl = self.model_admin.changelist_view(request=request)
        cl.render()

        soup = BeautifulSoup(cl.content, 'html.parser')

        add_tag = soup.find('a', class_='dummy-data-href')
        
        self.assertEqual(cl.status_code, 200)
        self.assertFalse(self.orduser.has_perm(self.add_perm_codename))
        self.assertIsNone(add_tag)

    def test_from_get(self):
        request = self.factory.get(self.dummy_data_url)
        request.user = self.superuser

        fv = self.model_admin.faker_view(request=request)
        fv.render()

        soup = BeautifulSoup(fv.content, 'html.parser')

        form_tag = soup.find('form', class_='dummy-data-form')
        input_tag = form_tag.find('input', {'name': 'size'})

        self.assertEqual(fv.status_code, 200)
        self.assertTrue(self.superuser.has_perm(self.add_perm_codename))
        self.assertIsNotNone(form_tag)
        self.assertIsNotNone(input_tag)
        self.assertEqual(input_tag['name'], 'size')

    def test_form_submit(self):
        data = self.create_model_instance(**self.init_data)
        data['size'] = self.size

        request = self.factory.post(self.dummy_data_url, data=data)
        request.user = self.superuser

        fv = self.model_admin.faker_view(request=request)

        qs = TestModel.objects.filter(
            ** self.init_data
        )

        self.assertEqual(fv.status_code, 302)
        self.assertTrue(self.superuser.has_perm(self.add_perm_codename))
        self.assertEqual(self.size, qs.count())

    def test_form_submit_no_perm(self):
        permission = self.get_permission_from_codename(self.add_perm_codename)
        self.orduser.user_permissions.remove(permission)

        data = self.create_model_instance(**self.init_data)
        data['size'] = self.size

        request = self.factory.post(self.dummy_data_url, data=data)
        request.user = self.orduser

        with self.assertRaises(PermissionDenied):
            self.model_admin.faker_view(request=request)

        qs = TestModel.objects.filter(
            ** self.init_data
        )

        self.assertFalse(self.orduser.has_perm(self.add_perm_codename))
        self.assertEqual(0, qs.count())
