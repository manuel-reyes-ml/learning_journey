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
            handle = open(fname)
            first_char = handle.read(1)  # Try reading the first character to ensure it's readable
            if not first_char:
                raise ValueError("File is empty or unreadable. Exiting now.")
            
            handle.seek(0)  # Reset file pointer to the beginning
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

    print(f"\nFile: {fname} has been opened successfully. Retreiving data now...\n")
    time.sleep(2)

    return handle, fname

def create_dict(handle, data):

    total_lines = 0
    unique_senders = 0
    datas = dict()
    
    #Read line by line to get from email and start counting assigning Key, Values to emails amd domains dictionary
    for line in handle: 
        if line.startswith("From "):
            total_lines += 1
            words = line.split()
            
            # Use a lambda function to extract email or domain based on 'data' parameter
            extractor = lambda words: words[1].split("@")[1] if data == "domain" else words[1]
            value = extractor(words)
           
            datas[value] = datas.get(value, 0) + 1
            if datas.get(value) == 1:
                unique_senders += 1

    return datas, total_lines, unique_senders

#
def count_senders(handle):

    return create_dict(handle, "email")

#In this function we iterate through the emails dict to extract domain and emails' count and create domain dict
def count_domains(handle):
    
    return create_dict(handle, "domain")

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
def main(choice, menu_choice, *menu_functions):

    handle, name = read_file()

    #Function to execute selected functions based on menu choice
    def execute_functions(*func_list):
        results = {}
        for func in func_list:
            if func == count_senders:
                results['emails'], results['total_lines'], results['unique_senders'] = func(handle)
            elif func == count_domains:
                results['domains'], results['total_lines'], results['unique_senders'] = func(handle)
            elif func == find_top_email:
                results['bemail_word'], results['bemail_count'] = func(**results['emails'])
            elif func == find_top_domain:
                results['bdomain_word'], results['bdomain_count'] = func(**results['domains'])
        return results

    results = execute_functions(*menu_functions)

    print(f"Data from {name} has been processed successfully. Working on calculations now...\n")
    time.sleep(1)

    #Extracting results from the dictionary, values assigned default values if key not found
    emails = results.get('emails', {})
    total_lines = results.get('total_lines', 0)
    unique_senders = results.get('unique_senders', 0)
    domains = results.get('domains', {})
    bemail_word = results.get('bemail_word', '')
    bemail_count = results.get('bemail_count', 0)
    bdomain_word = results.get('bdomain_word', '')
    bdomain_count = results.get('bdomain_count', 0)

    print("Calculations completed. Printing results below...\n\n")
    time.sleep(1)

    #Print results to screen
    print("====================")
    print(f"Email Summary\nfile: {name}")
    print("====================")
    print(f"\nReport: {choice}\n\n")

    print(f"Total Messages: {total_lines}")
    print(f"Unique Senders: {unique_senders}")
    print("\n")

    if menu_choice == "1":
        print(f"Top sender:     {bemail_word} ({bemail_count} messages)")
        print("\n")

        #use tabulate library for better output
        rows = sort_senders(**emails)
        senders_table = tabulate(rows, headers=["Email Address", "Count"], tablefmt="fancy_grid")
        print(f"Senders list:\n\n{senders_table}")
        print("\n")

    elif menu_choice == "2":
        print(f"Top domain:     {bdomain_word} ({bdomain_count} messages)")
        print("\n")

    elif menu_choice == "3":
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
                    ofile = ofile + "v3.txt"

            #Optionally persist results for later use
            write_summary_to_file(
                ofile if ofile else "email_summaryv3.txt", #if ofile is not empty use it, else use default name
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
        #Implementing menu to select what data to show
        menu = {"1": "Senders stats", "2": "Domain stats", "3": "All data", "4": "Exit"}
        menu_table = tabulate(menu.items(), headers=["Option", "Description"], tablefmt="github")

        print("\nWelcome to the Email Summary Program!\n")
        print("This program processes a text file containing email data and provides a summary of email senders and their domains.\n")
        print("Menu Options:\n")
        print(menu_table)
        print("\n")
        time.sleep(1)

        menu_choice = input("Please select an option from the menu above (1-4): ").strip()
        if menu_choice in menu:
            print(f"\nYou selected option {menu_choice}: {menu[menu_choice]}\n")
            if menu_choice == "4":
                print("\nExiting program. Goodbye!\n")
                quit()
        else:   
            print("\nInvalid option selected. Exiting now...\n")
            quit() 

        func_menu = {
            "1": [count_senders, find_top_email],
            "2": [count_domains, find_top_domain],
            "3": [count_senders, count_domains, find_top_email, find_top_domain]}
        
        main(menu.get(menu_choice), menu_choice, *func_menu[menu_choice])

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting now...\n")
        quit()
