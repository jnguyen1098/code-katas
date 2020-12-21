class Solution:
    def middleNode(self, head: ListNode) -> ListNode:
        fast = head
        slow = head
        while slow is not None and fast is not None and fast.next is not None:
            fast = fast.next.next
            slow = slow.next
        return slow
