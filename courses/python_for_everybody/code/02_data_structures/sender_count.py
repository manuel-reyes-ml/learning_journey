fname = input("Enter file name: ").strip().lower()
if len(fname) < 1:
    fname = "mbox-short.txt"

fh = open(fname)

sender_counter = dict()
for line in fh:
    if not line.startswith("From ") or len(line.strip()) < 2:
        continue
    words = line.strip().split()
    email = words[1].strip().lower()
    sender_counter[email] = sender_counter.get(email, 0) + 1
fh.close()

max_value = None
max_email = None
for k,v in sender_counter.items():
    if max_value is None or int(v) > max_value:
        max_value = int(v)
        max_email = k

print(max_email, max_value)
    