#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Function prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // 1. Prompt the user for some text
    string text = get_string("Text: ");

    // 2. Count letters, words, and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // 3. Calculate the Coleman-Liau index
    // Formula: index = 0.0588 * L - 0.296 * S - 15.8
    // L = letters per 100 words
    // S = sentences per 100 words

    // Cast to float to avoid integer division issues
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    // 4. Print the grade level (rounded to nearest integer)
    int grade = round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int count = 0;
    // Iterate through every character
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Only count alphabetic characters (a-z, A-Z)
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1; // Start at 1 because the last word usually doesn't have a space after it

    // Check for empty string case just to be safe
    if (strlen(text) == 0)
    {
        return 0;
    }

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // A space indicates a new word
        if (text[i] == ' ')
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count periods, exclamation points, and question marks
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}