bool isPalindrome(struct ListNode *head)
{
    struct ListNode *fast = head;
    struct ListNode *slow = head;
    
    while (fast && fast->next) {
        fast = fast->next->next;
        slow = slow->next;
    }
    
    struct ListNode *prev = NULL;
    struct ListNode *curr = slow;
    struct ListNode *next = NULL;
    
    while (curr) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    
    while (prev) {
        if (prev->val != head->val) {
            return false;
        }
        prev = prev->next;
        head = head->next;
    }
    
    return true;
}
