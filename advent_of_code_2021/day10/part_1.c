#include <stdio.h>

#if 0
# define INPUT "example"
#else
# define INPUT "real"
#endif

#define LEFT(c)((c) == '(' || (c) == '[' || (c) == '{' || (c == '<'))

int stack[BUFSIZ], sp = 0;

char inverse[128] = { [')'] = '(', [']'] = '[', ['}'] = '{', ['>'] = '<' };
int errscore[128] = { [')'] = 3, [']'] = 57, ['}'] = 1197, ['>'] = 25137 };

int main(void)
{
    int score = 0;
    char buf[BUFSIZ];
    FILE *input = fopen(INPUT, "r");
    while (fgets(buf, BUFSIZ, input)) {
        for (char *s = buf; *s && *s != '\n'; s++) {
            if (LEFT(*s)) {
                stack[sp++] = *s;
            } else {
                if (stack[--sp] != inverse[*s]) {
                    score += errscore[*s];
                }
            }
        }
    }
    printf("%d\n", score);
}

/*
inverse = { ")": "(", "]": "[", "}": "{", ">": "<" }
errorscore = { ")": 3, "]": 57, "}": 1197, ">": 25137 }

lines = open(inputname, "r").read().splitlines()

stack = []
score = 0

for idx, line in enumerate(lines):
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            popped = stack.pop()
            if popped != inverse[char]:
                score += errorscore[char]

print(score)
*/
