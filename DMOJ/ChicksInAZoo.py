// /* Initially, the zoo have a single chick. A chick gives birth to 2 chicks every day and the life expectancy of a chick is 6 days. Zoo officials want to buy food for chicks so they want to know the number of chicks on an Nth day.
// Help the officials with this task.*/


class Solution:

 def NoOfChicks(self, N):

 # Code here

 

 a=[0 for i in range(N+1)]

 s,a[0]=1,1

 for i in range(1,N):

     if (i-6>=0):

         s-=a[i-6]

     a[i]=2*s

     s+=a[i]

 return s
