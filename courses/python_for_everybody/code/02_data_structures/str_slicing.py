text = "X-DSPAM-Confidence:    0.8475"

# 1) Using find() to slice the string

# Find the position of the first occurrence of ":"
pos = text.find(":")

# Extract the substring from that position to the end and convert to float
snum = text[pos+1:].strip()
inum = float(snum)

print(inum)


