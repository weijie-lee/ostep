/* 第 32 章：原子性违反、顺序违反、死锁。坏的交错和修好的写法并排。 */
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

static pthread_barrier_t barrier;
static pthread_mutex_t balance_lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
static pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;
static int balance;
static int value;
static int observed;
static int try_fail_a;
static int try_fail_b;
static int take[2];

static void *withdraw_buggy(void *arg) {
    int id = *(int *)arg;
    pthread_barrier_wait(&barrier);
    /* 每个线程只写自己的槽，决定本身没有数据竞争。 */
    take[id] = balance >= 100;
    pthread_barrier_wait(&barrier);
    return NULL;
}

static void *withdraw_fixed(void *arg) {
    (void)arg;
    pthread_mutex_lock(&balance_lock);
    if (balance >= 100) {
        balance -= 100;
    }
    pthread_mutex_unlock(&balance_lock);
    return NULL;
}

static void *reader_too_soon(void *arg) {
    (void)arg;
    pthread_barrier_wait(&barrier);
    observed = value;
    pthread_barrier_wait(&barrier);
    return NULL;
}

static void *writer_too_late(void *arg) {
    (void)arg;
    pthread_barrier_wait(&barrier);
    pthread_barrier_wait(&barrier);
    value = 42;
    return NULL;
}

static void *hold_a(void *arg) {
    (void)arg;
    pthread_mutex_lock(&lock_a);
    pthread_barrier_wait(&barrier);
    if (pthread_mutex_trylock(&lock_b) != 0) {
        try_fail_a = 1;
    } else {
        pthread_mutex_unlock(&lock_b);
    }
    pthread_barrier_wait(&barrier);
    pthread_mutex_unlock(&lock_a);
    return NULL;
}

static void *hold_b(void *arg) {
    (void)arg;
    pthread_mutex_lock(&lock_b);
    pthread_barrier_wait(&barrier);
    if (pthread_mutex_trylock(&lock_a) != 0) {
        try_fail_b = 1;
    } else {
        pthread_mutex_unlock(&lock_a);
    }
    pthread_barrier_wait(&barrier);
    pthread_mutex_unlock(&lock_b);
    return NULL;
}

static void run_pair(void *(*first)(void *), void *(*second)(void *)) {
    pthread_t one;
    pthread_t two;
    CHECK(pthread_create(&one, NULL, first, NULL) == 0);
    CHECK(pthread_create(&two, NULL, second, NULL) == 0);
    CHECK(pthread_join(one, NULL) == 0);
    CHECK(pthread_join(two, NULL) == 0);
}

int main(void) {
    CHECK(pthread_barrier_init(&barrier, NULL, 2) == 0);

    balance = 100;
    take[0] = take[1] = 0;
    {
        pthread_t one;
        pthread_t two;
        int id0 = 0;
        int id1 = 1;
        CHECK(pthread_create(&one, NULL, withdraw_buggy, &id0) == 0);
        CHECK(pthread_create(&two, NULL, withdraw_buggy, &id1) == 0);
        CHECK(pthread_join(one, NULL) == 0);
        CHECK(pthread_join(two, NULL) == 0);
    }
    CHECK(take[0] == 1 && take[1] == 1);
    /* 两个“可以扣款”的决定都成立，依次执行就会把余额扣成负数。 */
    if (take[0]) {
        balance -= 100;
    }
    if (take[1]) {
        balance -= 100;
    }
    printf("原子性违反：两边都通过了余额检查，balance=%d\n", balance);
    CHECK(balance == -100);

    balance = 100;
    run_pair(withdraw_fixed, withdraw_fixed);
    printf("检查和扣款放进同一把锁，balance=%d\n", balance);
    CHECK(balance == 0);

    value = 0;
    observed = -1;
    run_pair(reader_too_soon, writer_too_late);
    printf("顺序违反：读者看到的 value=%d（写者还没赋值）\n", observed);
    CHECK(observed == 0);
    value = 42;
    observed = value;
    printf("先写后读：value=%d\n", observed);
    CHECK(observed == 42);

    run_pair(hold_a, hold_b);
    printf("死锁交错：A 握着锁 1 再试锁 2 %s，B 握着锁 2 再试锁 1 %s\n",
           try_fail_a ? "失败" : "成功", try_fail_b ? "失败" : "成功");
    CHECK(try_fail_a == 1 && try_fail_b == 1);
    printf("通过：trylock 打破持有并等待；若真的阻塞等待，这两条线程会循环等待\n");
    return 0;
}
