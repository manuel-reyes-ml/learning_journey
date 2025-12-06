# Notes from Computer Science Harvard:

## Computational Thinking

	•	What is an algorithm?
            Series of orderly steps needed to solve a problem
	•	Pseudocode examples.
            Describe the steps needed to solve a problem in our own words (no code expressions)
	•	Types of data: bool, int, string, etc.
	•	High-level vs low-level languages.

1 Byte = 8 Bits —> 1 bit can be only 0 and 1 (Binary) (transistor - on and off) = power of 2 — count until 256 (number)

bits on the left has more weight:
 0    0    0    0    0    0    0    0
256  128   64   32  16    8    4    2

## Cmds in command line:

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

## Algorithms

Algorithm = step by step instructions to solve a problem.

To do search more efficient we can use binary search (dividing in half each iteration and going to right or left of the array to the half of that slice)

binary search does not work if the data is not sorted first. 

the other option is linear search = going "door by door” searching until value is found (or not) -- takes more time. 

A good Algorithm is efficient in terms of Running time - investigate (better engineers write better better algorithms with better Running time.)

Investigate more about recursive algorithms** Use print bricks (hashtags) as example