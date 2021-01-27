int peakIndexInMountainArray(int *arr, int arrSize)
{
    for (int i = 1; i < arrSize; i++) {
        if (arr[i - 1] > arr[i]) {
            return i - 1;
        }
    }
    exit(0);
}
