int intcmp(const void *a, const void *b)
{
    return *(int *)b - *(int *)a;
}

void push(struct ListNode **list, int value)
{
    if (list) {
        struct ListNode *new_node = calloc(1, sizeof(struct ListNode));
        new_node->val = value;
        new_node->next = *list;
        *list = new_node;
    }
}

struct ListNode *sortList(struct ListNode *head)
{
    if (!head) return NULL;
    
    struct ListNode *sorted = NULL;
    
    int n = 0;
    for (struct ListNode *tmp = head; tmp; tmp = tmp->next) {
        n++;
    }
    
    int v = 0;
    int *values = malloc(sizeof(int) * n);
    
    for (struct ListNode *tmp = head; tmp; tmp = tmp->next) {
        values[v++] = tmp->val;
    }
    
    qsort(values, n, sizeof(int), intcmp);
    
    for (int i = 0; i < n; i++) {
        push(&sorted, values[i]);
    }
    
    free(values);
    return sorted;
}
