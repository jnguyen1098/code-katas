#define MIN(x,y)(x < y ? x : y)
int maxNumberOfBalloons(char *text)
{
    int count = INT_MAX;
    int map[26] = { 0 };
    
    for (int i = 0; text[i]; i++) {
        map[text[i] - 'a']++;
    }
    
    count = MIN(count, map['b' - 'a']);
    count = MIN(count, map['a' - 'a']);
    count = MIN(count, map['l' - 'a'] / 2);
    count = MIN(count, map['o' - 'a'] / 2);
    count = MIN(count, map['n' - 'a']);
    
    return count;
}
