fail = 0

while True:
 
 shours = input("Enter hours: ").strip()
 try:
    ihours = float(shours)
    break
 except KeyboardInterrupt:
    print("\nProgram terminated by user.\n")
    quit()
 except ValueError:
    fail += 1
    if fail == 3:
       print("\nTo many invalid attempts for hours. Exiting progam.\n")
       quit()
    else:
     print(f"Value entered: {shours} is not a numerical value. Please re-enter")
     continue

fail = 0

while True:
 
 srate = input ("Enter rate/hr: ").strip()
 try:
    irate = float(srate)
    break
 except KeyboardInterrupt: #When the user presses Ctrl+C
    quit()
 except ValueError: #conversion problems, wrong value
    fail += 1
    if fail == 3:
       print("\nTo many invalid attempts for rate/hr. Exiting progam.\n")
       quit()
    else:
     print(f"Value entered: {srate} is not a numerical value. Please re-enter")
     continue
 
fail = 0

if ihours <= 40:
    tpay = ihours * irate

else:
    ehours = ihours - 40
    tpay = (40 * irate) + (ehours * (irate * 1.5))

print(f"\nTotal Pay is ${tpay}\n")