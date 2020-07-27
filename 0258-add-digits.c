int addDigits(int num)
{
    if (num < 10)
        return num;
    
    int result = 0;
    
    while (num) {
        result += num % 10;
        num /= 10;
    }
    
    return addDigits(result);
}
