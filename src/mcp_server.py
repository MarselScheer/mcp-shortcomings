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
        def list_aspects() -> list[dict]:
            """List all available aspects (without nested features/shortcomings).


            Use this to discover available aspects first, then use list_features
            or list_shortcomings with a specific aspect_id to dive deeper.
            """
            aspects = self.store.list_aspects()
            return [
                {
                    "id": a.id,
                    "name": a.name,
                    "description": a.description,
                    "user_story": a.user_story,
                }
                for a in aspects
            ]

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
