import pytest

from live.guests import GuestQueueInterface
from live.models import Feature


@pytest.fixture
def feature(db):
    feature = Feature(title="Feature One Title")
    feature.save()
    yield feature


@pytest.mark.django_db(transaction=True)
def test_add_guests_to_queue(rf, feature, django_user_model, session_key_factory):
    users = []
    for n in range(4):
        user = django_user_model.objects.create(
            username=f"testuser+{n}", password=f"testpass+{n}"
        )
        user.request = rf.get("/index/")
        user.request.session = {"session_key": session_key_factory()}
        user.save()
        users.append(user)
    guest_queue = GuestQueueInterface(feature.slug)
    for user in users:
        guest_queue.add(user.request.session["session_key"])
    assert guest_queue
