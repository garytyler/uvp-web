import pytest

from live.models import Feature


def test_pytest():
    assert True == True


@pytest.mark.django_db(transaction=True)
def test_create_feature():
    feature = Feature()
    feature.save()
    assert feature
