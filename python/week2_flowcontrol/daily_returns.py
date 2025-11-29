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
                               Please enter 1 or 2.\n===>Re-enter here: """).strip()
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

        except ValueError:
            fail += 1
            if fail == 3:
                print(f"\nToo many invalid attempts for {step}. Exiting program.\n")
                quit()
            else:
                svalue = input(f"\nValue entered: {svalue} is not a numerical value.\n===>Please re-enter: ").strip()
                continue 
    return flt 

#Function to be called from main() only when data range is not valid for the algorithm to process = 
# (> 2 day closing prices)
def min_data(entry_format):

    fail = 0
    while True:

            fail +=1
            if fail == 3:
                print("\nToo many invalid attempts for Data Range. Exiting program.\n")
                quit()
            elif entry_format == 1:
                days = input("\nAlgorithm requires min 2 days. Please re-enter: ").strip()
                data_range = int(to_flt("Data Range", days))

                if data_range >= 2:
                    break
                
            elif entry_format == 2:
                data_range = []
                svalues = input("\nAlgorithm requires min 2 days of closing prices. Please re-enter \nclosing prices separated by commas: ").strip()
                prices = svalues.split(",")

                data_range = [to_flt("Price", svalue) for svalue in prices] #Test list comprehesion method
           
                #for svalue in prices:
                    #price = to_flt("Price", svalue)
                    #data_range.append(price)

                if len(data_range) >= 2:
                    break
            else:
                continue

    return data_range


def main():

    try:
        entry_format = input("""\n-Press Ctrl+C anytime to exit program-\n\nHow you like to enter data?\n
        1- By Day
        2- One line\n
        Enter option number: """).strip()

        entry_format = to_flt("Entry Type", entry_format, data_option = True)

        price_lst = list()

        if entry_format == 1:
            days = input("\nHow many days of prices?: ").strip()
            days = int(to_flt("Days", days))
            
            if days < 2:
                days = min_data(entry_format) #call function to force user to enter at least 2 closing prices

            print("\n")
            
            #Build price_lst from price per day, after converting them to numbers
            for day in range(days):
                day += 1
                svalue = input(f"Enter price for day {day}: ").strip()
                price = to_flt("Price", svalue)
                price_lst.append(price)

            
        else: #we defined that user can only enter option 1 or 2 in line 71
            svalues = input("\nEnter closing prices separated by commas (e.g 100, 101.5, 99.8)\nReply here: ").strip()
            prices = svalues.split(",")

            #Build pice_lst from prices(1 input as list), after converting them to numbers
            
            price_lst = [to_flt("Price", svalue) for price in prices] #test list comprehension
        
            #Old version below
            #for svalue in prices:
                #price = to_flt("Price", svalue)
                #price_lst.append(price)
            
            if len(price_lst) < 2:
                price_lst = min_data(entry_format) #call function to force user to enter at least 2 closing prices

        print(f"\n\n===============\n  Price List\n===============\n\n{price_lst}")
        print("\n\nCalculating Daily Returns now....\n")

        time.sleep(3)  #pauses for 3 seconds

        returns = list()
        for i, price in enumerate(price_lst):  #analyze other versions below at line 115
            if i > 0:
                daily_return = ((price_lst[i] - price_lst[i-1]) / price_lst[i-1]) * 100
                daily_return = round(daily_return, 2)
                print(f"Day {i+1}: {daily_return}%")
                returns.append(daily_return)

        print("\n")

        #avg_return = round(sum(returns) / len(returns), 2)
        avg_return = round(stats.mean(returns), 2)  #---> using statistics module instead (imported in line 2)
        max_return = max(returns)
        min_return = min(returns)

        print(f"Average Return: {avg_return}%\nMax Return: {max_return}%\nMin Return: {min_return}%\n")
    
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!\n")
        quit()

# ----- PROGRAM STARTS HERE -----
while True:
    if __name__ == "__main__":
        main()
    next = input("Would you like to analize more data? Y/N: ").upper().strip()

    if next == "Y":
        continue
    else:
        print("\n\nProgram terminated by user. Goodbye!\n")
        quit()

'''
- Other versions using rage() and enumerate() - line 96

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
