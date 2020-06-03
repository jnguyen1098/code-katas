#include <ctype.h>

int pten(size_t x)
{
    int result = 1;
    for (int i = 0; i < x; i++)
        result *= 10;
    return result;
}


int myAtoi(char *str)
{
    if (!str || !*str)
        return 0;
    
    while (*str == ' ')
        str++;
    
    if (!isdigit(*str) && *str != '-' && *str != '+' && *str != '0')
        return 0;
 
    int result = 0;
    _Bool is_negative = 0;
    
    if (*str == '-') {
        is_negative = 1;
        if (!isdigit(*++str))
            return 0;
    }
    
    if (*str == '+')
        str++;
    
    if (!isdigit(*str))
        return 0;
    
    while (*str == '0')
        str++;
    
    int n = 0;
    for (; isdigit(str[n]); n++)
        ;
    
    if (n > 10)
        return is_negative ? INT_MIN : INT_MAX;
    
    if (n >= 10 && ((*str - 48) > 2))
        return is_negative ? INT_MIN : INT_MAX;
    
    for (int i = 0; i < n; i++) {
        if (result > INT_MAX - ((str[i] - '0') * pten(n - i - 1)))
            return is_negative ? INT_MIN : INT_MAX;
        else
            result += (str[i] - '0') * pten(n - i - 1);
    }
    
    if (is_negative)
        result *= -1;
    
    return result;
}
