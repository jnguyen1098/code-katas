#include <stdio.h>

#define LEFT(c)((c) == '(' || (c) == '[' || (c) == '{' || (c == '<'))

int stack[BUFSIZ], sp = 0;

char inverse[128] = { [')'] = '(', [']'] = '[', ['}'] = '{', ['>'] = '<' };
int errscore[128] = { [')'] = 3, [']'] = 57, ['}'] = 1197, ['>'] = 25137 };

int main(void)
{
    int score = 0;
    char buf[BUFSIZ];
    FILE *input = fopen("real", "r");
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
