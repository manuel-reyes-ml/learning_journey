#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Function prototypes to keep main clean
bool validate_key(string key);
void encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // 1. Check for correct number of arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // 2. Validate the key
    if (!validate_key(key))
    {
        printf("Key must contain 26 unique characters.\n");
        return 1;
    }

    // 3. Get plaintext from user
    string plaintext = get_string("plaintext:  ");

    // 4. Encrypt and print ciphertext
    printf("ciphertext: ");
    encrypt(plaintext, key);
    printf("\n");

    return 0;
}

// Checks if the key is valid (length 26, all alpha, no duplicates)
bool validate_key(string key)
{
    // Check length
    if (strlen(key) != 26)
    {
        return false;
    }

    // Check content (must be alpha) and duplicates
    // We use a small array to track which letters we've seen
    int seen[26] = {0};

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        // Convert current char to uppercase index (0-25) to check for duplicates
        int index = toupper(key[i]) - 'A';

        if (seen[index] > 0)
        {
            return false; // Found a duplicate
        }
        seen[index]++;
    }

    return true;
}

// Prints the encrypted message character by character
void encrypt(string plaintext, string key)
{
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];

        if (isalpha(c))
        {
            // Determine the index of the letter (0-25)
            // 'A' is 65, 'a' is 97
            int index = toupper(c) - 'A';

            // If original was uppercase, print uppercase key letter
            if (isupper(c))
            {
                printf("%c", toupper(key[index]));
            }
            // If original was lowercase, print lowercase key letter
            else
            {
                printf("%c", tolower(key[index]));
            }
        }
        else
        {
            // Non-alphabetical characters stay the same
            printf("%c", c);
        }
    }
}