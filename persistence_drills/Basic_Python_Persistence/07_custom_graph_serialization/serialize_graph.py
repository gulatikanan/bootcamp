"""Module: serialize.py
Author: Kanan"""

from graph import Graph

graph = Graph()
graph.add_node("A")
graph.add_node("B")
graph.add_edge("A", "B")

# Serialize
graph.save_to_file("graph.json")

print("✅ Graph serialized to graph.json")
