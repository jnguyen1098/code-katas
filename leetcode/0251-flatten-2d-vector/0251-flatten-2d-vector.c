typedef struct {
    int top;
    int capacity;
    int data[];
} Vector2D;

Vector2D* vector2DCreate(int** v, int vSize, int* vColSize) {
    int capacity = 0;
    for (int i = 0; i < vSize; i++) {
        capacity += vColSize[i];
    }
    
    Vector2D *vector = calloc(1, (sizeof(int) * capacity) + sizeof(Vector2D));
    
    for (int i = 0; i < vSize; i++) {
        for (int j = 0; j < vColSize[i]; j++) {
            vector->data[vector->capacity++] = v[i][j];
        }
    }
    
    return vector;
}

int vector2DNext(Vector2D* obj) {
    return obj->data[obj->top++];
}

bool vector2DHasNext(Vector2D* obj) {
    return obj->top != obj->capacity;
}

void vector2DFree(Vector2D* obj) {
    free(obj);
}
