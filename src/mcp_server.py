import os
from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult
from pathlib import Path
from storage import AspectStore
from models import Aspect, Feature, Shortcoming, Criticality


class ShortcomingsServer:
    """MCP server for managing project aspects, features, and shortcomings."""

    def __init__(self, store: AspectStore | None = None) -> None:
        self.store = store or AspectStore()
        self.mcp = FastMCP("shortcomings")
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        def list_aspects() -> ToolResult:
            """List all available aspects (without nested features/shortcomings).

            Use this to discover available aspects first, then use list_features
            or list_shortcomings with a specific aspect_id to dive deeper.
            """
            aspects = self.store.list_aspects()
            return ToolResult(
                structured_content={
                    "aspects": [
                        {
                            "id": a.id,
                            "name": a.name,
                            "description": a.description,
                            "user_story": a.user_story,
                        }
                        for a in aspects
                    ]
                }
            )

        @self.mcp.tool()
        def list_features(aspect_id: str) -> ToolResult:
            """List all features for a given aspect."""
            aspect = self.store.get_aspect(aspect_id)
            if not aspect:
                return ToolResult(structured_content={"features": []})
            return ToolResult(
                structured_content={
                    "features": [f.model_dump() for f in aspect.features]
                }
            )

        @self.mcp.tool()
        def list_shortcomings(aspect_id: str) -> ToolResult:
            """List all shortcomings for a given aspect."""
            aspect = self.store.get_aspect(aspect_id)
            if not aspect:
                return ToolResult(structured_content={"shortcomings": []})
            return ToolResult(
                structured_content={
                    "shortcomings": [s.model_dump() for s in aspect.shortcomings]
                }
            )

        @self.mcp.tool()
        def add_aspect(
            id: str, name: str, description: str, user_story: str
        ) -> ToolResult:
            """Add a new aspect to the store.

            Args:
                id: Unique identifier for the aspect
                name: Display name of the aspect
                description: Brief description of the aspect
                user_story: User story for this aspect
            """
            aspect = Aspect(
                id=id,
                name=name,
                description=description,
                user_story=user_story,
            )
            self.store.save_aspect(aspect)
            return ToolResult(structured_content={"success": True, "id": id})

        @self.mcp.tool()
        def add_feature(
            aspect_id: str, id: str, title: str, description: str
        ) -> ToolResult:
            """Add a new feature to an existing aspect.

            Args:
                aspect_id: ID of the aspect to add the feature to
                id: Unique identifier for the feature
                title: Display title of the feature
                description: Brief description of the feature
            """
            aspect = self.store.get_aspect(aspect_id)
            if aspect is None:
                return ToolResult(
                    structured_content={
                        "success": False,
                        "error": f"Aspect {aspect_id} not found",
                    }
                )
            aspect.features.append(Feature(id=id, title=title, description=description))
            self.store.save_aspect(aspect)
            return ToolResult(structured_content={"success": True})

        @self.mcp.tool()
        def add_shortcoming(
            aspect_id: str, id: str, title: str, description: str, criticality: str
        ) -> ToolResult:
            """Add a new shortcoming to an existing aspect.

            Args:
                aspect_id: ID of the aspect to add the shortcoming to
                id: Unique identifier for the shortcoming
                title: Display title of the shortcoming
                description: Brief description of the shortcoming
                criticality: Criticality level (low, medium, high, critical)
            """
            aspect = self.store.get_aspect(aspect_id)
            if aspect is None:
                return ToolResult(
                    structured_content={
                        "success": False,
                        "error": f"Aspect {aspect_id} not found",
                    }
                )
            aspect.shortcomings.append(
                Shortcoming(
                    id=id,
                    title=title,
                    description=description,
                    criticality=Criticality(criticality),
                )
            )
            self.store.save_aspect(aspect)
            return ToolResult(structured_content={"success": True})


# Default instance
server = ShortcomingsServer()
mcp = server.mcp

if __name__ == "__main__":
    mcp.run()
