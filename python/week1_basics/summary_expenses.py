import statistics as stats

def main():

    fail = 0
    num_lst = []

    print("\n")

    while True:
        svalue = input("Enter an expense amount (or 'done' to finish): ").lower().strip()

        try:
            number = float(svalue)
        
        except ValueError:
            if svalue != "done":
                fail += 1
                if fail == 3:
                    print("\nToo many attempts. Exiting program now...\n")
                    quit()
                else:
                    print(f"'{svalue}' is not a valid number. Please re-enter.\n")
                    continue
        else:
            num_lst.append(number)
            fail = 0
            continue
        
        if svalue == "done" and len(num_lst) > 0:
                print("\n\n=====================")
                print("Expense Summary (USD)")
                print("=====================\n")
                print(f"Number of expenses: {len(num_lst)}")
                print(f"Total spent: ${round(sum(num_lst), 2)}")

                if len(num_lst) > 1:
                    print(f"Average expense: ${round(stats.mean(num_lst), 2)}")
                    print(f"Highest expense: ${max((num_lst))}")
                    print(f"Lowest expense: ${min(num_lst)}")
        else:
            print("\nNo expenses entered. Nothing to summarize.")
        
        break

    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.\n")
        quit()


#Used 'finally' for calculations in try/except block - however program ran through finally even after 
# 'continue' is used in 'else'