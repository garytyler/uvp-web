import pytest

from live.models import Feature

# @pytest.mark.django_db(transactional=True)
# @pytest.mark.parametrize("title, expected_slug", ([("Big Day", "big-day")]))
# def test_duplicate_slugs_raise_exception(title, expected_slug, transactional_db):
#     feature1 = Feature(title="x")
#     feature1.save()
#     feature2 = Feature(title="x")
#     feature2.save()
#     assert feature2


@pytest.mark.parametrize("title, expected_slug", ([("Big Day", "big-day")]))
def test_slug_creation(title, expected_slug, transactional_db):
    feature = Feature(title=title)
    feature.save()
    assert feature.slug == expected_slug
