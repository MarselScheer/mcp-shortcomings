from fastmcp import FastMCP
from pathlib import Path
from src.storage import AspectStore


class ShortcomingsServer:
    """MCP server for managing project aspects, features, and shortcomings."""

    def __init__(self, store: AspectStore | None = None) -> None:
        self.store = store or AspectStore(Path.home() / ".shortcomings")
        self.mcp = FastMCP("shortcomings")
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        def list_features(aspect_id: str) -> list[dict]:
            """List all features for a given aspect."""
            aspect = self.store.get_aspect(aspect_id)
            if not aspect:
                return []
            return [f.model_dump() for f in aspect.features]

        @self.mcp.tool()
        def list_shortcomings(aspect_id: str) -> list[dict]:
            """List all shortcomings for a given aspect."""
            aspect = self.store.get_aspect(aspect_id)
            if not aspect:
                return []
            return [s.model_dump() for s in aspect.shortcomings]


# Default instance
server = ShortcomingsServer()
mcp = server.mcp
