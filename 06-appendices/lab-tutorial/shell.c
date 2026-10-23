/* 附录：外壳的骨架。fork、exec、wait，不读终端。 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            fprintf(stderr, "检查失败 %s:%d: %s\n", __FILE__, __LINE__, #cond); \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

static int run_command(char *const argv[]) {
    pid_t pid = fork();
    int status = 0;
    CHECK(pid >= 0);
    if (pid == 0) {
        execvp(argv[0], argv);
        perror("execvp");
        _exit(127);
    }
    CHECK(waitpid(pid, &status, 0) == pid);
    CHECK(WIFEXITED(status));
    return WEXITSTATUS(status);
}

int main(void) {
    char *echo_argv[] = {"echo", "lab-tutorial", NULL};
    char *true_argv[] = {"true", NULL};
    char *false_argv[] = {"false", NULL};
    int echo_status = run_command(echo_argv);
    int true_status = run_command(true_argv);
    int false_status = run_command(false_argv);
    printf("shell: echo 退出码 %d，true 退出码 %d，false 退出码 %d\n",
           echo_status, true_status, false_status);
    CHECK(echo_status == 0 && true_status == 0 && false_status == 1);
    printf("通过：外壳本身不实现 echo，它只创建进程并等待\n");
    return 0;
}
