import pytest

from recipes.services import Services


def test_services_not_initialised() -> None:
    with pytest.raises(RuntimeError):
        Services().unit_of_work()
