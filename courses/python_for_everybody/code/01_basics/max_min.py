from numbers import Integral, Real

# function to handle user input and validate number. Give 3 attempts for valid input.
def input_number():
    num_list = []
    fail = 0 
    while True:
        snum = input("Enter number: ").strip()
        
        try: 
            if '.' in snum:
                fnum = float(snum)
            else:
                fnum = int(snum)
            if isinstance(fnum, (Integral, Real)):  
                num_list.append(fnum)
                fail = 0  # reset fail counter on successful input
        except ValueError:
            if snum.lower() == "done":
                return num_list
            fail += 1
            if fail >= 3:
                print("\nToo many invalid attempts. Exiting.\n")
                break
            print("Invalid input")
            continue
    return num_list

# function to find maximum and minimum from a list of numbers
def find_max_min(*num_list):
    largest = None
    smallest = None
    
    for num in num_list:
        if largest is None or num > largest:
            largest = num
        if smallest is None or num < smallest:
            smallest = num
            
    return largest, smallest

# main function to find max and min from user input
def main():
    
    try:
        largest, smallest = None, None
        
        print("\nEnter numbers one by one. Type 'done' when finished.")
        numbers = input_number()
        if numbers:
            largest, smallest = find_max_min(*numbers)
            print(f"Maximum is {largest}")
            print(f"Minimum is {smallest}")
        else:
            print("No valid numbers were entered.\n")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")


if __name__ == "__main__":
    main()