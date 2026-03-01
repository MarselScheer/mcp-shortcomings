"""Tests for environment configuration."""

from mcp_server import ShortcomingsServer


def test_uses_shortcomings_path_env_variable(tmp_path, monkeypatch):
    """Test that ShortcomingsServer uses SHORTCOMINGS_PATH environment variable."""
    # Set the environment variable to our temp directory
    monkeypatch.setenv("SHORTCOMINGS_PATH", str(tmp_path))

    # Create a new server instance (should read from env var)
    server = ShortcomingsServer()

    # Assert the store's base_path matches the env var
    assert server.store.base_path == tmp_path
