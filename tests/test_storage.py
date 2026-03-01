"""Tests for the storage layer."""

import pytest

from models import Aspect, Feature, Shortcoming, Criticality
from storage import AspectStore


@pytest.fixture
def temp_store(tmp_path):
    """Create a temporary aspect store for testing."""
    return AspectStore(base_path=tmp_path)


def test_save_and_load_aspect_with_models(temp_store):
    """Test that an aspect with Pydantic models can be saved and loaded."""
    aspect = Aspect(
        id="api-endpoints",
        name="API Endpoints",
        description="REST API endpoints of the project",
        user_story="As a developer, I want to know what API endpoints exist",
        features=[
            Feature(
                id="user-get-endpoint",
                title="GET /users endpoint",
                description="Returns a list of users",
                tags=["api", "users", "read"],
            )
        ],
        shortcomings=[
            Shortcoming(
                id="no-pagination",
                title="No pagination support",
                description="The users endpoint returns all users at once",
                criticality=Criticality.MEDIUM,
                tags=["api", "performance", "pagination"],
                depends_on_others=False,
            )
        ],
    )

    temp_store.save_aspect(aspect)
    loaded = temp_store.get_aspect("api-endpoints")

    assert loaded is not None
    assert loaded.id == "api-endpoints"
    assert loaded.name == "API Endpoints"
    assert len(loaded.features) == 1
    assert loaded.features[0].title == "GET /users endpoint"
    assert len(loaded.shortcomings) == 1
    assert loaded.shortcomings[0].criticality == Criticality.MEDIUM
    assert loaded.shortcomings[0].depends_on_others is False


def test_list_aspects(temp_store):
    """Test listing all aspects."""
    aspect1 = Aspect(
        id="aspect-1",
        name="Aspect 1",
        description="First aspect",
        user_story="User story 1",
        features=[],
        shortcomings=[],
    )
    aspect2 = Aspect(
        id="aspect-2",
        name="Aspect 2",
        description="Second aspect",
        user_story="User story 2",
        features=[],
        shortcomings=[],
    )
    temp_store.save_aspect(aspect1)
    temp_store.save_aspect(aspect2)

    aspects = temp_store.list_aspects()

    assert len(aspects) == 2
    ids = [a.id for a in aspects]
    assert "aspect-1" in ids
    assert "aspect-2" in ids


def test_delete_aspect(temp_store):
    """Test deleting an aspect."""
    aspect = Aspect(
        id="to-delete",
        name="To Delete",
        description="Will be deleted",
        user_story="User story",
        features=[],
        shortcomings=[],
    )
    temp_store.save_aspect(aspect)

    assert temp_store.get_aspect("to-delete") is not None

    temp_store.delete_aspect("to-delete")

    assert temp_store.get_aspect("to-delete") is None


def test_list_aspects_empty_dir_returns_empty_list(temp_store):
    """Test listing aspects when directory is empty returns empty list."""
    aspects = temp_store.list_aspects()

    assert aspects == []


def test_save_aspect_creates_directory_structure(temp_store):
    """Test that saving an aspect creates the grep-friendly directory structure."""
    aspect = Aspect(
        id="api-endpoints",
        name="API Endpoints",
        description="REST API endpoints of the project",
        user_story="As a developer, I want to know what API endpoints exist",
        features=[
            Feature(
                id="user-get-endpoint",
                title="GET /users endpoint",
                description="Returns a list of users",
                tags=["api", "users", "read"],
            )
        ],
        shortcomings=[
            Shortcoming(
                id="no-pagination",
                title="No pagination support",
                description="The users endpoint returns all users at once",
                criticality=Criticality.MEDIUM,
                tags=["api", "performance", "pagination"],
                depends_on_others=False,
            )
        ],
    )

    temp_store.save_aspect(aspect)

    # Verify directory structure for grep-ability
    base = temp_store.aspects_dir / "api-endpoints"
    assert (base / "aspect.yaml").exists(), "Aspect metadata should be in aspect.yaml"
    assert (base / "features" / "user-get-endpoint.yaml").exists(), "Feature should be in features/"
    assert (base / "shortcomings" / "no-pagination.yaml").exists(), "Shortcoming should be in shortcomings/"
