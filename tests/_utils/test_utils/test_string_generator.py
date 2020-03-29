import pytest

from ..strings import create_random_string


@pytest.mark.parametrize(
    "min_length, max_length, min_words, max_words",
    [
        (4, 4, 2, 2),
        (5, 5, 3, 3),
        (19, 19, 10, 10),
        (20, 20, 10, 10),
        (10, 30, 3, 5,),
        (70, 100, 3, 20),
        (2, 9, 2, 6),
    ],
)
def test_create_random_string_with_various_parameters(
    min_length, max_length, min_words, max_words
):
    string = create_random_string(
        lowercase_letters=True,
        uppercase_letters=True,
        numbers=True,
        min_length=min_length,
        max_length=max_length,
        min_words=min_words,
        max_words=max_words,
    )
    assert min_length <= len(string)
    assert max_length >= len(string)
    assert min_words <= len(string.split())
    assert max_words >= len(string.split())
    assert all([len(string.strip()) for string in string.split()])  # words have chars


def test_create_random_string_with_default_parameters():
    for _ in range(5):
        string = create_random_string()
        # check that words have chars
        assert all([len(string.strip()) for string in string.split()])
