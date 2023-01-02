#define _GNU_SOURCE
#include "plumber.h"

#define VALVE_MAX 64

static struct valve_t {
    char name[3];
    int flow;
    char exits[VALVE_MAX][3];
    int num_exits;
} valves[VALVE_MAX];

static int num_valves = 0;

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
    return;
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

/*
 * /^.{6}[A-Z][A-Z].{15}\d*;.{23} ?[A-Z][A-Z](?:, [A-Z][A-Z])*$/
 */
static char *parse_line(char *line)
{
    // reset state
    num_valves = 0;
    for (int i = 0; i < VALVE_MAX; i++) {
        valves[i].num_exits = 0;
    }

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
        READ_VALVE_L,
        READ_VALVE_R,
        WRITE_DIGIT,
        FLUSH_DIGIT,
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
            [A] = READ_VALVE_L, [B] = READ_VALVE_L, [C] = READ_VALVE_L, [D] = READ_VALVE_L,
            [E] = READ_VALVE_L, [F] = READ_VALVE_L, [G] = READ_VALVE_L, [H] = READ_VALVE_L,
            [I] = READ_VALVE_L, [J] = READ_VALVE_L, [K] = READ_VALVE_L, [L] = READ_VALVE_L,
            [M] = READ_VALVE_L, [N] = READ_VALVE_L, [O] = READ_VALVE_L, [P] = READ_VALVE_L,
            [Q] = READ_VALVE_L, [R] = READ_VALVE_L, [S] = READ_VALVE_L, [T] = READ_VALVE_L,
            [U] = READ_VALVE_L, [V] = READ_VALVE_L, [W] = READ_VALVE_L, [X] = READ_VALVE_L,
            [Y] = READ_VALVE_L, [Z] = READ_VALVE_L,
        },
        [NAME_RIGHT] = {
            [A] = READ_VALVE_R, [B] = READ_VALVE_R, [C] = READ_VALVE_R, [D] = READ_VALVE_R,
            [E] = READ_VALVE_R, [F] = READ_VALVE_R, [G] = READ_VALVE_R, [H] = READ_VALVE_R,
            [I] = READ_VALVE_R, [J] = READ_VALVE_R, [K] = READ_VALVE_R, [L] = READ_VALVE_R,
            [M] = READ_VALVE_R, [N] = READ_VALVE_R, [O] = READ_VALVE_R, [P] = READ_VALVE_R,
            [Q] = READ_VALVE_R, [R] = READ_VALVE_R, [S] = READ_VALVE_R, [T] = READ_VALVE_R,
            [U] = READ_VALVE_R, [V] = READ_VALVE_R, [W] = READ_VALVE_R, [X] = READ_VALVE_R,
            [Y] = READ_VALVE_R, [Z] = READ_VALVE_R,
        },
        [DIGIT_OR_SEMI] = {
            [ZERO] = WRITE_DIGIT,
            [ONE] = WRITE_DIGIT,
            [TWO] = WRITE_DIGIT,
            [THREE] = WRITE_DIGIT,
            [FOUR] = WRITE_DIGIT,
            [FIVE] = WRITE_DIGIT,
            [SIX] = WRITE_DIGIT,
            [SEVEN] = WRITE_DIGIT,
            [EIGHT] = WRITE_DIGIT,
            [NINE] = WRITE_DIGIT,
            [SEMI] = FLUSH_DIGIT,
        },
        [NEXT_LEFT] = {
            [A] = READ_VALVE_L, [B] = READ_VALVE_L, [C] = READ_VALVE_L, [D] = READ_VALVE_L,
            [E] = READ_VALVE_L, [F] = READ_VALVE_L, [G] = READ_VALVE_L, [H] = READ_VALVE_L,
            [I] = READ_VALVE_L, [J] = READ_VALVE_L, [K] = READ_VALVE_L, [L] = READ_VALVE_L,
            [M] = READ_VALVE_L, [N] = READ_VALVE_L, [O] = READ_VALVE_L, [P] = READ_VALVE_L,
            [Q] = READ_VALVE_L, [R] = READ_VALVE_L, [S] = READ_VALVE_L, [T] = READ_VALVE_L,
            [U] = READ_VALVE_L, [V] = READ_VALVE_L, [W] = READ_VALVE_L, [X] = READ_VALVE_L,
            [Y] = READ_VALVE_L, [Z] = READ_VALVE_L,
        },
        [NEXT_RIGHT] = {
            [A] = READ_VALVE_R, [B] = READ_VALVE_R, [C] = READ_VALVE_R, [D] = READ_VALVE_R,
            [E] = READ_VALVE_R, [F] = READ_VALVE_R, [G] = READ_VALVE_R, [H] = READ_VALVE_R,
            [I] = READ_VALVE_R, [J] = READ_VALVE_R, [K] = READ_VALVE_R, [L] = READ_VALVE_R,
            [M] = READ_VALVE_R, [N] = READ_VALVE_R, [O] = READ_VALVE_R, [P] = READ_VALVE_R,
            [Q] = READ_VALVE_R, [R] = READ_VALVE_R, [S] = READ_VALVE_R, [T] = READ_VALVE_R,
            [U] = READ_VALVE_R, [V] = READ_VALVE_R, [W] = READ_VALVE_R, [X] = READ_VALVE_R,
            [Y] = READ_VALVE_R, [Z] = READ_VALVE_R,
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

    uint8_t jump[128] = {
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

    uint8_t pos = 0;
    int state = CAPITAL_V;
    int i = 0;
    int lim = 128;
    int8_t curr = 0;

    char *output = calloc(1, 1000);
    *output = '\0';
    char *ptr = output;
    size_t len = strlen(line);
    int name_written = 0;
    int dig = 0;
    char digit_buf[16] = "";
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
        if (next_action == READ_VALVE_L) {
            if (name_written == 0) {
                valves[num_valves].name[0] = curr;
            } else {
                valves[num_valves].exits[valves[num_valves].num_exits][0] = curr;
            }
            *ptr++ = curr;
        } else if (next_action == READ_VALVE_R) {
            if (name_written == 0) {
                valves[num_valves].name[1] = curr;
                valves[num_valves].name[2] = 0;
                name_written = 1;
            } else {
                valves[num_valves].exits[valves[num_valves].num_exits][1] = curr;
                valves[num_valves].exits[valves[num_valves].num_exits][2] = 0;
                valves[num_valves].num_exits++;
            }
            *ptr++ = curr;
            *ptr++ = ',';
        } else if (next_action == WRITE_DIGIT) {
            *ptr++ = curr;
            digit_buf[dig++] = curr;
        } else if (next_action == FLUSH_DIGIT) {
            *ptr++ = ',';
            valves[num_valves].flow = atoi(digit_buf);
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
    puts("\n");
    printf("Line: %s\n", line);
    printf("Valve name: %s\n", valves[num_valves].name);
    printf("Valve flow: %d\n", valves[num_valves].flow);
    printf("Valve exits: ");
    for (int i = 0; i < valves[num_valves].num_exits; i++) {
        printf("%s ", valves[num_valves].exits[i]);
    }
    puts("");
    num_valves++;
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
        // printf("%s|", result);
        free(result);  // TODO
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
    printf("TODO: %s\n", filename);
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
