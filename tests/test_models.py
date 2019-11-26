import random

import pytest

from live.guests import GuestQueue
from live.models import Feature


@pytest.fixture
def feature(db):
    feature = Feature(title="Feature One Title")
    feature.save()
    yield feature


# @pytest.fixture
# def user(db, django_user_model):
#     yield


# @pytest.mark.django_db(transaction=True)
# def test_adding_guests(feature, django_user_model):
#     guest1 = Guest(
#         user=django_user_model.objects.create(
#             username="testuser1", password="testpass1"
#         )
#     )
#     guest2 = Guest(
#         user=django_user_model.objects.create(
#             username="testuser2", password="testpass2"
#         )
#     )
#     # print(dir)
#     print(dir(guest2.user))
#     print(dir(feature.guest_set))
#     print(feature.guest_set.user)
#     # assert guest1 in feature.guest_set.objects.all()
#     # assert guest1 in


@pytest.mark.django_db(transaction=True)
def test_adding_guests(rf, feature, django_user_model, random_string_factory):
    # guest1 = Guest(
    #     user=django_user_model.objects.create(
    #         username="testuser1", password="testpass1"
    #     )
    # )
    # guest2 = Guest(
    #     user=django_user_model.objects.create(
    #         username="testuser2", password="testpass2"
    #     )
    # )

    user1 = django_user_model.objects.create(username="testuser1", password="testpass1")
    user2 = django_user_model.objects.create(username="testuser2", password="testpass2")
    user3 = django_user_model.objects.create(username="testuser3", password="testpass3")
    user4 = django_user_model.objects.create(username="testuser4", password="testpass4")

    user1.request = rf.get("/index/")
    user2.request = rf.get("/index/")
    user3.request = rf.get("/index/")
    user4.request = rf.get("/index/")

    # user1.request.session = {"session_key": random_string_factory(32, 32)}
    # user2.request.session = {"session_key": random_string_factory(32, 32)}
    user1.request.session = {
        "session_key": int("".join([str(random.choice(range(9))) for n in range(32)]))
    }
    user2.request.session = {
        "session_key": int("".join([str(random.choice(range(9))) for n in range(32)]))
    }
    user3.request.session = {
        "session_key": int("".join([str(random.choice(range(9))) for n in range(32)]))
    }
    user4.request.session = {
        "session_key": int("".join([str(random.choice(range(9))) for n in range(32)]))
    }

    print(user1.request.session)
    print(user2.request.session)
    print(user3.request.session)
    print(user4.request.session)
    # user2.request.session = {"session_key": random.ran(32, 32)}

    # int("".join([random.choice(range(9)) for n in range(32)]))

    user1.save()
    user2.save()
    user3.save()
    user4.save()

    # guest_queue = GuestQueue(feature.queue_id)
    guest_queue = GuestQueue(feature.slug)
    guest_queue.add(user1.request.session["session_key"])
    guest_queue.add(user2.request.session["session_key"])
    guest_queue.add(user3.request.session["session_key"])
    guest_queue.add(user4.request.session["session_key"])
    print(guest_queue)
    assert guest_queue

    # print(dir(guest2.user))
    # print(dir(feature.guest_set))

    # print(feature.guest_set.user)
    # assert guest1 in feature.guest_set.objects.all()
    # assert guest1 in
