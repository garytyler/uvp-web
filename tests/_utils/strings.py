import random
from string import ascii_lowercase, ascii_uppercase


def create_random_string(
    min_length: int = 5,
    max_length: int = 25,
    min_words: int = 1,
    max_words: int = 5,
    lowercase_letters: bool = True,
    uppercase_letters: bool = True,
    numbers: bool = True,
):

    # Validate parameters
    if min_length > max_length:
        raise ValueError("'min_length' cannot be > 'max_length'")
    if min_words > max_words:
        raise ValueError("'min_words' cannot be > 'max_words'")
    for value in [
        min_words,
        max_words,
        min_length,
        max_length,
    ]:
        if value < 1:
            raise ValueError(value, "Value must be > 1")
    if min_words * 2 - 1 > max_length:
        raise AttributeError(
            f"Cannot generate a string with " f"{min_words=} and {max_length=}"
        )

    # Create population
    char_population: list = list()
    if lowercase_letters:
        char_population += ascii_lowercase
    if uppercase_letters:
        char_population += ascii_uppercase
    if numbers:
        char_population += "".join([str(n) for n in range(9)])

    # Create
    num_words = random.randint(min_words, max_words)
    while num_words * 2 - 1 > max_length:
        num_words -= 1
    assert num_words >= min_words
    str_length = random.randint(max([min_length, num_words * 2 - 1]), max_length)
    num_spaces = num_words - 1
    num_chars = str_length - num_spaces
    words = [random.choice(char_population) for _ in range(num_words)]
    for _ in range(num_chars - num_words):
        index = random.randint(0, num_words - 1)
        words[index] += random.choice(char_population)
    return " ".join(words)
