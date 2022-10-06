class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        furthest_left = defaultdict(int)
        for idx, colour in enumerate(colors):
            if colour not in furthest_left:
                furthest_left[colour] = idx
        
        furthest_right = defaultdict(int)
        for i in range(len(colors) - 1, -1, -1):
            colour = colors[i]
            if colour not in furthest_right:
                furthest_right[colour] = i
                
        unique_colours = set(colors)        
        
        furthest = 0
        
        for idx, color in enumerate(colors):
            for other_color, furthest_distance in furthest_left.items():
                if color != other_color:
                    furthest = max(furthest, abs(furthest_distance - idx))
            for other_color, furthest_distance in furthest_left.items():
                if color != other_color:
                    furthest = max(furthest, abs(furthest_distance - idx))
            
        
        return furthest
