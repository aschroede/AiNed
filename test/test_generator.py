from generator import FileRandomGenerator
from number_gen import generate_random_numbers

def test_file_random_generator():
    test_data ="./Test_Data/random_nums.txt"
    number_count = 10
    generate_random_numbers(number_count, test_data)
    generator = FileRandomGenerator(test_data)

    first_num = generator.get_random()

    num = 0
    for i in range(number_count):
        num = generator.get_random()

    assert num == first_num
