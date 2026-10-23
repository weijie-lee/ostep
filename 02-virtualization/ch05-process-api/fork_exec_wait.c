/* 第 5 章：fork、wait、exec，以及用 dup2 做输出重定向。 */
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#define CHECK(cond)                                                                 \
    do {                                                                            \
        if (!(cond)) {                                                              \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond);    \
            exit(1);                                                                \
        }                                                                           \
    } while (0)

static int wait_child(pid_t pid) {
    int status = 0;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        exit(1);
    }
    CHECK(WIFEXITED(status));
    return WEXITSTATUS(status);
}

static void demo_fork_wait(void) {
    pid_t pid = fork();
    CHECK(pid >= 0);
    if (pid == 0) {
        printf("fork: 子进程 pid=%d 父进程=%d\n", getpid(), getppid());
        _exit(42);
    }
    int code = wait_child(pid);
    printf("fork: 父进程收回子进程 %d，退出码 %d\n", pid, code);
    CHECK(code == 42);
}

static void demo_exec(void) {
    int fds[2];
    char buf[64];
    ssize_t n;
    pid_t pid;
    CHECK(pipe(fds) == 0);
    pid = fork();
    CHECK(pid >= 0);
    if (pid == 0) {
        CHECK(dup2(fds[1], STDOUT_FILENO) >= 0);
        close(fds[0]);
        close(fds[1]);
        execlp("echo", "echo", "hello-from-exec", (char *)NULL);
        perror("execlp");
        _exit(127);
    }
    close(fds[1]);
    n = read(fds[0], buf, sizeof(buf) - 1);
    CHECK(n > 0);
    buf[n] = '\0';
    close(fds[0]);
    CHECK(wait_child(pid) == 0);
    printf("exec: 子进程映像已被 /bin/echo 替换，父进程读到 \"%s\"", buf);
    CHECK(strcmp(buf, "hello-from-exec\n") == 0);
}

int main(void) {
    demo_fork_wait();
    demo_exec();
    printf("通过：fork 复制，exec 替换，wait 回收，dup2 把标准输出接进管道\n");
    return 0;
}
