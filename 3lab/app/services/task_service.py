import random
from app.schemas.Graphs import Graph, ACO


def solve_tsp(nodes, edges):
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    size = len(nodes)
    adj_matrix = [[float('inf')] * size for _ in range(size)]

    for u, v in edges:
        i = node_to_index[u]
        j = node_to_index[v]
        adj_matrix[i][j] = 1.0
        adj_matrix[j][i] = 1.0

    graph = Graph(adj_matrix)
    aco = ACO(ant_count=10, generations=150, alpha=1.0, beta=2.0, rho=0.5, Q=100)

    path, cost = aco.solve(graph)
    if not path:
        raise Exception("No valid path found")

    node_path = [nodes[i] for i in path]
    total_distance = len(node_path)

    return {
        "path": node_path,
        "total_distance": float(total_distance),
        "task_id": self.request.id
    }