# 05: Data Structures

**Course:** CS50: Introduction to Computer Science  
**Platform:** edX / Harvard  
**Instructor:** David J. Malan  
**Week:** 5  
**Started:** Dec 2025  
**Status:** Completed

---

## 📚 Overview

Introduction to abstract data structures — ways of organizing and linking data in memory to enable efficient operations. Covers linked lists, stacks, queues, hash tables, tries, and trees. Each structure trades off between insertion speed, lookup speed, and memory use. This week is the conceptual foundation for every data pipeline, database index, caching layer, and LLM token vocabulary you will build in later stages.

---

## ✅ Progress

- [x] Lecture: Data structures and abstract types
- [x] Sections: Linked lists and hash tables
- [x] Problem Set 5: Speller
- [x] Lab 5: Inheritance

---

## 🎯 Key Concepts

### Abstract Data Types vs. Data Structures

**What it is:**  
An **abstract data type (ADT)** defines *what* operations a structure supports (insert, delete, search). A **data structure** is the concrete *implementation* in memory.

**Why it matters:**  
Decouples interface from implementation — you can swap a linked list for a hash table without changing calling code if both implement the same ADT. This is the origin of Python's duck typing and Go's interfaces.

**Examples:**
| ADT | Possible Implementations |
|-----|--------------------------|
| List | Array, linked list |
| Queue | Linked list, circular array |
| Stack | Array, linked list |
| Dictionary / Map | Hash table, BST, trie |
| Set | Hash table, balanced BST |

---

### Linked Lists

**What it is:**  
A sequence of nodes where each node contains a value and a pointer to the next node. Nodes are scattered across the heap — not contiguous in memory like arrays.

**Why it matters:**  
Arrays have O(1) random access but O(n) insert/delete (must shift elements). Linked lists have O(n) access but O(1) insert/delete at a known position. Choosing between them is one of the most common engineering trade-offs.

**Node structure:**
```c
typedef struct Node
{
    int value;
    struct Node *next;  // Self-referential — pointer to same type
}
Node;
```

**Key points:**
- **Head pointer:** Points to the first node; `NULL` means empty list
- **Traversal:** Follow `.next` pointers until `NULL`
- **Insertion at head:** O(1) — create node, point it at current head, update head
- **Insertion at tail:** O(n) — must traverse to find end (unless you maintain a tail pointer)
- **Search:** O(n) — must check each node; cannot binary search (no random access)
- **Deletion:** O(n) to find node, but O(1) to unlink it once found
- **Memory:** Each node uses extra memory for the `*next` pointer (overhead vs. array)
- **No bounds:** Can grow indefinitely (limited only by heap)

**Visual:**
```
head
 |
[42 | *]──→ [17 | *]──→ [9 | *]──→ NULL
```

---

### Doubly Linked Lists

**What it is:**  
Each node has both a `next` and a `prev` pointer, allowing traversal in both directions.

**Why it matters:**  
Enables O(1) deletion when you already have the node pointer (no need to backtrack). Basis of Python's `collections.deque`.

**Node structure:**
```c
typedef struct Node
{
    int value;
    struct Node *next;
    struct Node *prev;
}
Node;
```

**Trade-off:** Double the pointer overhead per node; more complex insertion/deletion logic.

---

### Stacks

**What it is:**  
Last-In, First-Out (LIFO) data structure. Like a stack of plates — you can only add or remove from the top.

**Why it matters:**  
Function call stack (Week 4!) is a stack. Undo/redo history, expression parsing, DFS graph traversal, and browser back button are all stack-based.

**Operations:**
- **Push:** Add to top — O(1)
- **Pop:** Remove from top — O(1)
- **Peek:** View top without removing — O(1)

**Implementations:** Array (with top index) or linked list (insert/remove at head).

---

### Queues

**What it is:**  
First-In, First-Out (FIFO) data structure. Like a line at a store — first in, first served.

**Why it matters:**  
BFS graph traversal, task scheduling, message queues (Kafka, RabbitMQ), and print spoolers are all queue-based. In ML training, data loaders use queues to feed batches.

**Operations:**
- **Enqueue:** Add to back — O(1)
- **Dequeue:** Remove from front — O(1)

**Implementations:** Linked list (enqueue at tail, dequeue at head) or circular array.

---

### Hash Tables

**What it is:**  
An array of linked lists. A **hash function** maps a key to an index (bucket) in the array. Collisions (two keys mapping to the same bucket) are resolved with chaining (linked list at each bucket).

**Why it matters:**  
Average-case O(1) insert, delete, and lookup — the fastest general-purpose dictionary. Python's `dict`, Java's `HashMap`, Redis, and every database index you'll ever configure are hash tables (or B-tree variants). The speller problem set benchmarks this directly.

**Key points:**
- **Hash function:** Must be deterministic, fast, and distribute keys uniformly
- **Bucket array:** Size N array, each slot holds a linked list
- **Load factor:** `n_keys / n_buckets` — the lower it is, the fewer collisions
- **Collision:** Two keys hash to same index; solved by chaining or open addressing
- **Best case:** O(1) — key maps to a bucket with one or zero items
- **Worst case:** O(n) — all keys hash to the same bucket (terrible hash function)
- **Resize / rehash:** When load factor gets too high, double the table and rehash all keys
- **Real-world default:** Python `dict` starts at 8 buckets, resizes at 2/3 load

**Visual:**
```
Hash("apple")  → 2
Hash("banana") → 5
Hash("cherry") → 2  ← collision! chained at bucket 2

[0] → NULL
[1] → NULL
[2] → ["apple" | *] → ["cherry" | *] → NULL
[3] → NULL
...
[5] → ["banana" | *] → NULL
```

---

### Tries (Prefix Trees)

**What it is:**  
A tree where each node represents a character. Paths from root to a leaf spell out stored strings. The name comes from "re**trie**val."

**Why it matters:**  
O(k) lookup where k is the length of the key — independent of n (number of stored items). Autocomplete, spell checkers (the Speller problem!), IP routing tables, and genome sequence search all use trie variants.

**Key points:**
- **Node:** Contains an array of child pointers (one per possible character, e.g., 26 for lowercase letters) + a boolean `is_end`
- **Insert:** Follow (or create) path character by character; set `is_end = true` at last node
- **Search:** Follow path character by character; return `is_end` at final node
- **Prefix search:** Trie naturally supports "find all words starting with X"
- **Memory cost:** High — each node is an array of 26 pointers (or more for full Unicode)
- **Speed:** O(k) for k-character strings, regardless of dictionary size — O(1) with respect to n

**Visual:**
```
       root
      / | \
     c  b  t
     |  |  |
     a  a  h
     |  |  |
     t  t  e
     |      \
     ✓       r
              |
              ✓
("cat", "bat", "ther"...)
```

---

### Trees and Binary Search Trees (BSTs)

**What it is:**  
A hierarchical linked structure. In a **Binary Search Tree**, each node has at most two children, and all left-subtree values are less than the node's value; all right-subtree values are greater.

**Why it matters:**  
Enables O(log n) search, insert, and delete on ordered data — the bridge between the O(n) linked list and the O(1) hash table. Database indexes (B-Trees) are tree-based. Expression trees power compilers and calculators.

**Key points:**
- **Root:** Top node with no parent
- **Leaf:** Node with no children
- **Height:** Number of edges on longest path from root to leaf
- **BST search:** Compare target to current node; go left if smaller, right if larger
- **BST insert:** Search for the position where target would be; insert there
- **Balanced vs. unbalanced:** A balanced BST has height O(log n); inserting sorted data creates a degenerate tree of height O(n) (essentially a linked list!)
- **Self-balancing trees:** AVL trees, Red-Black trees automatically rebalance — used in `std::map` (C++) and `TreeMap` (Java)

**BST node structure:**
```c
typedef struct Node
{
    int value;
    struct Node *left;
    struct Node *right;
}
Node;
```

---

### Comparing Data Structures

**Decision guide:**

| Structure | Insert | Search | Delete | Space | Best Use Case |
|-----------|--------|--------|--------|-------|---------------|
| Array | O(n) | O(n) / O(log n)* | O(n) | Low | Fixed-size, random access |
| Linked List | O(1) head | O(n) | O(n) | Medium | Dynamic size, frequent insert/delete |
| Stack | O(1) | O(n) | O(1) top | Low | LIFO ordering |
| Queue | O(1) | O(n) | O(1) front | Low | FIFO ordering |
| Hash Table | O(1) avg | O(1) avg | O(1) avg | High | Fast key-value lookup |
| BST | O(log n) | O(log n) | O(log n) | Medium | Ordered data, range queries |
| Trie | O(k) | O(k) | O(k) | Very High | String prefix search |

*O(log n) if sorted and using binary search

---

## 💻 Code Examples

### Linked List — Build and Traverse
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *next;
}
Node;

// Insert at head — O(1)
Node *prepend(Node *head, int value)
{
    Node *node = malloc(sizeof(Node));
    if (node == NULL)
    {
        return head;  // Allocation failed
    }
    node->value = value;
    node->next = head;
    return node;   // New head
}

// Print all nodes
void print_list(Node *head)
{
    for (Node *cur = head; cur != NULL; cur = cur->next)
    {
        printf("%i → ", cur->value);
    }
    printf("NULL\n");
}

// Free all nodes — critical!
void free_list(Node *head)
{
    Node *cur = head;
    while (cur != NULL)
    {
        Node *next = cur->next;  // Save next before freeing!
        free(cur);
        cur = next;
    }
}

int main(void)
{
    Node *list = NULL;

    list = prepend(list, 3);
    list = prepend(list, 2);
    list = prepend(list, 1);

    print_list(list);   // 1 → 2 → 3 → NULL

    free_list(list);
    return 0;
}
```

---

### Stack — Array Implementation
```c
#include <stdio.h>
#include <stdbool.h>

#define CAPACITY 10

typedef struct
{
    int items[CAPACITY];
    int top;
}
Stack;

void stack_init(Stack *s)    { s->top = -1; }
bool stack_empty(Stack *s)   { return s->top == -1; }
bool stack_full(Stack *s)    { return s->top == CAPACITY - 1; }

bool push(Stack *s, int value)
{
    if (stack_full(s)) return false;
    s->items[++(s->top)] = value;
    return true;
}

int pop(Stack *s)
{
    if (stack_empty(s)) return -1;   // Sentinel; use error codes in production
    return s->items[(s->top)--];
}

int main(void)
{
    Stack s;
    stack_init(&s);

    push(&s, 10);
    push(&s, 20);
    push(&s, 30);

    printf("%i\n", pop(&s));   // 30 (LIFO)
    printf("%i\n", pop(&s));   // 20
    printf("%i\n", pop(&s));   // 10

    return 0;
}
```

---

### Queue — Linked List Implementation
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *next;
}
Node;

typedef struct
{
    Node *front;
    Node *back;
}
Queue;

void queue_init(Queue *q) { q->front = q->back = NULL; }

// Enqueue at back — O(1)
void enqueue(Queue *q, int value)
{
    Node *node = malloc(sizeof(Node));
    node->value = value;
    node->next = NULL;

    if (q->back == NULL)   // Empty queue
    {
        q->front = q->back = node;
    }
    else
    {
        q->back->next = node;
        q->back = node;
    }
}

// Dequeue from front — O(1)
int dequeue(Queue *q)
{
    if (q->front == NULL) return -1;

    Node *temp = q->front;
    int value = temp->value;

    q->front = q->front->next;
    if (q->front == NULL) q->back = NULL;   // Queue now empty

    free(temp);
    return value;
}

int main(void)
{
    Queue q;
    queue_init(&q);

    enqueue(&q, 1);
    enqueue(&q, 2);
    enqueue(&q, 3);

    printf("%i\n", dequeue(&q));   // 1 (FIFO)
    printf("%i\n", dequeue(&q));   // 2
    printf("%i\n", dequeue(&q));   // 3

    return 0;
}
```

---

### Hash Table — String Keys with Chaining
```c
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUCKETS 26

typedef struct Node
{
    char *word;
    struct Node *next;
}
Node;

Node *table[BUCKETS];   // Global array, initialized to NULL

// Simple hash: first letter of word → bucket index
int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Insert word into hash table
void insert(const char *word)
{
    int bucket = hash(word);

    Node *node = malloc(sizeof(Node));
    node->word = strdup(word);
    node->next = table[bucket];   // Prepend to chain
    table[bucket] = node;
}

// Search for word
bool search(const char *word)
{
    int bucket = hash(word);
    for (Node *cur = table[bucket]; cur != NULL; cur = cur->next)
    {
        if (strcasecmp(cur->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

int main(void)
{
    insert("apple");
    insert("avocado");   // Same bucket as "apple" (both start with 'a')
    insert("banana");

    printf("%s\n", search("apple")   ? "found" : "not found");   // found
    printf("%s\n", search("cherry")  ? "found" : "not found");   // not found

    return 0;
}
```

---

### BST — Insert and Search
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *left;
    struct Node *right;
}
Node;

// Create a new node
Node *new_node(int value)
{
    Node *node = malloc(sizeof(Node));
    node->value = value;
    node->left = node->right = NULL;
    return node;
}

// Insert — returns new root
Node *insert(Node *root, int value)
{
    if (root == NULL) return new_node(value);

    if (value < root->value)
        root->left = insert(root->left, value);
    else if (value > root->value)
        root->right = insert(root->right, value);

    return root;   // Value already in tree: no duplicate
}

// Search
bool search(Node *root, int target)
{
    if (root == NULL) return false;
    if (target == root->value) return true;
    if (target < root->value) return search(root->left, target);
    return search(root->right, target);
}

// In-order traversal (sorted output!)
void inorder(Node *root)
{
    if (root == NULL) return;
    inorder(root->left);
    printf("%i ", root->value);
    inorder(root->right);
}

int main(void)
{
    Node *tree = NULL;
    tree = insert(tree, 5);
    tree = insert(tree, 3);
    tree = insert(tree, 7);
    tree = insert(tree, 1);
    tree = insert(tree, 4);

    inorder(tree);   // 1 3 4 5 7 — sorted!
    printf("\n");

    printf("%s\n", search(tree, 4) ? "found" : "not found");   // found
    printf("%s\n", search(tree, 6) ? "found" : "not found");   // not found

    return 0;
}
```

---

### Trie — Insert and Search
```c
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHA 26

typedef struct Node
{
    struct Node *children[ALPHA];
    bool is_end;
}
Node;

Node *new_node(void)
{
    Node *node = calloc(1, sizeof(Node));   // calloc zeros all pointers
    return node;
}

void insert(Node *root, const char *word)
{
    Node *cur = root;
    for (int i = 0; word[i]; i++)
    {
        int idx = tolower(word[i]) - 'a';
        if (cur->children[idx] == NULL)
        {
            cur->children[idx] = new_node();
        }
        cur = cur->children[idx];
    }
    cur->is_end = true;
}

bool search(Node *root, const char *word)
{
    Node *cur = root;
    for (int i = 0; word[i]; i++)
    {
        int idx = tolower(word[i]) - 'a';
        if (cur->children[idx] == NULL) return false;
        cur = cur->children[idx];
    }
    return cur->is_end;
}

int main(void)
{
    Node *trie = new_node();

    insert(trie, "cat");
    insert(trie, "car");
    insert(trie, "card");
    insert(trie, "bat");

    printf("%s\n", search(trie, "car")  ? "found" : "not found");   // found
    printf("%s\n", search(trie, "ca")   ? "found" : "not found");   // not found (prefix only)
    printf("%s\n", search(trie, "card") ? "found" : "not found");   // found

    return 0;
}
```

---

## 📖 Important Terms

| Term | Definition | Example |
|------|------------|---------|
| **Abstract Data Type (ADT)** | Interface of operations, not implementation | Stack: push, pop, peek |
| **Linked list** | Nodes connected by pointers | `[1]→[2]→[3]→NULL` |
| **Node** | Struct holding value + pointer(s) | `{int value; Node *next;}` |
| **Head** | First node pointer in a linked list | `Node *head = NULL;` |
| **Self-referential struct** | Struct with pointer to same type | `struct Node *next;` |
| **Stack** | LIFO structure | Push/pop from top |
| **Queue** | FIFO structure | Enqueue back, dequeue front |
| **Hash function** | Maps key to array index | `hash("apple") → 2` |
| **Collision** | Two keys map to same bucket | Chain them in a list |
| **Chaining** | Linked list at each hash bucket | Resolves collisions |
| **Load factor** | Keys / buckets ratio | Should stay below ~0.7 |
| **BST** | Binary Search Tree | Left < node < right |
| **Trie** | Tree for string prefix search | Autocomplete |
| **Traversal** | Visiting all nodes | In-order, pre-order, BFS |
| **In-order traversal** | Left → Node → Right in BST | Produces sorted output |
| **Sentinel** | Dummy value signaling empty/error | `-1` for empty pop |
| **calloc** | Allocate + zero-initialize | Safe for pointer arrays |

---

## 🔧 Problem Sets

**Problem Set 5:**

**Lab: Inheritance**
- **Task:** Simulate genetic inheritance of blood type across three generations
- **Concepts:** Structs, dynamic allocation, recursion (tree-shaped allocation)
- **Approach:** Recursively `malloc` parent nodes; assign alleles; free recursively from leaves up

**Problem: Speller**
- **Task:** Build a spell-checker that loads a dictionary and checks a text document for misspellings
- **Concepts:** Hash tables (or tries), file I/O, performance benchmarking
- **Approach:**
  - `load()` — read dictionary file, hash each word, insert into table
  - `check(word)` — hash the word, search the chain at that bucket
  - `size()` — return word count
  - `unload()` — free every node in every bucket
- **Performance goal:** Minimize time in `load`, `check`, and `unload`
- **Key insight:** A better hash function and more buckets dramatically reduces check time

---

## 💡 Key Takeaways

1. **No single best data structure** — every choice is a trade-off: speed vs. memory, insert vs. lookup, simplicity vs. capability
2. **Hash tables are the everyday workhorse** — O(1) average is why Python `dict` and database indexes default to them
3. **Linked lists enable O(1) insert without reallocation** — arrays shift; linked lists just re-point
4. **Tries are O(k), not O(n)** — the dictionary size is irrelevant; only key length matters
5. **Self-referential structs are the building block of every recursive structure** — linked lists, trees, tries, graphs
6. **Always `free` recursively for tree structures** — free leaves before parents or you lose the pointers
7. **A bad hash function destroys hash table performance** — O(1) average assumes uniform distribution
8. **In-order traversal of a BST produces sorted output** — insert unsorted, traverse sorted for free
9. **These patterns appear everywhere in production** — Python's `dict`, pandas `Index`, Redis sorted sets, database B-trees, LLM vocabulary lookup tables all derive from this week

---

## 🔗 Resources

- [CS50 Week 5](https://cs50.harvard.edu/x/2024/weeks/5/)
- [VisuAlgo — Data Structure Visualizer](https://visualgo.net/)
- [Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Hash Table (Wikipedia)](https://en.wikipedia.org/wiki/Hash_table)
- [Trie (Wikipedia)](https://en.wikipedia.org/wiki/Trie)
- [CS50 Shorts: Linked Lists, Hash Tables, Tries](https://cs50.harvard.edu/x/2024/shorts/)

---

## 📝 My Notes

**What clicked:**
- A hash table is just "an array of linked lists" — once I saw it that way, the whole structure made sense
- Python's `dict` is a hash table under the hood; now I understand why key lookup is O(1) and why key order is insertion-order since Python 3.7 (they improved the implementation)
- The trie `is_end` flag is critical — without it, every prefix would look like a valid word
- BST in-order traversal outputting sorted data is elegant: you get a sort for free just by traversal order

**Challenges:**
- Freeing linked list: the classic mistake is `free(cur); cur = cur->next;` — you freed the node, the next pointer is now invalid
- Hash function design: getting uniform distribution is harder than it looks; simple character-sum functions produce terrible clusters
- Speller performance: getting load time under 0.05 seconds requires both a good hash function AND enough buckets (I used 65,536)
- Recursive tree freeing: must free children before the node itself (post-order free)

**Aha moments:**
- `calloc` zeroing all pointers is not just convenience — for a trie node with 26 child pointers, it's essential; uninitialized pointers are garbage addresses (instant segfault)
- Hash table with 26 buckets (one per letter) is just a very small trie at depth 1
- The Speller problem is a miniature search engine — load an index, query it, report misses; the architecture is identical to an inverted index in Elasticsearch or Lucene
- BST degenerates to a linked list if you insert sorted data — this is why `git` stores object trees as content-addressed hashes (randomized), not sorted keys

**To review:**
- Balancing BSTs: AVL and Red-Black tree rotation rules (Stage 3 math)
- Graph representations: adjacency list (linked list variant) and adjacency matrix (2D array) — coming in later algorithms work
- Min-heap / max-heap (priority queue) — used in Dijkstra, A*, and ML training schedulers
- B-Tree (disk-optimized BST used in database indexes) — Stage 2 deep dive

**Roadmap connection:**
- **Stage 1 (now):** Python `dict`, `set`, `list`, `deque` — you're using these structures every day; now you know the mechanics
- **Stage 2 (Data Engineering):** Database indexes are B-Trees; Redis uses hash tables + skip lists; Kafka queues are persistent FIFO structures
- **Stage 3 (ML):** Priority queues power beam search in NLP; tries power subword tokenizers (BPE — Byte Pair Encoding used in GPT models); graph structures underlie GNNs
- **Stage 4–5 (LLM Engineering):** Token vocabularies are hash maps from string → integer; vector store indexes (FAISS, Annoy) are tree variants optimized for approximate nearest-neighbor search
- **Speller = miniature RAG pipeline:** load index (embed + store), check word (query), report misses (hallucination detection) — the architecture is the same at every scale

**Common mistakes:**
- `free(node)` before saving `node->next` — the most common linked list bug
- Treating `calloc` and `malloc` as interchangeable — for pointer arrays, always use `calloc`
- Forgetting `free` for `strdup`'d strings inside nodes — two-level leak (node + word)
- Hash function returning negative values (e.g., with signed arithmetic on chars) — always cast to `unsigned` or `tolower` first

---

## ➡️ Next Steps

**Next week:** 06_python.md (Python syntax, data types, libraries — and how C concepts map to Python abstractions)  
**To practice:**
- Implement Speller with both hash table AND trie; benchmark both; understand the trade-off empirically
- Reimplement linked list, stack, queue in Python using classes — map `struct Node` to `@dataclass`
- Build a BST in Python with `insert`, `search`, and `inorder` — same logic, no pointer syntax
- Read CPython source for `dict` to see the real hash table implementation
- Benchmark Python `dict` vs. `list` search on 1M elements — confirm O(1) vs. O(n) empirically