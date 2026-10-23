/* 第 27 章：创建线程、传入参数、join 取回结果。 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define N 4

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

struct Task {
    int value;
    int result;
};

static void *square(void *arg) {
    struct Task *task = arg;
    task->result = task->value * task->value;
    return NULL;
}

int main(void) {
    pthread_t threads[N];
    struct Task tasks[N];
    int i;
    int sum = 0;
    for (i = 0; i < N; i++) {
        tasks[i].value = i;
        tasks[i].result = -1;
        CHECK(pthread_create(&threads[i], NULL, square, &tasks[i]) == 0);
    }
    for (i = 0; i < N; i++) {
        CHECK(pthread_join(threads[i], NULL) == 0);
        printf("thread_api: 线程 %d 计算 %d^2 = %d\n", i, tasks[i].value, tasks[i].result);
        sum += tasks[i].result;
    }
    CHECK(sum == 0 + 1 + 4 + 9);
    printf("通过：join 保证结果写回之后主线程才读取\n");
    return 0;
}
