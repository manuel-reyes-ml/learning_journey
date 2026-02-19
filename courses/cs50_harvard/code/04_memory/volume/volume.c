// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    // The header is exactly 44 bytes. A uint8_t is exactly 1 byte.
    uint8_t header[HEADER_SIZE];

    // Read 44 bytes from input into the header array
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);
    // Write those exact 44 bytes from the array into the output file
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file
    // A standard WAV sample is a 16-bit signed integer (int16_t).
    int16_t buffer;

    // fread returns the number of items successfully read.
    // It will return 0 when it hits the end of the file, breaking the loop.
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        // Update the volume by multiplying by the factor
        buffer = buffer * factor;

        // Write the single updated sample to the output file
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}