# mytool

`mytool` is a small prototype relationship graph DB for AI agents. It stores knowledge as nodes and directed relationships in SQLite and returns agent-friendly JSON from both the CLI and the optional MCP server.

## Design

### Data model

The schema intentionally has only two core tables:

- `nodes`: human-readable `key`, optional `label`, lightweight `kind`, and arbitrary JSON `props`.
- `edges`: directed `source -> type -> target` facts with arbitrary JSON `props`.

Relationship types are plain keys such as `uses`, `depends_on`, or `relation:causes`. If you want to describe a relationship type as knowledge, create a node with the same key and attach facts to it:

```bash
mytool add-node relation:uses --kind relation_type --label "uses"
mytool add-edge relation:uses description text:uses-definition --props '{"text":"source uses target"}'
```

### Choices and rationale

- **SQLite first**: easy to inspect, back up, embed, and run from MCP without operating a graph database.
- **Human-readable keys**: agents and humans can refer to `person:alice` or `paper:attention-is-all-you-need` without needing opaque IDs.
- **Multi-edges allowed**: there is no uniqueness constraint on `(source, type, target)`, so contradictory, time-scoped, or differently sourced facts can coexist.
- **Types are not forced into an ontology**: relationship types are strings, but can also be represented as normal nodes when metadata is useful.
- **JSON properties**: facts can carry confidence, source, timestamps, or extraction notes while the main schema stays simple.
- **JSON output shape**: reads return compact `nodes` and `edges` arrays that are easy for an AI agent to parse, quote, and feed into later tool calls.

## Install for development

```bash
python -m pip install -e .
```

Optional MCP support:

```bash
python -m pip install -e '.[mcp]'
```

## CLI examples

```bash
mytool --db graph.db add-node agent:alice --label Alice --props '{"role":"planner"}'
mytool --db graph.db add-node concept:graph-db --kind concept --label "Graph DB"
mytool --db graph.db add-edge agent:alice uses concept:graph-db --props '{"confidence":0.9}'
mytool --db graph.db find-edges --source agent:alice
mytool --db graph.db neighbors agent:alice --direction both --depth 2
mytool --db graph.db path agent:alice concept:graph-db --max-depth 4
```

All commands print JSON.

## MCP server

Run the MCP server with an optional database path:

```bash
MYTOOL_DB=graph.db mytool-mcp
```

Exposed tools:

- `add_node(key, label=None, kind="entity", props=None)`
- `add_edge(source, type, target, props=None, create_missing=True)`
- `find_edges(source=None, target=None, type=None, limit=100)`
- `neighbors(key, direction="both", depth=1, type=None, limit=100)`
- `path(source, target, max_depth=4, type=None)`

## Development

```bash
python -m pytest
```
