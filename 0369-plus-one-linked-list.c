struct ListNode *_plusOne(struct ListNode *head, int idx)
{
    struct ListNode *tmp = head;
    if (idx == 0 && head->val == 9) {
        tmp = malloc(sizeof(struct ListNode));
        tmp->val = 1;
        tmp->next = head;
        head->val = 0;
        return tmp;
    }
    for (int i = 0; i < idx; i++) {
        tmp = tmp->next;
    }
    if (tmp->val != 9) {
        tmp->val++;
    } else {
        tmp->val = 0;
        return _plusOne(head, idx - 1);
    }
    return head;
}

struct ListNode *plusOne(struct ListNode *head)
{
    if (head) {
        int n = 0;
        for (struct ListNode *tmp = head; tmp; tmp = tmp->next)
            n++;
        head = _plusOne(head, n - 1);
    }
    
    return head;
}
