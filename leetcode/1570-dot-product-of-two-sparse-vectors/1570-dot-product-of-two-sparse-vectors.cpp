class SparseVector {
public:
    unordered_map<int, int> _vec;
    
    SparseVector(vector<int> &nums) {
        for (int i = 0; i < nums.size(); i++) {
            _vec[i] = nums[i];
        }
    }
    
    // Return the dotProduct of two sparse vectors
    int dotProduct(SparseVector& vec) {
        int prod = 0;
        int n = vec._vec.size();
        
        for (int i = 0; i < n; i++) {
            if (_vec.find(i) != _vec.end()) {
                prod += vec._vec[i] * _vec[i];
            }
        }
        
        return prod;
    }
    
};
