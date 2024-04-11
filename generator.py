from abc import ABC, abstractmethod
import random
from ctypes import cdll, c_uint32
import os
from fxpmath import Fxp

DTYPE = "fxp-u16/16"

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


# To get the 32-bit pseudorandom number and extract the 16 uppermost bits:
# random_32_bit = tausworthe()
# upper_16_bits = random_32_bit >> 16

# print(f"32-bit random number: {random_32_bit}")
# print(f"Upper 16 bits: {upper_16_bits}")



class TausworthePRNG:
    def __init__(self):
        self.lib = cdll.LoadLibrary('/home/andrew/Documents/Semester 2/AiNed/ained/libtausworthe.so')
        self.lib.tausworthe_wrapper.restype = c_uint32

    def get_random(self):

        # lib.tausworthe_wrapper outputs a uint16 ctype in range 0 to 65535
        rand_number = self.lib.tausworthe_wrapper()
        # need to create a fixed point variable with the "fxp-u16/16" data type 
        value = Fxp(None, dtype=DTYPE)
        # need to load the random number as a raw value into the fxp type
        value.set_val(rand_number, raw=True)
        
        return value


# lib = cdll.LoadLibrary('/home/andrew/Documents/Semester 2/AiNed/ained/libtausworthe.so')
# lib.tausworthe_wrapper.restype = c_uint32

# first = lib.tausworthe_wrapper()
# value = Fxp(None, dtype=DTYPE)
# value.set_val(first, raw=True)
# print(value)

# second = lib.tausworthe_wrapper()
# print(f"First call result: {first}")
# print(f"Second call result: {second}")