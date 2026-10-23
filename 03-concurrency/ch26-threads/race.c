/* 第 26 章：没有锁的共享计数器会丢更新。屏障用来把交错固定下来。 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

static int shared;
static pthread_barrier_t barrier;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void *lost_update(void *arg) {
    int local;
    (void)arg;
    pthread_barrier_wait(&barrier);
    local = shared;
    pthread_barrier_wait(&barrier);
    local += 1;
    pthread_barrier_wait(&barrier);
    shared = local;
    return NULL;
}

static void *locked_update(void *arg) {
    (void)arg;
    pthread_mutex_lock(&lock);
    shared += 1;
    pthread_mutex_unlock(&lock);
    return NULL;
}

static void run_pair(void *(*fn)(void *)) {
    pthread_t one;
    pthread_t two;
    CHECK(pthread_create(&one, NULL, fn, NULL) == 0);
    CHECK(pthread_create(&two, NULL, fn, NULL) == 0);
    CHECK(pthread_join(one, NULL) == 0);
    CHECK(pthread_join(two, NULL) == 0);
}

int main(void) {
    CHECK(pthread_barrier_init(&barrier, NULL, 2) == 0);
    shared = 0;
    run_pair(lost_update);
    printf("无锁：两个线程都读到 0，都写回 1，最终 shared=%d\n", shared);
    CHECK(shared == 1);

    shared = 0;
    run_pair(locked_update);
    printf("互斥锁：临界区里的自增不能交错，最终 shared=%d\n", shared);
    CHECK(shared == 2);
    printf("通过：共享数据需要原子地读改写\n");
    return 0;
}
