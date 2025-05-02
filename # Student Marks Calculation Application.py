# Student Marks Calculation Application
# Author: Veer Rishabh Manoram 24006521
# Date: 17 March 2025
# To upload a file just add the text file to the same folder as the program then you can use the file in the program

# =============================== Part 1 ======================================

def input_numbers_manually():
    """
    Allows the user to enter numbers (marks) manually.
    Accepts single values or comma-separated entries.
    """
    numbers = []
    print("Enter student marks. Type 'done' when finished.")
    while True:
        user_input = input("Enter a number or comma-separated numbers: ")
        if user_input.lower() == 'done':
            break
        if ',' in user_input:
            try:
                new_numbers = [validate_numeric_input(num.strip()) for num in user_input.split(',')]
                numbers.extend(new_numbers)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            try:
                number = validate_numeric_input(user_input)
                numbers.append(number)
            except ValueError as e:
                print(f"Error: {e}")
    return numbers

def check_minimum_numbers(numbers):
    """
    Ensures there are at least two numbers before analysis.
    Prevents meaningless statistics.
    """
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required to perform statistical analysis.")

def process_numbers(numbers):
    """
    Provides a menu to perform statistical operations.
    Includes skewness and number modification options.
    """
    try:
        check_minimum_numbers(numbers)
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        print("\nStatistics Menu:")
        print("1. Calculate Mean")
        print("2. Calculate Median")
        print("3. Calculate Mode")
        print("4. Calculate Skewness")
        print("5. Add or Change Numbers")
        print("6. Return to Main Menu")
        print("7. Exit")

        choice = input("Enter your choice: ")
        try:
            if choice == '1':
                print(f"Mean: {calculate_mean(numbers):.2f}")
            elif choice == '2':
                print(f"Median: {calculate_median(numbers):.2f}")
            elif choice == '3':
                print(f"Mode: {calculate_mode(numbers)}")
            elif choice == '4':
                print(f"Skewness: {calculate_skewness(numbers)}")
            elif choice == '5':
                numbers = modify_numbers(numbers)
                check_minimum_numbers(numbers)
            elif choice == '6':
                break
            elif choice == '7':
                exit()
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")

# =============================== Part 2 ======================================

def validate_numeric_input(input_str):
    """
    Validates and converts string input to float.
    Disallows negatives and improper formats.
    """
    input_str = input_str.strip()
    if not input_str:
        raise ValueError("Input cannot be empty.")

    decimal_point_count = 0
    for i, char in enumerate(input_str):
        if i == 0 and char == '-':
            raise ValueError("Negative values are not allowed.")
        if char == '.':
            decimal_point_count += 1
            if decimal_point_count > 1:
                raise ValueError("Invalid number format.")
            continue
        if not ('0' <= char <= '9'):
            raise ValueError("Invalid characters in input.")

    # Manual float conversion
    whole_part = 0
    fractional_part = 0
    fractional_divisor = 1
    decimal_found = False
    for char in input_str:
        if char == '.':
            decimal_found = True
            continue
        digit_value = ord(char) - ord('0')
        if not decimal_found:
            whole_part = whole_part * 10 + digit_value
        else:
            fractional_part = fractional_part * 10 + digit_value
            fractional_divisor *= 10
    return whole_part + (fractional_part / fractional_divisor)

def calculate_mean(numbers):
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required to calculate mean.")
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def calculate_median(numbers):
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required to calculate median.")
    sorted_numbers = numbers.copy()
    for i in range(len(sorted_numbers)):
        for j in range(0, len(sorted_numbers) - i - 1):
            if sorted_numbers[j] > sorted_numbers[j + 1]:
                sorted_numbers[j], sorted_numbers[j + 1] = sorted_numbers[j + 1], sorted_numbers[j]
    count = len(sorted_numbers)
    mid = count // 2
    if count % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]

def calculate_mode(numbers):
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required to calculate mode.")
    unique_numbers = []
    frequencies = []
    for num in numbers:
        found = False
        for i, unique in enumerate(unique_numbers):
            if num == unique:
                frequencies[i] += 1
                found = True
                break
        if not found:
            unique_numbers.append(num)
            frequencies.append(1)
    max_freq = max(frequencies)
    modes = [unique_numbers[i] for i, freq in enumerate(frequencies) if freq == max_freq]
    return modes

def calculate_skewness(numbers):
    """
    Uses mean and median to determine skewness.
    """
    if len(numbers) < 2:
        raise ValueError("At least two numbers are required to calculate skewness.")
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    if mean > median:
        return "Positive Skew"
    elif mean < median:
        return "Negative Skew"
    else:
        return "Symmetric"

def modify_numbers(numbers):
    """
    Menu to allow users to replace or add more numbers.
    """
    print("\nModify Numbers Menu:")
    print("1. Replace the current list")
    print("2. Add more numbers")
    print("3. Cancel")

    choice = input("Enter your choice: ")
    if choice == '1':
        return input_numbers_manually()
    elif choice == '2':
        additional_numbers = input_numbers_manually()
        return numbers + additional_numbers
    else:
        return numbers

# =============================== Part 3 ======================================

def input_numbers_from_file():
    """
    Prompts user for a filename and reads numbers.
    Validates file extension and content.
    """
    filename = input("Enter the filename with marks: ")
    filename_lower = filename.lower()

    # Check for invalid file type
    if filename_lower.endswith(".xlsx"):
        raise ValueError("'.xlsx' files are not supported. Please provide a '.txt' file.")
    if not filename_lower.endswith(".txt"):
        raise ValueError("Invalid file type. Only '.txt' files are supported.")

    return read_numbers_from_file(filename)

def file_exists(filename):
    try:
        with open(filename, 'r') as file:
            return True
    except IOError:
        return False

def read_numbers_from_file(filename):
    """
    Reads numbers from a file line by line, validates each value.
    """
    if not file_exists(filename):
        raise FileNotFoundError(f"File '{filename}' does not exist.")
    numbers = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                values = line.split(',')
                for value in values:
                    try:
                        num = validate_numeric_input(value)
                        numbers.append(num)
                    except ValueError as e:
                        print(f"Error on line {line_num}: {e}")
        if not numbers:
            raise ValueError("No valid numbers found in the file.")
        return numbers
    except IOError:
        raise IOError(f"Error reading file '{filename}'.")

# =============================== Main Program ================================

def main():
    while True:
        print("\nStudent Marks Calculation Menu:")
        print("1. Enter numbers manually")
        print("2. Upload numbers from a file")
        print("3. Exit")

        choice = input("Enter your choice: ")
        numbers = []
        try:
            if choice == '1':
                numbers = input_numbers_manually()
            elif choice == '2':
                numbers = input_numbers_from_file()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            if numbers:
                process_numbers(numbers)
        except (ValueError, FileNotFoundError, IOError) as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
