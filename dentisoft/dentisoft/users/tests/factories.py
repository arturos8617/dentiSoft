from collections.abc import Sequence
from typing import Any

from factory import Faker as FactoryFaker, SubFactory, LazyFunction
from factory import post_generation
from factory.django import DjangoModelFactory
from core.models import Clinica, Rol
from dentisoft.users.models import User

class RolFactory(DjangoModelFactory[Rol]):
    nombre = "dentista"
    descripcion = FactoryFaker("sentence")

    class Meta:
        model = Rol
        django_get_or_create = ["nombre"]


def _short_phone() -> str:
    """Generate a phone number trimmed to the DB field length."""
    return FactoryFaker("phone_number").evaluate(None, None, extra={"locale": None})[:20]


class ClinicaFactory(DjangoModelFactory[Clinica]):
    nombre = FactoryFaker("company")
    direccion = FactoryFaker("street_address")
    telefono = LazyFunction(_short_phone)
    email = FactoryFaker("company_email")

    class Meta:
        model = Clinica
        django_get_or_create = ["nombre"]



class UserFactory(DjangoModelFactory[User]):
    email = FactoryFaker("email")
    first_name = FactoryFaker("first_name")
    last_name = FactoryFaker("last_name")
    telefono = LazyFunction(_short_phone)
    fecha_nacimiento = FactoryFaker("date_of_birth")
    genero = FactoryFaker("random_element", elements=["M", "F", "O", "N"])
    rol = SubFactory(RolFactory)
    clinica = SubFactory(ClinicaFactory)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):  # noqa: FBT001
        password = (
            extracted
            if extracted
            else FactoryFaker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = User
        django_get_or_create = ["email"]
