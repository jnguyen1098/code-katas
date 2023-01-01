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
    {.filename = "test_data/example1", .part_1_expected =  1651, .part_2_expected =  1707},
    {.filename =   "test_data/input1", .part_1_expected =  1850, .part_2_expected =  2306},
    {.filename =   "test_data/input2", .part_1_expected =  1728, .part_2_expected =  2304},
    {.filename =  "test_data/input33", .part_1_expected = 50000, .part_2_expected = 50304},
    {.filename =   "test_data/input5", .part_1_expected =  2640, .part_2_expected =  2670},
    {.filename =   "test_data/input6", .part_1_expected = 13468, .part_2_expected = 12887},
    {.filename =   "test_data/input7", .part_1_expected =  1288, .part_2_expected =  1484},
    {.filename =   "test_data/input8", .part_1_expected =  2400, .part_2_expected =  3680},
};

bool digit(char c) { return c >= '0' && c <= '9'; }
bool capital(char c) { return c >= 'A' && c <= 'Z'; }
bool non_digit(char c) { return c < '0' || c > '9'; }
bool lowercase_or_space(char c) { return c == ' ' || (c >= 'a' && c <= 'z'); }
bool lower_space_or_semi(char c) { return lowercase_or_space(c) || c == ';'; }
bool space(char c) { return c == ' '; }
bool comma(char c) { return c == ','; }

void v_mealy_action(char c, char *state, char **out)
{
    if (c == 'V') {
        *state = 'b';
    } else {
        *state = 'k';
    }
}

/*
 * /^V[a-z ]+([A-Z]{2})\D*\d+;[a-z ]+([A-Z]{2})(, [A-Z]{2})*$/
 */
static char *parse_line(char *line)
{
    int pos = 0;
    char state = 'a';
    int i = 0;
    int lim = 128;
    char curr = 0;

    char *output = calloc(1, 1000);
    *output = '\0';
    char *ptr = output;

    for (; i < lim; i++) {
        if (!line[pos]){
            break;
        }
        curr = line[pos];
        if (state == 'a') {
            v_mealy_action(curr, &state, &ptr);
            pos++;
        } else if (state == 'b') {
            if (lowercase_or_space(curr)) {
                pos++;
            } else if (capital(curr)) {
                *ptr++ = curr;
                state = 'c';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'c') {
            if (capital(curr)) {
                *ptr++ = curr;
                *ptr++ = ',';
                state = 'd';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'd') {
            if (non_digit(curr)) {
                state = 'e';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'e') {
            if (non_digit(curr)) {
                pos++;
            } else if (digit(curr)) {
                *ptr++ = curr;
                state = 'f';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'f') {
            if (lower_space_or_semi(curr)) {
                *ptr++ = ',';
                state = 'g';
                pos++;
            } else if (digit(curr)) {
                *ptr++ = curr;
                state = 'f';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'g') {
            if (lower_space_or_semi(curr)) {
                state = 'g';
                pos++;
            } else if (capital(curr)) {
                *ptr++ = curr;
                state = 'h';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'h') {
            if (capital(curr)) {
                *ptr++ = curr;
                *ptr++ = ',';
                state = 'i';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'i') {
            if (comma(curr)) {
                state = 'j';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'j') {
            if (space(curr)) {
                state = 'g';
                pos++;
            } else {
                state = 'k';
            }
        } else if (state == 'k') {
            pos++;
        } else {
            die(f("unknown state %c", state));
        }
    }
    if (i == lim) {
        die(f("timed out while parsing pos=%d at char=%c", pos, curr));
    }
    if (state != 'i') {
        die(f("can only terminate on state i but currently on state %c", state));
    }
    return output;
}

static void parse_file(char *filename)
{
    FILE *fp;
    if (!(fp = fopen(filename, "r"))) {
        perror("fopen");
        die(f("Could not open %s", filename));
    }
    char buf[BUFSIZ];

    printf("%s|", filename);
    while (fgets(buf, BUFSIZ, fp)) {
        buf[strcspn(buf, "\r\n")] = '\0';
        // printf("%s\n", buf);
        char *result = parse_line(buf);
        printf("%s|", result);
    }
    puts("");
    fclose(fp);
}

static void run_parsing_tests(void)
{
    return;
}

static int solve_part_one(char *filename)
{
    parse_file(filename);
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
    run_all_tests();
    return 0;
}
