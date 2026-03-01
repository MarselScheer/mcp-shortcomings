import pytest
from fastmcp import FastMCP
from fastmcp.tools.tool import ToolResult
from mcp_server import ShortcomingsServer
from storage import AspectStore
from models import Aspect, Feature, Shortcoming, Criticality


@pytest.fixture
def mcp(tmp_path) -> FastMCP:
    """Fixture that provides an MCP instance extracted from ShortcomingServer."""
    store = AspectStore(tmp_path)
    server = ShortcomingsServer(store=store)
    return server.mcp


class TestToolsExist:
    @pytest.mark.anyio
    async def test_add_aspect_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "add_aspect" for tool in tools)

    @pytest.mark.anyio
    async def test_add_feature_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "add_feature" for tool in tools)

    @pytest.mark.anyio
    async def test_add_shortcoming_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "add_shortcoming" for tool in tools)


class TestToolsWithStore:
    @pytest.mark.anyio
    async def test_add_aspect_creates_new_aspect(self, tmp_path):
        """add_aspect should create a new aspect in the store."""
        store = AspectStore(tmp_path)
        server = ShortcomingsServer(store=store)

        result: ToolResult = await server.mcp.call_tool(
            "add_aspect",
            {
                "id": "new-aspect",
                "name": "New Aspect",
                "description": "A brand new aspect",
                "user_story": "As a user, I want this",
            },
        )

        # Verify the aspect was saved
        saved_aspect = store.get_aspect("new-aspect")
        assert saved_aspect is not None
        assert saved_aspect.id == "new-aspect"
        assert saved_aspect.name == "New Aspect"
        assert saved_aspect.description == "A brand new aspect"
        assert saved_aspect.user_story == "As a user, I want this"

        # Verify result indicates success
        assert result.structured_content.get("success") is True

    @pytest.mark.anyio
    async def test_add_feature_returns_error_for_nonexistent_aspect(self, tmp_path):
        """add_feature should return an error when aspect doesn't exist."""
        store = AspectStore(tmp_path)
        server = ShortcomingsServer(store=store)

        result: ToolResult = await server.mcp.call_tool(
            "add_feature",
            {
                "aspect_id": "nonexistent",
                "id": "new-feature",
                "title": "New Feature",
                "description": "A brand new feature",
            },
        )

        assert result.structured_content.get("success") is False
        assert "error" in result.structured_content

    @pytest.mark.anyio
    async def test_add_shortcoming_returns_error_for_nonexistent_aspect(self, tmp_path):
        """add_shortcoming should return an error when aspect doesn't exist."""
        store = AspectStore(tmp_path)
        server = ShortcomingsServer(store=store)

        result: ToolResult = await server.mcp.call_tool(
            "add_shortcoming",
            {
                "aspect_id": "nonexistent",
                "id": "new-shortcoming",
                "title": "New Shortcoming",
                "description": "A brand new shortcoming",
                "criticality": "high",
            },
        )

        assert result.structured_content.get("success") is False
        assert "error" in result.structured_content

    @pytest.mark.anyio
    async def test_add_shortcoming_adds_shortcoming_to_aspect(self, tmp_path):
        """add_shortcoming should add a new shortcoming to an existing aspect."""
        store = AspectStore(tmp_path)
        # First create an aspect
        aspect = Aspect(
            id="test-aspect",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test",
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)

        result: ToolResult = await server.mcp.call_tool(
            "add_shortcoming",
            {
                "aspect_id": "test-aspect",
                "id": "new-shortcoming",
                "title": "New Shortcoming",
                "description": "A brand new shortcoming",
                "criticality": "high",
            },
        )

        # Verify the shortcoming was added
        saved_aspect = store.get_aspect("test-aspect")
        assert saved_aspect is not None
        assert len(saved_aspect.shortcomings) == 1
        assert saved_aspect.shortcomings[0].id == "new-shortcoming"
        assert saved_aspect.shortcomings[0].title == "New Shortcoming"

        # Verify result indicates success
        assert result.structured_content.get("success") is True

    @pytest.mark.anyio
    async def test_add_feature_adds_feature_to_aspect(self, tmp_path):
        """add_feature should add a new feature to an existing aspect."""
        store = AspectStore(tmp_path)
        # First create an aspect
        aspect = Aspect(
            id="test-aspect",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test",
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)

        result: ToolResult = await server.mcp.call_tool(
            "add_feature",
            {
                "aspect_id": "test-aspect",
                "id": "new-feature",
                "title": "New Feature",
                "description": "A brand new feature",
            },
        )

        # Verify the feature was added
        saved_aspect = store.get_aspect("test-aspect")
        assert saved_aspect is not None
        assert len(saved_aspect.features) == 1
        assert saved_aspect.features[0].id == "new-feature"
        assert saved_aspect.features[0].title == "New Feature"
        assert saved_aspect.features[0].description == "A brand new feature"

        # Verify result indicates success
        assert result.structured_content.get("success") is True
