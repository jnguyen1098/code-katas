class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        fast = head
        slow = head
        
        found = 0
        
        while slow is not None and fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            
            if fast == slow:
                found = 1
                break
        
        if found == 0:
            return None
            
        other = head
        while other != slow:
            if not slow:
                return None
            other = other.next
            slow = slow.next
            
        return other
