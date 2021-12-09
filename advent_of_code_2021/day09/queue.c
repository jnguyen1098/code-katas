#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

struct queue {
    int *data;
    int head;
    int nel;
    int max;
};

struct queue *create_queue(size_t size)
{
    struct queue *queue = calloc(1, sizeof(queue));
    queue->data = calloc(sizeof(int), size);
    queue->max = size;
    return queue;
}

int push(struct queue *queue, int val)
{
    if (queue->nel == queue->max) return 0;
    queue->data[queue->nel % queue->max] = val;
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
    queue->head++;
    return val;
}

void init_test(void)
{
    struct queue *queue = create_queue(10);
    assert(queue);
    assert(queue->data != NULL);
    assert(queue->head == 0);
    assert(queue->nel == 0);
    assert(queue->max == 10);
}

void push_test(void)
{
    struct queue *queue = create_queue(10);
    for (int i = 0; i < 10; i++) {
        assert(push(queue, i * 10));
        assert(queue->nel == i + 1);
        assert(queue->data[i] == i * 10);
    }
}

void pop_test(void)
{
    struct queue *queue = create_queue(10);
    for (int i = 0; i < 10; i++) {
        assert(push(queue, i * 10));
        assert(queue->nel == i + 1);
        assert(queue->data[i] == i * 10);
    }
    for (int i = 9; i >= 0; i--) {
        assert(pop(queue) == i);
    }
}

void run_all_tests(void)
{
    init_test();
    push_test();
}

int main(void)
{
    run_all_tests();
    return 0;
}
