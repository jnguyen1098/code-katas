/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

struct ListNode *rotateRight(struct ListNode *head, int k)
{
    if (!head) {
        return NULL;
    }
    
    if (!k) {
        return head;
    }
    
    size_t length = 1;
    struct ListNode *tmp = NULL;
    for (tmp = head; tmp->next; tmp = tmp->next) {
        length++;
    }
    
    tmp->next = head;
    
    size_t start = length - (k % length);
    
    tmp = head;
    for (int i = 0; i < start; i++) {
        tmp = tmp->next;
    }
    
    struct ListNode *return_ptr = tmp;
    
    for (int i = 0; i < length - 1; i++) {
        tmp = tmp->next;
    }
    
    tmp->next = NULL;
    
    return return_ptr;
}
