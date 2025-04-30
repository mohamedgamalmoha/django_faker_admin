import factory

from .models import TestModel


class TestModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = TestModel
