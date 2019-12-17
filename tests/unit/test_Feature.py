import pytest

from live.models import Feature


@pytest.mark.parametrize("title, expected_slug", ([("Big Day", "big-day")]))
def test_slug_creation(title, expected_slug, transactional_db):
    feature = Feature(title=title)
    feature.save()
    assert feature.slug == expected_slug
