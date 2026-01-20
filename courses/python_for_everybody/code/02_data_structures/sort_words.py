
fname = input("Enter file name: ").strip().lower()
if fname == "":
    fname = "romeo.txt"

fh = open(fname)
word_list = list()
for line in fh:
    if line.strip() == "":
        continue
    words = line.strip().split()
    for word in words:
        if word not in word_list:
            word_list.append(word.strip())
        
word_list.sort()

print(word_list)


