#define _GNU_SOURCE
#include "plumber.h"

noreturn void die(char *message)
{
    fprintf(stderr, "%s\n", message);
    exit(1);
}

char *fmt(const char *fmt, ...)
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

/*
 * /^V[a-z ]+([A-Z]{2})\D*\d+;[a-z ]+([A-Z]{2})(, [A-Z]{2})*$/
 */
static char *parse_line(char *line)
{
    enum states {
        REJECT,
        CAPITAL_V,
        NAME_LEFT,
        NAME_RIGHT,
        SKIP_SPACE,
        DIGIT_OR_SEMI,
        SPACE_AFTER_SEMI,
        NEXT_LEFT,
        NEXT_RIGHT,
        COMMA_OR_EOF,
        TRANSITION_SPACE,
        ACCEPT,
        state_count,
    };

    enum actions {
        NOTHING,
        EMIT_CHAR,
        EMIT_COMMA,
    };

    enum input {
        INVALID,
        END_OF_LINE,

        SPACE,
        COMMA,
        SEMI,
        EQ,

        ZERO,
        ONE,
        TWO,
        THREE,
        FOUR,
        FIVE,
        SIX,
        SEVEN,
        EIGHT,
        NINE,

        A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
        a, d, e, f, h, l, n, o, r, s, t, u, v, w,

        input_count,
    };

    int action_for[state_count][input_count] = {
        [NAME_LEFT] = {
            [A] = EMIT_CHAR, [B] = EMIT_CHAR, [C] = EMIT_CHAR, [D] = EMIT_CHAR,
            [E] = EMIT_CHAR, [F] = EMIT_CHAR, [G] = EMIT_CHAR, [H] = EMIT_CHAR,
            [I] = EMIT_CHAR, [J] = EMIT_CHAR, [K] = EMIT_CHAR, [L] = EMIT_CHAR,
            [M] = EMIT_CHAR, [N] = EMIT_CHAR, [O] = EMIT_CHAR, [P] = EMIT_CHAR,
            [Q] = EMIT_CHAR, [R] = EMIT_CHAR, [S] = EMIT_CHAR, [T] = EMIT_CHAR,
            [U] = EMIT_CHAR, [V] = EMIT_CHAR, [W] = EMIT_CHAR, [X] = EMIT_CHAR,
            [Y] = EMIT_CHAR, [Z] = EMIT_CHAR,
        },
        [NAME_RIGHT] = {
            [A] = EMIT_CHAR, [B] = EMIT_CHAR, [C] = EMIT_CHAR, [D] = EMIT_CHAR,
            [E] = EMIT_CHAR, [F] = EMIT_CHAR, [G] = EMIT_CHAR, [H] = EMIT_CHAR,
            [I] = EMIT_CHAR, [J] = EMIT_CHAR, [K] = EMIT_CHAR, [L] = EMIT_CHAR,
            [M] = EMIT_CHAR, [N] = EMIT_CHAR, [O] = EMIT_CHAR, [P] = EMIT_CHAR,
            [Q] = EMIT_CHAR, [R] = EMIT_CHAR, [S] = EMIT_CHAR, [T] = EMIT_CHAR,
            [U] = EMIT_CHAR, [V] = EMIT_CHAR, [W] = EMIT_CHAR, [X] = EMIT_CHAR,
            [Y] = EMIT_CHAR, [Z] = EMIT_CHAR,
        },
        [SKIP_SPACE] = {
            [SPACE] = EMIT_COMMA,
        },
        [DIGIT_OR_SEMI] = {
            [ZERO] = EMIT_CHAR,
            [ONE] = EMIT_CHAR,
            [TWO] = EMIT_CHAR,
            [THREE] = EMIT_CHAR,
            [FOUR] = EMIT_CHAR,
            [FIVE] = EMIT_CHAR,
            [SIX] = EMIT_CHAR,
            [SEVEN] = EMIT_CHAR,
            [EIGHT] = EMIT_CHAR,
            [NINE] = EMIT_CHAR,
            [SEMI] = EMIT_COMMA,
        },
        [NEXT_LEFT] = {
            [A] = EMIT_CHAR, [B] = EMIT_CHAR, [C] = EMIT_CHAR, [D] = EMIT_CHAR,
            [E] = EMIT_CHAR, [F] = EMIT_CHAR, [G] = EMIT_CHAR, [H] = EMIT_CHAR,
            [I] = EMIT_CHAR, [J] = EMIT_CHAR, [K] = EMIT_CHAR, [L] = EMIT_CHAR,
            [M] = EMIT_CHAR, [N] = EMIT_CHAR, [O] = EMIT_CHAR, [P] = EMIT_CHAR,
            [Q] = EMIT_CHAR, [R] = EMIT_CHAR, [S] = EMIT_CHAR, [T] = EMIT_CHAR,
            [U] = EMIT_CHAR, [V] = EMIT_CHAR, [W] = EMIT_CHAR, [X] = EMIT_CHAR,
            [Y] = EMIT_CHAR, [Z] = EMIT_CHAR,
        },
        [NEXT_RIGHT] = {
            [A] = EMIT_CHAR, [B] = EMIT_CHAR, [C] = EMIT_CHAR, [D] = EMIT_CHAR,
            [E] = EMIT_CHAR, [F] = EMIT_CHAR, [G] = EMIT_CHAR, [H] = EMIT_CHAR,
            [I] = EMIT_CHAR, [J] = EMIT_CHAR, [K] = EMIT_CHAR, [L] = EMIT_CHAR,
            [M] = EMIT_CHAR, [N] = EMIT_CHAR, [O] = EMIT_CHAR, [P] = EMIT_CHAR,
            [Q] = EMIT_CHAR, [R] = EMIT_CHAR, [S] = EMIT_CHAR, [T] = EMIT_CHAR,
            [U] = EMIT_CHAR, [V] = EMIT_CHAR, [W] = EMIT_CHAR, [X] = EMIT_CHAR,
            [Y] = EMIT_CHAR, [Z] = EMIT_CHAR,
        },
        [COMMA_OR_EOF] = {
            [COMMA] = EMIT_COMMA,
            [END_OF_LINE] = EMIT_COMMA,
        },
    };

    char *state_names[] = {
        [REJECT] = "REJECT",
        [CAPITAL_V] = "CAPITAL_V",
        [NAME_LEFT] = "NAME_LEFT",
        [NAME_RIGHT] = "NAME_RIGHT",
        [SKIP_SPACE] = "SKIP_SPACE",
        [DIGIT_OR_SEMI] = "DIGIT_OR_SEMI",
        [SPACE_AFTER_SEMI] = "SPACE_AFTER_SEMI",
        [NEXT_LEFT] = "NEXT_LEFT",
        [NEXT_RIGHT] = "NEXT_RIGHT",
        [COMMA_OR_EOF] = "COMMA_OR_EOF",
        [TRANSITION_SPACE] = "TRANSITION_SPACE",
        [ACCEPT] = "ACCEPT",
    };

    int jump[128] = {
        [CAPITAL_V] = 5,
        [SKIP_SPACE] = 14,
        [SPACE_AFTER_SEMI] = 22,
    };

    int char_map[128] = {
        [' '] = SPACE, [','] = COMMA, [';'] = SEMI, ['='] = EQ,

        ['0'] = ZERO, ['1'] = ONE, ['2'] = TWO, ['3'] = THREE, ['4'] = FOUR,
        ['5'] = FIVE, ['6'] = SIX, ['7'] = SEVEN, ['8'] = EIGHT, ['9'] = NINE,

        ['A'] = A, ['B'] = B, ['C'] = C, ['D'] = D, ['E'] = E, ['F'] = F, ['G'] = G,
        ['H'] = H, ['I'] = I, ['J'] = J, ['K'] = K, ['L'] = L, ['M'] = M, ['N'] = N,
        ['O'] = O, ['P'] = P, ['Q'] = Q, ['R'] = R, ['S'] = S, ['T'] = T, ['U'] = U,
        ['V'] = V, ['W'] = W, ['X'] = X, ['Y'] = Y, ['Z'] = Z,

        ['a'] = a, ['d'] = d, ['e'] = e, ['f'] = f, ['h'] = h, ['l'] = l, ['n'] = n,
        ['o'] = o, ['r'] = r, ['s'] = s, ['t'] = t, ['u'] = u, ['v'] = v, ['w'] = w,

        ['\0'] = END_OF_LINE,
    };

    int transposition_table[state_count][input_count] = {
        [CAPITAL_V] = {
            [V] = NAME_LEFT,
        },
        [NAME_LEFT] = {
            [A] = NAME_RIGHT, [B] = NAME_RIGHT, [C] = NAME_RIGHT, [D] = NAME_RIGHT,
            [E] = NAME_RIGHT, [F] = NAME_RIGHT, [G] = NAME_RIGHT, [H] = NAME_RIGHT,
            [I] = NAME_RIGHT, [J] = NAME_RIGHT, [K] = NAME_RIGHT, [L] = NAME_RIGHT,
            [M] = NAME_RIGHT, [N] = NAME_RIGHT, [O] = NAME_RIGHT, [P] = NAME_RIGHT,
            [Q] = NAME_RIGHT, [R] = NAME_RIGHT, [S] = NAME_RIGHT, [T] = NAME_RIGHT,
            [U] = NAME_RIGHT, [V] = NAME_RIGHT, [W] = NAME_RIGHT, [X] = NAME_RIGHT,
            [Y] = NAME_RIGHT, [Z] = NAME_RIGHT,
        },
        [NAME_RIGHT] = {
            [A] = SKIP_SPACE, [B] = SKIP_SPACE, [C] = SKIP_SPACE, [D] = SKIP_SPACE,
            [E] = SKIP_SPACE, [F] = SKIP_SPACE, [G] = SKIP_SPACE, [H] = SKIP_SPACE,
            [I] = SKIP_SPACE, [J] = SKIP_SPACE, [K] = SKIP_SPACE, [L] = SKIP_SPACE,
            [M] = SKIP_SPACE, [N] = SKIP_SPACE, [O] = SKIP_SPACE, [P] = SKIP_SPACE,
            [Q] = SKIP_SPACE, [R] = SKIP_SPACE, [S] = SKIP_SPACE, [T] = SKIP_SPACE,
            [U] = SKIP_SPACE, [V] = SKIP_SPACE, [W] = SKIP_SPACE, [X] = SKIP_SPACE,
            [Y] = SKIP_SPACE, [Z] = SKIP_SPACE,
        },
        [SKIP_SPACE] = {
            [SPACE] = DIGIT_OR_SEMI,
        },
        [DIGIT_OR_SEMI] = {
            [ZERO] = DIGIT_OR_SEMI,
            [ONE] = DIGIT_OR_SEMI,
            [TWO] = DIGIT_OR_SEMI,
            [THREE] = DIGIT_OR_SEMI,
            [FOUR] = DIGIT_OR_SEMI,
            [FIVE] = DIGIT_OR_SEMI,
            [SIX] = DIGIT_OR_SEMI,
            [SEVEN] = DIGIT_OR_SEMI,
            [EIGHT] = DIGIT_OR_SEMI,
            [NINE] = DIGIT_OR_SEMI,
            [SEMI] = SPACE_AFTER_SEMI,
        },
        [SPACE_AFTER_SEMI] = {
            [SPACE] = NEXT_LEFT,
        },
        [NEXT_LEFT] = {
            [A] = NEXT_RIGHT, [B] = NEXT_RIGHT, [C] = NEXT_RIGHT, [D] = NEXT_RIGHT,
            [E] = NEXT_RIGHT, [F] = NEXT_RIGHT, [G] = NEXT_RIGHT, [H] = NEXT_RIGHT,
            [I] = NEXT_RIGHT, [J] = NEXT_RIGHT, [K] = NEXT_RIGHT, [L] = NEXT_RIGHT,
            [M] = NEXT_RIGHT, [N] = NEXT_RIGHT, [O] = NEXT_RIGHT, [P] = NEXT_RIGHT,
            [Q] = NEXT_RIGHT, [R] = NEXT_RIGHT, [S] = NEXT_RIGHT, [T] = NEXT_RIGHT,
            [U] = NEXT_RIGHT, [V] = NEXT_RIGHT, [W] = NEXT_RIGHT, [X] = NEXT_RIGHT,
            [Y] = NEXT_RIGHT, [Z] = NEXT_RIGHT, [SPACE] = NEXT_LEFT,
        },
        [NEXT_RIGHT] = {
            [A] = COMMA_OR_EOF, [B] = COMMA_OR_EOF, [C] = COMMA_OR_EOF, [D] = COMMA_OR_EOF,
            [E] = COMMA_OR_EOF, [F] = COMMA_OR_EOF, [G] = COMMA_OR_EOF, [H] = COMMA_OR_EOF,
            [I] = COMMA_OR_EOF, [J] = COMMA_OR_EOF, [K] = COMMA_OR_EOF, [L] = COMMA_OR_EOF,
            [M] = COMMA_OR_EOF, [N] = COMMA_OR_EOF, [O] = COMMA_OR_EOF, [P] = COMMA_OR_EOF,
            [Q] = COMMA_OR_EOF, [R] = COMMA_OR_EOF, [S] = COMMA_OR_EOF, [T] = COMMA_OR_EOF,
            [U] = COMMA_OR_EOF, [V] = COMMA_OR_EOF, [W] = COMMA_OR_EOF, [X] = COMMA_OR_EOF,
            [Y] = COMMA_OR_EOF, [Z] = COMMA_OR_EOF,
        },
        [COMMA_OR_EOF] = {
            [END_OF_LINE] = ACCEPT,
            [COMMA] = TRANSITION_SPACE,
        },
        [TRANSITION_SPACE] = {
            [SPACE] = NEXT_LEFT,
        },
    };

    int pos = 0;
    int state = CAPITAL_V;
    int i = 0;
    int lim = 128;
    char curr = 0;

    char *output = calloc(1, 1000);
    *output = '\0';
    char *ptr = output;
    int len = strlen(line);

    for (; i < lim; i++) {
        if (pos > len){
            break;
        }
        curr = line[pos];
        /*
        printf(
            "Currently on state=%s, pos=%d, char='%c' (%d)\n",
            state_names[state], pos, curr, (int)curr
        );
        */
        pos += jump[state] + 1;
        int next_action = action_for[state][char_map[curr]];
        if (next_action == EMIT_CHAR) {
            *ptr++ = curr;
        } else if (next_action == EMIT_COMMA) {
            *ptr++ = ',';
        } else if (next_action == NOTHING) {
            // do nothing...
        } else {
            die(fmt("illegal action: %d", next_action));
        }
        state = transposition_table[state][char_map[curr]];
    }
    if (i == lim) {
        die(fmt("timed out while parsing pos=%d at char=%c", pos, curr));
    }
    if (state != ACCEPT) {
        die(fmt("can only terminate on state ACCEPT but currently on state %s", state_names[state]));
    }
    return output;
}

static void parse_file(char *filename)
{
    FILE *fp;
    if (!(fp = fopen(filename, "r"))) {
        perror("fopen");
        die(fmt("Could not open %s", filename));
    }
    char buf[BUFSIZ];

    printf("%s|", filename);
    while (fgets(buf, BUFSIZ, fp)) {
        buf[strcspn(buf, "\r\n")] = '\0';
        char *result = parse_line(buf);
        // printf("%s -> ", buf);
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
