import pytest

from live.consumers import get_feature_synchronously


@pytest.mark.django_db(transaction=True)
def test_add_guests_to_queue(rf, django_user_model, session_key_factory):
    guest_sessions = []
    for n in range(1, 5):
        user = django_user_model.objects.create(
            username=f"testuser+{n}", password=f"testpass+{n}"
        )
        user.request = rf.get("/home/")
        user.request.session = {"session_key": session_key_factory()}
        user.save()
        guest_sessions.append(user.request.session["session_key"])
    guest_queue = get_feature_synchronously().guest_queue
    for guest_session in guest_sessions:
        guest_queue.add(guest_session)
    queued_sessions = guest_queue.ordered_members()
    assert len(queued_sessions)
    assert len(queued_sessions) == len(guest_sessions)
    assert tuple(queued_sessions) == tuple(guest_sessions)
