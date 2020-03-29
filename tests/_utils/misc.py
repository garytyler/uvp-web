import json
import random
from typing import Union

from .strings import create_random_string


def create_random_session_key() -> str:
    """Create a new random 32-character integer that imitates a session key"""
    return create_random_string(
        min_length=32,
        max_length=32,
        min_words=1,
        max_words=1,
        uppercase_letters=True,
        lowercase_letters=True,
        numbers=True,
    )


def create_random_euler_rotation():
    return [random.uniform(0, 360) for i in range(3)]


def ppjson(value: Union[dict, str]):
    if isinstance(value, str):
        value = json.loads(value)
    print(json.dumps(value, indent=4, sort_keys=True))
