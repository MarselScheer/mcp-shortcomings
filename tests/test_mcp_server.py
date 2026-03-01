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
    async def test_list_features_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_features" for tool in tools)

    @pytest.mark.anyio
    async def test_list_shortcomings_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_shortcomings" for tool in tools)

    @pytest.mark.anyio
    async def test_list_aspects_tool_exists(self, mcp):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_aspects" for tool in tools)

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
    async def test_list_aspects_returns_aspects_without_nested_data(self, tmp_path):
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test",
        )
        aspect.features.append(
            Feature(id="f1", title="Feature 1", description="desc 1")
        )
        aspect.shortcomings.append(
            Shortcoming(
                id="s1",
                title="Shortcoming 1",
                description="desc 1",
                criticality=Criticality.HIGH,
            )
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result: ToolResult = await server.mcp.call_tool("list_aspects", {})

        # Access via structured_content (dict wrapper)
        aspects = result.structured_content["aspects"]

        # Verify aspect metadata is returned
        assert len(aspects) == 1
        assert aspects[0]["id"] == "test"
        assert aspects[0]["name"] == "Test Aspect"
        assert aspects[0]["description"] == "test description"
        assert aspects[0]["user_story"] == "As a user, I want test"

        # Verify nested features/shortcomings are NOT included
        assert "features" not in aspects[0]
        assert "shortcomings" not in aspects[0]

    @pytest.mark.anyio
    async def test_list_features_returns_features(self, tmp_path):
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test",
        )
        aspect.features.append(
            Feature(id="f1", title="Feature 1", description="desc 1")
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result: ToolResult = await server.mcp.call_tool(
            "list_features", {"aspect_id": "test"}
        )
        features = result.structured_content["features"]
        assert any(f["title"] == "Feature 1" for f in features)

    @pytest.mark.anyio
    async def test_list_shortcomings_returns_shortcomings(self, tmp_path):
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test2",
            name="Test Aspect 2",
            description="test description",
            user_story="As a user, I want test",
        )
        aspect.shortcomings.append(
            Shortcoming(
                id="s1",
                title="Shortcoming 1",
                description="desc 1",
                criticality=Criticality.HIGH,
            )
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result: ToolResult = await server.mcp.call_tool(
            "list_shortcomings", {"aspect_id": "test2"}
        )
        shortcomings = result.structured_content["shortcomings"]
        assert any(s["title"] == "Shortcoming 1" for s in shortcomings)

    @pytest.mark.anyio
    async def test_list_features_returns_toolresult_with_structured_content(
        self, tmp_path
    ):
        """list_features should return ToolResult with structured_content like list_aspects."""
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test",
        )
        aspect.features.append(
            Feature(id="f1", title="Feature 1", description="desc 1")
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result: ToolResult = await server.mcp.call_tool(
            "list_features", {"aspect_id": "test"}
        )

        # Should use structured_content like list_aspects does
        features = result.structured_content["features"]
        assert len(features) == 1
        assert features[0]["title"] == "Feature 1"

    @pytest.mark.anyio
    async def test_list_shortcomings_returns_toolresult_with_structured_content(
        self, tmp_path
    ):
        """list_shortcomings should return ToolResult with structured_content like list_aspects."""
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test2",
            name="Test Aspect 2",
            description="test description",
            user_story="As a user, I want test",
        )
        aspect.shortcomings.append(
            Shortcoming(
                id="s1",
                title="Shortcoming 1",
                description="desc 1",
                criticality=Criticality.HIGH,
            )
        )
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result: ToolResult = await server.mcp.call_tool(
            "list_shortcomings", {"aspect_id": "test2"}
        )

        # Should use structured_content like list_aspects does
        shortcomings = result.structured_content["shortcomings"]
        assert len(shortcomings) == 1
        assert shortcomings[0]["title"] == "Shortcoming 1"

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
