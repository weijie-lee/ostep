/* 第 4 章：从 /proc 读出内核为当前进程保存的机器状态。 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void show(const char *path, const char *key) {
    FILE *fp = fopen(path, "r");
    char line[256];
    if (fp == NULL) {
        perror(path);
        exit(1);
    }
    while (fgets(line, sizeof(line), fp) != NULL) {
        if (strncmp(line, key, strlen(key)) == 0) {
            fputs(line, stdout);
        }
    }
    fclose(fp);
}

int main(void) {
    printf("pid=%d ppid=%d\n", getpid(), getppid());
    printf("内核进程表里能看到的几项（/proc/self/status）：\n");
    show("/proc/self/status", "State:");
    show("/proc/self/status", "Pid:");
    show("/proc/self/status", "PPid:");
    show("/proc/self/status", "Threads:");
    show("/proc/self/status", "voluntary_ctxt_switches:");
    return 0;
}
