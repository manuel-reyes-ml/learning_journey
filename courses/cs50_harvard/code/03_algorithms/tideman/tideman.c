#include <cs50.h>
#include <stdio.h>
#include <string.h> // Added for strcmp

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool makes_cycle(int start, int end); // Custom helper prototype

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            // Update the ranks array at the current rank to hold the candidate's index
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Iterate through each ranked candidate
    for (int i = 0; i < candidate_count; i++)
    {
        // Compare them to every candidate ranked strictly lower than them
        for (int j = i + 1; j < candidate_count; j++)
        {
            // ranks[i] is preferred over ranks[j]
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Compare each candidate to every other candidate
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // If i is preferred over j
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            // If j is preferred over i
            else if (preferences[j][i] > preferences[i][j])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
            // If they are tied, do nothing.
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // A standard Bubble Sort
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            // Calculate strengths: how many voters preferred the winner
            int strength1 = preferences[pairs[j].winner][pairs[j].loser];
            int strength2 = preferences[pairs[j + 1].winner][pairs[j + 1].loser];

            // If the next pair has a higher strength, swap them
            if (strength1 < strength2)
            {
                pair temp = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temp;
            }
        }
    }
    return;
}

// Helper function to check if locking a pair creates a cycle using recursion
bool makes_cycle(int start, int end)
{
    // Base Case: If the end of the chain circles back to our starting winner, it's a cycle
    if (start == end)
    {
        return true;
    }

    // Recursive Step: Check all possible outward paths from 'end'
    for (int i = 0; i < candidate_count; i++)
    {
        // If there is an existing lock from 'end' to 'i'
        if (locked[end][i])
        {
            // See if that path eventually leads back to 'start'
            if (makes_cycle(start, i))
            {
                return true;
            }
        }
    }

    // If we exhaust all paths and never hit 'start', no cycle exists
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        // If tracing a path from the loser DOES NOT lead back to the winner
        if (!makes_cycle(pairs[i].winner, pairs[i].loser))
        {
            // It's safe to lock the pair
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // Look at each candidate
    for (int i = 0; i < candidate_count; i++)
    {
        bool is_source = true;

        // Check if ANY candidate is locked over them
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                is_source = false;
                break; // No need to keep checking, they aren't the source
            }
        }

        // If no one is locked over them, they are the source (the winner!)
        if (is_source)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}