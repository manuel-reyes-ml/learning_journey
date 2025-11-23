shours = input("Enter hours: ").strip()
srate = input ("Enter rate/hr: ").strip()

ihours = float(shours)
irate = float(srate)

if ihours <= 40:
    tpay = ihours * irate

else:
    ehours = ihours - 40
    tpay = (40 * irate) + (ehours * (irate * 1.5))

print(f"\nTotal Pay is ${tpay}\n")