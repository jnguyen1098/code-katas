int findComplement(int num)
{
    num = ~num;
    for (int i = 31; i >= 0; i--) {
        if (num & (1U << i)) {
            num &= ~(1U << i);
        } else {
            break;
        }
    }
    return num;
}
