#ifndef PLUMBER_H
#define PLUMBER_H

#include <assert.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>
#include "seethe.h"

noreturn void die(char *message);
static void test_assert(int expected, int actual);
char *f(const char *fmt, ...);

#endif
