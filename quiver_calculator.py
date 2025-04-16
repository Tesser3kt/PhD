import networkx as nx
import matplotlib.pyplot as plt
from sage.all import *
from copy import deepcopy


class Quiver:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_vertex(self, n: int) -> None:
        self.graph.add_node(n)

    def add_edge(self, n: int, m: int) -> None:
        self.graph.add_edge(n, m)

    def from_string(edges: str) -> "Quiver":
        quiver = Quiver()
        edges = edges.split(" ")
        for edge in edges:
            v_from, v_to = tuple(edge.split('->'))
            quiver.add_edge(int(v_from), int(v_to))

            for v in v_to.split(","):
                quiver.add_edge(int(v_from), int(v))

        return quiver

    def reflect(self, n: int) -> "Quiver":
        if n not in self.graph:
            print(f"Vertex {n} not in quiver.")
            return None
        if self.graph.out_degree[n] > 0:
            print(f"Vertex {n} not a sink.")
            return None

        q = deepcopy(self)
        preds = list(q.graph.predecessors(n))
        for ngh in preds:
            q.graph.remove_edge(ngh, n)
            q.graph.add_edge(n, ngh, color="r")

        return q

    def linear(n: int) -> "Quiver":
        """ Returns A_n linearly oriented (1 is the sink). """
        return Quiver.from_string(
            " ".join([f"{i+1}->{i}" for i in range(1, n)])
        )

    def __getitem__(self, n: int) -> set[int]:
        return self.graph[n]


q = Quiver.linear(10)
q2 = q.reflect(1)
nx.draw_spring(q2.graph, with_labels=True)
plt.savefig('quiver.png', dpi=300)
