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
