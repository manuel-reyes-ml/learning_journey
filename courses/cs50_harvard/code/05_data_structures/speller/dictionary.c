// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Global word count for the size function
unsigned int word_count = 0;

// Increased N for better performance (65536 is a common choice for this size)
const unsigned int N = 65536;

// Hash table
node *table[N];

// Hashes word to a number
// Using the djb2 hash algorithm for better distribution than just the first letter
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;
    while ((c = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word_buffer[LENGTH + 1];

    // Read each word from the file
    while (fscanf(file, "%s", word_buffer) != EOF)
    {
        // Create a new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        // Copy word into node and set next pointer
        strcpy(new_node->word, word_buffer);

        // Hash the word to find the bucket
        unsigned int index = hash(word_buffer);

        // Insert node into the hash table (at the head of the list)
        new_node->next = table[index];
        table[index] = new_node;

        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to find which list to search
    unsigned int index = hash(word);

    // Traverse the linked list at that index
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // strcasecmp is perfect here for case-insensitivity
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        // Free every node in the linked list
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}