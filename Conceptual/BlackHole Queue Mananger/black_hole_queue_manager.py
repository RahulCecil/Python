import numpy as np
import time

class SingularityQueue:
    def __init__(self, capacity=100, gravity=0.5):
        self.capacity = capacity
        self.gravity = gravity
        self.tasks = []

    def get_event_horizon(self):
        # R shrinks as the queue density increases
        density = len(self.tasks)
        return self.capacity / (density + 1)

    def add_task(self, name, features):
        # features = [complexity, length, memory_req, etc.]
        initial_dist = np.linalg.norm(features)
        self.tasks.append({
            "name": name,
            "d_initial": initial_dist,
            "entry_time": time.time(),
            "features": features
        })

    def step(self):
        """Processes the queue by finding tasks that have crossed the horizon."""
        R = self.get_event_horizon()
        now = time.time()
        
        # Calculate current 'collapsed distance' S for all tasks
        for task in self.tasks:
            age = now - task["entry_time"]
            # S(t) = d - (G * t^2)
            task["S"] = task["d_initial"] - (self.gravity * (age**2))

        # Split tasks into 'Captured' and 'Accretion Disk'
        captured = [t for t in self.tasks if t["S"] <= R]
        accretion_disk = [t for t in self.tasks if t["S"] > R]

        # 1. Process Captured (The Event Horizon)
        # Small tasks zip through; heavy tasks eventually cross as S collapses.
        if captured:
            # Sort captured tasks so the 'closest' to singularity goes first
            captured.sort(key=lambda x: x["S"])
            processing = captured.pop(0)
            self.tasks = captured + accretion_disk
            return f"EXECUTING: {processing['name']} (Crossed R={R:.2f} with S={processing['S']:.2f})"

        # 2. Rearrange Accretion Disk (Optimization logic here)
        # We could sort the disk by feature similarity to optimize next steps
        self.tasks = accretion_disk
        return "STASIS: All tasks still in Accretion Disk."

# --- Usage ---
sq = SingularityQueue(capacity=50)
sq.add_task("Heavy_Compute", [40, 80]) # Far from origin
sq.add_task("Quick_Ping", [2, 1])      # Near origin

print(sq.step()) # Likely executes Quick_Ping immediately
