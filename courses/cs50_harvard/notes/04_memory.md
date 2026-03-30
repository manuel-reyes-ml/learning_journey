# 04: Memory

**Course:** CS50: Introduction to Computer Science  
**Platform:** edX / Harvard  
**Instructor:** David J. Malan  
**Week:** 4  
**Started:** Dec 2025  
**Status:** Completed

---

## 📚 Overview

Deep dive into how computers actually store and manage data in memory. Learn hexadecimal notation, pointers (memory addresses), dynamic memory allocation with `malloc`/`free`, common memory bugs, and how to use Valgrind to detect them. Covers the mechanics behind strings as pointers, passing by reference vs. value, and file I/O. This week bridges low-level C memory management with the abstractions you'll rely on in Python.

---

## ✅ Progress

- [x] Lecture: Memory, pointers, and allocation
- [x] Sections: Pointer arithmetic and memory layout
- [x] Problem Set 4: Filter (Less/More), Recover
- [x] Lab 4: Smiley / Volume

---

## 🎯 Key Concepts

### Hexadecimal

**What it is:**  
Base-16 number system using digits 0–9 and letters A–F. Used to represent memory addresses and binary data compactly.

**Why it matters:**  
Memory addresses are expressed in hexadecimal by convention. Every debugger, pointer print, and memory dump you'll ever read uses it.

**Key points:**
- **Base 16:** One hex digit represents 4 bits (a nibble); two hex digits = one byte (8 bits)
- **Prefix:** `0x` denotes a hexadecimal value (e.g., `0x1A`, `0xFF`)
- **Conversion:** `0xFF` = 255 in decimal, `0x0A` = 10
- **Colors:** RGB in web design is hexadecimal (e.g., `#FF0000` = red)
- **Why not binary?** Binary is 8 digits per byte; hex is just 2 — far more readable
- **Example:** Memory address `0x7ffd12a4b3c0` is just a number — the location in RAM

**Decimal → Hex:**
```
255 ÷ 16 = 15 remainder 15 → FF
16  ÷ 16 = 1  remainder 0  → 10
10  ÷ 16 = 0  remainder 10 → 0A
```

---

### Pointers

**What it is:**  
A variable that stores a memory address — the location of another variable in RAM, not the value itself.

**Why it matters:**  
Pointers are how C (and under the hood, Python and every compiled language) passes data efficiently, modifies original variables from inside functions, and manages dynamic memory. Understanding pointers makes you a fundamentally better programmer.

**Key points:**
- **Declaration:** `int *p;` — `p` is a pointer to an integer
- **Address-of operator `&`:** Get the memory address of a variable: `p = &x;`
- **Dereference operator `*`:** Get the value at the address: `*p` gives the int stored at address `p`
- **Size:** On 64-bit systems, every pointer is 8 bytes regardless of what it points to
- **NULL pointer:** A pointer that points to nothing; always initialize pointers to `NULL` if not assigning immediately
- **Pointer arithmetic:** `p + 1` moves the address forward by the size of the type (e.g., 4 bytes for int)
- **Strings are pointers:** `char *s = "hello"` — `s` holds the address of `'h'`

**Mental model:**
```
Variable x lives at address 0x123
Value of x = 42

Pointer p = 0x123   ← stores the address
*p = 42             ← dereferencing gives the value
```

---

### Memory Layout of a Program

**What it is:**  
How a running C program's memory is divided into distinct regions, each with a specific purpose.

**Why it matters:**  
Explains stack overflows, why local variables disappear after functions return, and why `malloc` is needed for data that must outlive a function call.

**Regions (top to bottom in typical layout):**

| Region | Purpose | Lifetime |
|--------|----------|----------|
| **Text (code)** | Compiled program instructions | Entire program |
| **Globals / Data** | Global and static variables | Entire program |
| **Heap** | Dynamic memory (`malloc`) | Until you call `free()` |
| **Stack** | Local variables, function call frames | Until function returns |

**Key points:**
- **Stack grows downward** (toward lower addresses); **Heap grows upward**
- **Stack overflow:** Too many nested function calls (infinite recursion) exhausts stack space
- **Heap overflow / memory leak:** Forgetting to `free()` leaves memory allocated forever
- **Local variables are stack-allocated:** They're gone when the function returns

---

### Dynamic Memory Allocation

**What it is:**  
Requesting memory from the heap at runtime using `malloc`, `calloc`, or `realloc`, and releasing it with `free`.

**Why it matters:**  
The stack has limited, fixed-size frames. The heap lets you allocate exactly as much memory as you need at runtime — for arrays whose size isn't known at compile time, data structures, and data that must persist across function calls.

**Key functions:**

- **`malloc(size)`:** Allocate `size` bytes; returns `void *` pointer or `NULL` on failure
- **`calloc(n, size)`:** Allocate `n` items of `size` bytes each, **zero-initialized**
- **`realloc(ptr, new_size)`:** Resize a previously allocated block
- **`free(ptr)`:** Release the memory back to the heap

**Key points:**
- Always check that `malloc` didn't return `NULL` before using the pointer
- Every `malloc` must have exactly one corresponding `free` — no more, no less
- **Double free:** Calling `free` twice on the same pointer → undefined behavior
- **Use after free:** Accessing memory after freeing it → undefined behavior
- **Memory leak:** Forgetting to call `free` — program consumes more and more RAM

---

### Valgrind

**What it is:**  
A command-line tool that runs your program inside a virtual machine and tracks every memory operation — detecting leaks, invalid reads/writes, and use-after-free bugs.

**Why it matters:**  
Memory bugs are silent. The program might seem to work and crash much later, in a completely different place. Valgrind catches the actual source.

**Usage:**
```bash
valgrind ./program
valgrind --leak-check=full ./program
```

**Common Valgrind errors:**
- **"definitely lost":** Memory was allocated and never freed (leak)
- **"invalid read/write":** Accessing memory outside allocated bounds
- **"use of uninitialised value":** Reading a variable before assigning it
- **"invalid free":** Freeing already-freed or never-allocated memory

---

### Pointers and Strings

**What it is:**  
Strings in C are just `char *` — a pointer to the first character of a null-terminated character array.

**Why it matters:**  
Explains why `s1 == s2` compares addresses (not values!), why `strcpy` is needed instead of `=`, and how string functions work under the hood.

**Key points:**
- `char *s = "hello"` — `s` points to a read-only string literal; cannot modify it
- `char s[] = "hello"` — `s` is a copy on the stack; can modify characters
- **Comparing strings:** Always use `strcmp(s1, s2)`, never `s1 == s2` (compares addresses!)
- **Copying strings:** Use `strcpy(dest, src)` or `strdup(src)` (allocates on heap)
- `strdup(s)` is shorthand for `malloc(strlen(s) + 1)` + `strcpy` — must `free()` the result

---

### Pass by Value vs. Pass by Reference

**What it is:**  
Two ways to pass data to functions. By value sends a copy; by reference (via pointer) lets the function modify the original.

**Why it matters:**  
The classic "why didn't my swap function work?" bug — you passed copies, not the originals.

**Key points:**
- **By value (default in C):** Function gets a copy; changes don't affect the caller
- **By reference (pointer):** Function gets the address; changes affect the original
- Arrays are always passed by reference (they decay to a pointer to the first element)
- In Python, objects are passed by object reference (similar to pointer semantics for mutables)

---

### File I/O

**What it is:**  
Reading from and writing to files on disk using the `<stdio.h>` file functions.

**Why it matters:**  
Real programs don't only work with terminal input — they read CSVs, images, configs, and write logs. File I/O is the foundation of data pipelines.

**Key functions:**
- **`fopen(filename, mode)`:** Open a file; returns `FILE *` or `NULL`
  - Modes: `"r"` read, `"w"` write (truncate), `"a"` append, `"rb"` read binary
- **`fclose(f)`:** Close file; always do this
- **`fread(buffer, size, count, f)`:** Read binary data
- **`fwrite(buffer, size, count, f)`:** Write binary data
- **`fgetc(f)` / `fputc(c, f)`:** Read/write one character
- **`fgets(buffer, n, f)`:** Read a line of text
- **`fprintf(f, ...)`:** Write formatted text (like printf but to a file)
- **`feof(f)`:** Check if end-of-file reached

**Key points:**
- Always check if `fopen` returned `NULL` (file not found, permissions, etc.)
- Binary mode (`"rb"`, `"wb"`) is critical for non-text files (images, audio)
- `fread` returns number of items actually read — check it!

---

## 💻 Code Examples

### Pointers — Basics
```c
#include <stdio.h>

int main(void)
{
    int x = 42;
    int *p = &x;    // p holds the address of x

    printf("Value of x:       %i\n", x);
    printf("Address of x:     %p\n", &x);
    printf("Value of p:       %p\n", p);    // Same address
    printf("Dereferenced *p:  %i\n", *p);   // 42

    // Modify x through the pointer
    *p = 100;
    printf("x after *p = 100: %i\n", x);    // 100

    return 0;
}
```

**Output:**
```
Value of x:       42
Address of x:     0x7ffd5a3c1b04
Value of p:       0x7ffd5a3c1b04
Dereferenced *p:  42
x after *p = 100: 100
```

---

### Pass by Reference — Working Swap
```c
#include <stdio.h>

// WRONG — swaps copies, original unchanged
void swap_wrong(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
}

// CORRECT — swaps originals via pointers
void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(void)
{
    int x = 1;
    int y = 2;

    printf("Before: x=%i, y=%i\n", x, y);
    swap(&x, &y);
    printf("After:  x=%i, y=%i\n", x, y);

    return 0;
}
```

**Output:**
```
Before: x=1, y=2
After:  x=2, y=1
```

---

### Dynamic Memory Allocation
```c
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = get_int("How many scores? ");

    // Allocate array on the heap
    int *scores = malloc(n * sizeof(int));
    if (scores == NULL)  // Always check!
    {
        return 1;
    }

    // Fill and print
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
    printf("Average: %.2f\n", (float) sum / n);

    free(scores);   // Always free!
    return 0;
}
```

---

### String Copy — The Right Way
```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char *s = get_string("s: ");

    // strdup allocates exact memory needed + copies
    char *t = strdup(s);
    if (t == NULL)
    {
        return 1;
    }

    // Capitalize only the copy
    if (strlen(t) > 0)
    {
        t[0] = toupper(t[0]);
    }

    printf("s: %s\n", s);   // Original unchanged
    printf("t: %s\n", t);   // Copy is capitalized

    free(t);
    return 0;
}
```

**Input:** `hello`  
**Output:**
```
s: hello
t: Hello
```

---

### File I/O — Read and Copy a File
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: ./copy source destination\n");
        return 1;
    }

    FILE *src = fopen(argv[1], "rb");
    if (src == NULL)
    {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }

    FILE *dst = fopen(argv[2], "wb");
    if (dst == NULL)
    {
        printf("Could not create %s\n", argv[2]);
        fclose(src);
        return 1;
    }

    // Read and write one byte at a time
    unsigned char buffer[1];
    while (fread(buffer, 1, 1, src) == 1)
    {
        fwrite(buffer, 1, 1, dst);
    }

    fclose(src);
    fclose(dst);
    return 0;
}
```

---

### Valgrind — Detecting a Memory Leak
```c
// leak.c — intentional leak for demonstration
#include <stdlib.h>

int main(void)
{
    int *p = malloc(10 * sizeof(int));
    p[0] = 42;
    // Forgot to free(p)!
    return 0;
}
```

**Run:**
```bash
gcc -g -o leak leak.c
valgrind --leak-check=full ./leak
```

**Valgrind output:**
```
LEAK SUMMARY:
   definitely lost: 40 bytes in 1 blocks
```

**Fixed:**
```c
free(p);
return 0;
```

---

### Bitmap Image Processing (Problem Set 4 Pattern)
```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Simplified 24-bit RGB pixel
typedef struct
{
    uint8_t blue;
    uint8_t green;
    uint8_t red;
} RGBTRIPLE;

// Grayscale: average R, G, B channels
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            uint8_t avg = (image[i][j].red + image[i][j].green + image[i][j].blue) / 3;
            image[i][j].red = avg;
            image[i][j].green = avg;
            image[i][j].blue = avg;
        }
    }
}
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Pointer** | Variable storing a memory address | `int *p = &x;` |
| **Address** | Location of a variable in RAM | `0x7ffd5a3c` |
| **Dereference** | Get value at a pointer's address | `*p` |
| **`&` operator** | Get address of a variable | `&x` |
| **`*` operator** | Declare pointer / dereference | `int *p;` / `*p` |
| **Heap** | Region for dynamic memory | `malloc` allocates here |
| **Stack** | Region for local variables | Freed when function returns |
| **`malloc`** | Allocate bytes on the heap | `malloc(10 * sizeof(int))` |
| **`free`** | Release heap memory | `free(ptr)` |
| **Memory leak** | Allocated memory never freed | Slow crash over time |
| **Segfault** | Access to invalid memory address | Crash with no clear message |
| **NULL** | Pointer to nothing | `if (ptr == NULL)` |
| **Valgrind** | Memory debugging tool | Detects leaks, invalid reads |
| **`strdup`** | Copy string onto heap | Must `free()` the result |
| **Buffer overflow** | Write past end of allocated memory | Classic security vulnerability |
| **Hexadecimal** | Base-16 number system | `0xFF = 255` |
| **`FILE *`** | Pointer to open file | `fopen("data.csv", "r")` |
| **`fread` / `fwrite`** | Binary file read/write | Used for images, audio |
| **`typedef struct`** | Named custom data type | `RGBTRIPLE pixel;` |

---

## 🔧 Problem Sets

**Problem Set 4:**

**Lab: Smiley**
- **Task:** Turn all black pixels in a BMP image to a custom color
- **Concepts:** Structs, 2D arrays, file I/O, pixel manipulation
- **Approach:** Open BMP, iterate over pixel array, modify RGBTRIPLE values

**Lab: Volume**
- **Task:** Scale the volume of a WAV audio file by a factor
- **Concepts:** Binary file I/O, structs, reading headers vs. data separately
- **Approach:** Copy WAV header unchanged, read samples, multiply by factor, write out

**Problem: Filter (Less)**
- **Task:** Apply image filters — grayscale, sepia, reflection, blur
- **Concepts:** Pixel math, nested loops, 2D array manipulation, averaging
- **Approach:** Each filter is a separate function transforming the pixel grid

**Problem: Filter (More)**
- **Task:** All of Filter Less, plus edge detection using Sobel operator
- **Concepts:** Convolution, kernel math, neighboring pixel access
- **Approach:** Compute Gx and Gy for each pixel using surrounding 3×3 grid

**Problem: Recover**
- **Task:** Recover deleted JPEG files from a raw memory card image
- **Concepts:** File I/O, binary patterns, JPEG signatures, dynamic filenames
- **Approach:** Read 512-byte blocks, detect JPEG header `0xFF 0xD8 0xFF`, write new file per JPEG found

---

## 💡 Key Takeaways

1. **Pointers are just addresses** — demystify them: they're numbers that happen to represent locations in RAM
2. **Every `malloc` needs a `free`** — treat them as paired: one in, one out
3. **Strings are `char *`** — `==` compares addresses; always use `strcmp`
4. **Always check `malloc` / `fopen` return values** — both return `NULL` on failure; ignoring this crashes programs
5. **Stack vs. heap** — local variables → stack (auto-freed); data that must outlive functions → heap (manual free)
6. **Buffer overflows are security vulnerabilities** — writing past array bounds is how many real exploits work
7. **Valgrind is non-negotiable** — run it on every C program before calling it done
8. **`typedef struct` is your first data modeling tool** — composing types is the foundation of data structures (Week 5)
9. **Binary file I/O is universal** — CSV, images, audio, network packets all reduce to bytes

---

## 🔗 Resources

- [CS50 Week 4](https://cs50.harvard.edu/x/2024/weeks/4/)
- [C Pointers Guide — cppreference](https://en.cppreference.com/w/c/language/pointer)
- [Valgrind Quick Start](https://valgrind.org/docs/manual/quick-start.html)
- [CS50 Memory Diagram (Shorts)](https://cs50.harvard.edu/x/2024/shorts/pointers/)
- [BMP File Format](https://en.wikipedia.org/wiki/BMP_file_format)
- [JPEG Signature Reference](https://www.file-recovery.com/jpg-signature-format.htm)

---

## 📝 My Notes

**What clicked:**
- The `&` / `*` symmetry: `&` takes you from value to address; `*` takes you from address back to value — they're inverses
- Why Python doesn't have this problem: CPython manages reference counts automatically — but the mechanism underneath is exactly this
- `strdup` is just `malloc + strcpy` under the hood — now I understand why Python strings are immutable by default
- JPEG recovery was the most satisfying problem set so far — felt like actual forensics work

**Challenges:**
- Mentally tracking what `*` means in different contexts: declaration vs. dereference
- Pointer arithmetic: `p + 1` does not add 1 byte — it adds `sizeof(*p)` bytes (confusing at first!)
- Understanding that arrays and pointers are related but not identical
- Segfaults give almost no information — learning to read Valgrind output was essential

**Aha moments:**
- `int arr[5]` and `int *arr` are nearly equivalent — `arr` is a pointer to the first element
- You can have a pointer to a pointer: `char **argv` is an array of strings (array of `char *`)
- `free` doesn't zero out memory — the data may still be there, just "available" to be overwritten (security implication!)
- Reading 512-byte blocks for JPEG recovery mirrors how actual disk forensics tools work

**To review:**
- Pointer arithmetic in detail (incrementing pointers of different types)
- `realloc` patterns for growing arrays (preview of dynamic data structures)
- Function pointers (used in sorting comparators — `qsort` in stdlib)
- Stack vs. heap visualization in a debugger

**Common mistakes:**
- `int *p; *p = 5;` — declared pointer but never assigned an address before dereferencing → instant segfault
- `free(p); printf("%i", *p);` — use after free (undefined behavior, not always a crash!)
- `char *s = get_string(...); free(s);` — never `free` memory you didn't `malloc` yourself
- Forgetting `fclose` after `fopen` — file handle leak (same concept as memory leak)

**Roadmap connection:**
- Python's memory model (reference counting, garbage collection) makes complete sense now — it's automating exactly what we did manually here
- `struct` + file I/O = foundations of data serialization (CSV, JSON, Parquet in Stage 2)
- Valgrind's philosophy (instrument + detect leaks) reappears in Python memory profilers (`tracemalloc`, `memray`)
- Pixel manipulation here directly maps to NumPy array operations on image tensors in Stage 3 (ML)

---

## ➡️ Next Steps

**Next week:** 05_data_structures.md (Linked lists, hash tables, tries, trees, stacks, queues)  
**To practice:**
- Complete all Problem Set 4 problems; run Valgrind on every solution
- Implement a dynamic array that grows with `realloc`
- Write a program that reads a CSV file byte-by-byte to understand file I/O deeply
- Practice drawing memory diagrams on paper: stack frames, heap allocations, pointer arrows