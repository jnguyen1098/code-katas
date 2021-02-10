int confuse[] = {
    0, 1, -1, -1, -1, -1, 9, -1, 8, 6
};

bool confusingNumber(int N)
{
    int original = N;
    int converted = 0;
    
    while (N) {
        if (confuse[N % 10] == -1) {
            return false;
        }
        converted = (converted * 10) + confuse[N % 10];
        N /= 10;
    }
    
    return converted != original;
}
