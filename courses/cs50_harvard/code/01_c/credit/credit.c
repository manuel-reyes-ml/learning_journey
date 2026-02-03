#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // 1. Get input using CS50's get_long to handle 16-digit numbers
    long long number = get_long("Number: ");

    // Create copies of the number to use later
    long long original_number = number;
    long long length_checker = number;
    long long start_checker = number;

    // --- STEP 1: LUHN'S ALGORITHM ---
    int sum = 0;

    // We start with the last digit, which we DO NOT multiply.
    // So, we set our "multiply flag" to false initially.
    bool multiply_flag = false;

    // 2. Loop through the number until it runs out of digits
    while (number > 0)
    {
        // Get the last digit
        int digit = number % 10;

        if (multiply_flag)
        {
            // This is the "every other digit" part
            int product = digit * 2;

            // "Add those products’ digits together"
            // Example: if product is 12, we want 1 + 2 = 3
            // product / 10 gives the tens place (1)
            // product % 10 gives the ones place (2)
            sum += (product / 10) + (product % 10);
        }
        else
        {
            // Just add the digit to the sum
            sum += digit;
        }

        // Toggle the flag for the next iteration
        multiply_flag = !multiply_flag;

        // Remove the last digit from the number
        // Long type will chop off decimal digit(s)
        number = number / 10;
    }

    // 3. Check if the total's last digit is 0
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // --- STEP 2: CHECK LENGTH ---
    int length = 0;
    while (length_checker > 0)
    {
        length_checker = length_checker / 10;
        length++;
    }

    // --- STEP 3: CHECK STARTING DIGITS ---
    // We reduce the number until only the first 2 digits remain
    long long start_digits = original_number;
    while (start_digits >= 100)
    {
        start_digits = start_digits / 10;
    }
    // Now 'start_digits' holds the first two digits (e.g., 34, 55, 40)

    // --- STEP 4: DETERMINE CARD TYPE ---

    // Check AMEX (15 digits, starts with 34 or 37)
    if (length == 15 && (start_digits == 34 || start_digits == 37))
    {
        printf("AMEX\n");
        return 0;
    }
    // Check MASTERCARD (16 digits, starts with 51-55)
    else if (length == 16 && (start_digits >= 51 && start_digits <= 55))
    {
        printf("MASTERCARD\n");
        return 0;
    }
    // Check VISA (13 or 16 digits, starts with 4)
    // Note: If start_digits is 40-49, the integer division / 10 gives 4
    else if ((length == 13 || length == 16) && (start_digits / 10 == 4))
    {
        printf("VISA\n");
        return 0;
    }
    else
    {
        printf("INVALID\n");
        return 0;
    }
}