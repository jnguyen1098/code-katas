#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

struct game_t {
    int rows;
    int cols;
    int nThreads;
    int nIterations;
    char *board;
    char *buffer;
    bool display;
};

struct pair_t {
    int x;
    int y;
};

char *create_board(int x, int y)
{
    return calloc(x * y, sizeof(char));
}

int get1d(struct game_t *game, int x, int y)
{
    return (game->cols * x) + y;
}

struct pair_t get2d(struct game_t *game, int disp)
{
    return (struct pair_t){
        .x = disp / game->cols,
        .y = disp % game->cols,
    };
}

void initializeBoard(struct game_t *game, void *data_ptr, int dataRows, int dataCols)
{
    assert(game->rows == dataRows);
    assert(game->cols == dataCols);

    game->board = create_board(dataRows, dataCols);

    // TODO clean this up
    game->buffer = create_board(dataRows, dataCols);
    memset(game->buffer, 64, dataRows * dataCols);

    char (*data)[dataCols] = data_ptr;

    for (int i = 0; i < dataRows; i++) {
        for (int j = 0; j < dataCols; j++) {
            game->board[get1d(game, i, j)] = data[i][j];
        }
    }
}

void destroyBoards(struct game_t *game)
{
    free(game->board);
    free(game->buffer);
}

int count(struct game_t *game, int x, int y)
{
    int moves[8][2] = {
        {-1, -1}, {-1, 0}, {-1, 1},
        {0, -1},            {0, 1},
        {1, -1},  {1, 0},    {1, 1},
    };
    
    int count = 0;
    
    for (int i = 0; i < 8; i++) {
        int dx = moves[i][0];
        int dy = moves[i][1];
        
        int nx = x + dx;
        int ny = y + dy;
        
        int disp = get1d(game, nx, ny);

        if ((nx >= 0 && nx < game->rows) && (ny >= 0 && ny < game->cols) && game->board[disp] == 1) {
            count += 1;
        }
    }
    
    return count;
}

int get_outcome(struct game_t *game, int x, int y)
{
    int neigh = count(game, x, y);
    int state = game->board[get1d(game, x, y)];
    
    assert(state == 0 || state == 1);
    
    if (state == 0) {
        if (neigh == 3) {
            return 1;
        } else {
            return 0;
        }
    } else {
        if (neigh < 2) {
            return 0;
        }
        if (neigh == 2 || neigh == 3) {
            return 1;
        }
        if (neigh > 3) {
            return 0;
        }
    }
    puts("hi you fucked up");
    printf("x=%d y=%d neigh=%d state=%d\n", x, y, neigh, state);
    exit(1);
}

struct pair_t get_work(int work_count, int num_workers, int rank)
{
    if (num_workers > work_count || rank >= num_workers) {
        printf("BRO WHAT DID YOU DO\n");
        assert(false);
    }
    int slice_size = work_count / num_workers;
    int start = rank * slice_size;
    int end = rank < num_workers - 1 ? (rank + 1) * slice_size : work_count;
    return (struct pair_t){ .x = start, .y = end - 1};
}

void iterate(struct game_t *game, int startInclusive, int endInclusive)
{
    for (int i = startInclusive; i <= endInclusive; i++) {
        struct pair_t mapping = get2d(game, i);
        // TODO remove this too
        assert(game->buffer[i] == 64);
        game->buffer[i] = get_outcome(game, mapping.x, mapping.y);
    }
}

void flush(struct game_t *game)
{
    for (int i = 0; i < game->rows * game->cols; i++) {
        assert(game->buffer[i] != 64);
    }
    char *tmp = game->board;
    game->board = game->buffer;
    game->buffer = tmp;
    // TODO temporary debugging
    memset(game->buffer, 64, game->cols * game->rows);
}

void iterate_all_slices(struct game_t *game, int num_workers)
{
    for (int i = 0; i < num_workers; i++) {
        struct pair_t work = get_work(game->rows * game->cols, num_workers, i);
        iterate(game, work.x, work.y);
    }
}

void testOutcome(struct game_t *game)
{
    assert(get_outcome(game, 11, 4) == 0);  // 1 dies underpopulation
    assert(get_outcome(game, 2, 7) == 1);  // 2 or 3 lives on 
    assert(get_outcome(game, 1, 1) == 0);  // overpopulation
    assert(get_outcome(game, 0, 13) == 1);  // revives
}

void testMapping(struct game_t *game)
{
    assert(get1d(game, 1, 0) == 21);
    assert(get1d(game, 6, 1) == 127);
    assert(get2d(game, 21).x == 1 && get2d(game, 21).y == 0);
    assert(get2d(game, 127).x == 6 && get2d(game, 127).y == 1);
}

void testCount(struct game_t *game)
{
    assert(count(game, 11, 11) == 6);
}

void testContiguous(struct game_t *game, void *data_ptr)
{
    char (*expected)[game->cols] = data_ptr;
    
    iterate(game, 0, game->rows * game->cols - 1);
    flush(game);
    
    for (int i = 0; i < game->rows; i++) {
        for (int j = 0; j < game->cols; j++) {
            if (game->board[get1d(game, i, j)] != expected[i][j]) {
                printf("Mismatch of result at %d,%d\n", i, j);
            }
        }
    }
}

void testSplitWorkSinglethreaded(struct game_t *game, void *data_ptr)
{
    char (*expected)[game->cols] = data_ptr;
    
    iterate_all_slices(game, 7);
    flush(game);
    
    for (int i = 0; i < game->rows; i++) {
        for (int j = 0; j < game->cols; j++) {
            if (game->board[get1d(game, i, j)] != expected[i][j]) {
                printf("Mismatch of result at %d,%d\n", i, j);
            }
        }
    }
}

void test(struct game_t *game, void *data, int dataRows, int dataCols, void *expected)
{
    initializeBoard(game, data, dataRows, dataCols);
    testCount(game);
    testMapping(game);
    testOutcome(game);
    destroyBoards(game);

    initializeBoard(game, data, dataRows, dataCols);
    testContiguous(game, expected);
    destroyBoards(game);

    initializeBoard(game, data, dataRows, dataCols);
    testSplitWorkSinglethreaded(game, expected);
    destroyBoards(game);
}

void run_all_tests()
{
    puts("STARTING TEST");
    char TEST[21][21] = {
        {1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0},
        {1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1},
        {0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1},
        {1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0},
        {1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1},
        {1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0},
        {0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0},
        {0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0},
        {0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1},
        {0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1},
        {0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0},
        {1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1},
        {1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1},
        {0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0},
        {0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1},
        {0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1},
        {1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1},
        {1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0},
        {1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1},
    };
    
    char RESULT[21][21] = {
        {1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0},
        {1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0},
        {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0},
        {1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1},
        {0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1},
        {0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1},
        {0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0},
        {0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0},
        {1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0},
        {0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0},
        {0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1},
        {0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1},
        {0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},
        {1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0},
        {1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1},
    };
    
    struct game_t game = {
        .nThreads = 1,
        .rows = 21,
        .cols = 21,
        .nIterations = 1,
        .display = true,
    };
    
    test(&game, TEST, 21, 21, RESULT);

    puts("ENDING TEST");
}


void gameOfLife(int** board, int boardSize, int* boardColSize){
    struct game_t game = {
        .rows = boardSize,
        .cols = *boardColSize,
    };
    
    char *(*flatten)(void) = ({
        char *flat(void) {
            char *result = calloc(boardSize * (*boardColSize), sizeof(char));
            int p = 0;
            for (int i = 0; i < boardSize; i++) {
                for (int j = 0; j < *boardColSize; j++) {
                    result[p++] = (char)board[i][j];
                }
            }
            return result;
        }
        flat;
    });
    
    initializeBoard(&game, flatten(), boardSize, *boardColSize);
    iterate(&game, 0, game.rows * game.cols - 1);
    flush(&game);
    
    for (int i = 0; i < boardSize; i++) {
        for (int j = 0; j < *boardColSize; j++) {
            board[i][j] = game.board[get1d(&game, i, j)];
        }
    }
}

int main(void)
{
    run_all_tests();
}