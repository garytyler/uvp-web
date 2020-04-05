from app.models.features import Feature
from app.models.guests import Guest
from tests._utils.strings import create_random_string


def create_random_guest_name() -> str:
    return create_random_string(
        uppercase_letters=True,
        lowercase_letters=True,
        numbers=False,
        min_length=3,
        max_length=9,
        min_words=2,
        max_words=3,
    )


async def create_random_guest(feature: Feature) -> Guest:
    return await Guest.create(name=create_random_guest_name(), feature_id=feature.id)
