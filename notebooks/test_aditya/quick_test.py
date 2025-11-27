from ambulance import DispatchSystem, CityGraph, Ambulance
G = CityGraph(); G.add_node(0); G.add_node(1); G.add_edge(0,1,12.0)
amb = Ambulance(1,0,avg_speed_kmph=60)
ds = DispatchSystem(G, [amb])
print(ds.compute_travel_time_min(12.0, amb))
