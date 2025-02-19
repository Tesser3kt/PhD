from sage.all import *
from copy import deepcopy


class Quiver:
    def __init__(self):
        self.graph = dict()

    def add_vertex(self, n: int) -> None:
        if n in self.graph:
            return

        self.graph[n] = set()

    def add_edge(self, n: int, m: int) -> bool:
        if n not in self.graph or m not in self.graph:
            return False
        self.graph[n].add(m)
        return True

    def from_string(edges: str) -> "Quiver":
        quiver = Quiver()
        edges = edges.split(" ")
        for edge in edges:
            v_from, v_to = tuple(edge.split('->'))
            quiver.add_vertex(int(v_from))

            for v in v_to.split(","):
                quiver.add_vertex(int(v))
                if not quiver.add_edge(int(v_from), int(v)):
                    print(f"Error adding edge {v_from}->{v_to}.")
                    return None

        return quiver

    def reflect(self, n: int) -> "Quiver":
        if n not in self.graph:
            print(f"Vertex {n} not in quiver.")
            return None
        if len(self.graph[n]) > 0:
            print(f"Vertex {n} is not a sink.")

    def __getitem__(self, n: int) -> set[int]:
        return self.graph[n]

    def __repr__(self):
        """ So far only works for A_n. """
        for n in self.graph:
            edges_out = len(self.graph[n])
            edges_in = len([m for m in self.graph if n in self.graph[m]])
            if edges_in + edges_out == 1:
                start = n
                break

        drawn = set()
        next_ = start

        result = ""
        while next_:
            result += str(next_)
            drawn.add(next_)
            v = next_
            next_ = None
            for w in self.graph[v]:
                if w not in drawn:
                    next_ = w
                    result += " -> "
                    break

            if not next_:
                for n in self.graph:
                    if v in self.graph[n] and n not in drawn:
                        next_ = n
                        result += " <- "
                        break

        return result


q = Quiver.from_string("2->1 3->2 4->3 5->4")
