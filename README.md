# 🚑 Intelligent Emergency Dispatch System

## 📘 Overview
The **Intelligent Emergency Dispatch System** simulates real-time ambulance assignment to emergencies in a city, aiming to **minimize response time** while efficiently handling **multiple emergencies and ambulance distributions**.  
The city is represented as a **weighted graph**, where:
- **Nodes** represent locations (e.g., hospitals, intersections, residential areas)
- **Edges** represent roads with associated travel times.

The system implements **three algorithmic versions** to analyze **space–time trade-offs**:

- **Version A:** Uses Heaps (Priority Queues) + Adjacency Lists with Dijkstra/BFS for nearest-ambulance selection.
- **Version B:** Uses Adjacency List + HashMap and Multi-Source Dijkstra for optimized global shortest-path updates.
- **Version C:** Uses k-d Tree / Range Tree for nearest-neighbor queries and local BFS/Dijkstra for regional pathfinding.

Each version is tested on synthetic city data and compared based on **runtime, memory usage, and average response time**, demonstrating how data structure design impacts real-world dispatch efficiency.

---

## 📂 Dataset Structure
This project uses **synthetic datasets** representing different aspects of the city and emergency dispatch system.  
Each dataset is stored as a `.csv` file for modular design and easy experimentation.

### **1️⃣ city_nodes.csv**
Represents all important locations in the simulated city.

| Attribute | Description |
|------------|-------------|
| **node_id** | Unique identifier for each location (integer). |
| **name** | Human-readable name of the location (e.g., “Hospital A”, “Sector 5”). |
| **latitude** | Latitude coordinate of the location. |
| **longitude** | Longitude coordinate of the location. |
| **type** | Type of location — e.g., `hospital`, `residential`, `commercial`, `intersection`. |

---

### **2️⃣ city_edges.csv**
Defines the road network connections between different city nodes.

| Attribute | Description |
|------------|-------------|
| **edge_id** | Unique identifier for each road segment. |
| **source_node** | Starting node of the road (refers to `node_id` from `city_nodes.csv`). |
| **destination_node** | Ending node of the road. |
| **distance_km** | Physical distance between nodes (in kilometers). |
| **travel_time_min** | Average travel time between the nodes under normal conditions (in minutes). |
| **road_condition** | Road status (e.g., `smooth`, `moderate`, `congested`). |

---

### **3️⃣ ambulance_locations.csv**
Represents the initial locations and capacities of ambulances available for dispatch.

| Attribute | Description |
|------------|-------------|
| **ambulance_id** | Unique identifier for each ambulance. |
| **current_node** | Current location of the ambulance (`node_id` from `city_nodes.csv`). |
| **status** | Current status — `available`, `on-duty`, `maintenance`. |
| **capacity** | Maximum number of patients that can be transported (usually 1–2). |
| **avg_speed_kmph** | Average speed of the ambulance (used to estimate response time). |

---

### **4️⃣ emergency_requests.csv**
Contains simulated emergency call data to test dispatch algorithms.

| Attribute | Description |
|------------|-------------|
| **emergency_id** | Unique identifier for each emergency event. |
| **timestamp** | Time of emergency occurrence. |
| **location_node** | Node ID of the emergency’s location. |
| **urgency_level** | Severity level of the emergency (`Low`, `Medium`, `High`, `Critical`). |
| **num_patients** | Number of patients involved. |
| **type_of_emergency** | Type of incident (e.g., `accident`, `cardiac arrest`, `fire injury`). |

---

### **5️⃣ hospital_data.csv**
Details about hospitals in the city where ambulances deliver patients.

| Attribute | Description |
|------------|-------------|
| **hospital_id** | Unique identifier for each hospital. |
| **node_id** | Node ID corresponding to the hospital’s location (`city_nodes.csv`). |
| **name** | Hospital name. |
| **available_beds** | Number of beds currently available for patients. |
| **emergency_capacity** | Maximum capacity for handling simultaneous emergencies. |
| **avg_treatment_time_min** | Average time taken for patient stabilization. |

---

### **6️⃣ traffic_conditions.csv**
Represents real-time or simulated dynamic traffic variations in the city.

| Attribute | Description |
|------------|-------------|
| **timestamp** | Time when traffic data was recorded. |
| **edge_id** | Road segment (`city_edges.csv`) affected by traffic. |
| **traffic_level** | Traffic intensity (`Low`, `Medium`, `High`). |
| **delay_factor** | Additional delay multiplier applied to `travel_time_min` based on traffic conditions. |

---

## ⚙️ Workflow Overview

1. **Data Generation:** Synthetic datasets (CSV files) are generated using Python.
2. **City Graph Construction:** Load `city_nodes.csv` and `city_edges.csv` to build a weighted graph.
3. **Algorithm Implementation:**
   - **Version A:** Dijkstra/BFS + Priority Queue.
   - **Version B:** Multi-Source Dijkstra with HashMaps.
   - **Version C:** k-d Tree for nearest-neighbor + local Dijkstra.
4. **Emergency Simulation:** Load `emergency_requests.csv` and assign ambulances dynamically.
5. **Performance Evaluation:** Compare algorithms using metrics:
   - Average response time
   - Memory usage
   - Computation time
6. **Visualization:** Use network plots and real-time dispatch animations (optional).

---

## 📊 Example Metrics
| Metric | Description |
|--------|--------------|
| **Avg Response Time** | Average time taken for an ambulance to reach the emergency. |
| **Memory Utilization** | Amount of memory consumed by each version. |
| **Computation Time** | Total runtime for processing all emergency requests. |

---

## 🧠 Key Learning Outcomes
- Understanding of **graph-based optimization** for real-world systems.
- Analysis of **data structure efficiency** under varying workloads.
- Insights into **space–time trade-offs** in algorithm design.
- Simulation of **real-time decision-making** in emergency services.

---

## 🧩 Technologies Used
- **Python 3.x**
- **Pandas**, **NumPy**, **NetworkX**, **Matplotlib**
- **Heapq / PriorityQueue**
- **Scikit-learn (for k-d Tree implementation)**

---

## 📁 Repository Structure
```bash
Intelligent-Emergency-Dispatch-System/
│
├── data/
│   ├── city_nodes.csv
│   ├── city_edges.csv
│   ├── ambulance_locations.csv
│   ├── emergency_requests.csv
│   ├── hospital_data.csv
│   └── traffic_conditions.csv
│
├── src/
│   ├── version_A_dijkstra.py
│   ├── version_B_multi_source.py
│   ├── version_C_kd_tree.py
│   └── utils.py
│
├── results/
│   ├── runtime_comparison.csv
│   └── response_time_analysis.png
│
├── README.md
└── requirements.txt
```
---

## 🧩 Developer Workflow & Setup

### 🧱 Branches
- **main** → stable, tested code  
- **dev** → integration branch for testing all versions  
- **aditya**, **urvi**, **sanjana** → personal working branches  

### ⚙️ Setup Instructions
1. Clone repository:
   ```bash
   git clone <repo_url>
   cd Intelligent-Emergency-Dispatch-System
---

---
## Create virtual environment:
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

---

## Install dependencies:
pip install -r requirements.txt

---

Run your version:
python src/version_A_dijkstra.py
 or version_B_multi_source.py / version_C_kd_tree.py

---

Push workflow:

git checkout aditya
git add .
git commit -m "Implemented Dijkstra version"
git push origin aditya

---

## 🧾 License
This project is open-source under the **MIT License** — free to use, modify, and distribute with attribution.

---
## ✨ Team Members
**Sanjana Nathani**  
🎓 M.Sc. Data Science | DAU, Gandhinagar  
📍 Vadodara, Gujarat, India  
📧 [sanjananathani06@gmailcom](mailto:sanjananathani06@gmail.com)

**Urvi Kava**  
🎓 M.Sc. Data Science | DAU, Gandhinagar  
📍 Vadodara, Gujarat, India  
📧 [urvikawa2004@gmailcom](mailto:urvikawa2004@gmail.com)

**Aditya Jana**  
🎓 M.Sc. Data Science | DAU, Gandhinagar  
📍 Vadodara, Gujarat, India  
📧 [adityajana20.6@gmailcom](mailto:adityajana20.6@gmail.com)

---

## 💡 Acknowledgments
Special thanks to open-source libraries and contributors that make simulation and data analysis possible — **NetworkX**, **Pandas**, **NumPy**, and **Matplotlib**.
