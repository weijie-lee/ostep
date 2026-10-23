# 编译全部 C 演示，或编译并运行每一章。
CC      := gcc
CFLAGS  := -std=c11 -D_GNU_SOURCE -Wall -Wextra -Werror -pthread
PYTHON  := python3

.PHONY: all test clean list

all test:
	$(PYTHON) scripts/test_all.py $(if $(filter test,$@),,--build-only)

clean:
	rm -rf build

list:
	@find 0* -name '*.c' -o -name '*.py' -o -name 'README.md' | sort
