struct ListNode *rotateRight(struct ListNode *head, int k)
{
    // No work if NULL list or k == 0
    if (!head || !k) {
        return head;
    }
    
    // Find last node and keep track of length
    size_t length = 1;
    struct ListNode *tmp = NULL;
    for (tmp = head; tmp->next; tmp = tmp->next) {
        length++;
    }
    
    // Create circular linked list
    tmp->next = head;

    // Go to the new start of the list    
    tmp = head;
    for (int i = 0; i < length - (k % length); i++) {
        tmp = tmp->next;
    }
    
    // Update to the new head
    head = tmp;
    
    // From this point on, find the new tail
    for (int i = 0; i < length - 1; i++) {
        tmp = tmp->next;
    }
    
    // Update tail
    tmp->next = NULL;
    
    // Return updated head
    return head;
}
