# 02: Arrays

**Course:** CS50: Introduction to Computer Science  
**Platform:** edX / Harvard  
**Instructor:** David J. Malan  
**Week:** 2  
**Started:** Nov 2025  
**Status:** Completed

---

## 📚 Overview

Deep dive into arrays - collections of values stored contiguously in memory. Learn how strings are actually arrays of characters, work with command-line arguments, and understand memory addresses. Introduction to compilation stages and debugging techniques.

---

## ✅ Progress

- [x] Lecture: Arrays and strings
- [x] Sections: Memory and debugging
- [x] Problem Set 2: Readability, Caesar/Substitution
- [x] Lab 2: Scrabble

---

## 🎯 Key Concepts

### Arrays

**What it is:**  
Collection of values of the same type stored in contiguous memory locations. Fixed size, indexed starting at 0.

**Why it matters:**  
Fundamental data structure. Efficient for storing and accessing collections of related data.

**Key points:**
- **Declaration:** `int scores[3];` - array of 3 integers
- **Initialization:** `int scores[3] = {72, 73, 33};`
- **Indexing:** `scores[0]` is first element (0-indexed!)
- **Size is fixed:** Cannot change size after creation
- **Bounds:** No automatic bounds checking - accessing `scores[10]` when size is 3 = undefined behavior!
- **Passing to functions:** Arrays passed by reference (function modifies original)
- **Memory:** Stored contiguously (elements side-by-side in RAM)

---

### Strings as Arrays

**What it is:**  
In C, strings are arrays of characters terminated by a null character `\0`.

**Why it matters:**  
Understanding this reveals how strings work under the hood and why certain operations behave as they do.

**Key points:**
- **String = char array + `\0`:** `"Hi"` is actually `['H', 'i', '\0']`
- **Null terminator:** `\0` marks end of string (has value 0)
- **Length:** String length doesn't include `\0`, but storage does
- **Access:** Can access individual characters: `name[0]`
- **Modification:** Can change characters: `name[0] = 'J'`
- **Library:** `#include <string.h>` for string functions
- **strlen():** Get string length (doesn't count `\0`)
- **Immutable literals:** `"hello"` stored in read-only memory

---

### Command-Line Arguments

**What it is:**  
Values passed to program when executing from terminal.

**Why it matters:**  
Professional programs accept arguments (like `grep pattern file.txt`). Essential for automation.

**Syntax:**
```c
int main(int argc, string argv[])
{
    // argc = argument count
    // argv = argument vector (array)
}
```

**Key points:**
- **argc:** Number of arguments (including program name)
- **argv[0]:** Program name itself
- **argv[1]:** First actual argument
- **Check argc:** Always verify enough arguments before accessing
- **Example:** `./program hello world` → argc=3, argv=["./program", "hello", "world"]

---

### String Functions

**What it is:**  
Pre-written functions in `<string.h>` library for string manipulation.

**Common functions:**
- **strlen(s):** Length of string
- **strcmp(s1, s2):** Compare strings (returns 0 if equal)
- **strcpy(dest, src):** Copy string
- **strcat(dest, src):** Concatenate strings
- **toupper(c):** Convert char to uppercase (needs `<ctype.h>`)
- **tolower(c):** Convert char to lowercase
- **isalpha(c):** Check if alphabetic character
- **isdigit(c):** Check if digit

---

### Compilation Stages (Deep Dive)

**What it is:**  
Four stages that convert source code to executable.

**Stages:**

1. **Preprocessing:**
   - Handle `#include` (paste library contents)
   - Handle `#define` (replace constants)
   - Remove comments
   - Output: Still C code, but expanded

2. **Compiling:**
   - Convert C to assembly language
   - Assembly is human-readable machine instructions
   - Output: .s file

3. **Assembling:**
   - Convert assembly to machine code (binary)
   - Creates object file (.o)
   - Output: Binary, but not yet executable

4. **Linking:**
   - Combine object files with libraries
   - Resolve external references
   - Output: Final executable

**Command:** `clang -o program program.c` does all four stages

---

### Debugging

**What it is:**  
Finding and fixing errors in code.

**Techniques:**
- **printf debugging:** Add print statements to see values
- **Rubber duck debugging:** Explain code to inanimate object
- **debugger (debug50):** Step through code line by line
- **Breakpoints:** Pause execution at specific line
- **Watch variables:** See value changes in real-time
- **Step over:** Execute current line, move to next
- **Step into:** Enter function being called

---

## 💻 Code Examples

### Array Basics
```c
#include <stdio.h>

int main(void)
{
    // Declare and initialize array
    int scores[3] = {72, 73, 33};
    
    // Access elements (0-indexed)
    printf("First score: %i\n", scores[0]);   // 72
    printf("Second score: %i\n", scores[1]);  // 73
    printf("Third score: %i\n", scores[2]);   // 33
    
    // Calculate average
    int sum = scores[0] + scores[1] + scores[2];
    printf("Average: %f\n", sum / 3.0);  // Use 3.0 for float division!
    
    return 0;
}
```

**Output:**
```
First score: 72
Second score: 73
Third score: 33
Average: 59.333333
```

---

### Array with Loop
```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get number of scores
    int n = get_int("How many scores? ");
    
    // Declare array with variable size
    int scores[n];
    
    // Input scores
    for (int i = 0; i < n; i++)
    {
        scores[i] = get_int("Score %i: ", i + 1);
    }
    
    // Calculate average
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum += scores[i];
    }
    
    printf("Average: %f\n", sum / (float) n);
    
    return 0;
}
```

---

### Strings as Character Arrays
```c
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string name = get_string("Name: ");
    
    // Print each character
    printf("Characters:\n");
    for (int i = 0; i < strlen(name); i++)
    {
        printf("%c\n", name[i]);
    }
    
    // Or more efficiently (calculate length once)
    int len = strlen(name);
    for (int i = 0; i < len; i++)
    {
        printf("%c\n", name[i]);
    }
    
    return 0;
}
```

**Input:** `Manuel`

**Output:**
```
Characters:
M
a
n
u
e
l
```

---

### String Manipulation - Uppercase
```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string text = get_string("Before: ");
    
    printf("After:  ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        printf("%c", toupper(text[i]));
    }
    printf("\n");
    
    return 0;
}
```

**Input:** `hello`  
**Output:** `HELLO`

---

### Command-Line Arguments
```c
#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    // Check if user provided argument
    if (argc == 2)
    {
        printf("hello, %s\n", argv[1]);
    }
    else
    {
        printf("hello, world\n");
    }
    
    return 0;
}
```

**Usage:**
```bash
$ ./program
hello, world

$ ./program Manuel
hello, Manuel
```

---

### Command-Line Arguments - Multiple
```c
#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[])
{
    // Print all arguments
    printf("argc: %i\n", argc);
    
    for (int i = 0; i < argc; i++)
    {
        printf("argv[%i]: %s\n", i, argv[i]);
    }
    
    return 0;
}
```

**Usage:**
```bash
$ ./program foo bar baz
argc: 4
argv[0]: ./program
argv[1]: foo
argv[2]: bar
argv[3]: baz
```

---

### Caesar Cipher (Simple Encryption)
```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    // Convert argument to integer
    int key = atoi(argv[1]);
    
    // Get plaintext
    string plaintext = get_string("plaintext:  ");
    
    printf("ciphertext: ");
    
    // Encrypt each character
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];
        
        if (isalpha(c))
        {
            // Preserve case
            if (isupper(c))
            {
                printf("%c", (c - 'A' + key) % 26 + 'A');
            }
            else
            {
                printf("%c", (c - 'a' + key) % 26 + 'a');
            }
        }
        else
        {
            // Non-alphabetic characters unchanged
            printf("%c", c);
        }
    }
    
    printf("\n");
    return 0;
}
```

**Usage:**
```bash
$ ./caesar 1
plaintext:  HELLO
ciphertext: IFMMP

$ ./caesar 13
plaintext:  hello, world
ciphertext: uryyb, jbeyq
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Array** | Collection of values of same type | `int nums[5];` |
| **Index** | Position in array (starts at 0) | `nums[0]` is first |
| **Element** | Individual value in array | Each number in array |
| **Null terminator** | `\0` marking end of string | `"Hi"` = `['H','i','\0']` |
| **strlen** | Function to get string length | `strlen("hello")` = 5 |
| **argc** | Argument count (command line) | Number of arguments |
| **argv** | Argument vector (array) | Array of string arguments |
| **Bounds** | Valid range of indices | For size 5: 0-4 |
| **Segmentation fault** | Accessing invalid memory | Common with arrays! |
| **Buffer** | Temporary storage in memory | Array is a buffer |
| **ASCII** | Character encoding | 'A' = 65, 'a' = 97 |

---

## 🔧 Problem Sets

**Problem Set 2:**

**Lab: Scrabble**
- **Task:** Calculate score for Scrabble words
- **Concepts:** Arrays, string functions, loops
- **Approach:** Array of point values, loop through word, sum points

**Problem: Readability**
- **Task:** Calculate reading level using Coleman-Liau index
- **Concepts:** String analysis, counting letters/words/sentences
- **Approach:** Loop through text, count, apply formula

**Problem: Caesar (Less)**
- **Task:** Encrypt message using Caesar cipher
- **Concepts:** Command-line args, character arithmetic, modulo
- **Approach:** Shift each letter by key amount, wrap with mod 26

**Problem: Substitution (More)**
- **Task:** Encrypt using substitution cipher (custom alphabet)
- **Concepts:** Arrays, validation, mapping
- **Approach:** Validate key (26 unique letters), map each char

---

## 💡 Key Takeaways

1. **Arrays are 0-indexed** - First element is [0], not [1]
2. **Strings = char arrays** - Always end with `\0`
3. **No bounds checking** - C won't stop you from accessing invalid indices (segfault!)
4. **strlen() in loop is inefficient** - Calculate once, store in variable
5. **Command-line args are strings** - Use `atoi()` to convert to int
6. **Check argc before accessing argv** - Prevent crashes
7. **Character arithmetic works** - 'A' + 1 = 'B' (uses ASCII values)
8. **toupper/tolower from ctype.h** - Don't write your own
9. **Arrays passed by reference** - Function can modify original

---

## 🔗 Resources

- [CS50 Week 2](https://cs50.harvard.edu/x/2024/weeks/2/)
- [ASCII Table](https://www.asciitable.com/)
- [String Functions Reference](https://en.cppreference.com/w/c/string/byte)
- [debug50 Guide](https://cs50.readthedocs.io/debug50/)

---

## 📝 My Notes

**What clicked:**  
- Strings being char arrays explains so much!
- `\0` is why `strlen("Hi")` = 2 but memory = 3 bytes
- Command-line args enable automation (no interactive input needed)
- Character arithmetic: 'A' = 65, so 'A' - 'A' = 0, 'B' - 'A' = 1

**Challenges:**  
- Segmentation faults from invalid array access (confusing errors!)
- Remembering `strlen()` in loop condition is inefficient
- Understanding when to use `argc` vs `argv`
- Modulo arithmetic for wrapping (Caesar cipher)

**Aha moments:**  
- Can iterate string until `\0`: `while (s[i] != '\0')`
- `toupper()` and `tolower()` only affect letters (ignore others)
- Command-line args perfect for testing (no manual input!)
- ASCII math: `'a' - 'a'` gives position in alphabet (0-25)

**To review:**  
- Multidimensional arrays
- Passing arrays to functions
- Pointer notation (arrays and pointers related!)
- String copying (why can't just use `=`?)

**Common mistakes:**
- Off-by-one errors (accessing beyond array end)
- Forgetting null terminator in calculations
- Using `strlen()` in loop condition (recalculates every iteration!)
- Comparing strings with `==` instead of `strcmp()`

**Debugging tips:**
- Print array contents to verify values
- Print loop index to see where error occurs
- Use debug50 to step through and watch variables
- Check argc before accessing argv elements

---

## ➡️ Next Steps

**Next week:** 03_algorithms.md (Searching, sorting, Big O notation, algorithm efficiency)  
**To practice:**  
- Complete all Problem Set 2 problems
- Practice with different string manipulations
- Experiment with command-line arguments
- Try writing functions that take arrays as parameters