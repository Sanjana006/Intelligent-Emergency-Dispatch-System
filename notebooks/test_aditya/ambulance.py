import heapq
from collections import defaultdict
import random

class CityGraph:
    def __init__(self):
        self.adj = defaultdict(list)  # node -> list of (neighbor, weight)

    def add_node(self, u):
        # ensure a node key exists even if it has no edges
        _ = self.adj[u]

    def add_edge(self, u, v, w, edge_id=None):
        self.adj[u].append((v, w, edge_id))
        self.adj[v].append((u, w, edge_id))

    def neighbors(self, u):
        return self.adj.get(u, [])

class Ambulance:
    def __init__(self, aid, location, avg_speed_kmph=40.0, capacity=1, base_station=None, status="Available"):
        self.aid = int(aid)
        self.location = int(location)
        self.avg_speed_kmph = float(avg_speed_kmph) if avg_speed_kmph is not None else 40.0
        self.capacity = int(capacity)
        self.base_station = base_station
        self.status = status  # "Available", "OnDuty", "Unavailable"
        self.available_until = None  # datetime until which ambulance is busy

    def is_available_at(self, when):
        if self.status and str(self.status).lower() in ("unavailable", "out_of_service"):
            return False
        if self.available_until is None:
            return True
        return when >= self.available_until

    def __repr__(self):
        return f"Ambulance(aid={self.aid}, loc={self.location}, speed={self.avg_speed_kmph}, until={self.available_until})"


class DispatchSystem:
    def __init__(self, graph, ambulances):
        self.graph = graph
        self.ambulances = ambulances

    def _dijkstra_all_from(self, src):
        pq = [(0.0, src)]
        dist = {src: 0.0}
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist.get(u, float('inf')):
                continue
            # neighbors stored as (v, w, edge_id)
            for v, w, _edge_id in self.graph.neighbors(u):
                nd = d + float(w)
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist


    def assign_ambulance(self, incident_loc, urgency=1, current_time=None, service_time_min=0.0, treat_weight_as="distance_km"):
        """
        Minimal time-aware assign:
        - current_time defaults to now() if not provided.
        - service_time_min used to set available_until = current_time + travel + service.
        Returns (ambulance, distance_weight, travel_time_min) or None.
        """
        from datetime import datetime, timedelta
        if current_time is None:
            current_time = datetime.now()

        dist_from_incident = self._dijkstra_all_from(incident_loc)
        best = None
        for amb in self.ambulances:
            # use the new is_available_at check
            if not amb.is_available_at(current_time):
                continue

            d_weight = dist_from_incident.get(amb.location, float('inf'))
            if d_weight == float('inf'):
                continue

            pr = (-int(urgency), float(d_weight), int(amb.aid))
            if best is None or pr < best[0]:
                best = (pr, amb, d_weight)

        if best is None:
            return None

        _, amb, d_weight = best

        travel_time_min = self.compute_travel_time_min(d_weight, amb, treat_weight_as=treat_weight_as)
        total_busy_min = travel_time_min + float(service_time_min)

        amb.available_until = current_time + timedelta(minutes=total_busy_min)
        amb.location = int(incident_loc)
        amb.status = "OnDuty"

        return amb, d_weight, travel_time_min

    
    def compute_travel_time_min(self, distance_or_weight, amb: Ambulance, treat_weight_as="distance_km"):
        if treat_weight_as == "travel_time_min":
          return float(distance_or_weight)
        speed = amb.avg_speed_kmph if amb.avg_speed_kmph > 0 else 40.0
        travel_min = (float(distance_or_weight) / speed) * 60.0
        return travel_min
    
        
    def reset_ambulances(self, make_available=True):
        """
        Utility: reset ambulance statuses for tests or synthetic runs.
        If make_available=True, clears available_until and sets status to 'Available'.
        """
        for amb in self.ambulances:
            if make_available:
                amb.status = "Available"
                amb.available_until = None

