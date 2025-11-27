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

    # 1) explicitly add all nodes so isolated nodes exist
    for _, r in nodes_df.iterrows():
        nid = int(r.get("node_id", r.get("id")))
        G.add_node(nid)

    # 2) add edges (store edge_id so traffic can be applied later)
    for _, row in edges_df.iterrows():
        u = int(row.get("source_node", row.get("source", row.get("u"))))
        v = int(row.get("destination_node", row.get("destination", row.get("v"))))
        # prefer distance_km, else travel_time_min, else generic weight
        if "distance_km" in row.index and not pd.isna(row["distance_km"]):
            w = float(row["distance_km"])
        elif "travel_time_min" in row.index and not pd.isna(row["travel_time_min"]):
            w = float(row["travel_time_min"])
        else:
            w = float(row.get("weight", 1.0))

        edge_id = int(row["edge_id"]) if "edge_id" in row.index and not pd.isna(row["edge_id"]) else None
        # no time multiplier here — we'll apply time-based traffic when computing travel time
        G.add_edge(u, v, w, edge_id=edge_id)

        
    # --- 2. Create ambulances (time-aware) ---
    base_speed_kmph = 40.0
    ambs = []
    for _, row in ambulances_df.iterrows():
        aid = int(row.get("ambulance_id", row.get("id")))
        loc = int(row.get("current_node", row.get("current_location", row.get("node"))))
        # speed: either speed_factor multiplier or avg_speed_kmph directly
        if "speed_factor" in row.index and not pd.isna(row["speed_factor"]):
            avg_speed = float(row["speed_factor"]) * base_speed_kmph
        elif "avg_speed_kmph" in row.index and not pd.isna(row["avg_speed_kmph"]):
            avg_speed = float(row["avg_speed_kmph"])
        else:
            avg_speed = base_speed_kmph
        status = row.get("status", "Available")
        base_station = row.get("base_station", None)
        capacity = int(row.get("capacity", 1))
        ambs.append(Ambulance(aid, loc, avg_speed_kmph=avg_speed, capacity=capacity, base_station=base_station, status=status))

    # --- 3. Emergency time/service preprocessing ---
    def get_col(df, names, default=None):
        for n in names:
            if n in df.columns:
                return n
        return default

    time_col = get_col(emergencies_df, ["timestamp", "time", "call_time", "datetime"])
    service_col = get_col(emergencies_df, ["service_time_min", "service_time", "service_minutes"])

    if time_col:
        emergencies_df[time_col] = pd.to_datetime(emergencies_df[time_col], errors="coerce")
        emergencies_df = emergencies_df.sort_values(by=time_col).reset_index(drop=True)

    
    # --- 3. Create the DispatchSystem ---
    ds = DispatchSystem(G, ambs)

    # --- 4. Time-aware assignment loop + save results ---
    urgency_map = {
        "Critical": 4,
        "High": 3,
        "Moderate": 2,
        "Low": 1
    }

    results = []
    for _, row in emergencies_df.iterrows():
        # safe extraction of node and urgency
        incident_loc = int(row.get("location_node", row.get("location", row.get("node"))))
        urgency_str = str(row.get("urgency_level", "Low")).strip()
        urgency = urgency_map.get(urgency_str, 1)

        # determine current_time and service_time_min for this incident
        current_time = row[time_col] if time_col else datetime.now()
        service_time_min = 0.0
        if service_col and pd.notna(row.get(service_col)):
            try:
                service_time_min = float(row.get(service_col))
            except Exception:
                service_time_min = 0.0

        # attempt assignment (time-aware)
        assigned = ds.assign_ambulance(incident_loc, urgency, current_time=current_time, service_time_min=service_time_min)

        if not assigned:
            # keep a concise, single-line log (avoid huge prints)
            print(f"No ambulance found for location {incident_loc} with urgency {urgency}")
            results.append((row.get("emergency_id", None), None, None, None, None))
            continue

        amb, dist_weight, travel_time_min = assigned
        free_at = amb.available_until.strftime("%Y-%m-%d %H:%M:%S") if amb.available_until else None
        results.append((row.get("emergency_id", None), amb.aid, dist_weight, travel_time_min, free_at))

    # --- 5. Save results ---
    results_df = pd.DataFrame(results, columns=[
        "emergency_id", "ambulance_id", "distance_weight", "travel_time_min", "ambulance_free_at"
    ])
    out_file = f"assignments_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df.to_csv(out_file, index=False)
    print("Saved", out_file)
    print(results_df.head())

    
    # --- From your last cell ---
    print(emergencies_df[["location_node", "urgency_level"]].head())
    print("Sample test:", ds.assign_ambulance(1, 4))