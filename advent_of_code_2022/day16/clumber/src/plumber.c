#define _GNU_SOURCE
#include "plumber.h"

noreturn void die(char *message)
{
    fprintf(stderr, "%s\n", message);
    exit(1);
}

char *f(const char *fmt, ...)
{
    va_list argp;
    va_start(argp, fmt);
    char *result;
    vasprintf(&result, fmt, argp);
    return result;
}

static void test_assert(int expected, int actual) {
    if (expected != actual) {
        fprintf(stderr, "FAIL -> expected %d but got %d\n", expected, actual);
        exit(1);
    }
}

static struct {
    char *filename;
    int part_1_expected;
    int part_2_expected;
} test_cases[] = {
    {.filename = "example1", .part_1_expected =  1651, .part_2_expected =  1707},
    {.filename =   "input1", .part_1_expected =  1850, .part_2_expected =  2306},
    {.filename =   "input2", .part_1_expected =  1728, .part_2_expected =  2304},
    {.filename =  "input33", .part_1_expected = 50000, .part_2_expected = 50304},
    {.filename =   "input5", .part_1_expected =  2640, .part_2_expected =  2670},
    {.filename =   "input6", .part_1_expected = 13468, .part_2_expected = 12887},
    {.filename =   "input7", .part_1_expected =  1288, .part_2_expected =  1484},
    {.filename =   "input8", .part_1_expected =  2400, .part_2_expected =  3680},
};

static void parse_file(char *filename)
{
    return;
}

static void run_parsing_tests(void)
{
    return;
}

static int solve_part_one(char *filename)
{
    return 0;
}

static int solve_part_two(char *filename)
{
    return 0;
}

static void run_test_suite(void)
{
    printf("\nSTARTING PART ONE TESTS\n");
    for (size_t i = 0; i < sizeof(test_cases) / sizeof(*test_cases); i++) {
        printf("  %-8s -> %5d -> %5d\n", test_cases[i].filename, test_cases[i].part_1_expected, test_cases[i].part_2_expected);
        test_assert(test_cases[i].part_1_expected, solve_part_one(test_cases[i].filename));
    }
    printf("\nSTARTING PART TWO TESTS\n");
    for (size_t i = 0; i < sizeof(test_cases) / sizeof(*test_cases); i++) {
        printf("  %-8s -> %5d -> %5d\n", test_cases[i].filename, test_cases[i].part_1_expected, test_cases[i].part_2_expected);
        test_assert(test_cases[i].part_2_expected, solve_part_two(test_cases[i].filename));
    }
    printf("\nTESTS ARE DONE\n\n");
    return;
}

static void run_all_tests(void)
{
    run_parsing_tests();
    run_test_suite();
    return;
}

int main(void)
{
    int num = 42;
    char *string = "lmao";
    error(f("this is a number: %d but this is a string: %s\n", num, string));
    run_all_tests();
    return 0;
}
