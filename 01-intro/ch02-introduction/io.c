/* 第 2 章：一次磁盘读写会让进程阻塞，直到 I/O 完成。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    char path[] = "/tmp/ostep-ch02-io-XXXXXX";
    int fd = mkstemp(path);
    const char *msg = "persistence";
    char got[32];
    ssize_t n;
    if (fd < 0) {
        perror("mkstemp");
        return 1;
    }
    printf("io: 进程调用 write，在数据进入内核缓冲区之前它在系统调用里等待\n");
    if (write(fd, msg, strlen(msg)) < 0) {
        perror("write");
        return 1;
    }
    if (lseek(fd, 0, SEEK_SET) < 0) {
        perror("lseek");
        return 1;
    }
    n = read(fd, got, sizeof(got) - 1);
    if (n < 0) {
        perror("read");
        return 1;
    }
    got[n] = '\0';
    printf("io: read 返回 \"%s\"（文件是持久抽象，进程退出后数据仍在这块临时文件里）\n", got);
    close(fd);
    unlink(path);
    if (strcmp(got, msg) != 0) {
        fprintf(stderr, "读回的内容不一致\n");
        return 1;
    }
    return 0;
}
