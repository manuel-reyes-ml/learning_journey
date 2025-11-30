#Use input() function separately to retrieve user data for each variable
#Use strip() function to remove white space from both sides of the string (letf and right)
#Use float() function to convert from string to float, if string is a number
rate = float(input("Hourly rate: ").strip())
hours = float(input("Hours worked: ").strip())

#Use variables to calculate amount and assign it to pay (variable)
pay = rate * hours

#Use print() function to output the content of pay (variable) to the screen
#Use f"" to include both string and variable under double quote
print(f"Total pay is: {pay}")