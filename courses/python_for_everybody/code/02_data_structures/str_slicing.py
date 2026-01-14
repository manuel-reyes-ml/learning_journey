text = "X-DSPAM-Confidence:    0.8475"


# 1) Using find() to slice the string

'''
# Find the position of the first occurrence of ":"
pos = text.find(":")

# Extract the substring from that position to the end and convert to float
snum = text[pos+1:].strip()
inum = float(snum)

print(f"Decimal number: {inum}")
'''

# 2) Using regular expressions(regex) to extract the floating-point number

import re

# Use regex to find the floating-point number in the string
# re.search() returns a match object if found, otherwise None
#   [-+]? matches an optional sign
#   \d* matches zero or more digits before the decimal point
#   \. matches the decimal point 
#   \d+ matches one or more digits after the decimal point
match = re.search(r"[-+]?\d*\.\d+", text)
if match:
    inum = float(match.group()) # .group() retrieves the matched string
    print(f"Decimal number: {inum}")
else:
    print("No floating-point number found.")