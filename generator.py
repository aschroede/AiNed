from abc import ABC, abstractmethod
import random


class IGenerator(ABC):
    @abstractmethod
    def get_random(self):
        pass


class RandomIntGenerator(IGenerator):
    def __init__(self, lower=0, upper=100, seed=None):
        self.lower = lower
        self.upper = upper
        if seed:
            random.seed(seed)

    def get_random(self):
        return random.randint(self.lower, self.upper)


class FileRandomGenerator(IGenerator):
    def __init__(self, file_path):
        self.file_path = file_path
        self.numbers = self._load_numbers()
        self.counter = -1

    def _load_numbers(self):
        with open(self.file_path, 'r') as file:
            numbers = [int(line.strip()) for line in file.readlines()]
        return numbers

    def get_random(self):
        if not self.numbers:
            raise ValueError("No numbers loaded from file.")
        self.counter += 1
        return self.numbers[self.counter % len(self.numbers)]

    # Here's a Python version of the Tausworthe PRNG based on the C code provided

    class TausworthePRNG:
        def __init__(self):
            self.s0 = 0xFFFFFFFF
            self.s1 = 0xFFFFFFFF
            self.s2 = 0xFFFFFFFF

        def generate(self):
            self.s0 = (((self.s0 & 0xFFFFFFFE) << 12) ^ (((self.s0 << 13) ^ self.s0) >> 19)) & 0xFFFFFFFF
            self.s1 = (((self.s1 & 0xFFFFFFF8) << 4) ^ (((self.s1 << 2) ^ self.s1) >> 25)) & 0xFFFFFFFF
            self.s2 = (((self.s2 & 0xFFFFFFF0) << 17) ^ (((self.s2 << 3) ^ self.s2) >> 11)) & 0xFFFFFFFF
            return (self.s0 ^ self.s1 ^ self.s2) & 0xFFFFFFFF

