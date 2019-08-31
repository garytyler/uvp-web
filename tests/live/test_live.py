import pytest

from live.models import Feature


def test_pytest():
    assert True


@pytest.fixture()
def new_feature():
    def delete_all_features():
        for old_feature in Feature.objects.all():
            old_feature.delete()

    delete_all_features()
    new_feature = Feature()
    new_feature.save()
    yield new_feature
    delete_all_features()


@pytest.mark.django_db
def test_db(new_feature):
    assert new_feature
