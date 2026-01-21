# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008

fname = input("Enter file name: ").strip().lower()
if len(fname) < 1:
    fname = "mbox-short.txt"

fh = open(fname)

hour_counter = dict()
for line in fh:
    if not line.startswith("From ") or len(line.strip().split()) < 6:
        continue
    words = line.strip().split()
    hour, _, _ = words[5].partition(":")
    hour_counter[hour] = hour_counter.get(hour, 0) + 1

for (hour, count) in sorted(hour_counter.items()):
    print(hour, count)
    