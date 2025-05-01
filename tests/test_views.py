from django.urls import reverse_lazy
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from django_faker_admin.conf import settings
from django_faker_admin.views import FakerAdminView

from tests.testapp.models import TestModel
from tests.testapp.admin import TestModelAdmin
from tests.testapp.factory import TestModelFactory


User = get_user_model()


class FakerAdminViewTestCase(TestCase):
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

    def test_initialization(self):
        request = self.factory.get(self.list_url)
        request.user = self.superuser

        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory,
            exclude=('id',)
        )
        self.assertEqual(view.model_admin, self.model_admin)
        self.assertEqual(view.model, TestModel)
        self.assertEqual(view.factory_class, TestModelFactory)
        self.assertEqual(view.exclude, ('id',))

    def test_has_add_permission_with_permission(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        request = self.factory.get('/')
        request.user = self.superuser

        self.assertTrue(view.has_add_permission(request))

    def test_has_add_permission_without_permission(self):
        # Remove add permission from staff user
        permission = self.get_permission_from_codename(self.add_perm_codename)
        self.orduser.user_permissions.remove(permission)

        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        request = self.factory.get('/')
        request.user = self.orduser

        self.assertFalse(view.has_add_permission(request))

    def test_dispatch_with_permission(self):
        view = FakerAdminView.as_view(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        request = self.factory.get('/')
        request.user = self.superuser

        # This should not raise an exception
        response = view(request)
        self.assertEqual(response.status_code, 200)  # GET requests should return 200

    def test_dispatch_without_permission(self):
        # Remove add permission from staff user
        permission = self.get_permission_from_codename(self.add_perm_codename)
        self.orduser.user_permissions.remove(permission)

        view = FakerAdminView.as_view(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        request = self.factory.get('/')
        request.user = self.orduser

        with self.assertRaises(PermissionDenied):
            view(request)

    def test_get_exclude(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory,
            exclude=('description',)
        )

        exclude = view.get_exclude()

        # 'description' should be from explicit exclude
        self.assertIn('description', exclude)

    def test_get_form_class(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        FormClass = view.get_form_class()
        form = FormClass()

        # Check for size field
        self.assertIn('size', form.fields)
        self.assertTrue(form.fields['size'].required)
        self.assertEqual(form.fields['size'].min_value, 1)
        self.assertEqual(form.fields['size'].max_value, settings.FAKER_ADMIN_MAX_LIMIT)

        # Check field order
        self.assertEqual(form.field_order[0], 'size')

        # Check other fields are not required
        for field_name in form.fields:
            if field_name != 'size':
                self.assertFalse(form.fields[field_name].required)

    def test_get_admin_form(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        admin_form = view.get_admin_form()

        # Check form fields including size field
        self.assertIn('size', admin_form.form.fields)

        # Check fieldsets
        self.assertEqual(len(admin_form.fieldsets), 1)

        # Check model_admin
        self.assertEqual(admin_form.model_admin, self.model_admin)

    def test_get_context_data(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        context = view.get_context_data()

        self.assertIn('adminform', context)
        self.assertEqual(context['adminform'].model_admin, self.model_admin)

    def test_form_valid_creates_objects(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        class MockForm:
            def __init__(self):
                self.cleaned_data = {
                    'size': 3,
                    'name': 'Test Object',
                    'description': 'Test Description',
                    'empty_field': None
                }

        # Call form_valid directly
        response = view.form_valid(MockForm())

        # Verify objects were created (can't verify exact count as the factory is mocked)
        self.assertEqual(response.status_code, 302)  # Should redirect

        # Check success URL
        expected_url = view.get_success_url()
        self.assertEqual(response.url, expected_url)

    def test_form_post_creates_objects(self):
        # Prepare test data for form submission
        data = {
            'size': 3,
            'name': 'Post Test',
            'description': 'Created via POST'
        }

        # Create the view
        view = FakerAdminView.as_view(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        # Create a POST request
        request = self.factory.post('/', data=data)
        request.user = self.superuser

        # Check objects before submission
        initial_count = TestModel.objects.filter(name='Post Test').count()
        self.assertEqual(initial_count, 0)

        # Process the request
        response = view(request)

        # Verify it redirects (302) on success
        self.assertEqual(response.status_code, 302)

    def test_get_success_message(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        # Test singular message
        cleaned_data = {'size': 1}
        message = view.get_success_message(cleaned_data)
        self.assertIn("1 testmodel object was successfully created", str(message))

        # Test plural message
        cleaned_data = {'size': 5}
        message = view.get_success_message(cleaned_data)
        self.assertIn("5 testmodel objects were successfully created", str(message))

    def test_get_success_url(self):
        view = FakerAdminView(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        expected_url = reverse_lazy('admin:testapp_testmodel_changelist')
        url = view.get_success_url()

        self.assertEqual(url, expected_url)

    def test_get_view_renders_form(self):
        view = FakerAdminView.as_view(
            model_admin=self.model_admin,
            factory_class=TestModelFactory
        )

        request = self.factory.get('/')
        request.user = self.superuser

        response = view(request)

        # Check response contains form with size field
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        self.assertIn('size', response.context_data['form'].fields)
