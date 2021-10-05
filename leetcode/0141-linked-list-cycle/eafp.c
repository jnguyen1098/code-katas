#include <signal.h>
#include <setjmp.h>

jmp_buf env_buffer;

void handler(int signo)
{
    longjmp(env_buffer, 1);  // 3. unwind stack upon segfault
}

bool hasCycle(struct ListNode *head)
{
    signal(SIGSEGV, handler);  // 1. install segfault signal catcher
    if (setjmp(env_buffer) != 0) {  // 4. return false on stack unwind on SIGSEGV
        return false;
    }

    struct ListNode *slow = head;
    struct ListNode *fast = head->next;

    while (slow != fast) {
        slow = slow->next;
        fast = fast->next->next;  // 2. seg fault here will trip handler()
    }

    return true;
}
