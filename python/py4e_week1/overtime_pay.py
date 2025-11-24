#Creating function first to use it two or more times in the program - NOT REPEATING CODE

def get_value(request):

    fail = 0

    while True:
    
        try:
            sinput = input(f"Enter {request}: ").strip()
            fvalue = float(sinput)
            break
        except KeyboardInterrupt:
            print("\nProgram terminated by user.\n")
            quit()
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
    ihours = get_value("hours")
    irate = get_value("rate/hr")

    if ihours <= 40:
        tpay = ihours * irate

    else:
        ehours = ihours - 40
        tpay = (40 * irate) + (ehours * (irate * 1.5))

    print(f"\nTotal Pay is ${tpay}\n")

if __name__ == "__main__":
    main()