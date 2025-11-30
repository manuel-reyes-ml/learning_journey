#Creating function first to use it two or more times in the program - NOT REPEATING CODE
def get_value(request):

    fail = 0

    while True:
    
        #Use try/except block to catch error and handling them without the program to crash
        try:
            #Requests user input and 'try' to convert it to float, if error go to 'except'
            sinput = input(f"Enter {request}: ").strip()
            fvalue = float(sinput)
            break
        #If user enters Control+C, except will be triggered and program will exit out, quit()
        except KeyboardInterrupt:
            print("\nProgram terminated by user.\n")
            quit()
        #If if user enters a string of letters, ValueError will be triggered as input validation sequence
        except ValueError:
            fail += 1
            if fail == 3:
                print(f"\nToo many invalid attempts for {request}. Exiting program.\n")
                quit()
            else:
                print(f"Value entered: {sinput} is not a numerical value. Please re-enter\n")
                continue
    return fvalue

def main():
    #Use custom functions to retrieve data from and converting to float, handling input validation
    ihours = get_value("hours")
    irate = get_value("rate/hr")

    #Use conditionals to identify if normal pay or overtime calculation applies
    if ihours <= 40:
        tpay = ihours * irate

    else:
        ehours = ihours - 40
        tpay = (40 * irate) + (ehours * (irate * 1.5))

    print(f"\nTotal Pay is ${tpay}\n")

#Program starts here, calling main() function
if __name__ == "__main__":
    main()