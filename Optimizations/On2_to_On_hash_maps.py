# Bruteforce Approach: O(n^2) Time
def slow_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# Optimized Approach: O(n) Time
def fast_sum(nums, target):
    lookup = {} # Space: O(n)
    for i, num in enumerate(nums):
        needed = target - num
        if needed in lookup:
            return [lookup[needed], i]
        lookup[num] = i
    return None

# Trade-off: We reduce Time Complexity significantly by slightly increasing Space Complexity (storing the dictionary).
