import networkx as nx
import random

class LogisticsNetwork:
    def __init__(self, num_nodes=20):
        # Create a realistic "Scale-Free" graph (like airline hubs)
        self.graph = nx.scale_free_graph(num_nodes, seed=42)
        self.graph = nx.DiGraph(self.graph)
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))
        
        # Add Physics to links
        for u, v in self.graph.edges():
            self.graph[u][v]['cost'] = random.randint(50, 500)
            self.graph[u][v]['capacity'] = random.randint(100, 1000)

    def get_route_context(self, path):
        total_cost = 0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            if self.graph.has_edge(u, v):
                total_cost += self.graph[u][v]['cost']
        
        return {'total_cost': total_cost}

    def find_random_route(self):
        try:
            nodes = list(self.graph.nodes())
            start = random.choice(nodes)
            end = random.choice(nodes)
            if start == end: return None
            return nx.shortest_path(self.graph, start, end)
        except:
            return None