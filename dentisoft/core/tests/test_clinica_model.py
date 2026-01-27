import pytest
from django.core.exceptions import ValidationError

from core.models import Clinica

pytestmark = pytest.mark.django_db


def test_clinica_requires_contact_fields():
    clinic = Clinica(nombre="Name", direccion="Dir")
    with pytest.raises(ValidationError):
        clinic.save()