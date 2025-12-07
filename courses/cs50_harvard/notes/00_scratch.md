# 00: Scratch

**Course:** CS50: Introduction to Computer Science  
**Platform:** edX / Harvard  
**Instructor:** David J. Malan  
**Week:** 0  
**Started:** Nov 2025  
**Status:** In progress

---

## 📚 Overview

Introduction to computational thinking using Scratch, a visual programming language. Learn fundamental programming concepts (loops, conditions, variables, events) without syntax complexity. Build your first interactive program using drag-and-drop blocks.

---

## ✅ Progress

- [x] Lecture: Introduction to Computer Science
- [x] Sections: Scratch basics
- [ ] Problem Set 0: Create a Scratch project
- [ ] Lab 0: (Optional warm-up)

---

## 🎯 Key Concepts

### What is Computer Science?

**What it is:**  
Computer science is problem-solving. Taking inputs, processing them through algorithms, and producing outputs.

**Why it matters:**  
Understanding how computers solve problems helps you think algorithmically - breaking big problems into smaller, solvable steps.

**Key points:**
- **Input → Algorithm → Output:** Core model of computing
- **Binary:** Computers use only 0s and 1s (bits)
- **Abstraction:** Hide complexity, focus on what matters
- **Algorithms:** Step-by-step instructions to solve problems
- **Computational thinking:** Problem-solving approach used in CS

---

### Binary and Representation

**What it is:**  
Computers represent everything (numbers, text, images, sound) using only binary digits (0 and 1).

**Why it matters:**  
Understanding how computers store information reveals limitations (overflow, precision) and capabilities.

**Key points:**
- **Bit:** Single binary digit (0 or 1)
- **Byte:** 8 bits (can represent 0-255)
- **Decimal to binary:** 123 in decimal = 1111011 in binary
- **ASCII:** Standard for representing text (A = 65, a = 97)
- **Unicode:** Modern standard supporting all languages (emoji too!)
- **RGB:** Colors as three numbers (Red, Green, Blue)

1 Byte = 8 Bits —> 1 bit can be only 0 and 1 (Binary) (transistor - on and off) = power of 2 — count until 256 (number)

bits on the left has more weight:
 0    0    0    0    0    0    0    0
256  128   64   32  16    8    4    2

---

### Programming Fundamentals (in Scratch)

**What it is:**  
Core programming constructs that exist in all languages - just represented visually in Scratch.

**Why it matters:**  
These concepts transfer to every programming language. Master them once, apply everywhere.

**Key points:**
- **Functions:** Reusable blocks of code (like "say Hello")
- **Conditions:** Make decisions (if/else)
- **Boolean expressions:** True/false questions (touching edge?)
- **Loops:** Repeat actions (forever, repeat 10, until)
- **Variables:** Store data (score, lives, speed)
- **Events:** Trigger code (when flag clicked, when key pressed)
- **Threads:** Multiple scripts running simultaneously

---

### Scratch Blocks

**What it is:**  
Visual programming blocks that snap together like LEGO. Different colors for different categories.

**Why it matters:**  
No syntax errors! Focus on logic, not memorizing keywords. Great for prototyping ideas.

**Block categories:**
- **Motion (blue):** Move sprite, turn, go to position
- **Looks (purple):** Show/hide, change costume, say/think
- **Sound (pink):** Play sounds, change volume
- **Events (yellow):** When flag clicked, when key pressed, broadcast
- **Control (orange):** If/else, loops, wait
- **Sensing (light blue):** Detect key pressed, touching, mouse position
- **Operators (green):** Math, comparison, logic (and/or/not)
- **Variables (orange):** Create/set/change variables
- **My Blocks (red):** Create custom functions

---

## 💻 Scratch Examples

### Example 1: Basic Movement

**Blocks:**
```
When [flag] clicked
Forever
    Move (10) steps
    If <touching [edge]?> then
        Turn (180) degrees
    End
End
```

**What it does:** Sprite moves forward continuously, bounces off edges

**Concepts:** Event, loop, condition, sensing

---

### Example 2: User Input

**Blocks:**
```
When [flag] clicked
Ask [What's your name?] and wait
Say (join [Hello, ] (answer)) for (2) seconds
```

**What it does:** Asks for name, greets user

**Concepts:** Event, input, string concatenation, output

---

### Example 3: Counter with Variable

**Blocks:**
```
When [flag] clicked
Set [counter] to (0)
Forever
    Wait (1) seconds
    Change [counter] by (1)
    Say (counter)
End
```

**What it does:** Counts up every second

**Concepts:** Variables, loops, wait

---

### Example 4: Interactive Game Loop

**Blocks:**
```
When [flag] clicked
Set [score] to (0)
Forever
    If <key [space] pressed?> then
        Change [score] by (1)
        Play sound [pop]
    End
End
```

**What it does:** Increases score when space pressed

**Concepts:** Game loop, input detection, score tracking

---

### Example 5: Multiple Sprites (Threads)

**Sprite 1:**
```
When [flag] clicked
Forever
    Move (5) steps
End
```

**Sprite 2:**
```
When [flag] clicked
Forever
    Turn (15) degrees
End
```

**What it does:** Two sprites moving independently at the same time

**Concepts:** Concurrency, parallel execution

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Algorithm** | Step-by-step instructions | Recipe, GPS directions |
| **Binary** | Base-2 number system (0s and 1s) | 101 = 5 in decimal |
| **Bit** | Single binary digit | 0 or 1 |
| **Byte** | 8 bits | Can represent 0-255 |
| **ASCII** | Character encoding standard | 'A' = 65 |
| **Sprite** | Character/object in Scratch | Cat, ball, player |
| **Block** | Puzzle piece in Scratch | Motion, looks, control |
| **Loop** | Repeat code | Forever, repeat 10 |
| **Condition** | Decision point | If touching edge |
| **Variable** | Storage container | score, speed, lives |
| **Event** | Trigger for code | Flag clicked, key pressed |
| **Thread** | Independent execution path | Multiple scripts running |

---

## 🔧 Problem Sets

**Problem Set 0: Scratch Project**
- **Task:** Create an interactive Scratch project with at least:
  - 2 sprites
  - 3 scripts total
  - 1 condition
  - 1 loop
  - 1 variable
  - 1 custom block
- **Concepts:** All fundamental programming concepts
- **Approach:** Start simple (make sprite move), then add features incrementally
- **Ideas:** Game, animation, interactive story, music visualizer

---

## 💡 Key Takeaways

1. **CS is problem-solving** - Not about memorizing code, about thinking algorithmically
2. **Binary is universal** - Everything computers do comes down to 0s and 1s
3. **Abstraction is powerful** - Scratch hides complexity so you focus on logic
4. **Fundamental concepts are language-agnostic** - Loops, conditions, variables exist everywhere
5. **Programming is creative** - Infinite possibilities from simple building blocks
6. **Start simple, iterate** - Build working version, then enhance
7. **Debugging is normal** - Even experienced programmers spend most time debugging

---

## 🔗 Resources

- [CS50 Week 0](https://cs50.harvard.edu/x/2024/weeks/0/)
- [Scratch Website](https://scratch.mit.edu/)
- [CS50 Scratch Examples](https://scratch.mit.edu/studios/25128634/)
- [Binary/ASCII Converter](https://www.rapidtables.com/convert/number/ascii-to-binary.html)

---

## 📝 My Notes

**What clicked:**  
- Programming concepts are universal - just different syntax in different languages
- Visual blocks make logic visible - easier to see structure
- Scratch removes syntax barriers - focus purely on problem-solving
- Events/threads concept is powerful for interactive programs

**Challenges:**  
- Organizing blocks cleanly (easy to make spaghetti code)
- Understanding coordinate system (x, y positions)
- Timing issues with broadcasts and waits
- Debugging without error messages (code just doesn't work)

**Aha moments:**  
- Forever loop + condition = game loop pattern!
- Variables persist between script runs
- Can have multiple scripts per sprite (parallel execution)
- Custom blocks = functions (reusable code!)

**To review:**  
- Broadcasting for sprite communication
- Clone blocks for creating copies dynamically
- Advanced sensing (distance, timer)
- Pen blocks for drawing

**Fun project ideas:**
- Pong game (paddle, ball, score)
- Catching game (falling objects, player moves)
- Music sequencer (keyboard triggers sounds)
- Interactive story (choices affect outcome)

---

## ➡️ Next Steps

**Next week:** 01_c.md (Introduction to C programming language)  
**To practice:**  
- Build complete Scratch project for Problem Set 0
- Experiment with different block combinations
- Study others' projects on Scratch website
- Think about how Scratch concepts map to real programming languages

# Notes from Computer Science Harvard:

## Computational Thinking

	•	What is an algorithm?
            Series of orderly steps needed to solve a problem
	•	Pseudocode examples.
            Describe the steps needed to solve a problem in our own words (no code expressions)
	•	Types of data: bool, int, string, etc.
	•	High-level vs low-level languages.



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