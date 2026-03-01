"""Main entry point for the MCP server.

This module provides the primary entry point for running the
shortcomings MCP server.
"""

from storage import AspectStore
from mcp_server import ShortcomingsServer


def main() -> None:
    """Run the MCP server."""
    server = ShortcomingsServer(AspectStore())
    server.mcp.run()


if __name__ == "__main__":
    main()
