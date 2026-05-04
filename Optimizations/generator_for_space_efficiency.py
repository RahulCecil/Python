import sys

# List Comprehension: O(n) Space
big_list = [i**2 for i in range(1000000)]
print(f"List size: {sys.getsizeof(big_list)} bytes") 

# Generator Expression: O(1) Space
big_gen = (i**2 for i in range(1000000))
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")
