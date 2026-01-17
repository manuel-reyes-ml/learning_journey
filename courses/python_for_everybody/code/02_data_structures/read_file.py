from pathlib import Path # Path module for handling file path

cwd = Path.cwd() # Get the current working directory
file_directory = cwd if (cwd / "data").exists() else cwd.parent # Determine the file directory based on the existence of the "data" folder
file_root = file_directory / "data"

def main():
    fname = input("Enter file name: ").strip().lower() # Convert input to lowercase and strip whitespace
    if fname == "":
        fname = "words.txt"
    file_path = file_root / fname


    try:
        file_path.open("r") # Try to open the file to check if it exists

    except FileNotFoundError: # Handle the case where the file does not exist
        print(f"File not found: {file_path}. Exiting the program.\n")
        exit()
        

    print(f"File opened successfully: {fname} in path: {file_path}\n") 
    print("Contents of the file in uppercase:\n")
    with file_path.open("r") as fhand: # Open the file using the Path object's open method, and close it automatically after the block
        for line in fhand:
            line = line.rstrip()
            print(line.upper())

    print("\nFile read and displayed in uppercase successfully.\n")
    
if __name__ == "__main__": # Ensure the main function runs only when the script is executed directly
    try:
        main()
    except KeyboardInterrupt: # Handle user interruption gracefully
        print("\n\nProgram interrupted by user. Exiting...\n")
