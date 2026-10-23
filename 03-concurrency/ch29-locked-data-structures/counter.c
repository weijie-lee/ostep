/* 第 29 章：近似计数器。局部值攒到阈值再加进全局。 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define THREADS 4
#define PER_THREAD 100000
#define THRESHOLD 1024

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

struct Local {
    pthread_mutex_t lock;
    int value;
};

static struct Local local[THREADS];
static pthread_mutex_t global_lock = PTHREAD_MUTEX_INITIALIZER;
static int global_count = 0;
static pthread_mutex_t exact_lock = PTHREAD_MUTEX_INITIALIZER;
static int exact = 0;

static void *worker(void *arg) {
    int id = *(int *)arg;
    int i;
    for (i = 0; i < PER_THREAD; i++) {
        pthread_mutex_lock(&local[id].lock);
        local[id].value += 1;
        if (local[id].value >= THRESHOLD) {
            pthread_mutex_lock(&global_lock);
            global_count += local[id].value;
            pthread_mutex_unlock(&global_lock);
            local[id].value = 0;
        }
        pthread_mutex_unlock(&local[id].lock);

        pthread_mutex_lock(&exact_lock);
        exact += 1;
        pthread_mutex_unlock(&exact_lock);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[THREADS];
    int ids[THREADS];
    int i;
    int pending = 0;
    int total = THREADS * PER_THREAD;
    for (i = 0; i < THREADS; i++) {
        ids[i] = i;
        local[i].value = 0;
        pthread_mutex_init(&local[i].lock, NULL);
        CHECK(pthread_create(&threads[i], NULL, worker, &ids[i]) == 0);
    }
    for (i = 0; i < THREADS; i++) {
        CHECK(pthread_join(threads[i], NULL) == 0);
    }
    for (i = 0; i < THREADS; i++) {
        pending += local[i].value;
    }
    printf("精确计数（每次都抢全局锁）= %d\n", exact);
    printf("近似计数尚未刷入的全局值 = %d，各线程手里还握着 %d\n", global_count, pending);
    CHECK(exact == total);
    CHECK(global_count + pending == total);
    CHECK(global_count % THRESHOLD == 0);
    CHECK(pending <= THREADS * (THRESHOLD - 1));

    pthread_mutex_lock(&global_lock);
    global_count += pending;
    pthread_mutex_unlock(&global_lock);
    printf("把局部计数刷进全局之后 = %d\n", global_count);
    CHECK(global_count == total);
    printf("通过：读全局值可以稍旧，但误差有上界\n");
    return 0;
}
