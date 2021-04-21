bool validMountainArray(int *arr, int arrSize)
{
    if (arrSize < 3) return false;
    
    int n = 1;
    
    STATE_ONE:
        if (n == arrSize) return false;
        if (arr[n] > arr[n - 1]) {
            n++;
            goto STATE_TWO;
        } else {
            return false;
        }

    STATE_TWO:
        if (n == arrSize) return false;
        if (arr[n] > arr[n - 1]) {
            n++;
            goto STATE_TWO;
        } else {
            goto STATE_THREE;
        }

    STATE_THREE:
        if (n == arrSize) return true;
        if (arr[n] < arr[n - 1]) {
            n++;
            goto STATE_THREE;
        } else {
            return false;
        }
}
