import pytest
from channels.testing import WebsocketCommunicator

from seevr.routing import application

# @pytest.fixture
# def communicator_factory():
#     def _create_communicator(client, path):
#         communicator = WebsocketCommunicator(
#             application=application,
#             path=path,
#             headers=[
#                 (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"))
#             ],
#         )
#         return communicator

#     return _create_communicator


@pytest.fixture
def feature_communicator(client):
    yield WebsocketCommunicator(
        # application=URLRouter([url(r"^feature/(?P<message>\w+)/$", FeatureConsumer)],),
        application=application,
        path="/feature/fancy/",
        headers=[
            (b"cookie", f"sessionid={client.session.session_key}".encode("ascii"))
        ],
    )


@pytest.fixture
def feature_client(client):
    yield client


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_feature_connect(feature_client, feature_communicator):
    connected = await feature_communicator.connect()
    assert connected
    # print(feature_communicator.session)
    # assert feature_communicator.session
