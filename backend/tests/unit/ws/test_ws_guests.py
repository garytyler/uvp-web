# import pytest
# from async_asgi_testclient import TestClient


# @pytest.mark.asyncio
# async def test_guest_ws_broadcasts_feature_to_guests_on_connect(
#     app, create_random_feature_obj, create_random_guest_obj
# ):
#     random_feature = await create_random_feature_obj()
#     await create_random_guest_obj(feature=random_feature)
#     async with TestClient(app) as tc:
#         async with tc.websocket_connect(f"/ws/guest/{random_feature.slug}") as ws:
#             received_json = await ws.receive_json()
#             assert received_json["feature"]["id"] == str(random_feature.id)
#             assert received_json["feature"]["title"] == random_feature.title
#             assert received_json["feature"]["slug"] == random_feature.slug
#             async with tc.websocket_connect(f"/ws/guest/{random_feature.slug}") as ws2:
#                 received_json2 = await ws2.receive_json()
#                 assert received_json2["feature"]["id"] == str(random_feature.id)
#                 assert received_json2["feature"]["title"] == random_feature.title
#                 assert received_json2["feature"]["slug"] == random_feature.slug
