import pytest

from app.models.users import User


@pytest.mark.asyncio
async def test_configure_empty_test_db(app):
    all_user_objs = await User.all()
    assert not all_user_objs
