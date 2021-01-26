enum Point { X, Y, Z };

#define MIN(x,y,z)(x < y && x < z ? X : y < z ? Y : Z)

int *arraysIntersection(int *arr1, int arr1Size, int *arr2, int arr2Size, int *arr3, int arr3Size, int *returnSize)
{
    int *result = malloc(10000 * sizeof(int));
    int n = 0;
    
    int p1 = 0;
    int p2 = 0;
    int p3 = 0;
    
    while (p1 != arr1Size && p2 != arr2Size && p3 != arr3Size) {
        switch (MIN(arr1[p1], arr2[p2], arr3[p3])) {
            case X:
                if (arr1[p1] == arr2[p2] && arr2[p2] == arr3[p3]) {
                    p2++;
                    p3++;
                    result[n++] = arr1[p1];
                }
                p1++;
                break;
                
            case Y:
                if (arr1[p1] == arr2[p2] && arr2[p2] == arr3[p3]) {
                    p1++;
                    p3++;
                    result[n++] = arr2[p2];
                }
                p2++;
                break;
                
            case Z:
                if (arr1[p1] == arr2[p2] && arr2[p2] == arr3[p3]) {
                    p1++;
                    p2++;
                    result[n++] = arr3[p3];
                }
                p3++;
                break;
        }
    }
    
    *returnSize = n;
    return result;
}
