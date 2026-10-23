/* 第 39 章：创建、读写、硬链接、符号链接、删除。 */
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define CHECK(cond)                                                              \
    do {                                                                         \
        if (!(cond)) {                                                           \
            perror(#cond);                                                       \
            fprintf(stderr, "检查失败 %s:%d\n", __FILE__, __LINE__);            \
            exit(1);                                                             \
        }                                                                        \
    } while (0)

int main(void) {
    char dir[] = "/tmp/ostep-ch39-XXXXXX";
    char path[128];
    char linkpath[128];
    char sympath[128];
    char target[128];
    char buf[32];
    int fd;
    ssize_t n;
    struct stat st_file;
    struct stat st_link;
    CHECK(mkdtemp(dir) != NULL);
    snprintf(path, sizeof(path), "%s/note", dir);
    snprintf(linkpath, sizeof(linkpath), "%s/alias", dir);
    snprintf(sympath, sizeof(sympath), "%s/shortcut", dir);

    fd = open(path, O_CREAT | O_RDWR, 0644);
    CHECK(fd >= 0);
    CHECK(write(fd, "inode", 5) == 5);
    CHECK(lseek(fd, 0, SEEK_SET) == 0);
    n = read(fd, buf, sizeof(buf));
    CHECK(n == 5);
    buf[n] = '\0';
    close(fd);

    CHECK(link(path, linkpath) == 0);
    CHECK(stat(path, &st_file) == 0);
    CHECK(stat(linkpath, &st_link) == 0);
    CHECK(st_file.st_ino == st_link.st_ino);
    CHECK(st_file.st_nlink == 2);

    CHECK(symlink("note", sympath) == 0);
    n = readlink(sympath, target, sizeof(target) - 1);
    CHECK(n > 0);
    target[n] = '\0';

    printf("目录 %s\n", dir);
    printf("  note 与 alias 的 inode 都是 %llu，链接计数 %lu\n",
           (unsigned long long)st_file.st_ino, (unsigned long)st_file.st_nlink);
    printf("  shortcut 的内容是路径 \"%s\"，不是同一份 inode\n", target);
    printf("  读回字节 \"%s\"\n", buf);

    CHECK(strcmp(buf, "inode") == 0);
    CHECK(strcmp(target, "note") == 0);
    CHECK(unlink(linkpath) == 0);
    CHECK(stat(path, &st_file) == 0);
    CHECK(st_file.st_nlink == 1);
    CHECK(unlink(path) == 0);
    CHECK(unlink(sympath) == 0);
    CHECK(rmdir(dir) == 0);
    printf("通过：硬链接共享 inode，符号链接保存的是名字\n");
    return 0;
}
