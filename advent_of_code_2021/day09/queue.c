#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

struct queue {
    int *data;
    size_t head;
    size_t nel;
    size_t max;
};

struct queue *create_queue(size_t size)
{
    struct queue *queue = calloc(1, sizeof(struct queue));
    queue->data = calloc(sizeof(int), size);
    queue->max = size;
    return queue;
}

void destroy_queue(struct queue *queue)
{
    free(queue->data);
    free(queue);
}

int push(struct queue *queue, int val)
{
    if (queue->nel == queue->max) return 0;
    queue->data[(queue->head + queue->nel) % queue->max] = val;
    queue->nel++;
    return 1;
}

int pop(struct queue *queue)
{
    if (queue->nel == 0) {
        fprintf(stderr, "Popped empty queue\n");
        exit(1);
    }
    int val = queue->data[queue->head];
    queue->head = (queue->head + 1) % queue->max;
    queue->nel--;
    return val;
}

void print_queue(struct queue *queue)
{
    puts("All Data");
    for (int i = 0; i < queue->max; i++) {
        printf("%d ", queue->data[i]);
    }
    puts("");
    puts("Head");
    for (int i = 0; i < queue->nel; i++) {
        printf("%d ", queue->data[(i + queue->head) % queue->max]);
    }
    puts("\n");
}

void init_test(void)
{
    struct queue *queue = create_queue(10);
    assert(queue);
    assert(queue->data != NULL);
    assert(queue->head == 0);
    assert(queue->nel == 0);
    assert(queue->max == 10);
    destroy_queue(queue);
}

void push_test(void)
{
    struct queue *queue = create_queue(10);
    for (int i = 0; i < 10; i++) {
        assert(push(queue, i * 10));
        assert(queue->nel == i + 1);
        assert(queue->data[i] == i * 10);
    }
    destroy_queue(queue);
}

void pop_test(void)
{
    struct queue *queue = create_queue(10);
    for (int i = 0; i < 10; i++) {
        push(queue, i * 10);
    }
    assert(queue->nel == 10);
    for (int i = 0; i < 10; i++) {
        assert(pop(queue) == i * 10);
        assert(queue->nel == 10 - i - 1);
        assert(queue->head == (i + 1) % queue->max);
    }
    destroy_queue(queue);
}

void spillover_test(void)
{
    struct queue *queue = create_queue(10);
    for (int i = 0; i < 10; i++) {
        push(queue, i * 10);
    }
    print_queue(queue);
    for (int i = 0; i < 5; i++) {
        pop(queue);
    }
    assert(queue->nel == 5);
    print_queue(queue);
    for (int i = 0; i < 5; i++) {
        push(queue, i);
    }
    assert(queue->nel == 10);
    print_queue(queue);
    destroy_queue(queue);
}

void run_all_tests(void)
{
    init_test();
    push_test();
    pop_test();
    spillover_test();
}

int main(void)
{
    run_all_tests();
    return 0;
}
