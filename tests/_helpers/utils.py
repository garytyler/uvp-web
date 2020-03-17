import random
from string import ascii_lowercase


class UniqueRandomStringFactory:
    def __init__(
        self,
        letters: bool = True,
        numbers: bool = True,
        num_words_min: int = 1,
        num_words_max: int = 1,
        word_length_min: int = 3,
        word_length_max: int = 9,
        exclude: list = [],
    ):
        self.letters = letters
        self.numbers = numbers
        self.num_words_min = num_words_min or 1
        self.num_words_max = num_words_max or 1
        self.word_length_min = word_length_min or 1
        self.word_length_max = word_length_max or 1
        self._exclude: list = list(set(exclude))
        self._char_options: list = list()
        if self.letters:
            self._char_options += ascii_lowercase
        if self.numbers:
            self._char_options += "".join([str(n) for n in range(9)])

    def __call__(self):
        while True:
            words = []
            for n in range(random.randint(self.num_words_min, self.num_words_max)):
                word_length = random.randint(self.word_length_min, self.word_length_max)
                words.append("".join(random.choices(self._char_options, k=word_length)))
            result = " ".join(words)
            if result not in self._exclude:
                self._exclude.append(result)
                return result
