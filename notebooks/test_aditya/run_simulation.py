import random
from ambulance import CityGraph, Ambulance, DispatchSystem  # <-- UPDATED

def make_random_graph(n_nodes=20, edge_prob=0.2, max_w=10):
    G = CityGraph()
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
    for amb in dispatch_system.ambulances:
        amb.available = True
    for _ in range(n_incidents):
        loc = random.choice(node_range)
        out = dispatch_system.assign_ambulance(loc, urgency=1)
        if out is None:
            stats['unreachable'] += 1
        else:
            amb, d = out
            stats['assigned'] += 1
            stats['total_distance'] += d
            amb.available = True  # This was in your original simulate function
    stats['avg_distance'] = (
        stats['total_distance'] / stats['assigned'] if stats['assigned'] else float('inf')
    )
    return stats

# This block runs the simulation when the script is executed
if __name__ == "__main__":
    print("Running random graph simulation...")
    random.seed(0)
    G_sim = make_random_graph(30, edge_prob=0.12)
    ambs_sim = [Ambulance(i, random.randrange(0, 30)) for i in range(5)]
    ds_sim = DispatchSystem(G_sim, ambs_sim)
    
    stats = simulate(ds_sim, n_incidents=100)
    print(stats)