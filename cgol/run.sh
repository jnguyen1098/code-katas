#!/usr/bin/env sh

clear && gcc cgol.c -Wall -Wextra -Wpedantic -ggdb3 -std=gnu99 -pthread && valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --read-var-info=yes ./a.out
