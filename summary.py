import pandas as pd
import matplotlib.pyplot as plt

# 1. Load your output CSV (edit file name if needed)
df = pd.read_csv(r"D:\projects\DAU_projects\SEM_1\DSA\assignments_output_20251127_214213.csv")

# ------------------ Plot 1: Ambulance Utilization ------------------
util = df['ambulance_id'].value_counts().sort_index()

plt.figure(figsize=(8,5))
util.plot(kind='bar')
plt.title("Ambulance Utilization (Dispatch Count)")
plt.xlabel("Ambulance ID")
plt.ylabel("Number of Dispatches")
plt.tight_layout()
plt.savefig("results/ambulance_utilization.png")
plt.close()

# ----------------- Plot 2: Emergency Hotspot -----------------------
em_df = pd.read_csv("Datasets/emergencies.csv")

hotspots = em_df['location_node'].value_counts().head(20)

plt.figure(figsize=(8,5))
hotspots.plot(kind='bar')
plt.title("Top 20 Emergency Hotspots (Nodes)")
plt.xlabel("Node ID")
plt.ylabel("Number of Emergencies")
plt.tight_layout()
plt.savefig("results/emergency_hotspots.png")
plt.close()

plt.figure(figsize=(8,5))
df['travel_time_min'].plot(kind='hist', bins=20)
plt.title("Distribution of Travel Times")
plt.xlabel("Travel Time (minutes)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("results/travel_time_distribution.png")
plt.close()

print("Saved: ambulance_utilization.png, emergency_hotspots.png and travel_time_distribution.png")