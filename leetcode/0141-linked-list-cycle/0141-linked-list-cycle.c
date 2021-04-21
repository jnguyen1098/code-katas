bool hasCycle(struct ListNode *head)
{
    struct ListNode *slow = head;
    struct ListNode *fast = head;
    
    while (slow && fast) {
        slow = slow->next;
        fast = fast->next;
        if (!fast || !slow) {
            break;
        }
        fast = fast->next;
        if (fast == slow) {
            return true;
        }
    }
    
    return false;
}
