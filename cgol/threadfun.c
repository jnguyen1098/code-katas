#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

struct worker_info_t {
    int rank;
    int nIterations;
};

int rand_int(int min, int max)
{
    return min + rand() / (RAND_MAX / (max - min + 1) + 1);
}

pthread_barrier_t barrier;

void super_critical_function(void)
{
    puts("performing important task (like writing to the cgol array)");
}

void *work_function(void *work_slice)
{
    struct worker_info_t *work_info = work_slice;
    for (int i = 0; i < work_info->nIterations; i++) {
        int wait_time = rand_int(1, 8);
        printf("Thread #%d iteration %d of %d... will wait for %ds\n",
                work_info->rank,
                i + 1, work_info->nIterations,
                wait_time);
        sleep(wait_time);
        printf("Thread #%d done - waiting for the others\n", work_info->rank);
        pthread_barrier_wait(&barrier);
        if (work_info->rank == 0) {
            super_critical_function();
        }
        pthread_barrier_wait(&barrier);
    }
    return NULL;
}

int main()
{
    int THREAD_COUNT = 4;
    
    if (pthread_barrier_init(&barrier, NULL, THREAD_COUNT)) {
        perror("pthread_barrier_init");
        exit(1);
    }
    
    int nIterations = 5;
    pthread_t threads[THREAD_COUNT];
    struct worker_info_t work[THREAD_COUNT];

    for (int i = 0; i < THREAD_COUNT; i++) {
        work[i].rank = i;
        work[i].nIterations = nIterations;
    }
    
    // Start the threads
    for (int i = 0; i < THREAD_COUNT; i++) {
        if (pthread_create(&threads[i], NULL, work_function, &work[i])) {
            perror("pthread_create");
            exit(1);
        }
    }
    
    // Finish
    for (int i = 0; i < THREAD_COUNT; i++) {
        if (pthread_join(threads[i], NULL)) {
            perror("pthread_join");
            exit(1);
        }
    }

    puts("We are done here");
}

