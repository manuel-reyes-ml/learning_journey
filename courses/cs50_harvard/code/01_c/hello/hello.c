#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get name from user
    string name = get_string("What´s your name? ");
    // Print 'hello' + name variable
    printf("hello, %s\n", name);
}