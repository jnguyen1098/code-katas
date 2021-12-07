#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define int unsigned long long int

#define FILENAME "input"
#define MAX_FILE 10000
#define NUM_FISH 300
#define ANSWER   1686252324092
#define DAYS     256

typedef struct arr_struct {
    int *data;
    size_t size;
} arr_t;

arr_t read_ints(char *filename, int max)
{
    char *tok = strtok(fgets(malloc(MAX_FILE), BUFSIZ, fopen(filename, "r")), ",");
    int *ints = malloc(max * sizeof(int));
    int i = 0;
    while (tok) {
        ints[i++] = atoi(tok);
        tok = strtok(NULL, ",");
    }
    return (arr_t){.data = ints, .size = i};
}

int *counter(arr_t arr)
{
    int *cnt = calloc(9, sizeof(int));
    for (int i = 0; i < arr.size; i++) {
        cnt[arr.data[i]]++;
    }
    return cnt;
}

void advance(int *arr)
{
    static int tmp[9];
    for (int i = 0; i < 9; i++) {
        tmp[i] = arr[(i + 1) % 9];
    }
    tmp[6] += arr[0];
    for (int i = 0; i < 9; i++) {
        arr[i] = tmp[i];
    }
}

int main(void)
{
    arr_t arr = read_ints(FILENAME, NUM_FISH);

    int *data = counter(arr);

    for (int i = 0; i < DAYS; i++) {
        advance(data);
    }

    int sum = 0;
    for (int i = 0; i < 9; i++) {
        sum += data[i];
    }

    printf("%ld\n", sum);
    puts(sum == ANSWER ? "Solved" : "Error");

    return 0;
}
