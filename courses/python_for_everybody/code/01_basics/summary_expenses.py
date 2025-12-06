import statistics as stats

def main():

    fail = 0
    num_lst = []

    print("\n")

    while True:
        #Use input() function to retrieve a string of numbers from user
        #Use lower() function to validate if 'done' has been enter
        #User strip() function to remove white space from both sides (left and right)
        svalue = input("Enter an expense amount (or 'done' to finish): ").lower().strip()

        #Use try/except block to 'try' and convert string number to float, if not, program will handle error
        try:
            number = float(svalue)
        
        except ValueError:
            #When trying to convert string of letter, give user 3 opportunities to enter accepted format if not
            #program will exit out automatically
            if svalue != "done":
                fail += 1
                if fail == 3:
                    print("\nToo many attempts. Exiting program now...\n")
                    quit()
                else:
                    print(f"'{svalue}' is not a valid number. Please re-enter.\n")
                    continue
        #Use 'else' inside 'try/except' block to run code only if no exception was found
        #If string was converted to float successfully we add it to num_lst list
        else:
            num_lst.append(number)
            fail = 0
            continue
        
        #If user enter 'done' we move from enter new values and start calculating results
        #If num_lst has more than 1 expenses we calculate everything, if not just numer of expenses and total
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
                    
        #If user didn´t enter anything we provide a message and exit out the program
        else:
            print("\nNo expenses entered. Nothing to summarize.")
        
        break

    print("\n")

#Program starts here
if __name__ == "__main__":
    #Using try/except block to identify if user wants to terminate program early by using Ctrl + C
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.\n")
        quit()


#Used 'finally' for calculations in try/except block - however program ran through finally even after 
# 'continue' is used in 'else'