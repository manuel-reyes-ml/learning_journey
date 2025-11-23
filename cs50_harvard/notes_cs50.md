## Notes from Computer Science Harvard:

1 Byte = 8 Bits —> 1 bit can be only 0 and 1 (Binary) (transistor - on and off) = power of 2 — count until 256 (number)

bits on the left has more weight:
 0    0    0    0    0    0    0    0
256  128   64   32  16    8    4    2

# Cmds in command line:

ls = list of files
mv = move file (hello.c hello) or rename a file
mkdir = create a new folder
cp = copy a file
rm = remove a file 
cd = enter a folder
.. = refers to the parent directory / folder
rmdir = remove directory/folder
Control + c =  terminate a program

In C we need to compile program first by code (name of the program - without .c) in the command line to produce another file to run the program.

Python: cmmd touch to create a new .py file in VS code terminal (at last)

run the program in C = ./file-name (without .c)

Debugging technique: using printf (c) or print() (python) to see the variables or data or loos in motion
**but using print function is not good, since we need to remember to erase after code is finish. A SPECIAL TOOL THAT WILL SAVE HOURS in VS code is run debug50 ./buggy (filename) and put a breakpoint and see the variables in memory line by line**

write in command: echo $? (return of program failure or succesful) only for C?