// BOOKMARK
void printLinkedListInReverse(struct ImmutableListNode *head)
{
    if (head) {
        printLinkedListInReverse(head->getNext(head));
        head->printValue(head);
    }
}
