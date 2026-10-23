/* 第 33 章：一个线程用 select 同时等两条管道。 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include <unistd.h>

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

int main(void) {
    int left[2];
    int right[2];
    int got_left = 0;
    int got_right = 0;
    char left_byte = 0;
    char right_byte = 0;
    CHECK(pipe(left) == 0);
    CHECK(pipe(right) == 0);
    CHECK(write(left[1], "L", 1) == 1);
    CHECK(write(right[1], "R", 1) == 1);
    CHECK(close(left[1]) == 0);
    CHECK(close(right[1]) == 0);

    while (!got_left || !got_right) {
        fd_set readable;
        int maxfd = -1;
        int ready;
        FD_ZERO(&readable);
        if (!got_left) {
            FD_SET(left[0], &readable);
            maxfd = left[0];
        }
        if (!got_right) {
            FD_SET(right[0], &readable);
            if (right[0] > maxfd) {
                maxfd = right[0];
            }
        }
        ready = select(maxfd + 1, &readable, NULL, NULL, NULL);
        CHECK(ready > 0);
        if (!got_left && FD_ISSET(left[0], &readable)) {
            CHECK(read(left[0], &left_byte, 1) == 1);
            got_left = 1;
            printf("event: 左管道就绪，读到 %c\n", left_byte);
        }
        if (!got_right && FD_ISSET(right[0], &readable)) {
            CHECK(read(right[0], &right_byte, 1) == 1);
            got_right = 1;
            printf("event: 右管道就绪，读到 %c\n", right_byte);
        }
    }
    close(left[0]);
    close(right[0]);
    CHECK(left_byte == 'L' && right_byte == 'R');
    printf("通过：一个控制流处理了两个事件源，阻塞发生在 select 而不是某一个 read\n");
    return 0;
}
