import numpy as np
import time
import heapq

class Task:
    def __init__(self, name, complexity, length):
        self.name = name
        self.coords = np.array([complexity, length])
        self.entry_time = time.time()
        
    def get_distance(self):
        # Euclidean distance from origin
        return np.linalg.norm(self.coords)

    def get_priority_score(self):
        # S = Distance / (Age^2 + 1) 
        # Lower score = Higher priority
        age = time.time() - self.entry_time
        return self.get_distance() / (age**2 + 1)

class BalancedQueue:
    def __init__(self, fast_track_radius=5.0):
        self.queue = []
        self.radius = fast_track_radius

    def add_task(self, task):
        score = task.get_priority_score()
        # Add to min-heap
        heapq.heappush(self.queue, (score, task))

    def process_next(self):
        if not self.queue:
            return None
        
        # We re-sort or re-heapify if we want to be truly dynamic, 
        # but for simplicity, we pop the current best
        score, task = heapq.heappop(self.queue)
        
        if task.get_distance() < self.radius:
            print(f"[FAST TRACK] Processing Small Task: {task.name}")
        else:
            print(f"[STRATEGY] Processing Heavy Task: {task.name} (Dist: {task.get_distance():.2f})")
        return task

# --- Execution ---
manager = BalancedQueue(fast_track_radius=10.0)

# A heavy task
manager.add_task(Task("BigData_Job", complexity=50, length=200))
# A small task
manager.add_task(Task("Ping_Check", complexity=1, length=2))

# The small task will always come out first because its distance is tiny
manager.process_next() 
manager.process_next()
