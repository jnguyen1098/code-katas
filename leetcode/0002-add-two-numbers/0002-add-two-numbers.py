# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        def recurse(node, nums):
            if node:
                recurse(node.next, nums)
                nums.append(str(node.val))
                return nums
        
        l1n = recurse(l1, [])
        l2n = recurse(l2, [])
        
        head = ListNode(val=0, next=None)
        tail = head
        
        cheat = int("".join(l1n)) + int("".join(l2n))
        while cheat:
            tail.next = ListNode(cheat % 10)
            tail = tail.next
            cheat //= 10
        
        return head.next if head.next else ListNode(0)
