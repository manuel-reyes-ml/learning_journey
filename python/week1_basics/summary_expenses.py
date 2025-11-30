num_lst = []

print("\n")

while True:
    svalue = input("Enter an expense amount (or 'done' to finish): ").lower().strip()

    try:
        number = float(svalue)
    
    except ValueError:
        if svalue != "done":
            print(f"'{svalue}' is not a valid number. Please re-enter.\n")
            continue
    else:
        num_lst.append(number)
        continue
    
    if svalue == "done" and len(num_lst) > 0:
            print("\n\n===============")
            print("Expense Summary")
            print("===============\n")
            print(f"Number of expenses: {len(num_lst)}")
            print(f"Total spent: {round(sum(num_lst), 2)}")

            if len(num_lst) > 1:
                print(f"Average expense: {round(sum(num_lst)/len(num_lst), 2)}")
    else:
        print("\nNo expenses entered. Nothing to summarize.")
    
    break

print("\n")


#Used 'finally' for calculations in try/except block - however program ran through finally even after 
# 'continue' is used in 'else'