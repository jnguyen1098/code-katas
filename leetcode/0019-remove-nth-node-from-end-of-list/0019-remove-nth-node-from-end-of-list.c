struct ListNode *removeNthFromEnd(struct ListNode *head, int n)
{   
    struct ListNode *tmp = head;
    while (n--) {
        tmp = tmp->next;
    }
    
    struct ListNode **tracer = &head;
    while (tmp) {
        tracer = &(*tracer)->next;
        tmp = tmp->next;
    }
    
    (*tracer) = (*tracer)->next;
    
    return head;
}   
