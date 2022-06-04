struct ListNode **try_advance_two(struct ListNode **node)
{
    if (*node) node = &(*node)->next;
    if (*node) node = &(*node)->next;
    return node;
}

struct ListNode **swap_two_nodes(struct ListNode **source)
{
    struct ListNode *first = *source;
    struct ListNode *second = (*source)->next;
    struct ListNode *out = second->next;
    
    *source = second;
    second->next = first;
    first->next = out;
    
    return source;
}

struct ListNode *swapPairs(struct ListNode *head)
{
    if (!head || !head->next) {
        return head;
    }
    
    for (struct ListNode **tracer = &head; *tracer && (*tracer)->next; tracer = try_advance_two(tracer)) {
        swap_two_nodes(tracer);
    }
    
    return head;
}
