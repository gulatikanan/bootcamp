"""Module: graph.py
Author: Kanan"""

import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, source, target):
        self.edges.append((source, target))

    def to_dict(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        graph = cls()
        graph.nodes = data["nodes"]
        graph.edges = data["edges"]
        return graph
