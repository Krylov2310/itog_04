import math
# from typing import List, Dict, Any, Tuple, Optional
from point import *


class DeliveryGraph:
    def __init__(self):
        self.nodes: Dict[str, DeliveryPoint] = {}
        self.edges: Dict[Tuple[str, str], Dict[str, float]] = {}

    def add_node(self, point: DeliveryPoint):
        self.nodes[point.name] = point

    @staticmethod
    def calculate_distance(p1: DeliveryPoint, p2: DeliveryPoint) -> float:
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    def build_edges(self, speed_kmh: float = 60.0, cost_per_km: float = 15.0):
        for name1, p1 in self.nodes.items():
            for name2, p2 in self.nodes.items():
                if name1 == name2:
                    continue
                dist = self.calculate_distance(p1, p2)
                time = dist / speed_kmh
                cost = dist * cost_per_km
                self.edges[(name1, name2)] = {
                    'distance': dist,
                    'time': time,
                    'cost': cost
                }
                self.edges[(name2, name1)] = {
                    'distance': dist,
                    'time': time,
                    'cost': cost
                }

    def get_edge(self, u: str, v: str, weight_type: str) -> Optional[float]:
        if (u, v) in self.edges:
            return self.edges[(u, v)].get(weight_type)
        return None
