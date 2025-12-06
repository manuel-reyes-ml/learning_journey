import statistics as stats
import time
from tabulate import tabulate

#Category string validation function
def str_validation():

    sfail = 0

    while True:
        
        category = input("Enter a category (e.g. food, rent, transport, other): ").lower().strip()
        
        if category == "done":
            break

        try:
            category = int(category)
        
        except ValueError:
                category = category.capitalize()
                sfail = 0
                break
        else:
            sfail += 1
            if sfail == 3:
                print("\nToo many attempts. Exiting program now...\n")
                quit()
            else:    
                print(f"{category} is not a valid string. Category was not saved.\n")
    
    return category

#Expense amount user input and validation function
def user_input():

    ifail = 0
    category = None
    number = None

    print("\n")

    while True:
        #Use input() function to retrieve a string of numbers from user
        #Use lower() function to validate if 'done' has been enter
        #User strip() function to remove white space from both sides (left and right)
        svalue = input("Enter an expense amount (or 'done' to finish): ").lower().strip()

        if svalue == "done":
            break

        #Use try/except block to 'try' and convert string number to float, if not, program will handle error
        try:
            number = float(svalue)
        
        except ValueError:
            #When trying to convert string of letter, give user 3 opportunities to enter accepted format if not
            #program will exit out automatically
            ifail += 1
            if ifail == 3:
                print("\nToo many attempts. Exiting program now...\n")
                quit()
            else:
                print(f"'{svalue}' is not a valid number. Amount was not saved.\n")
                continue
        #Use 'else' inside 'try/except' block to run code only if no exception was found
        #If string was converted to float successfully we add it to num_lst list
        else:
            ifail = 0
            category = str_validation()
            break

    return category, number, svalue

#Function to build dictionary with categories as keys and list of amounts as values 
def build_dict(key, value, **dictionary):

    if dictionary.get(key, "missing") == "missing":
        cat_lst = []
        cat_lst.append(value)  #need to append first and then assign to dict
        dictionary[key] = cat_lst
    else:
        dictionary.get(key).append(value)

    return dictionary


def main():

    expenses = dict()

    while True:
    
        category, number, svalue = user_input()

        if category != "done" and svalue != "done":
            expenses = build_dict(category, number, **expenses)
        else:
            break
    
    print("\nCalculating summary statistics...\n")

    time.sleep(1)
    #Print summary statistics for each category
    for cat, amounts in expenses.items(): #
        total = sum(amounts)
        count = len(amounts)
        average = stats.mean(amounts)
        minimum = min(amounts)
        maximum = max(amounts)

        print(f"\nCategory: {cat}")
        print(f"  Total expenses: ${total:.2f}") #use f strings to format float to 2 decimal places
        print(f"  Number of entries: {count}")
        print(f"  Average expense: ${average:.2f}")
        print(f"  Minimum expense: ${minimum:.2f}")
        print(f"  Maximum expense: ${maximum:.2f}\n")
        print("-" * 40)
    
    print("-" * 40)
    print("\nList of expenses from largest to smallest:\n")

    time.sleep(1)
    #Print table of total expenses by category sorted from largest to smallest
    print_lst = []
    for cat, amounts in sorted(expenses.items(), key=lambda item: sum(item[1]), reverse=True):
        total = f"${sum(amounts):.2f}"
        print_lst.append((cat, total))
    
    print(tabulate(print_lst, headers=["Category", "Total Expenses"], tablefmt="fancy_grid"))
    print("\n")
    

    #print("\n\n Summary of expenses by category:\n")
    #print(f"\n\n Expenses data: {expenses}\n")


#---PROGRAM STARTS HERE---
if __name__ == "__main__":
    #Using try/except block to identify if user wants to terminate program early by using Ctrl + C
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.\n")
        quit()


#Used 'finally' for calculations in try/except block - however program ran through finally even after 
# 'continue' is used in 'else'