import pandas as pd
from datetime import datetime
from ambulance import CityGraph, Ambulance, DispatchSystem  # <-- UPDATED

if __name__ == "__main__":
    
    # --- 1. Load data and build the graph ---
    base_path = r"D:\projects\DAU_projects\SEM_1\DSA\Datasets"

    nodes_df = pd.read_csv(fr"{base_path}\nodes.csv")
    edges_df = pd.read_csv(fr"{base_path}\edges.csv")
    ambulances_df = pd.read_csv(fr"{base_path}\ambulances.csv")
    traffic_df = pd.read_csv(fr"{base_path}\traffic.csv")
    emergencies_df = pd.read_csv(fr"{base_path}\emergencies.csv")

    # Create the graph 
    G = CityGraph()
    for _, row in edges_df.iterrows():
        u = int(row["source_node"])
        v = int(row["destination_node"])
        w = float(row["distance_km"])  # or use travel_time_min if you prefer time-based weight

        # apply traffic multiplier if available
        traffic_factor = 1.0
        if "travel_time_multiplier" in traffic_df.columns and "edge_id" in traffic_df.columns:
            match = traffic_df[traffic_df["edge_id"] == row["edge_id"]]
            if not match.empty:
                traffic_factor = float(match["travel_time_multiplier"].iloc[0])

        G.add_edge(u, v, w * traffic_factor)
        
    # --- 2. Create ambulances ---
    ambs = [
        Ambulance(int(row["ambulance_id"]), int(row["current_node"]))
        for _, row in ambulances_df.iterrows()
    ]
    
    # --- 3. Create the DispatchSystem ---
    ds = DispatchSystem(G, ambs)

    # --- 4. Assign ambulances to real emergencies ---
    # Defined using urgency mapping
    urgency_map = {
        "Critical": 4,
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }

    results = []
    for _, row in emergencies_df.iterrows():
        incident_loc = int(row["location_node"])
        urgency_str = str(row["urgency_level"]).strip()
        urgency = urgency_map.get(urgency_str, 1)  # default to Low if not found

        assigned = ds.assign_ambulance(incident_loc, urgency)
        if not assigned:
            print(f"No ambulance found for location {incident_loc} with urgency {urgency}")


        if assigned:
            amb, dist = assigned
            results.append((row["emergency_id"], amb.aid, dist))
        else:
            results.append((row["emergency_id"], None, None))

    # Save results
    results_df = pd.DataFrame(results, columns=["emergency_id", "ambulance_id", "distance"])

    # --- 5. Save or analyze results ---
    results_df.to_csv(f"assignments_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)
    print("Saved assignments_output.csv")
    print(results_df.head())
    
    # --- From your last cell ---
    print(emergencies_df[["location_node", "urgency_level"]].head())
    print("Sample test:", ds.assign_ambulance(1, 4))