height = 0
# Prompt the user for the pyramid's height
while True:
    height = input("Enter height between 1 and 8: ")
    if height.isdigit():
        height = int(height)
        if height >= 1 and height < 8:
            break
    else:
        height = 0

# Print a pyramid for that height        
for i in range(height):
    
    # Inner Loop 1: Print the spaces
    for j in range(height - i - 1):
        print(" ", end="")
    # Inner loop 2: Print left hashes
    for k in range(i + 1):
        print("#", end="")
    # THE GAP: Print 2 spaces (no loop needed, it's constant)    
    print("  ", end="")
    # Inner loop 3: Print right hashes    
    for l in range(i + 1):
        print("#", end="")
            
    print("\n", end="") 