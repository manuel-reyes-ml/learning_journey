#This program uses Dictionaries, Lists and Tuples to manage data through the flow.

import time
from tabulate import tabulate

#In this funtion we validate user input for file name, we give 3 opportunities until program exits
def read_file():

    fname = None
    handle = None
    fail = 0

    while True:
        #Use input() function to get file name from user
        #We use if conditional to get to the file by pressing 'return'
        fname = input("\nEnter file name: ").lower().strip()
        if len(fname) < 1:
            fname = "mbox-short.txt"
        
        try:
            #Open file to access data - in this case no need to decode it, since we see the file and is TXT
            base_dir = "/Users/manuelreyes/Desktop/dev/learning_journey/courses/python_for_everybody/code/02_data_structures/email_analyzer/data"
            handle = open(f"{base_dir}/{fname}")
            break
        except FileNotFoundError:
            fail += 1
            if fail == 3:
                print(f"Ooops file: {fname} couldn't be opened. Looks like file is not in this directory.")
                print("\nToo many attempts. Program will terminate now...\n")
                quit()
            else:
                print(f"Ooops file: {fname} couldn't be opened. Looks like file is not in this directory.")
                continue
    return handle, fname

#In this function we iterate through each line of file, when our desired line is found we extract email and count
def count_senders(handle):

    total_lines = 0
    unique_senders = 0
    email = None
    emails = dict()

    #Read line by line to get from email and start counting assigning Key, Values to emails amd domains dictionary
    for line in handle: 
        if line.startswith("From "):
            total_lines += 1
            words = line.split()
            email = words[1]
            emails[email] = emails.get(email, 0) + 1
            if emails.get(email) == 1:
                unique_senders += 1

    return emails, total_lines, unique_senders

#In this function we iterate through the emails dict to extract domain and emails' count and create domain dict
def count_domains(**emails):
      
    domain = None      
    domains = dict()

    for email, count in emails.items():
        domain = email.split("@")[1]
        domains[domain] = domains.get(domain, 0) + count
    
    return domains

#In this function we iterate through the dict to find the largest count and identigy its email
def find_top_email(**emails):

    evalue = None
    bemail_count = None
    bemail_word = None

    #items() returns dictionary as a list of tuples - key, value pairs - to assigning largest count to variables
    for email, evalue in emails.items():
        if bemail_count == None or  evalue > bemail_count:
            bemail_count = evalue
            bemail_word = email
    
    return bemail_word, bemail_count

#In this function we iterate through the dict to find the largest count and identigy its domain
def find_top_domain(**domains):

    dvalue = None
    bdomain_count = None
    bdomain_word = None

    for domain, dvalue in domains.items():
        if bdomain_count is None or dvalue > bdomain_count:
            bdomain_count = dvalue
            bdomain_word = domain

    return bdomain_word, bdomain_count

#Write a human readable summary to disk so results can be reused without rerunning the script
def write_summary_to_file(output_file, name, total_lines, unique_senders, bemail_word, bemail_count, bdomain_word, bdomain_count, rows):

    summary_lines = [
        "====================",
        f"Email Summary\nfile: {name}",
        "====================",
        "",
        f"Total Messages: {total_lines}",
        f"Unique Senders: {unique_senders}",
        "",
        f"Top sender:     {bemail_word} ({bemail_count} messages)",
        f"Top domain:     {bdomain_word} ({bdomain_count} messages)",
        "",
        "Senders list:",
        tabulate(rows, headers=["Email Address", "Count"], tablefmt="fancy_grid"),
        "",
    ]

    with open(output_file, "w", encoding="utf-8") as outfile: #open file for writing, create if doesn't exist
        outfile.write("\n".join(summary_lines)) #join list items with newline and write to file

    print(f"Summary saved to {output_file}\n")

#In this function we flip tuples (after dict is unpacked) to sort by count, not email
#reverse = True (default is False) to sort from largest to smallest
def sort_senders(**emails):

    #implement 'key=' and lambda in sorted() function
    esorted_lst = sorted(emails.items(), key=lambda item: item[1], reverse=True)

    """#For more compact use comprehension
    sorted_lst = [(count, email) for email, count in emails.items()]

        #Regular version
        for email, count in emails.items():   
            sorted_lst.append((count, email))
    
        sorted_lst = sorted(sorted_lst, reverse = True)"""

    return esorted_lst

#Call custom functions to get data structurs and calculate results
def main():

    handle, name = read_file()
    print(f"\nFile: {name} has been opened successfully. Retreiving data now...\n")
    time.sleep(2)

    emails, total_lines, unique_senders = count_senders(handle)
    domains = count_domains(**emails)
    print(f"Data from {name} has been processed successfully. Working on calculations now...\n")
    time.sleep(1)

    bemail_word, bemail_count = find_top_email(**emails)
    bdomain_word, bdomain_count = find_top_domain(**domains)
    print("Calculations completed. Printing results below...\n\n")
    time.sleep(1)

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

    #use tabulate library for better output
    rows = sort_senders(**emails)
    senders_table = tabulate(rows, headers=["Email Address", "Count"], tablefmt="fancy_grid")
    print(f"Senders list:\n\n{senders_table}")

    print("\n")

    fwrite = input("Would like to save this report to a TXT file for later use? (Y/N): ").upper().strip()
    if fwrite == "Y":
        ofile = None
        ofile = input("\nEnter file name you would like to use: ").strip()

        #collapse multiple spaces and swap remaining spaces with underscores
        if ofile:
            ofile = "_".join(ofile.split()) # use join/split to collapse spaces
            if not ofile.lower().endswith(".txt"): #append .txt if not provided
                ofile = f"v2_{ofile}" + ".txt"

        #Optionally persist results for later use
        write_summary_to_file(
            ofile if ofile else "v2_email_summary.txt", #if ofile is not empty use it, else use default name
            name,
            total_lines,
            unique_senders,
            bemail_word,
            bemail_count,
            bdomain_word,
            bdomain_count,
            rows,
        )

    elif fwrite == "N":
        print("\nOkay, no file will be created. Exiting now...\n")

    else:
        print("\nInvalid option selected. Exiting now...\n")

    print("\n")



#---PROGRAM STARTS HERE---
if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting now...\n")
        quit()
