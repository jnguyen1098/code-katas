class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        prereqs = {}
        frees = set()
        
        for prereq in prerequisites:
            if prereq[0] not in prereqs:
                prereqs[prereq[0]] = set()
            prereqs[prereq[0]].add(prereq[1])
            
        for i in range(numCourses):
            if i not in prereqs:
                frees.add(i)
                
        while frees and prereqs:
            deletes = []
            popped = frees.pop()
            for course, requirements in prereqs.items():
                if popped in requirements:
                    requirements.remove(popped)
                if not requirements:
                    deletes.append(course)
                    frees.add(course)     
            for delete in deletes:
                prereqs.pop(delete)
        
        return len(prereqs) == 0
