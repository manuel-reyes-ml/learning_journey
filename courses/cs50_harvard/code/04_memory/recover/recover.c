#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Define the block size for an SD card
#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // 1. Ensure the user provided the forensic image
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover card.raw\n");
        return 1;
    }

    // 2. Open the memory card file
    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        fprintf(stderr, "Could not open file %s\n", argv[1]);
        return 1;
    }

    // Variables for recovery
    BYTE buffer[BLOCK_SIZE];
    int image_count = 0;
    FILE *out_file = NULL;
    char filename[8]; // Enough for "xxx.jpg\0"

    // 3. Read the card block by block
    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        // Check if this block is the start of a new JPEG
        // Using the bitwise math: (buffer[3] & 0xf0) == 0xe0
        bool is_jpeg = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
                       (buffer[3] & 0xf0) == 0xe0;

        if (is_jpeg)
        {
            // If we already have a file open, close it before starting a new one
            if (out_file != NULL)
            {
                fclose(out_file);
            }

            // Create a new filename (e.g., 000.jpg)
            sprintf(filename, "%03i.jpg", image_count);
            out_file = fopen(filename, "w");

            if (out_file == NULL)
            {
                fprintf(stderr, "Could not create output file %s\n", filename);
                return 1;
            }

            image_count++;
        }

        // If we have an active JPEG file, write the current block to it
        if (out_file != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, out_file);
        }
    }

    // 4. Final Cleanup
    if (out_file != NULL)
    {
        fclose(out_file);
    }
    fclose(raw_file);

    printf("Recovery complete. Found %i images.\n", image_count);
    return 0;
}
