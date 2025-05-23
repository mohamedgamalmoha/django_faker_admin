from typing import Type, Tuple

from django import forms
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.admin import ModelAdmin
from django.contrib.admin.helpers import AdminForm
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy, ngettext
from factory.django import DjangoModelFactory

from django_faker_admin.conf import settings


class FakerAdminView(FormView):
    """
    A view to populate dummy data for a given model.

    This view integrates with the Django admin and uses a factory class to generate dummy data for a specified model.
    It provides a custom form within the admin interface where the user can specify the number of dummy items to create.
    The form excludes specified fields and ensures that only the desired number of dummy items are created.
    """
    #: Factory class to be used for creating dummy data
    factory_class: Type[DjangoModelFactory] = None
    #: ModelAdmin instance for the model to be populated
    model_admin: ModelAdmin = None
    #: URL to redirect to after form submission
    exclude: Tuple[str] = None
    #: Template name for the view
    template_name = settings.FAKER_ADMIN_TEMPLATE_NAME

    def __init__(
            self,
            model_admin: ModelAdmin,
            factory_class: Type[DjangoModelFactory],
            exclude: Tuple[str] = None,
            **kwargs
        ) -> None:
        """
        Initializes the view with the model admin and factory class.

        Args:
            - model_admin (ModelAdmin): The admin class for the model to be populated.
            - factory_class (Type[DjangoModelFactory]): The factory class used to create dummy data.
            - exclude (Tuple[str]): A tuple of field names to be excluded from the form.
            - **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.model_admin = model_admin
        self.model = self.model_admin.model
        self.factory_class = factory_class
        self.exclude = exclude

    def has_add_permission(self, request):
        """
        Checks if the user has permission to add dummy data for the model.

        Args:
            - request: The HTTP request object.

        Returns:
            - bool: True if the user has permission, False otherwise.
        """
        return request.user.has_perm(f"{self.model._meta.app_label}.add_{self.model._meta.model_name}")

    def dispatch(self, request, *args, **kwargs):
        """
        Handles the HTTP request and checks for permissions.
        This method is called before the view processes the request. It checks if the user has permission to add
        dummy data for the model. If not, it raises a PermissionDenied exception.

        Args:
            - request: The HTTP request object.
            - *args: Additional positional arguments.
            - **kwargs: Additional keyword arguments.

        Returns:
            - HttpResponse: The response object.

        Raises:
            - PermissionDenied: If the user does not have permission to add dummy data.
        """
        # Check if the user has add permission for the model
        if not self.has_add_permission(request):
            raise PermissionDenied(
                gettext_lazy("You don't have permission to preform this action.")
            )
        return super().dispatch(request, *args, **kwargs)

    def get_exclude(self):
        """
        Constructs a tuple of field names to be excluded.

        Returns:
            - A tuple containing the names of fields to be excluded. This includes both fields explicitly listed in
              `self.exclude` and fields in the model marked as unique.
        """
        # Find all field names in the model that are marked as unique.
        unique_fields = tuple(
            field.name for field in self.model._meta.get_fields()
            if getattr(field, 'unique', False)
        )
        # Combine the explicitly excluded fields with the unique fields.
        return self.exclude or () + unique_fields

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        This method is used to pass the initial data and request data to the form.
        It includes the initial data, prefix, and any POST or PUT data if the request method is either of those.

        Returns:
            - dict: A dictionary of keyword arguments to be passed to the form class.
        """
        kwargs =  {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if hasattr(self, 'request') and self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )

        return kwargs

    def get_form_class(self):
        """
        Dynamically creates and returns a form class for dummy data creation.

        This method overrides the default form to include a 'size' field, which specifies the number of dummy instances
        to be created. It also sets all fields inherited from the base form class as not required, except for the
        'size' field which is mandatory and constrained to a range between 1 and 20.

        Returns:
            - MainForm (forms.ModelForm): A dynamically created form class that inherits from the base form class
              associated with the factory model.
        """
        # Dynamically generate a base form class using the model, excluding specified fields
        FromBase = forms.modelform_factory(
            self.model,
            exclude=self.get_exclude()
        )
        # Get the base fields from the generated form class
        form_fields = FromBase.base_fields

        # Define a new form class that includes a 'size' field and sets all other fields as not required
        class MainForm(FromBase):
            # Define a 'size' field that is required, with a minimum value.
            size = forms.IntegerField(required=True, min_value=1, max_value=settings.FAKER_ADMIN_MAX_LIMIT)
            # Specify the order of fields, placing 'size' at the beginning
            field_order = ('size', *form_fields)

            def __init__(self, *args, **kwargs):
                # Call the superclass initializer
                super(MainForm, self).__init__(*args, **kwargs)
                # Iterate over the form fields and set them as not required
                for field in form_fields:
                    self.fields[field].required = False

        # Return the dynamically created form class
        return MainForm

    def get_admin_form(self):
        """
        Creates and returns an admin form for the dummy data creation.

        Returns:
            - AdminForm: The admin form with fields for dummy data creation.
        """
        form = self.get_form()
        return AdminForm(
            form=form,
            fieldsets=list([(None, {'fields': form.field_order})]),
            prepopulated_fields={},
            readonly_fields=(),
            model_admin=self.model_admin
        )

    def get_context_data(self, **kwargs):
        """
        Adds the admin form to the context data.

        Args:
            - **kwargs: Additional keyword arguments passed to the superclass method.

        Returns:
            - dict: Context data including the admin form.
        """
        context = super().get_context_data(**kwargs)
        context['adminform'] = self.get_admin_form()
        return context

    def form_valid(self, form):
        """
        Handles valid form submission, creating dummy data using the factory class.

        Args:
            - form: The submitted form with valid data.

        Returns:
            - HttpResponseRedirect: A redirect response to the success URL.
        """
        cleaned_data = {k: v for k, v in form.cleaned_data.items() if v}
        self.factory_class.create_batch(**cleaned_data)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        """
        Generates a success message after creating dummy data.

        Args:
            - cleaned_data: The cleaned data from the submitted form.

        Returns:
            - str: A success message indicating the number of objects created.
        """
        return gettext_lazy(
                ngettext(
                    "%d %s object was successfully created.",
                    "%d %s objects were successfully created.",
                    cleaned_data['size'],
                ) % (cleaned_data['size'], self.model._meta.model_name)
            )

    def get_success_url(self):
        """
        Returns the URL to redirect to after successfully creating dummy data.

        Returns:
            - str: A URL to redirect to after form submission.
        """
        info = self.model._meta.app_label, self.model._meta.model_name
        return reverse('admin:%s_%s_changelist' % info)
