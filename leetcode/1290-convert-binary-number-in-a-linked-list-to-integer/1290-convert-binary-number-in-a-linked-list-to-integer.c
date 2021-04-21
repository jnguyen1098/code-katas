/*
    256 128  64  32  16  8    4   2   1
    2^8 2^7 2^6 2^5 2^4 2^3 2^2 2^1 2^0
*/

int getDecimalValue(struct ListNode *head)
{
    int result = 0;
    
    for (struct ListNode *tmp = head; tmp; tmp = tmp->next) {
        result <<= 1;
        result += tmp->val;
    }
    
    return result;
}
