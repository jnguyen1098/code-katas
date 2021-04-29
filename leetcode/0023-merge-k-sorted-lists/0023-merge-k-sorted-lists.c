struct ListNode *pull(struct ListNode **list)
{
    struct ListNode *tmp = *list;
    *list = (*list)->next;
    return tmp;
}

struct ListNode *pop_min(struct ListNode **lists, int listsSize)
{
    int min = INT_MAX;
    int min_idx = -1;
    for (int i = 0; i < listsSize; i++) {
        if (!lists[i]) continue;
        int tmp = lists[i]->val;
        if (tmp < min) min = tmp, min_idx = i;
    }
    return min_idx == -1 ? NULL : pull(&lists[min_idx]);
}

void push(struct ListNode **list, struct ListNode *new)
{
    if (!*list) {
        *list = new;
        (*list)->next = NULL;
        return;
    }
    (*list)->next = new;
}

struct ListNode *mergeKLists(struct ListNode **lists, int listsSize)
{
    struct ListNode *list = NULL;
    struct ListNode **tail = &list;
    for (struct ListNode *to_push = NULL; (to_push = pop_min(lists, listsSize)); ) {
        push(tail, to_push);
        tail = &(*tail)->next;
    }
    return list;
}
