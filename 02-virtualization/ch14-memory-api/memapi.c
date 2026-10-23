/* 第 14 章：malloc/free 的正确用法，以及泄漏和重复释放怎么被发现。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TRACK 64

typedef struct {
    void *ptr;
    size_t size;
    int live;
} Record;

static Record table[MAX_TRACK];
static int leaks = 0;
static int double_frees = 0;

static void *xmalloc(size_t size) {
    void *ptr = malloc(size);
    int i;
    if (ptr == NULL) {
        perror("malloc");
        exit(1);
    }
    for (i = 0; i < MAX_TRACK; i++) {
        if (!table[i].live && table[i].ptr == NULL) {
            table[i].ptr = ptr;
            table[i].size = size;
            table[i].live = 1;
            return ptr;
        }
    }
    fprintf(stderr, "跟踪表满了\n");
    exit(1);
}

static void xfree(void *ptr) {
    int i;
    for (i = 0; i < MAX_TRACK; i++) {
        if (table[i].ptr == ptr) {
            if (!table[i].live) {
                double_frees += 1;
                printf("memapi: 拒绝重复释放 %p\n", ptr);
                return;
            }
            table[i].live = 0;
            free(ptr);
            return;
        }
    }
    fprintf(stderr, "释放了未跟踪的指针\n");
    exit(1);
}

static void report_leaks(void) {
    int i;
    for (i = 0; i < MAX_TRACK; i++) {
        if (table[i].live) {
            leaks += 1;
            printf("memapi: 泄漏 %p （%zu 字节）\n", table[i].ptr, table[i].size);
            free(table[i].ptr);
            table[i].live = 0;
        }
    }
}

int main(void) {
    void *keep = xmalloc(32);
    void *temporary = xmalloc(16);
    memset(keep, 0xab, 32);
    printf("memapi: malloc 两块，正常释放其中一块\n");
    xfree(temporary);
    xfree(temporary);
    report_leaks();
    if (double_frees != 1 || leaks != 1) {
        fprintf(stderr, "应发现 1 次重复释放和 1 次泄漏\n");
        return 1;
    }
    printf("通过：接口很薄，错误用法要靠约定或者这种记账才能早发现\n");
    return 0;
}
