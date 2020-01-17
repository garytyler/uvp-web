import struct

import pytest


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_transact_orientation_array(
    connected_guest_presenter_feature_factory, random_orientation
):
    # Create objects
    guest, presenter, feature = await connected_guest_presenter_feature_factory()
    orientation_bytes = struct.pack("!ddd", *random_orientation)
    assert orientation_bytes and orientation_bytes[0] != orientation_bytes[1]

    # Send and receive
    await guest["communicator"].send_to(bytes_data=orientation_bytes)
    received_bytes = await presenter["communicator"].receive_from()

    # Test results
    assert received_bytes == orientation_bytes
    received_data = struct.unpack("!ddd", received_bytes)
    assert tuple(received_data) == tuple(random_orientation)
