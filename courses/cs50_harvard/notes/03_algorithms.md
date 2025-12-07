# 03: Algorithms

**Course:** CS50: Introduction to Computer Science  
**Platform:** edX / Harvard  
**Instructor:** David J. Malan  
**Week:** 3  
**Started:** Nov 2025  
**Status:** In progress

---

## 📚 Overview

Introduction to algorithms - step-by-step procedures for solving problems. Learn searching algorithms (linear, binary), sorting algorithms (bubble, selection, merge), and how to analyze algorithm efficiency using Big O notation. Understanding time complexity and making informed choices about which algorithm to use.

---

## ✅ Progress

- [x] Lecture: Algorithms and efficiency
- [x] Sections: Searching and sorting
- [ ] Problem Set 3: Plurality, Runoff/Tideman
- [ ] Lab 3: Sort

---

## 🎯 Key Concepts

### What is an Algorithm?

**What it is:**  
Step-by-step procedure for solving a problem. Like a recipe - specific instructions that produce consistent results.

**Why it matters:**  
Different algorithms solve the same problem with vastly different efficiency. Choosing the right algorithm matters at scale.

**Key points:**
- **Input:** Data to process
- **Output:** Solution/result
- **Steps:** Clear, unambiguous instructions
- **Correctness:** Must produce correct answer
- **Efficiency:** Speed and memory usage matter
- **Deterministic:** Same input → same output

---

### Searching Algorithms

**What it is:**  
Finding a specific value in a collection of data.

#### **Linear Search**

**How it works:** Check each element one by one from start to finish.

**Algorithm:**
```
For each element in array:
    If element equals target:
        Return index
Return "not found"
```

**Time complexity:**
- Best case: O(1) - found immediately
- Worst case: O(n) - check every element
- Average: O(n)

**Pros:** Works on unsorted data, simple to implement  
**Cons:** Slow for large datasets

#### **Binary Search**

**How it works:** Repeatedly divide sorted array in half, eliminate half each time.

**Algorithm:**
```
While array has elements:
    Check middle element
    If target equals middle:
        Return index
    If target < middle:
        Search left half
    Else:
        Search right half
Return "not found"
```

**Time complexity:**
- Best case: O(1) - middle element
- Worst case: O(log n) - keep halving
- Average: O(log n)

**Pros:** Very fast (log n growth)  
**Cons:** **Requires sorted data**

**Example:** Finding name in phone book - open to middle, eliminate half each time

---

### Sorting Algorithms

**What it is:**  
Arranging elements in order (ascending or descending).

#### **Bubble Sort**

**How it works:** Repeatedly swap adjacent elements if they're in wrong order. Largest elements "bubble up" to end.

**Algorithm:**
```
Repeat until no swaps:
    For each pair of adjacent elements:
        If out of order:
            Swap them
```

**Time complexity:**
- Best case: O(n) - already sorted, one pass
- Worst case: O(n²) - reversed, maximum swaps
- Average: O(n²)

**Pros:** Simple, works in-place  
**Cons:** Slow for large datasets

---

#### **Selection Sort**

**How it works:** Find smallest element, swap with first position. Repeat for remaining elements.

**Algorithm:**
```
For i from 0 to n-1:
    Find smallest element from i to end
    Swap smallest with position i
```

**Time complexity:**
- Best case: O(n²) - always check all
- Worst case: O(n²)
- Average: O(n²)

**Pros:** Simple, few swaps  
**Cons:** Always O(n²), even if sorted

---

#### **Merge Sort**

**How it works:** Divide array in half recursively until single elements, then merge back together in sorted order.

**Algorithm:**
```
If array has 1 element:
    Return (already sorted)
Else:
    Split array in half
    Sort left half (recursively)
    Sort right half (recursively)
    Merge sorted halves
```

**Time complexity:**
- Best case: O(n log n)
- Worst case: O(n log n)
- Average: O(n log n)

**Pros:** Consistent O(n log n), stable  
**Cons:** Requires extra memory (not in-place)

---

### Big O Notation

**What it is:**  
Mathematical notation describing algorithm efficiency as input size grows. Focuses on worst-case scenario.

**Why it matters:**  
Helps compare algorithms objectively. Small differences don't matter with small data, but scale dramatically.

**Common complexities (fastest to slowest):**
- **O(1):** Constant - same time regardless of size
  - Example: Array access `arr[5]`
- **O(log n):** Logarithmic - halves each step
  - Example: Binary search
- **O(n):** Linear - proportional to size
  - Example: Linear search
- **O(n log n):** Log-linear - efficient sorting
  - Example: Merge sort
- **O(n²):** Quadratic - nested loops
  - Example: Bubble sort, selection sort
- **O(2ⁿ):** Exponential - doubles each step (very slow!)
  - Example: Recursive Fibonacci (naive)

**Visual:**
```
Time
 ^
 |                                    O(2^n)
 |                              O(n^2)
 |                        O(n log n)
 |                  O(n)
 |           O(log n)
 |     O(1)
 |_______________________________________________> Size (n)
```

---

### Big Omega (Ω) and Big Theta (Θ)

**Big Omega (Ω):** Best case (lower bound)  
**Big Theta (Θ):** Average case (tight bound)

**Example - Linear Search:**
- **O:** O(n) - worst case: check all elements
- **Ω:** Ω(1) - best case: first element
- **Θ:** Θ(n) - average case: check half elements

---

### Recursion

**What it is:**  
Function that calls itself. Base case stops recursion.

**Why it matters:**  
Elegant solution for divide-and-conquer problems. Essential for merge sort and many advanced algorithms.

**Structure:**
```c
function(input)
{
    if (base case)
    {
        return simple answer
    }
    else
    {
        return function(smaller input)  // Recursive call
    }
}
```

**Example - Factorial:**
```c
int factorial(int n)
{
    // Base case
    if (n == 1)
    {
        return 1;
    }
    // Recursive case
    else
    {
        return n * factorial(n - 1);
    }
}
```

---

## 💻 Code Examples

### Linear Search
```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int numbers[] = {4, 6, 8, 2, 7, 5, 0};
    int n = 7;
    
    int target = get_int("Number to find: ");
    
    // Linear search
    for (int i = 0; i < n; i++)
    {
        if (numbers[i] == target)
        {
            printf("Found at index %i\n", i);
            return 0;
        }
    }
    
    printf("Not found\n");
    return 1;
}
```

---

### Binary Search
```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // MUST be sorted!
    int numbers[] = {0, 2, 4, 5, 6, 7, 8};
    int n = 7;
    
    int target = get_int("Number to find: ");
    
    // Binary search
    int left = 0;
    int right = n - 1;
    
    while (left <= right)
    {
        int middle = (left + right) / 2;
        
        if (numbers[middle] == target)
        {
            printf("Found at index %i\n", middle);
            return 0;
        }
        else if (numbers[middle] < target)
        {
            left = middle + 1;  // Search right half
        }
        else
        {
            right = middle - 1;  // Search left half
        }
    }
    
    printf("Not found\n");
    return 1;
}
```

---

### Bubble Sort
```c
#include <stdio.h>

void bubble_sort(int arr[], int n)
{
    // Repeat until no swaps
    int swapped;
    do
    {
        swapped = 0;
        
        // Compare adjacent elements
        for (int i = 0; i < n - 1; i++)
        {
            if (arr[i] > arr[i + 1])
            {
                // Swap
                int temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
                swapped = 1;
            }
        }
    }
    while (swapped);
}

int main(void)
{
    int numbers[] = {5, 2, 7, 4, 1, 6, 3};
    int n = 7;
    
    bubble_sort(numbers, n);
    
    // Print sorted array
    for (int i = 0; i < n; i++)
    {
        printf("%i ", numbers[i]);
    }
    printf("\n");
    
    return 0;
}
```

**Output:** `1 2 3 4 5 6 7`

---

### Selection Sort
```c
#include <stdio.h>

void selection_sort(int arr[], int n)
{
    // For each position
    for (int i = 0; i < n - 1; i++)
    {
        // Find minimum in remaining array
        int min_index = i;
        for (int j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[min_index])
            {
                min_index = j;
            }
        }
        
        // Swap minimum with current position
        int temp = arr[i];
        arr[i] = arr[min_index];
        arr[min_index] = temp;
    }
}

int main(void)
{
    int numbers[] = {5, 2, 7, 4, 1, 6, 3};
    int n = 7;
    
    selection_sort(numbers, n);
    
    for (int i = 0; i < n; i++)
    {
        printf("%i ", numbers[i]);
    }
    printf("\n");
    
    return 0;
}
```

---

### Merge Sort (Conceptual)
```c
// Pseudocode - actual implementation more complex

void merge_sort(int arr[], int n)
{
    // Base case
    if (n < 2)
    {
        return;  // Already sorted
    }
    
    // Divide
    int mid = n / 2;
    int left[mid];
    int right[n - mid];
    
    // Copy halves
    for (int i = 0; i < mid; i++)
        left[i] = arr[i];
    for (int i = mid; i < n; i++)
        right[i - mid] = arr[i];
    
    // Recursively sort halves
    merge_sort(left, mid);
    merge_sort(right, n - mid);
    
    // Merge sorted halves back
    merge(left, mid, right, n - mid, arr);
}
```

---

### Recursion - Factorial
```c
#include <cs50.h>
#include <stdio.h>

int factorial(int n)
{
    // Base case
    if (n == 1)
    {
        return 1;
    }
    // Recursive case
    else
    {
        return n * factorial(n - 1);
    }
}

int main(void)
{
    int n = get_int("Number: ");
    printf("%i! = %i\n", n, factorial(n));
    return 0;
}
```

**Example:** `factorial(5)` = 5 × 4 × 3 × 2 × 1 = 120

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Algorithm** | Step-by-step problem-solving procedure | Search, sort |
| **Linear search** | Check each element sequentially | O(n) |
| **Binary search** | Divide and conquer on sorted data | O(log n) |
| **Sorting** | Arranging elements in order | Ascending/descending |
| **Bubble sort** | Swap adjacent out-of-order elements | O(n²) |
| **Selection sort** | Find minimum, swap with current | O(n²) |
| **Merge sort** | Divide, sort, merge | O(n log n) |
| **Big O** | Upper bound (worst case) | O(n), O(n²) |
| **Big Omega (Ω)** | Lower bound (best case) | Ω(1), Ω(n) |
| **Recursion** | Function calling itself | factorial, fibonacci |
| **Base case** | Stops recursion | n == 1 |
| **Divide and conquer** | Break problem into smaller parts | Binary search, merge sort |

---

## 🔧 Problem Sets

**Problem Set 3:**

**Lab: Sort**
- **Task:** Analyze sorting algorithms by timing them
- **Concepts:** Empirical analysis, big O validation
- **Approach:** Run sorts on different data, measure time, identify algorithm

**Problem: Plurality (Less)**
- **Task:** Run plurality (first-past-the-post) election
- **Concepts:** Arrays, counting, finding max
- **Approach:** Count votes for each candidate, find winner

**Problem: Runoff (More)**
- **Task:** Run ranked-choice voting election
- **Concepts:** 2D arrays, sorting by preference, eliminating candidates
- **Approach:** Simulate runoff rounds, eliminate last place iteratively

**Problem: Tideman (More challenging)**
- **Task:** Implement Tideman voting system (Condorcet method)
- **Concepts:** Graph theory, cycle detection, complex algorithms
- **Approach:** Build preference graph, lock pairs without creating cycles

---

## 💡 Key Takeaways

1. **Binary search requires sorting** - Can't skip this step!
2. **O(n log n) is practical limit** - Can't sort faster without extra info
3. **O(n²) algorithms don't scale** - Avoid for large datasets
4. **Logarithmic growth is powerful** - Halving is incredibly efficient
5. **Recursion needs base case** - Else infinite loop/stack overflow
6. **Choose algorithm based on data** - Consider size, sorted?, memory
7. **Constant factors matter too** - O(n) can be slower than O(n²) for small n
8. **Trade-offs exist** - Time vs space, simplicity vs efficiency

---

## 🔗 Resources

- [CS50 Week 3](https://cs50.harvard.edu/x/2024/weeks/3/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Sorting Algorithm Visualizations](https://www.toptal.com/developers/sorting-algorithms)
- [VisuAlgo](https://visualgo.net/) - Visualize algorithms

---

## 📝 My Notes

**What clicked:**  
- Binary search's O(log n) means 1 billion items needs only ~30 steps!
- Merge sort always O(n log n) - no worst case penalty
- Recursion is just breaking problem into smaller identical subproblems
- Big O ignores constants - O(2n) = O(n)

**Challenges:**  
- Understanding recursion (tracing call stack mentally is hard!)
- Implementing merge sort (more complex than bubble/selection)
- Remembering which algorithm requires sorted data
- Visualizing log n growth

**Aha moments:**  
- Phone book example makes binary search obvious
- Selection sort always makes n² comparisons (even if sorted!)
- Bubble sort's best case O(n) when already sorted (early exit)
- Logarithms are just "how many times divide by 2?"

**To review:**  
- Merge sort implementation details
- Recursion call stack mechanics
- Stability in sorting (preserving order of equal elements)
- Space complexity (memory usage)

**Algorithm selection guide:**
- **Small dataset (<100):** Any algorithm works
- **Already sorted:** Bubble sort O(n) or just verify
- **Need stability:** Merge sort
- **Limited memory:** Selection sort (in-place)
- **General case:** Merge sort (reliable O(n log n))

**Real-world applications:**
- Databases use optimized sorting (similar to merge sort)
- Search engines use variants of binary search
- Autocomplete uses sorted data + binary search
- Social media feeds: sorting by time/relevance

---

## ➡️ Next Steps

**Next week:** 04_memory.md (Pointers, dynamic memory allocation, memory management, hexadecimal)  
**To practice:**  
- Complete all Problem Set 3 problems
- Implement sorting algorithms from scratch
- Practice recursion with different problems (Fibonacci, towers of Hanoi)
- Analyze Big O of your own code
- Visualize algorithm execution (use VisuAlgo or draw on paper)