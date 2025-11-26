import time
import statistics as stats

#Custom function that will be called inside to_flt() to force user to use option 1 or 2 (only!)
def entry_type(step, svalue, flt, faile):
        
    if flt not in (1, 2):
        faile += 1
        if faile == 3:
                print(f"\nToo many invalid attempts for {step}. Exiting program.\n")
                quit()
        else:
            svalue = input(f"""\nValue entered: {svalue} is not a valid entry; 
                               Please enter 1 or 2.\n===>Re-enter here: """)
            approved = False
            
    else:
        approved = True
        
    return svalue, approved, faile


#Function to try to convert str to flt (if not go to error), if flt we check the input number to force user
#to use either 1 or 2 - we do this with a separate custom function entry_type()
def to_flt(step,svalue, data_option = False):

    fail = 0
    faile = 0
    while True:
        try:
            flt = float(svalue)
            if not data_option:
                break

            else:
                svalue, approved, faile = entry_type(step, svalue, flt, faile) #2nd custom function

                if approved:
                    break
                else:
                    continue

        except KeyboardInterrupt:
            print("\nProgram terminated by user.\n")
            quit()
        except ValueError:
            fail += 1
            if fail == 3:
                print(f"\nToo many invalid attempts for {step}. Exiting program.\n")
                quit()
            else:
                svalue = input(f"\nValue entered: {svalue} is not a numerical value.\n===>Please re-enter: ")
                continue 
    return flt        

# ----- PROGRAM STARTS HERE -----
entry_format = input("""\nHow you like to enter data?\n
1- By Day
2- One line\n
Enter option number: """)

entry_format = to_flt("Entry Type", entry_format, data_option = True)

price_lst = list()

if entry_format == 1:
    days = input("\nHow many days of prices?: ")
    days = int(to_flt("days", days))

    print("\n")
    
    #Build pice_lst from price per day, after converting them to numbers
    for day in range(days):
        day += 1
        svalue = input(f"Enter price for day {day}: ").strip()
        price = to_flt("price", svalue)
        price_lst.append(price)

    
elif entry_format == 2:
    svalues = input("\nEnter closing prices separated by commas (e.g 100, 101.5, 99.8)\nReply here: ").strip()
    prices = svalues.split(",")

    #Build pice_lst from prices(1 input), after converting them to numbers
    for svalue in prices:
        price = to_flt("price", svalue)
        price_lst.append(price)

print(f"\n\n===============\n  Price List\n===============\n\n{price_lst}")
print("\n\nCalculating Daily Returns now....\n")

time.sleep(3)  #pauses for 3 seconds

returns = list()
for i, price in enumerate(price_lst):  #analyze other versions below
    if i > 0:
        daily_return = ((price_lst[i] - price_lst[i-1]) / price_lst[i-1]) * 100
        daily_return = round(daily_return, 2)
        print(f"Day {i+1}: {daily_return}%")
        returns.append(daily_return)

print("\n")

#avg_return = round(sum(returns) / len(returns), 2)
avg_return = round(stats.mean(returns), 2)
max_return = max(returns)
min_return = min(returns)

print(f"Average Return: {avg_return}%\nMax Return: {max_return}%\nMin Return: {min_return}%\n")

'''
- Other versions using rage() and enumerate() -

for i in range(1, len(price_lst)):
    prev_price = price_lst[i - 1]
    curr_price = price_lst[i]
    daily_return = ((curr_price - prev_price) / prev_price) * 100
    returns.append(daily_return)

    # Start at i = 1 because i = 0 has no previous day.

for i, price in enumerate(price_lst[1:], start=1):
    prev_price = price_lst[i - 1]
    curr_price = price          # same as price_lst[i]
    daily_return = ((curr_price - prev_price) / prev_price) * 100
    daily_returns.append(daily_return)

    Here:

        price_lst[1:] → starts the list from index 1 (second element)
        start=1 → so i still matches the original index in price_lst

    So:

        i → 1, 2, 3, ...
        price → price_lst[i]

    No need to index price itself.
'''
