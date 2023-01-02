#ifndef PLUMBER_H
#define PLUMBER_H

#include <assert.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdnoreturn.h>
#include <string.h>
#include "seethe.h"

#define DEFAULT_START_VALVE 0

noreturn void die(char *message);
static void test_assert(int expected, int actual);
char *fmt(const char *fmt, ...);

#endif
