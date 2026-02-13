# Step 1: Create a translation table
table = str.maketrans("abc", "xyz")

# Step 2: See what the table looks like
print(f"Table: {table}")
# Table: {97: 120, 98: 121, 99: 122}
# Keys = ASCII codes of original characters
# Values = ASCII codes of replacement characters

print(f"Type: {type(table)}") 
# Type: <class 'dict'>


# ord() gives the ASCII number of a character
print(f"ord('a') = {ord('a')}")  # 97
print(f"ord('b') = {ord('b')}")  # 98
print(f"ord('c') = {ord('c')}")  # 99

print(f"ord('x') = {ord('x')}")  # 120
print(f"ord('y') = {ord('y')}")  # 121
print(f"ord('z') = {ord('z')}")  # 122

# char() gives the ASCHII character of a number
print(chr(97))   # 'a'
print(chr(98))   # 'b'
print(chr(65))   # 'A'
print(chr(49))   # '1'
print(chr(32))   # ' '


# Step 3: Run translation (substitution)
# Simple example
text = "abcdef"
result = text.translate(table)

print(f"Original: {text}")
print(f"Translated: {result}")

# Using cipher strings
alphabet = "abcdefghijklmnopqrstuvwxyz"
key =      "nqxpomaftrhlzgecyjiuwskdvb"

# Create translation table: a→n, b→q, c→x, d→p, etc.
table = str.maketrans(alphabet, key)

text_cipher = "hello"
result_cipher = text.translate(table)

print(f"Original: {text_cipher}")
print(f"Encrypted: {result_cipher}")