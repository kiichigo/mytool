from __future__ import annotations

import os
from typing import Any

from .graphdb import GraphDB

DB_PATH = os.environ.get("MYTOOL_DB", "graph.db")
_db = GraphDB(DB_PATH)


def add_node(key: str, label: str | None = None, kind: str = "entity", props: dict[str, Any] | None = None) -> dict[str, Any]:
    """Create or update a node identified by a human-readable key."""
    return _db.add_node(key, label, kind, props)


def add_edge(source: str, type: str, target: str, props: dict[str, Any] | None = None, create_missing: bool = True) -> dict[str, Any]:
    """Create a directed edge. Multiple edges between the same nodes are allowed."""
    return _db.add_edge(source, type, target, props, create_missing)


def find_edges(source: str | None = None, target: str | None = None, type: str | None = None, limit: int = 100) -> dict[str, Any]:
    """Search relationships by source, target, and/or relationship type."""
    return _db.find_edges(source, target, type, limit)


def neighbors(key: str, direction: str = "both", depth: int = 1, type: str | None = None, limit: int = 100) -> dict[str, Any]:
    """Return a JSON subgraph around a node."""
    return _db.neighbors(key, direction, depth, type, limit)


def path(source: str, target: str, max_depth: int = 4, type: str | None = None) -> dict[str, Any]:
    """Find a shortest directed path between two nodes."""
    return _db.path(source, target, max_depth, type)


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("Install MCP support with: pip install 'mytool[mcp]' or pip install mcp") from exc

    mcp = FastMCP("mytool-graphdb")
    for tool in (add_node, add_edge, find_edges, neighbors, path):
        mcp.tool()(tool)
    mcp.run()


if __name__ == "__main__":
    main()
