/* 第 28 章：测试并设置锁，以及按号服务的票锁。 */
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>

#define THREADS 4
#define LOOPS 20000

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

static atomic_int tas_flag = 0;
static atomic_int ticket = 0;
static atomic_int serving = 0;
static int counter = 0;
static int order_log[THREADS];
static int order_n = 0;

static void tas_lock(void) {
    while (atomic_exchange(&tas_flag, 1) == 1) {
        sched_yield();
    }
}

static void tas_unlock(void) {
    atomic_store(&tas_flag, 0);
}

static void ticket_lock(void) {
    int mine = atomic_fetch_add(&ticket, 1);
    while (atomic_load(&serving) != mine) {
        sched_yield();
    }
}

static void ticket_unlock(void) {
    atomic_fetch_add(&serving, 1);
}

static void *tas_worker(void *arg) {
    int id = *(int *)arg;
    int i;
    for (i = 0; i < LOOPS; i++) {
        tas_lock();
        if (order_n < THREADS) {
            order_log[order_n++] = id;
        }
        counter += 1;
        tas_unlock();
    }
    return NULL;
}

static void *ticket_worker(void *arg) {
    int i;
    (void)arg;
    for (i = 0; i < LOOPS; i++) {
        ticket_lock();
        counter += 1;
        ticket_unlock();
    }
    return NULL;
}

static void run(void *(*fn)(void *), int *ids) {
    pthread_t threads[THREADS];
    int i;
    for (i = 0; i < THREADS; i++) {
        ids[i] = i;
        CHECK(pthread_create(&threads[i], NULL, fn, &ids[i]) == 0);
    }
    for (i = 0; i < THREADS; i++) {
        CHECK(pthread_join(threads[i], NULL) == 0);
    }
}

int main(void) {
    int ids[THREADS];
    int i;
    counter = 0;
    run(tas_worker, ids);
    printf("测试并设置锁：counter=%d，先进入临界区的线程", counter);
    for (i = 0; i < order_n; i++) {
        printf(" %d", order_log[i]);
    }
    printf("\n");
    CHECK(counter == THREADS * LOOPS);

    counter = 0;
    ticket = 0;
    serving = 0;
    run(ticket_worker, ids);
    printf("票锁：counter=%d（取号顺序就是进入顺序，不会饿死）\n", counter);
    CHECK(counter == THREADS * LOOPS);
    printf("通过\n");
    return 0;
}
