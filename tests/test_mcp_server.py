import pytest
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


class TestToolsWithStore:
    @pytest.mark.anyio
    async def test_list_features_returns_features(self, tmp_path):
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test",
            name="Test Aspect",
            description="test description",
            user_story="As a user, I want test"
        )
        aspect.features.append(Feature(id="f1", title="Feature 1", description="desc 1"))
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result = await server.mcp.call_tool("list_features", {"aspect_id": "test"})
        assert "Feature 1" in str(result)

    @pytest.mark.anyio
    async def test_list_shortcomings_returns_shortcomings(self, tmp_path):
        store = AspectStore(tmp_path)
        aspect = Aspect(
            id="test2",
            name="Test Aspect 2",
            description="test description",
            user_story="As a user, I want test"
        )
        aspect.shortcomings.append(Shortcoming(
            id="s1",
            title="Shortcoming 1",
            description="desc 1",
            criticality=Criticality.HIGH
        ))
        store.save_aspect(aspect)

        server = ShortcomingsServer(store=store)
        result = await server.mcp.call_tool("list_shortcomings", {"aspect_id": "test2"})
        assert "Shortcoming 1" in str(result)
