import random
from ambulance import CityGraph, Ambulance, DispatchSystem  
from datetime import datetime

def make_random_graph(n_nodes=20, edge_prob=0.2, max_w=10):
    G = CityGraph()
    # explicitly create nodes so isolated nodes exist
    for i in range(n_nodes):
        G.add_node(i)

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < edge_prob:
                w = random.randint(1, max_w)
                G.add_edge(i, j, w)
    return G


def simulate(dispatch_system, n_incidents=50, node_range=None, seed=0):
    random.seed(seed)
    node_range = node_range or list(dispatch_system.graph.adj.keys())
    stats = {'assigned': 0, 'unreachable': 0, 'total_distance': 0.0}

    # ensure all ambulances are initially available
    dispatch_system.reset_ambulances(make_available=True)

    for _ in range(n_incidents):
        loc = random.choice(node_range)
        current_time = datetime.now()
        out = dispatch_system.assign_ambulance(loc, urgency=1, current_time=current_time, service_time_min=0.0)

        if out is None:
            stats['unreachable'] += 1
        else:
            amb, d_weight, travel_time_min = out
            stats['assigned'] += 1
            stats['total_distance'] += float(d_weight)
            # keep original synthetic behavior: immediate reuse
            amb.available_until = None
            amb.status = "Available"

    stats['avg_distance'] = (
        stats['total_distance'] / stats['assigned'] if stats['assigned'] else float('inf')
    )
    return stats

# This block runs the simulation when the script is executed
if __name__ == "__main__":
    print("Running random graph simulation...")
    random.seed(0)
    G_sim = make_random_graph(30, edge_prob=0.12)
    ambs_sim = [Ambulance(i, random.randrange(0, 30), avg_speed_kmph=40.0) for i in range(5)]
    ds_sim = DispatchSystem(G_sim, ambs_sim)
    
    stats = simulate(ds_sim, n_incidents=100)
    print(stats)