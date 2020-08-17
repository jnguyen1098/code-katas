int *distributeCandies(int candies, int num_people, int *returnSize)
{
    int *answer = calloc(sizeof(int), num_people);
    
    for (int next = 1, i = 0; ; next++, i++) {
        if (candies - next >= 0) {
            answer[i % num_people] += next;
            candies -= next;
        } else {
            answer[i % num_people] += candies;
            break;
        }
    }
    
    *returnSize = num_people;
    return answer;
}
