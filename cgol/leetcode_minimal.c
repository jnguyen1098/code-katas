#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

// When threads wait at a barrier, all other threads must wait before they can proceed.
// Some threads may finish writing to the CGOL temporary array before others, and we can't
// just proceed without them. For n threads, this barrier requires n waits.
pthread_barrier_t barrier;

// Context object
struct game_t {
    int rows;
    int cols;
    char *board;
    char *buffer;
    int nThreads;
    int nIterations;
    bool display;
};

// Neighbour counting function
int count_neighbours(struct game_t *game, int x, int y)
{
    // Eight possible moves
    int moves[8][2] = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1},            {0, 1},
        {1, -1},  {1, 0},   {1, 1},
    };
    
    int count = 0;
    
    // There are eight possible neighboring spots
    for (int i = 0; i < 8; i++) {

        // dx = change in x, we get it from the moves array
        int dx = moves[i][0];

        // dy = change in y, . . .
        int dy = moves[i][1];
        
        // The new x and y
        int nx = x + dx;
        int ny = y + dy;
        
        // There are three AND clauses. The first two just check if it's a valid coord.
        // The last one checks if there really is a neighbour in the array. This is done using
        // a 1D flattened approach (look back to CIS*2030).
        if ((nx >= 0 && nx < game->rows) && (ny >= 0 && ny < game->cols) && game->board[game->cols * nx + ny] == 1) {
            count += 1;
        }
    }
    
    return count;
}

// Get new cell value. 1 means will live, 0 means will die.
// Need neighbour count as well as the current state
// if dead but 3 near, then revive
// if 2 or 3 neighbours and youre alive, continue living
// if more than 3 neighbors, die by overpopulation
// if alive but less than 2 neighbors, die from loneliness
int get_outcome(struct game_t *game, int x, int y)
{
    int neigh = count_neighbours(game, x, y);
    int state = game->board[game->cols * x + y];
    if (state == 0) {
        if (neigh == 3) {
            return 1;
        } else {
            return 0;
        }
    } 
    if (neigh < 2) {
        return 0;
    }
    if (neigh == 2 || neigh == 3) {
        return 1;
    }
    return 0;
}

// Returns two integers, start and end, using pointer out variables.
// Gets the start (inclusive) and end (inclusive) of the work that must be done.
// Determined using the rank, number of workers, and the amount of work needed
// 
// We take the floor of work_count divided by num_workers - this is our offset.
// Every thread is responsible for some unique offset count. However, the last thread
// will take every remaining leftovers (as you can see in the ternary).
void get_work(int work_count, int num_workers, int rank, int *startOut, int *endOut)
{
    int slice_size = work_count / num_workers;
    int start = rank * slice_size;
    int end = rank < num_workers - 1 ? (rank + 1) * slice_size : work_count;
    *startOut = start;
    *endOut = end - 1;
}

// Message passing struct used to tell each thread what rank they are
// as well as a reference to the game struct, though I could probably
// just move this out into global scope lol but this is relatively important
// for more complex applications of parallel programming.
struct work_unit_t {
    int rank;
    struct game_t *game;
};

// Discrete work function for a thread. Each thread calls this function
void *work_function(void *input)
{
    // Cast the work unit struct from the input
    struct work_unit_t *work = input;

    // Define our context variables
    int rank = work->rank;
    struct game_t *game = work->game;

    int rows = game->rows;
    int cols = game->cols;

    int total_work = rows * cols;
    int num_workers = game->nThreads;

    // Get work start and end as explained earlier. It is written in start and end
    int start, end;
    get_work(total_work, num_workers, rank, &start, &end);

    // Get outcomes for conway's game of life using the start and end range
    // as specified from earlier - we only want to work on our own territory.
    //
    // Buffer array is used as we do not want to clobber other threads from
    // reading their own data.
    for (int i = start; i <= end; i++) {
        game->buffer[i] = get_outcome(game, i / cols, i % cols);
    }

    // As stated earlier, all threads will block here until everyone arrives
    pthread_barrier_wait(&barrier);

    // Then, and only then, does the rank 0 thread swap the two boards
    if (rank == 0) {
        char *tmp = game->board;
        game->board = game->buffer;
        game->buffer = tmp;
    }

    // Then, we wait once more just in case
    pthread_barrier_wait(&barrier);

    return NULL;
}

void iterate_parallel(struct game_t *game)
{
    // Initialize the barrier with the number of workers
    int num_workers = game->nThreads;
    pthread_barrier_init(&barrier, NULL, num_workers);

    // Create work units - note that we are using an array because
    // threads share the same address space - if we just create the
    // struct by reference on the fly we'd clobber the values each run
    pthread_t threads[num_workers];
    struct work_unit_t work[num_workers];

    // Write each work unit - we just put the rank and the context
    for (int i = 0; i < num_workers; i++) {
        work[i].rank = i;
        work[i].game = game;
    }

    // Create each thread
    for (int i = 0; i < num_workers; i++) {
        pthread_create(&threads[i], NULL, work_function, &work[i]);
    }

    // Join each thread
    for (int i = 0; i < num_workers; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // Destroy the barrier
    pthread_barrier_destroy(&barrier);
}

// This isn't actually needed in the assignment, but it is needed
// for leetcode to pipeline its input into my code correctly
void gameOfLife(int** board, int boardSize, int* boardColSize)
{
    int rows = boardSize;
    int cols = *boardColSize;
    
    int totalCells = rows * cols;
    
    char myBoard[totalCells];
    char myBuffer[totalCells];
    
    struct game_t game = {
        .board = myBoard,
        .buffer = myBuffer,
        .rows = rows,
        .cols = cols,
        .nThreads = 16,
        .nIterations = 1,
    };
    
    int iter = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            myBoard[iter++] = board[i][j];
        }
    }
    
    iterate_parallel(&game);
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            board[i][j] = game.board[i * cols + j];
        }
    }
}

