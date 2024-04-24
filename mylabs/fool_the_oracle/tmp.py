import time
from chall import encrypt


def measure_loop_time(percentage, with_sleep: float = 0):
    total_iterations = 2**32
    iterations = int(total_iterations * percentage)
    
    start_time = time.time()
    for _ in range(iterations):
        pass
    end_time = time.time()
    
    time_taken = end_time - start_time
    
    # Approximating total time
    total_seconds = time_taken / percentage * total_iterations * with_sleep
    
    return total_seconds

def gen_byte():
    C = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for i in C:
        for j in C:
            yield i + j

def gen_hex():
    C = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    for i in C:
        yield i


def generate_hex_configurations(length):
    hex_characters = '0123456789abcdef'

    def generate_configurations_helper(current_configuration):
        if len(current_configuration) == length:
            yield current_configuration
            return

        for char in hex_characters:
            new_configuration = current_configuration + char
            yield from generate_configurations_helper(new_configuration)

    yield from generate_configurations_helper('')


def brutte_force():
    string = bytes('CRYPTO23{'.encode()).hex() # len() = 18

