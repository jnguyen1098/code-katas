struct ListNode *removeElements(struct ListNode *head, int val)
{
    for (struct ListNode **tracer = &head; *tracer; tracer = &(*tracer)->next) {
        while (*tracer && (*tracer)->val == val)
            *tracer = (*tracer)->next;
        if (!*tracer) break;
    }
    return head;
}
