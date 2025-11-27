# test overtime_pay.py import

import overtime_pay

print("\nImported overtime_pay module successfully.\n")

run = input("Do you want to run the progam? Y/N: ").upper().strip()

if run == "Y":
    overtime_pay.main()
else:
    print("\nProgram terminated by user.\n")
    quit()