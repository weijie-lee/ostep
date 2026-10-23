/* 第 2 章：分配并访问一块虚拟内存。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 4096

int main(void) {
    int *buf = malloc(sizeof(int) * N);
    size_t i;
    long sum = 0;
    if (buf == NULL) {
        perror("malloc");
        return 1;
    }
    for (i = 0; i < N; i++) {
        buf[i] = (int)i;
    }
    for (i = 0; i < N; i += 1024) {
        sum += buf[i];
    }
    printf("mem: malloc 返回虚拟地址 %p，共 %zu 字节\n", (void *)buf, sizeof(int) * N);
    printf("mem: 抽样求和 = %ld（地址是否连续由硬件和页表保证，程序只看到线性空间）\n", sum);
    free(buf);
    if (sum != 0 + 1024 + 2048 + 3072) {
        fprintf(stderr, "抽样求和不正确\n");
        return 1;
    }
    return 0;
}
