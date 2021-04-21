int numberOfSteps(int num)
{
    int count = 0;
    
    while (num) {
        if (!(num % 2)) {
            num /= 2;
        } else {
            num--;
        }
        count++;
    }
    
    return count;
}
