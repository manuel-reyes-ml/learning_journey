# test overtime_pay.py import
import overtime_pay

print("\nImported overtime_pay module successfully.\n")

run = input("Do you want to run the progam? Y/N: ").upper().strip()

#If 'Yes' this program will launch overtime_pay script and run main() function (main program)
if run == "Y":
    overtime_pay.tpay()
else:
    print("\nProgram terminated by user.\n")
    quit()