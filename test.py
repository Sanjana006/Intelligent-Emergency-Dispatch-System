from ambulance import CityGraph, Ambulance, DispatchSystem  # <-- UPDATED

if __name__ == "__main__":
    # Test 1
    G = CityGraph()
    G.add_edge(0, 1, 5)
    G.add_edge(1, 2, 3)
    ambs = [Ambulance(1, 0), Ambulance(2, 2)]
    ds = DispatchSystem(G, ambs)
    assert ds.assign_ambulance(1) is not None

    # Test 2
    G2 = CityGraph()
    G2.add_edge(0, 1, 2)
    ambs2 = [Ambulance(1, 2)]
    ds2 = DispatchSystem(G2, ambs2)
    assert ds2.assign_ambulance(0) is None

    # Test 3
    G3 = CityGraph()
    G3.add_edge(0, 1, 1)
    ambs3 = [Ambulance(1, 0), Ambulance(2, 0)]
    ds3 = DispatchSystem(G3, ambs3)
    assert ds3.assign_ambulance(1)[0].aid == 1

    print("unit tests passed")