//Array changing from number to roman
char *table[1001] = {
    [1] = "I",
    [4] = "IV",
    [5] = "V",
    [9] = "IX",
    [10] = "X",
    [40] = "XL",
    [50] = "L",
    [90] = "XC",
    [100] = "C",
    [400] = "CD",
    [500] = "D",
    [900] = "CM",
    [1000] = "M",
};

int choices[] = {
    1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1,
}, n = sizeof(choices) / sizeof(*choices);

//Function changing number to roman
char *intToRoman(int num)
{
    char *result = calloc(1000, 1);
    while (num) {
        for (int i = 0; i < n; i++) {
            if (num - choices[i] >= 0) {
                num -= choices[i];
                strcat(result, table[choices[i]]);
                break;
            }
        }
    }
    return result;
}
