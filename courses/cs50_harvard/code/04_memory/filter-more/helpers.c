#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the average and round it. 
            // Divide by 3.0 (a float) to prevent integer division truncation before rounding.
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // Only loop halfway through the width! 
        // If you loop all the way, you'll swap the pixels back to their original places.
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the original image to read from
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Iterate through every pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0, sumGreen = 0, sumBlue = 0;
            float count = 0.0; 

            // Look at neighboring pixels (a 3x3 grid centered on i, j)
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di; // neighbor row
                    int nj = j + dj; // neighbor col

                    // Make sure the neighbor is actually inside the image boundaries
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sumRed += copy[ni][nj].rgbtRed;
                        sumGreen += copy[ni][nj].rgbtGreen;
                        sumBlue += copy[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }
            
            // Assign the blurred averages to the original image
            image[i][j].rgbtRed = round(sumRed / count);
            image[i][j].rgbtGreen = round(sumGreen / count);
            image[i][j].rgbtBlue = round(sumBlue / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy to read from
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Define the Sobel kernels
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Use floats to accumulate kernel calculations
            float gxRed = 0, gxGreen = 0, gxBlue = 0;
            float gyRed = 0, gyGreen = 0, gyBlue = 0;

            
            
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Only process if neighbor is within bounds 
                    // (Pixels outside bounds are treated as solid black/0, meaning they add nothing to the sum)
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        // Array indices for Gx/Gy must be 0, 1, or 2 (hence + 1)
                        int weightX = Gx[di + 1][dj + 1];
                        int weightY = Gy[di + 1][dj + 1];

                        gxRed += copy[ni][nj].rgbtRed * weightX;
                        gxGreen += copy[ni][nj].rgbtGreen * weightX;
                        gxBlue += copy[ni][nj].rgbtBlue * weightX;

                        gyRed += copy[ni][nj].rgbtRed * weightY;
                        gyGreen += copy[ni][nj].rgbtGreen * weightY;
                        gyBlue += copy[ni][nj].rgbtBlue * weightY;
                    }
                }
            }

            // Calculate magnitude: √(Gx² + Gy²)
            int finalRed = round(sqrt(gxRed * gxRed + gyRed * gyRed));
            int finalGreen = round(sqrt(gxGreen * gxGreen + gyGreen * gyGreen));
            int finalBlue = round(sqrt(gxBlue * gxBlue + gyBlue * gyBlue));

            // Cap at 255 and assign back to the image
            image[i][j].rgbtRed = (finalRed > 255) ? 255 : finalRed;
            image[i][j].rgbtGreen = (finalGreen > 255) ? 255 : finalGreen;
            image[i][j].rgbtBlue = (finalBlue > 255) ? 255 : finalBlue;
        }
    }
    return;
}