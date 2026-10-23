/* 第 13 章：代码、静态数据、堆、栈处在同一地址空间的不同区域。 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int global_data = 7;
static int global_bss;

static int recurse(int depth, uintptr_t *prev) {
    int local = depth;
    uintptr_t here = (uintptr_t)&local;
    printf("  栈深度 %d  局部变量地址 %p\n", depth, (void *)&local);
    if (*prev != 0 && here >= *prev) {
        fprintf(stderr, "栈应向低地址增长\n");
        return 1;
    }
    *prev = here;
    if (depth == 4) {
        return 0;
    }
    return recurse(depth + 1, prev);
}

int main(void) {
    int stack_local = 1;
    int *heap = malloc(sizeof(int) * 4);
    uintptr_t prev = 0;
    if (heap == NULL) {
        perror("malloc");
        return 1;
    }
    heap[0] = 1;
    printf("代码   main        %p\n", (void *)&main);
    printf("静态   global_data %p\n", (void *)&global_data);
    printf("静态   global_bss  %p\n", (void *)&global_bss);
    printf("堆     malloc      %p\n", (void *)heap);
    printf("栈     stack_local %p\n", (void *)&stack_local);
    printf("递归调用，观察栈帧：\n");
    if (recurse(0, &prev) != 0) {
        return 1;
    }
    if (!((uintptr_t)&main < (uintptr_t)heap && (uintptr_t)heap < (uintptr_t)&stack_local)) {
        fprintf(stderr, "期望布局：代码 < 堆 < 栈\n");
        return 1;
    }
    free(heap);
    printf("通过：一个进程看到的是连续私有地址，实际由后面的翻译机制映射到物理内存\n");
    return 0;
}
