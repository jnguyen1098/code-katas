int bitwiseComplement(int num)
{
    if (!num) return 1;
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
