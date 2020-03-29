from random import randint

from app.models.features import Feature
from tests._utils.strings import create_random_string


def create_random_feature_title() -> str:
    return create_random_string(
        min_length=10,
        max_length=25,
        min_words=2,
        max_words=6,
        uppercase_letters=True,
        lowercase_letters=True,
        numbers=True,
    )


def create_random_feature_slug() -> str:
    string = create_random_string(
        min_length=10,
        max_length=50,
        min_words=3,
        max_words=6,
        uppercase_letters=True,
        lowercase_letters=True,
        numbers=True,
    )
    return "-".join(string.split()).lower()


async def create_random_feature() -> Feature:
    return await Feature.create(
        title=create_random_feature_title(),
        slug=create_random_feature_slug(),
        turn_duration=randint(1, 99),
    )
