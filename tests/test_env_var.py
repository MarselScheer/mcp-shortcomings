"""Tests for AspectStore environment variable handling."""

import os
import pytest
from pathlib import Path

from storage import AspectStore


def test_store_uses_shortcomings_path_env_var(monkeypatch, tmp_path):
    """Test that AspectStore uses SHORTCOMINGS_PATH env var when no base_path provided."""
    # Set the environment variable to our tmp path
    monkeypatch.setenv("SHORTCOMINGS_PATH", str(tmp_path))
    
    # Create store without passing base_path
    store = AspectStore()
    
    # Should use the env var value
    assert store.base_path == tmp_path


def test_store_raises_error_when_env_var_not_set(monkeypatch):
    """Test that AspectStore raises error when env var is not set."""
    # Ensure the env var is not set
    monkeypatch.delenv("SHORTCOMINGS_PATH", raising=False)
    
    # Should raise KeyError
    with pytest.raises(KeyError):
        AspectStore()
