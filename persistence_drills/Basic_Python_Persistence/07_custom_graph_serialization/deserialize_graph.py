from graph import Graph

# Deserialize
graph = Graph.load_from_file("graph.json")

print("✅ Graph deserialized from graph.json:")
print("Nodes:", graph.nodes)
print("Edges:", graph.edges)
