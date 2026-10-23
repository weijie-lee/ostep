/* 第 31 章：用信号量做汇合，以及做有界缓冲区。 */
#include <pthread.h>
#include <semaphore.h>
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

static sem_t arrived_a;
static sem_t arrived_b;
static int met_a;
static int met_b;

static void *party_a(void *arg) {
    (void)arg;
    sem_post(&arrived_a);
    sem_wait(&arrived_b);
    met_a = 1;
    return NULL;
}

static void *party_b(void *arg) {
    (void)arg;
    sem_post(&arrived_b);
    sem_wait(&arrived_a);
    met_b = 1;
    return NULL;
}

static int buffer[SLOTS];
static int head;
static int tail;
static sem_t empty_slots;
static sem_t filled_slots;
static sem_t mutex;

static void *producer(void *arg) {
    int i;
    (void)arg;
    for (i = 0; i < ITEMS; i++) {
        sem_wait(&empty_slots);
        sem_wait(&mutex);
        buffer[tail] = i;
        tail = (tail + 1) % SLOTS;
        sem_post(&mutex);
        sem_post(&filled_slots);
    }
    return NULL;
}

static void *consumer(void *arg) {
    int i;
    int *out = arg;
    for (i = 0; i < ITEMS; i++) {
        sem_wait(&filled_slots);
        sem_wait(&mutex);
        out[i] = buffer[head];
        head = (head + 1) % SLOTS;
        sem_post(&mutex);
        sem_post(&empty_slots);
    }
    return NULL;
}

int main(void) {
    pthread_t ta;
    pthread_t tb;
    pthread_t prod;
    pthread_t cons;
    int out[ITEMS];
    int i;

    CHECK(sem_init(&arrived_a, 0, 0) == 0);
    CHECK(sem_init(&arrived_b, 0, 0) == 0);
    CHECK(pthread_create(&ta, NULL, party_a, NULL) == 0);
    CHECK(pthread_create(&tb, NULL, party_b, NULL) == 0);
    CHECK(pthread_join(ta, NULL) == 0);
    CHECK(pthread_join(tb, NULL) == 0);
    printf("汇合：两边都到达之后才继续，met_a=%d met_b=%d\n", met_a, met_b);
    CHECK(met_a == 1 && met_b == 1);

    CHECK(sem_init(&empty_slots, 0, SLOTS) == 0);
    CHECK(sem_init(&filled_slots, 0, 0) == 0);
    CHECK(sem_init(&mutex, 0, 1) == 0);
    CHECK(pthread_create(&prod, NULL, producer, NULL) == 0);
    CHECK(pthread_create(&cons, NULL, consumer, out) == 0);
    CHECK(pthread_join(prod, NULL) == 0);
    CHECK(pthread_join(cons, NULL) == 0);
    for (i = 0; i < ITEMS; i++) {
        CHECK(out[i] == i);
    }
    printf("有界缓冲区：empty 初始为 %d，full 初始为 0，传完 %d 个整数\n", SLOTS, ITEMS);
    printf("通过\n");
    return 0;
}
