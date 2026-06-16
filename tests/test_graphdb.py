from mytool import GraphDB


def test_nodes_edges_and_edge_search():
    db = GraphDB()
    db.add_node("agent:alice", "Alice", props={"role": "planner"})
    db.add_node("concept:graph-db", "Graph DB", kind="concept")

    edge1 = db.add_edge("agent:alice", "uses", "concept:graph-db", {"confidence": 0.9})
    edge2 = db.add_edge("agent:alice", "likes", "concept:graph-db")

    assert edge1["type"] == "uses"
    assert edge2["id"] != edge1["id"]
    found = db.find_edges(source="agent:alice", target="concept:graph-db")
    assert found["count"] == 2


def test_neighbors_support_depth_and_direction():
    db = GraphDB()
    db.add_edge("a", "knows", "b")
    db.add_edge("b", "knows", "c")
    db.add_edge("x", "knows", "a")

    subgraph = db.neighbors("a", direction="out", depth=2)

    assert {node["key"] for node in subgraph["nodes"]} == {"a", "b", "c"}
    assert [edge["source"] for edge in subgraph["edges"]] == ["a", "b"]


def test_path_finds_shortest_directed_route():
    db = GraphDB()
    db.add_edge("a", "rel", "b")
    db.add_edge("b", "rel", "c")
    db.add_edge("a", "rel", "c")

    result = db.path("a", "c")

    assert result["found"] is True
    assert result["length"] == 1
    assert [edge["target"] for edge in result["edges"]] == ["c"]


def test_path_returns_not_found():
    db = GraphDB()
    db.add_node("a")
    db.add_node("z")

    result = db.path("a", "z")

    assert result == {"found": False, "nodes": [], "edges": [], "length": None}
