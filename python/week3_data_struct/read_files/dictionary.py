#Use input() function to get file name from user
#We use if conditional to get to the file by pressing 'return'
fname = input("Enter file name: ").lower().strip()
if len(fname) < 1:
    name = "mbox-short.txt"

#Open file to access data - in this case no need to decode it, since we see the file and is TXT
handle = open(name)

key = None
value = None
emails = dict()

#Read line by line to get from email and start counting assigning Key, Values to dictionary
for line in handle: 
    if line.startswith("From "):
        words = line.split()
        key = words[1]
        emails[key] = emails.get(key, 0) + 1

bigcount = None
bigword = None

#items() returns dictionary as a list of tuples - key, value pairs - to assigning largest count to variables
for key, value in emails.items():
    if bigcount == None or  value > bigcount:
        bigcount = value
        bigword = key

#Print results to screen
print(bigword, bigcount)
