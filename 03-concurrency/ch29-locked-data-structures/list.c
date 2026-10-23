/* 第 29 章：用一把锁保护链表的插入和查找。 */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define THREADS 4
#define PER_THREAD 50

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

struct Node {
    int key;
    struct Node *next;
};

static struct Node *head = NULL;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void insert(int key) {
    struct Node *node = malloc(sizeof(*node));
    CHECK(node != NULL);
    node->key = key;
    pthread_mutex_lock(&lock);
    node->next = head;
    head = node;
    pthread_mutex_unlock(&lock);
}

static int contains(int key) {
    struct Node *node;
    int found = 0;
    pthread_mutex_lock(&lock);
    for (node = head; node != NULL; node = node->next) {
        if (node->key == key) {
            found = 1;
            break;
        }
    }
    pthread_mutex_unlock(&lock);
    return found;
}

static void *worker(void *arg) {
    int base = *(int *)arg;
    int i;
    for (i = 0; i < PER_THREAD; i++) {
        insert(base + i);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[THREADS];
    int bases[THREADS];
    int i;
    int found = 0;
    struct Node *node;
    for (i = 0; i < THREADS; i++) {
        bases[i] = i * PER_THREAD;
        CHECK(pthread_create(&threads[i], NULL, worker, &bases[i]) == 0);
    }
    for (i = 0; i < THREADS; i++) {
        CHECK(pthread_join(threads[i], NULL) == 0);
    }
    for (i = 0; i < THREADS * PER_THREAD; i++) {
        found += contains(i);
    }
    printf("并发插入 %d 个键，查找命中 %d 个\n", THREADS * PER_THREAD, found);
    CHECK(found == THREADS * PER_THREAD);
    while (head != NULL) {
        node = head;
        head = head->next;
        free(node);
    }
    printf("通过：锁盖住了“改头指针”和“沿链表走”这两段临界区\n");
    return 0;
}
