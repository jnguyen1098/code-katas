class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        prereqs = {}
        frees = set()
        courses = []
        
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
            courses.append(popped)
            for course, requirements in prereqs.items():
                if popped in requirements:
                    requirements.remove(popped)
                if not requirements:
                    deletes.append(course)
                    frees.add(course)     
            for delete in deletes:
                prereqs.pop(delete)
        
        return courses + list(frees) if not prereqs else []
