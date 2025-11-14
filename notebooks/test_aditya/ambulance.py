import heapq
from collections import defaultdict
import random

class CityGraph:
    def __init__(self):
        self.adj = defaultdict(list)  # node -> list of (neighbor, weight)

    def add_edge(self, u, v, w):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

class Ambulance:
    def __init__(self, aid, location):
        self.aid = aid
        self.location = location
        self.available = True

class DispatchSystem:
    def __init__(self, graph, ambulances):
        self.graph = graph
        self.ambulances = ambulances

    def _dijkstra_all_from(self, src):
        pq = [(0, src)]
        dist = {src: 0}
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist.get(u, float('inf')):
                continue
            for v, w in self.graph.adj.get(u, ()):
                nd = d + w
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    def assign_ambulance(self, incident_loc, urgency=1):
        dist_from_incident = self._dijkstra_all_from(incident_loc)
        best = None
        for amb in self.ambulances:
            if not amb.available:
                continue
            d = dist_from_incident.get(amb.location, float('inf'))
            if d == float('inf'):
                continue
            pr = (-urgency, d, amb.aid)
            if best is None or pr < best[0]:
                best = (pr, amb, d)
        if best is None:
            return None
        _, amb, d = best
        amb.available = False
        return amb, d