# function to convert score to grade
def print_grade(score):
    
    while True:
        
        if 0.0 <= score <= 1.0:
            if score >= 0.9:
                return 'A'
            elif score >= 0.8:
                return 'B'
            elif score >= 0.7:
                return 'C'
            elif score >= 0.6:
                return 'D'
            elif score < 0.6:
                return 'F'
        else:
            return 'Invalid score'
        
# function to handle user input and validate score. Give 3 attempts for valid input.
def input_score():
    
    fail = 0 
    while True:
        score = input("Enter score: ").strip()
        
        try: 
            score = float(score)
            score = print_grade(score)
            if score != "Invalid score":
                return score
            else:
                fail += 1
                if fail >= 3:
                    print("Too many invalid attempts. Exiting.\n")
                    break
                print(f"{score}\n")
                continue
        except ValueError:
            fail += 1
            if fail >= 3:
                print("Too many invalid attempts. Exiting.\n")
                break
            print("Invalid input. Please enter a numeric value.\n")
            continue

# main function to run the program
def main():
    
    try:
        score = input_score()
        if score:
            print(f"Grade: {score}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting.")

# entry point of the program
if __name__ == "__main__":
    main()