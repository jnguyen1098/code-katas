#define NUM_LETTER 26

typedef struct trie_struct {
    int is_word;
    struct trie_struct *next[NUM_LETTER];
} Trie;

Trie *trieCreate()
{
    Trie *trie = calloc(1, sizeof(Trie));
    return trie;
}

void trieInsert(Trie *obj, char *word)
{
    if (!obj || !word) return;
    
    Trie *start = obj;
    while (*word) {
        if (start->next[*word - 'a'] == NULL) {
            start->next[*word - 'a'] = calloc(1, sizeof(Trie));
        }
        
        if (!*(word + 1)) {
            start->next[*word - 'a']->is_word = 1;
        }
        
        start = start->next[*word - 'a'];
        word++;
    }
}

bool trieSearch(Trie *obj, char *word) {
    Trie *start = obj;
    while (*word) {
        if (start->next[*word - 'a'] == NULL) {
            return false;
        }
        if (!*(word + 1) && !start->next[*word - 'a']->is_word) {
            return false;
        }
        start = start->next[*word - 'a'];
        word++;
    }
    return true;
}

bool trieStartsWith(Trie *obj, char *word)
{
    Trie *start = obj;
    while (*word) {
        if (start->next[*word - 'a'] == NULL) {
            return false;
        }
        start = start->next[*word - 'a'];
        word++;
    }
    return true;
}

void trieFree(Trie* obj)
{
    for (int i = 0; i < NUM_LETTER; i++) {
        if (obj->next[i])
            trieFree(obj->next[i]);
    }
    free(obj);
}
