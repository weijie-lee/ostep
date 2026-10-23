/* 第 2 章：一个进程占用 CPU，就是在反复执行指令。 */
#include <stdio.h>

#define LOOPS 50000000u

int main(void) {
    unsigned i;
    volatile unsigned sink = 0;
    for (i = 0; i < LOOPS; i++) {
        sink += i;
    }
    printf("cpu: 循环 %u 次，累加结果 %u\n", LOOPS, sink);
    printf("cpu: 这段时间进程一直处于运行态，操作系统用时间片让别的进程也有机会跑\n");
    if (sink == 0) {
        fprintf(stderr, "累加结果不应为 0\n");
        return 1;
    }
    return 0;
}
