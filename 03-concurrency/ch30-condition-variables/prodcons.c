/* 第 30 章：有界缓冲区。等待条件用 while，符合 Mesa 语义。 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 4
#define ITEMS 20

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

static int buffer[SLOTS];
static int head;
static int tail;
static int count;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;
static pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;

static void *producer(void *arg) {
    int i;
    (void)arg;
    for (i = 0; i < ITEMS; i++) {
        pthread_mutex_lock(&mu);
        while (count == SLOTS) {
            pthread_cond_wait(&not_full, &mu);
        }
        buffer[tail] = i;
        tail = (tail + 1) % SLOTS;
        count += 1;
        pthread_cond_signal(&not_empty);
        pthread_mutex_unlock(&mu);
    }
    return NULL;
}

static void *consumer(void *arg) {
    int i;
    int *out = arg;
    for (i = 0; i < ITEMS; i++) {
        pthread_mutex_lock(&mu);
        while (count == 0) {
            pthread_cond_wait(&not_empty, &mu);
        }
        out[i] = buffer[head];
        head = (head + 1) % SLOTS;
        count -= 1;
        pthread_cond_signal(&not_full);
        pthread_mutex_unlock(&mu);
    }
    return NULL;
}

int main(void) {
    pthread_t prod;
    pthread_t cons;
    int out[ITEMS];
    int i;
    CHECK(pthread_create(&prod, NULL, producer, NULL) == 0);
    CHECK(pthread_create(&cons, NULL, consumer, out) == 0);
    CHECK(pthread_join(prod, NULL) == 0);
    CHECK(pthread_join(cons, NULL) == 0);
    for (i = 0; i < ITEMS; i++) {
        CHECK(out[i] == i);
    }
    printf("生产者写入 0..%d，消费者按原顺序读出，缓冲区只有 %d 格\n", ITEMS - 1, SLOTS);
    printf("通过：while 在被叫醒后重新检查缓冲区是否真的有数据\n");
    return 0;
}
