int getValue(struct NestedInteger *item, int level)
{
    int value = 0;
    
    if (NestedIntegerIsInteger(item)) {
        value += NestedIntegerGetInteger(item) * level;
    } else {
        int n = NestedIntegerGetListSize(item);
        struct NestedInteger **subList = NestedIntegerGetList(item);
        for (int i = 0; i < n; i++) {
            value += getValue(subList[i], level + 1);
        }
    }
    
    return value;
}

int depthSum(struct NestedInteger** nestedList, int nestedListSize)
{
    int result = 0;
    for (int i = 0; i < nestedListSize; i++) {
        result += getValue(nestedList[i], 1);
    }
    return result;
}
