class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        cycles = 0
        transcript = {}
        
        for relation in relations:
            if relation[0] not in transcript:
                transcript[relation[0]] = set()
            if relation[1] not in transcript:
                transcript[relation[1]] = set()
            
        for relation in relations:
            transcript[relation[1]].add(relation[0])
        
        while True:
            to_remove = []
            
            for key, item in transcript.items():
                if item == set():
                    to_remove.append(key)
            
            if to_remove == []:
                return -1
            
            for course in to_remove:
                transcript.pop(course)
                
                for key, item in transcript.items():
                    if course in item:
                        item.remove(course)
                        
            cycles += 1
            
            if len(transcript.items()) == 0:
                break
        
        return cycles
