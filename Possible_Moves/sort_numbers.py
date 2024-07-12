"""
This file provides functionality to read the numbers, which represent the first moves from a connect 4 game, sort them while ignoring the last digit,
and write the sorted numbers to a new file. It includes functions to handle file operations and a main
function to execute the entire process.
"""

def read_numbers_from_file(filename):
    """
    Read numbers from a file and return them as a list of strings.
    """
    with open(filename, 'r') as file:
        numbers = file.readlines()
    return [number.strip() for number in numbers]

def sort_numbers_ignore_last_digit(numbers):
    """
    Sort a list of numbers as strings, ignoring the last digit in each number.
    """
    return sorted(numbers, key=lambda x: int(x[:-1]))

def write_numbers_to_file(filename, numbers):
    """
    Write a list of numbers to a file, each on a new line.
    """
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

def main():
    """
    Main function to execute the process of reading numbers from a file,
    sorting them while ignoring the last digit, and writing the sorted numbers to a new file.
    """
    input_filename = 'moves_5.txt'
    output_filename = 'Possible_Moves/moves_5.txt'
    numbers = read_numbers_from_file(input_filename)
    sorted_numbers = sort_numbers_ignore_last_digit(numbers)
    write_numbers_to_file(output_filename, sorted_numbers)

if __name__ == "__main__":
    main()
