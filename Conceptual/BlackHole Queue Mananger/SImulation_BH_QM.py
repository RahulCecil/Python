import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

class Task:
    def __init__(self, task_id, features):
        self.task_id = task_id
        # The n-dimensional coordinates (Complexity, Length, Memory, etc.)
        self.features = np.array(features)
        # Calculate initial distance from origin (the 'Mass')
        self.initial_dist = np.linalg.norm(self.features)
        self.entry_time = 0 
        self.finish_time = None
        self.wait_time = 0
        self.current_s = self.initial_dist

class SingularityQueue:
    def __init__(self, capacity=20, gravity=0.1):
        self.capacity = capacity  # The 'power' of the singularity
        self.gravity = gravity    # How fast age pulls tasks in
        self.tasks = []
        self.finished_tasks = []
        self.current_time = 0
        self.horizon_history = []

    def add_task(self, task):
        task.entry_time = self.current_time
        self.tasks.append(task)

    def get_event_horizon(self):
        # R = Capacity / (Number of tasks + 1)
        # Horizon shrinks when the system is crowded
        density = len(self.tasks)
        return self.capacity / (density + 1)

    def run_simulation(self):
        while self.tasks:
            R = self.get_event_horizon()
            self.horizon_history.append(R)
            
            # Update the 'collapsed distance' S for all tasks
            for task in self.tasks:
                age = self.current_time - task.entry_time
                # S(t) = d - (G * t^2)
                task.current_s = task.initial_dist - (self.gravity * (age**2))
            
            # Capture tasks that have crossed the horizon (S <= R)
            captured = [t for t in self.tasks if t.current_s <= R]
            
            if captured:
                # Of those inside the horizon, process the one closest to center
                captured.sort(key=lambda x: x.current_s)
                to_process = captured[0]
                
                # Update task stats
                to_process.finish_time = self.current_time
                to_process.wait_time = to_process.finish_time - to_process.entry_time
                self.finished_tasks.append(to_process)
                self.tasks.remove(to_process)
            
            # Step the simulation clock
            self.current_time += 1
            
            # Failsafe for infinite loops
            if self.current_time > 2000: break

# --- Execution Logic ---

# 1. Generate 50 Tasks (Mixture of Small and Large)
np.random.seed(42)
tasks_list = []
for i in range(50):
    if i < 20: 
        features = np.random.uniform(1, 15, 3) # Lightweight tasks
    else: 
        features = np.random.uniform(30, 100, 3) # Heavyweight tasks
    tasks_list.append(Task(f"ID-{i}", features))

# 2. Run the Queue
# Gravity 0.05 is 'gentle', making heavy tasks wait longer.
sq = SingularityQueue(capacity=35, gravity=0.05)
for t in tasks_list:
    sq.add_task(t)

sq.run_simulation()

# 3. Compile Results for Matplotlib
data = [{
    "ID": t.task_id,
    "Mass": t.initial_dist,
    "Wait": t.wait_time,
    "Order": i + 1
} for i, t in enumerate(sq.finished_tasks)]

df = pd.DataFrame(data)

# 4. Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Left Plot: Mass vs Execution Order
sc = ax1.scatter(df["Mass"], df["Order"], c=df["Wait"], cmap='magma', s=80)
plt.colorbar(sc, ax=ax1, label='Wait Time (Ticks)')
ax1.set_title("The Singularity Effect: Mass vs. Order")
ax1.set_xlabel("Initial Distance from Origin (Mass)")
ax1.set_ylabel("Execution Sequence")

# Right Plot: The Event Horizon over time
ax2.plot(sq.horizon_history, color='royalblue', label="Horizon Radius (R)")
ax2.set_title("Event Horizon Expansion Over Time")
ax2.set_xlabel("Simulation Ticks")
ax2.set_ylabel("Radius R")
ax2.fill_between(range(len(sq.horizon_history)), sq.horizon_history, alpha=0.2)

plt.tight_layout()
plt.show()
