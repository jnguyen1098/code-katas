#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct arr_struct {
    int *data;
    size_t size;
} arr_t;

arr_t read_ints(char *filename, int max)
{
    char *tok = strtok(fgets(malloc(999999), BUFSIZ, fopen(filename, "r")), ",");
    int *ints = malloc(max * sizeof(int));
    int i = 0;
    while (tok) {
        ints[i++] = atoi(tok);
        tok = strtok(NULL, ",");
    }
    return (arr_t){.data = ints, .size = i};
}

int main(void)
{
    arr_t arr = read_ints("example", 5);
    for (int i = 0; i < arr.size; i++) {
        printf("%d\n", arr.data[i]);
    }
    return 0;
}
