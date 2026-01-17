fname = input("Enter file name: ")
if fname == "":
    fname = "mbox-short.txt"

fhand = open(fname)

total_numbers = 0
count = 0

for line in fhand:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    colon_pos = line.find(":")
    number_str = line[colon_pos + 1:]
    number_flt = float(number_str)
    total_numbers = total_numbers + number_flt
    count = count + 1

average = total_numbers / count
print("Average spam confidence:", average)