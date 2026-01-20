fname = input("Enter file name: ").strip().lower()
if len(fname) < 1:
    fname = "mbox-short.txt"

fh = open(fname)

count = 0
for line in fh:
    if not line.startswith("From ") or len(line.strip()) < 2: # safeguard pattern to avoid unexpected traceback for wrong line 
        continue
    words = line.strip().split()
    email = str(words[1])
    print(email)
    count += 1
fh.close()

print(f"There were {count} lines in the file with From as the first word")
    