class Solution:
    def rob(self, nums: List[int]) -> int:
        
        """
            Trivial case [a]
            
            If the test case only has one house, then it is impossible to rob an adjacent
            house. Therefore, the answer is a.
            
            
            Trivial case [a, b]
            
            If the test case has two houses, then we can only, by definition, take money
            from one house. If we take a and b, then we lose. This means we have to take
            the maximum of either house, and only rob that. Therefore, the answer is max(a, b).
            
            
            Case [a, b, c]
            This case is interesting. The possible answers are:
                - a
                - b
                - c
                - a, c
            Trying out all of these possibilities is a thing, however that will TLE once the
            test cases reach some absurd weed-out number like 100 houses.
            
            One thing we can note is that a dynamic programming problem has two properties:
                - Optimal substructure
                - Overlapping sub-problems
                
            What's the first one? Optimal substructure. It means that a solution is made up of
            smaller solutions. For example, in the Fibonacci sequence, we can define:
            
                f(n) = f(n - 1) + f(n - 2)
            
            so... f(n) is defined in terms of itself. That means a solution, f(n), is made up
            of other solutions, f(n - 1) and f(n - 2).
            
            This problem exhibits optimal substructure because we can take existing "runs" or
            subarrays' solutions and use them to create other solutions. For example, let's use
            
                [1, 2, 3]
                
            So we already established that the base cases occur at len=1 and len=2. Let's solve
            for len=2, or [1, 2]. 2 > 1, so the answer for the subarray [1, 2], or [[1, 2], 3],
            is 2.
            
            How do we relate the fact that the solution to the [1, 2] subarray is 2 to the rest
            of the array (which is 3)?
            
            Well, to establish some basis: the answer to [1, 2, 3] is 4. We can take from the
            first and the third house to make (1 + 3) = 4 dollars. The other answers (1, 2, and
            3 respectively) are inferior.
            
            Hmm, it appears something isn't right. There isn't a way to easily discern the answer
            (1, 3) from [[1, 2], 3] because in order to get to [[1], 2, [3]], you have to first
            create an INFERIOR solution to the subarray [1, 2], because in order to connect with
            3 you must have a subarray that is not going to trigger an adjacent alarm with 3...
            
            Perhaps we could create two possible answers for each subarray mini solution? Perhaps
            one where the last element is added, and one where it isn't?
            
            [1, 2, 3]
            
            First, let's create a mini solution for the subarray [1]. The element of focus is 1.
            We create two universes. One where we do include the element of focus, and one where
            we don't.
            
                Universe 1: []
                
                Universe 2: [1]
                
            OK, now how are we going to progress...? Now we need to create the solution to the
            subarray [1, 2] using this newfangled logic I tried coming up with.
            
            Well, if my predictions are correct, then the solution to the subarray [1, 2] is
            actually the solution to the subarray [1] (whose two universes we just enumerated)
            plus potentially the element of interest (depending whether we take it or not).
            
            Solution([1,2]) is bigger of WeTakeElementFrom([1]) or WeDontTakeElementFrom([1]) + 2
            Solution([1,2]) = max(didntTakeLastElement(Solution[1]) + 2,
                                  didTakeLastElement(Solution[1]))
                                  
            I haven't implemented this, but this literally just looks like brute force. I might
            need to look back at the drawing board. Or just trace a solution to see what happens.
            
            Solution([1, 2, 3]) is
                max( Solution([1, 2]).taken , Solution([1, 2]).notTaken + 3 )
                    Solution([1, 2]).taken is
                        max( Solution([1]).taken , Solution([1]).notTaken + 2 )
                            Solution([1]).taken is
                                1
                            Solution([1]).notTaken is
                                0
                        max( 1 , 0 + 2 )
                        max( 1 , 2 )
                        2
                    Solution([1, 2]).notTaken is
                        Solution([1])
                            Solution([1]) is
                                1
                        1
                max( 2 , 1 + 3 )
                max( 2 , 4 )
                4
                        
            This doesn't really help much. Maybe I can generalize taken and not taken?
            
                Solution(array).taken    = Solution(arrayMinusLastTwoElement) + arrayLastElement
                Solution(array).notTaken = Solution(arrayMinusLastElement)
                
            I feel like I'm getting a little closer, but I should probably define a proper notation
            for subproblems.
            
            How about this. For 0-indexed array [0, 1, 2, ..., n], I denote the subproblem for array
            [0, ..., x] as Sub(x). So for array
            
                [1, 2, 3, 4, 5]
                            
            We can say:
            
                Sub(0) = [1]
                Sub(1) = [1, 2]
                Sub(4) = [1, 2, 3, 4, 5]
                
            and for any given array of length n, we are looking for the solution to Sub(n - 1)
            
            Or maybe we should just drop the Sub() moniker entirely. So instead of
            
                Solution(Sub(n - 1))
                
            we look for
            
                Solution(n - 1)
                
            Solution(0) = arr[0]
            Solution(1) = max(arr[0], arr[1])
            Solution(2) = max(Solution(0) + arr[2], Solution(1))
            ...
            Solution(n) = max(Solution(n - 2) + arr[n], Solution(n - 1))
            
            
            For array [1, 2, 3] let us test this hypothesis.
            
            Solution(2) = Solution for [1, 2, 3]
                        = max(Solution(0) + arr[2], Solution(1))
                          Solution(0) = arr[0]
                                      = 1 // CACHED SOLUTION(0) = 1
                          Solution(1) = max(arr[0], arr[1])
                                      = max(1, 2)
                                      = 2 // CACHED SOLUTION(1) = 2
                        = max(1 + arr[2], 2)
                        = max(1 + 2, 2)
                        = max(3, 2)
                        = 3 // CACHED SOLUTION(2) = 3
            
            We didn't get to use any of our cached values; let's try the harder example.
            
            Array = [2, 7, 9, 3, 1]
            
            Solution(4) = max(Solution(2) + arr[4], Solution(3))
                          Solution(2) = max(Solution(0) + arr[2], Solution(1))
                                        Solution(0) = arr[0]
                                                    = 2 // CACHED SOLUTION(0) = 2
                                        Solution(1) = max(arr[0], arr[1])
                                                    = max(2, 7)
                                                    = 7 // CACHED SOLUTION(1) = 7
                                      = max(2 + arr[2], 7)
                                      = max(2 + 9, 7)
                                      = max(11, 7)
                                      = 11 // CACHED SOLUTION(2) = 11 
                          Solution(3) = max(Solution(1) + arr[3], Solution(2))
                                      = max(7 + 3, 11) // CACHED VALUES USED!!! 0 and 1
                                      = max(10, 11)
                                      = 11 // CACHED SOLUTION(3) = 11
                        = max(11 + 1, 11)
                        = max(12, 11)
                        = 12
        """
        
        if len(nums) == 1:
            return nums[0]
        
        if len(nums) == 2:
            return max(nums[0], nums[1])
        
        solutions = [-math.inf] * len(nums)
        solutions[0] = nums[0]
        solutions[1] = max(nums[0], nums[1])
        
        for i in range(2, len(nums)):
            solutions[i] = max(solutions[i - 2] + nums[i], solutions[i - 1])
        
        return solutions[len(nums) - 1]
    
        """
        I fucking did it. I can't believe I actually did it. My solution worked.
        I'm so happy.
        """
