#define MAX(x,y)((x) > (y) ? (x) : (y))

unsigned long long int create_mask(char *word)
{
    unsigned long long int mask = 0UL;
    
    for (; *word; word++) {
        mask |= (1UL << (*word) - 'a');
    }
    
    return mask;
}

int maxProduct(char **words, int wordsSize)
{
    unsigned long long int *masks = calloc(wordsSize, sizeof(unsigned long long int));
    unsigned long long int *lengths = calloc(wordsSize, sizeof(unsigned long long int));
    unsigned long long int max_length = 0;
    
    for (int i = 0; i < wordsSize; i++) {
        lengths[i] = strlen(words[i]);
    }
    
    for (int i = 0; i < wordsSize; i++) {
        masks[i] = create_mask(words[i]);
    }
    
    for (int i = 0; i < wordsSize; i++) {
        for (int j = i + 1; j < wordsSize; j++) {
            if (masks[i] & masks[j]) {
                continue;
            }
            max_length = MAX(max_length, lengths[i] * lengths[j]);
        }
    }
    
    return max_length;
}
