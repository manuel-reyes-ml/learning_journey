import time

#Use input() function to get file name from user
#We use if conditional to get to the file by pressing 'return'
fname = input("\nEnter file name: ").lower().strip()
if len(fname) < 1:
    name = "mbox-short.txt"

#Open file to access data - in this case no need to decode it, since we see the file and is TXT
handle = open(name)

print(f"\nFile: {name} has been opened successfully. Retreiving data now...\n")
time.sleep(2)

total_lines = 0
unique_senders = 0
email = None
evalue = None
domain = None
dvalue = None
emails = dict()
domains = dict()

#Read line by line to get from email and start counting assigning Key, Values to dictionary
for line in handle: 
    if line.startswith("From "):
        total_lines += 1
        words = line.split()
        email = words[1]
        emails[email] = emails.get(email, 0) + 1
        if emails.get(email) == 1:
            unique_senders += 1

        domain = email.split("@")[1]
        domains[domain] = domains.get(domain, 0) + 1
        

print(f"Data from {name} has been processed successfully. Working on calculations now...\n")
time.sleep(1)

bdomain_count = None
bdomain_word = None
bemail_count = None
bemail_word = None

#items() returns dictionary as a list of tuples - key, value pairs - to assigning largest count to variables
for email, evalue in emails.items():
    if bemail_count == None or  evalue > bemail_count:
        bemail_count = evalue
        bemail_word = email

for domain, dvalue in domains.items():
    if bdomain_count == None or dvalue > bdomain_count:
        bdomain_count = dvalue
        bdomain_word = domain


print("Calculations completed. Printing results below...\n\n")

#Print results to screen
print("====================")
print(f"Email Summary\nfile: {name}")
print("====================\n\n")

print(f"Total Messages: {total_lines}")
print(f"Unique Senders: {unique_senders}")
print("\n")
print(f"Top sender:     {bemail_word} ({bemail_count} messages)")
print(f"Top domain:     {bdomain_word} ({bdomain_count} messages)")
print("\n")

