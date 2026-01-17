from pathlib import Path

import statistics as stat
import re

def _extract_numbers(file_path):
    """Generator function to extract floating-point numbers from lines starting with 'X-DSPAM-Confidence:' in the file."""
    
    with file_path.open("r") as fhand:
        for line in fhand:
            if not line.startswith("X-DSPAM-Confidence:"):
                continue
            match = re.search(r"[-+]?\d*\.\d+", line)
            if match:
                yield float(match.group())
                

def _file_input():
    """
    Function to handle user input for file name and validate its existence.
    provides up to 3 attempts to enter a valid file name before exiting.
    Returns the Path object of the valid file.
    """
    
    cwd = Path.cwd()
    file_directory = cwd if (cwd / "data").exists() else cwd.parent
    file_root = file_directory / "data"
    
    fname = input("Enter file name: ").strip().lower()
    if fname == "":
        fname = "mbox-short.txt"
    file_path = file_root / fname

    print(f"(Looking for file: {fname} in directory: {file_root})")

    fail = 0

    while True:
        try:
            file_path.open("r")
            print("\nFile opened successfully.")
            return file_path
        except FileNotFoundError:
            fail += 1
            if fail > 3:
                print("\nToo many failed attempts. Exiting.\n")
                exit()
            
            if fname != "mbox-short.txt":
                fname = input(f"\nFile name: {fname}, is incorrect. Please enter a valid file name: ").strip().lower()
            else:
                print(f"\nFile {fname} not found in directory {file_root}. Please try again.\n")
                fname = input("Enter file name: ").strip().lower()


def compute_average():
    """Function to compute the average of spam confidence values from the specified file."""
    
    numbers = []
    for number in _extract_numbers(_file_input()):
        numbers.append(number)
    
    if not numbers:
        print("No numbers or lines starting with 'X-DSPAM-Confidence:' found in the file.\n")
        exit()
    
    average = stat.mean(numbers)
    count = len(numbers)
    
    return average, count
    
        
   
def main():

    print("\nThis program computes the average of the spam confidence values from a specified file. Enter ctrl+c to exit.\n")
    
    try:
        average, count = compute_average()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...\n")
        exit()
    
    print("\n==== Computation completed successfully ====")
    print(f"\nCount of 'X-DSPAM-Confidence:' lines: {count}")
    print(f"Average spam confidence: {average} || Rounded: {round(average, 2)}\n")
    
    print("Thank you for using the program. Goodbye!\n")
    
    
if __name__ == "__main__":
    main()