import time

def to_flt(step,svalue):

    fail = 0
    while True:
        try:
            flt = float(svalue)
            break
        except KeyboardInterrupt:
            print("\nProgram terminated by user.\n")
            quit()
        except ValueError:
            fail += 1
            if fail == 3:
                print(f"\nToo many invalid attempts for {step}. Exiting program.\n")
                quit()
            else:
                svalue = input(f"\nValue entered: {svalue} is not a valid or a numerical value.\n===>Please re-enter: ")
                continue
    return flt

format = input("""\nHow you like to enter data?\n
1- By Day
2- One line\n
Enter option number: """)

price_lst = list()
if format == "1":
    days = input("\nHow many days of prices?: ")
    days = int(to_flt("days", days))
    
    #Build pice_lst from price per day, after converting them to numbers
    for day in range(days):
        day += 1
        svalue = input(f"Enter price for day {day}: ").strip()
        price = to_flt("price", svalue)
        price_lst.append(price)

    
elif format == "2":
    svalues = input("\nEnter closing prices separated by commas (e.g 100, 101.5, 99.8): ").strip()
    prices = svalues.split(",")

    #Build pice_lst from prices(1 input), after converting them to numbers
    for svalue in prices:
        price = to_flt("price", svalue)
        price_lst.append(price)

print(f"\n\n===============\n  Price List\n===============\n\n{price_lst}")
print("\n\nCalculating Daily Returns now....\n")

time.sleep(3)  #pauses for 3 seconds

returns = list()
for i, price in enumerate(price_lst):  #analyze another versions below
    if i > 0:
        daily_return = ((price_lst[i] - price_lst[i-1]) / price_lst[i-1]) * 100
        daily_return = round(daily_return, 2)
        print(f"Day {i+1}: {daily_return}%")
        returns.append(daily_return)

print("\n")

avg_return = round(sum(returns) / len(returns), 2)
max_return = max(returns)
min_return = min(returns)

print(f"Average Return: {avg_return}%\nMax Return: {max_return}%\nMin Return: {min_return}%\n")

'''
- Another version using rage() and enumerate() -

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
