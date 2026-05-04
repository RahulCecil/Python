from functools import lru_cache

# Without @lru_cache, fib(40) takes ages.
# With it, it's nearly instantaneous.
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(40))
