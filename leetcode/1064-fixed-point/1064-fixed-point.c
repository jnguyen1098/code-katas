int fixedPoint(int *arr, int arrSize)
{
    for (int i = 0; i < arrSize; i++) {
        if (arr[i] == i) {
            return i;
        }
    }
    return -1;
}
