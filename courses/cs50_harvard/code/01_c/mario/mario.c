#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt the user for the pyramid´s height
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    // Print a pyramid for that height
    for (int i = 0; i < h; i++)
    {
        // Inner Loop 1: Print the spaces
        for (int j = 0; j < (h - i - 1); j++)
        {
            printf(" ");
        }

        // Inner loop 2: Print left hashes
        for (int k = 0; k < (i + 1); k++)
        {
            printf("#");
        }

        // THE GAP: Print 2 spaces (no loop needed, it's constant)
        printf("  ");

        // Inner loop 3: Print right hashes
        for (int l = 0; l < (i + 1); l++)
        {
            printf("#");
        }

        printf("\n");
    }
}