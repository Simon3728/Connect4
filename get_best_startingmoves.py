"""
File to play against a Connect4 algorithm (https://connect4.gamesolver.org/) and get all possible game moves and save them. 
This process runs in multiple windows to speed up the execution.
"""
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import itertools
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Selenium WebDriver
def setup_driver():
    """
    Setup and return a Selenium WebDriver for Chrome.
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Open the Connect 4 game in the browser
def open_game(driver):
    """
    Navigate to the Connect 4 game URL using the provided WebDriver.
    """
    driver.get("https://connect4.gamesolver.org/")
    time.sleep(3)  # Wait for the game to load

# Get the RGB color of a pixel on the screen
def get_pixel_color(driver, x, y):
    """
    Capture a screenshot and return the RGB color of the pixel at (x, y).
    """
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    rgb = image.getpixel((x, y))
    return rgb

# Calculate the pixel position for a given column and row in the game grid
def calculate_position(col, row):
    """
    Calculate the pixel position in the browser window for a given column and row in the Connect 4 game.
    """
    x = col * 88 + 350
    y = 480 - row * 88 
    return x, y

# Click the red button to automate the game
def click_red_automate(driver):
    """
    Click the 'Red' button to let the computer make a move for the red player.
    """
    x = 170
    y = 510
    click_at_position(driver, x, y)

# Click the yellow button to automate the game
def click_yellow_automate(driver):
    """
    Click the 'Yellow' button to let the computer make a move for the yellow player.
    """
    x = 170
    y = 585
    click_at_position(driver, x, y)

# Click the 'New Game' button to reset the game
def new_game(driver):
    """
    Click the 'New Game' button to start a new game.
    """
    x = 170
    y = 390
    click_at_position(driver, x, y)

# Compare two numbers to find the differing digit
def compare_numbers(num1, num2):
    """
    Compare two numbers represented as strings. If num2 is num1 with one additional digit, return num1 with that digit added.
    """
    sorted_num1 = ''.join(sorted(num1))
    sorted_num2 = ''.join(sorted(num2))
    if len(sorted_num1) + 1 == len(sorted_num2):
        for i, c in enumerate(sorted_num2):
            if sorted_num1[i] != c:
                return num1 + c
            elif len(sorted_num1) == i + 1:
                return num1 + sorted_num2[i+1] 
    else:
        return None

# Get the current state of the board as a string representation
def get_board(driver, number):
    """
    Analyze the game board and return the current state as a string of column numbers. If a black pixel is found, it indicates the game is over.
    """
    current_number = ''
    for col in range(7):
        for row in range(6):
            x, y = calculate_position(col, row)
            rgb = get_pixel_color(driver, x, y)
            # if black --> Game over
            if rgb[0] <= 50 and rgb[1] <= 50 and rgb[2] <= 50:
                return compare_numbers(number, current_number)
            if rgb[0] >= 220 and rgb[1] >= 220 and rgb[2] >= 220:
                break
            else:
                current_number += str(col+1)
    return compare_numbers(number, current_number)

# Click at a specific position in the browser window
def click_at_position(driver, x, y):
    """
    Perform a click action at the specified (x, y) position in the browser window using Selenium.
    """
    actions = ActionChains(driver)
    try:
        actions.move_by_offset(x, y).click().perform()
        actions.reset_actions()
    except Exception as e:
        logging.error(f'Error clicking at position x: {x}, y: {y} - {e}')

# Generate all possible move sequences of length n
def generate_moves(n, columns=7, height=6):
    """
    Generate all possible move sequences of length n for the Connect 4 game.
    """
    column_indices = list(range(1, columns + 1))
    combinations = itertools.product(column_indices, repeat=n)

    valid_moves = []
    for combo in combinations:
        if all(combo.count(col) <= height for col in column_indices):
            valid_moves.append(int(''.join(map(str, combo))))
    return valid_moves

# Write sequences to a file
def write_sequences_to_file(sequences, filename):
    """
    Write the list of move sequences to a file.
    """
    with open(filename, 'w') as file:
        for sequence in sequences:
            file.write(f"{sequence}\n")

# Perform a binary search on a file to find a target ignoring the last digit
def binary_search_ignore_last_digit(filename, target):
    """
    Perform a binary search on a sorted file of numbers, ignoring the last digit of each number during comparison.
    """
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        numbers = [int(line) for line in lines]

        target_int = int(target)  # Convert target to int

        left, right = 0, len(numbers) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_value = numbers[mid] // 10  # Ignore the last digit

            if mid_value == target_int:
                last_digit = numbers[mid] % 10
                return numbers[mid], last_digit  # Return the whole number and the last digit
            elif mid_value < target_int:
                left = mid + 1
            else:
                right = mid - 1

        return -1, None  # Target not found

# Split workload into chunks
def split_workload(moves, num_chunks):
    """
    Split the list of moves into the specified number of chunks for parallel processing.
    """
    chunk_size = len(moves) // num_chunks
    return [moves[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

# Process a chunk of moves
def process_moves(moves_chunk):
    """
    Process a chunk of moves by playing them in the Connect 4 game and recording the results.
    """
    driver = setup_driver()
    open_game(driver)
    results = []

    for move in moves_chunk:
        number = ''
        for c in str(move):
            col = int(c) - 1
            x, y = calculate_position(col, 5)
            click_at_position(driver, x, y)
            number += str(col+1)

        if len(number) % 2 == 0:
            click_red_automate(driver)
            time.sleep(0.3)
        else:
            click_yellow_automate(driver)
            time.sleep(0.3)

        new_number = get_board(driver, number)
        if new_number is not None:
            results.append(new_number)

        if len(number) % 2 == 0:
            click_red_automate(driver)
            time.sleep(0.1)
        else:
            click_yellow_automate(driver)
            time.sleep(0.1)

        new_game(driver)
        time.sleep(0.2)

    driver.quit()
    return results

# Run the processing in parallel
def run_parallel_processes(moves, num_processes):
    """
    Run the move processing in parallel using the specified number of processes.
    """
    chunks = split_workload(moves, num_processes)
    all_results = []

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_moves, chunk) for chunk in chunks]
        for future in as_completed(futures):
            result = future.result()
            logging.info(f'Chunk completed with {len(result)} results')
            all_results.extend(result)

    return all_results

def main():
    """
    Main function to execute the Connect 4 move generation and processing.
    """
    n = 5  # Depth of moves
    moves = generate_moves(n)
    num_processes = 12  # Number of processes to run in parallel

    start_time = time.time()
    all_results = run_parallel_processes(moves, num_processes)
    end_time = time.time()

    logging.info(f'Total results collected: {len(all_results)}')
    logging.info(f'Total time taken: {end_time - start_time} seconds')

    with open(f'moves_{n}.txt', 'w') as file:
        for result in all_results:
            file.write(f"{result}\n")

if __name__ == "__main__":
    main()
