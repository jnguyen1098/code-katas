#define MIN(x,y)(x > y ? y : x)
#define INFINITY 1000000
int coinChange(int *coins, int coinsSize, int amount)
{
    int *dp = malloc(sizeof(int) * (amount + 1));
    for (int i = 0; i < amount + 1; i++) dp[i] = INFINITY;
    dp[0] = 0;
    
    for (int i = 0; i < coinsSize; i++) {
        for (int j = coins[i]; j < amount + 1; j++) {
            dp[j] = MIN(dp[j], dp[j - coins[i]] + 1);
        }
    }
    
    return dp[amount] != INFINITY ? dp[amount] : -1;
}
