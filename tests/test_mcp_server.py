import json
import pytest
from fastmcp.tools.tool import ToolResult
from src.mcp_server import mcp, ShortcomingsServer
from src.storage import AspectStore
from src.models import Aspect, Feature, Shortcoming, Criticality


class TestShortcomingsServerClass:
    def test_shortcomings_server_class_exists(self):
        assert ShortcomingsServer is not None

    def test_mcp_instance_exists(self):
        assert mcp is not None
        assert mcp.name == "shortcomings"


class TestToolsExist:
    @pytest.mark.anyio
    async def test_list_features_tool_exists(self):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_features" for tool in tools)

    @pytest.mark.anyio
    async def test_list_shortcomings_tool_exists(self):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_shortcomings" for tool in tools)

    @pytest.mark.anyio
    async def test_list_aspects_tool_exists(self):
        tools = await mcp.list_tools()
        assert any(tool.name == "list_aspects" for tool in tools)


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

        # Parse the JSON response
        aspects = json.loads(result.content[0].text)

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
        features = json.loads(result.content[0].text)
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
        shortcomings = json.loads(result.content[0].text)
        assert any(s["title"] == "Shortcoming 1" for s in shortcomings)
