height = 0
# Prompt the user for the pyramid's height
while True:
    height = input("Enter height between 1 and 8: ")
    if height.isdigit():
        height = int(height)
        if height > 1 and height < 8:
            break
    else:
        height = 0
        
for i in range(height):
        
    for j in range(height - i - 1):
        print(" ", end="")
        
    for k in range(i + 1):
        print("#", end="")
        
    print("  ", end="")
        
    for l in range(i + 1):
        print("#", end="")
            
    print("\n", end="")