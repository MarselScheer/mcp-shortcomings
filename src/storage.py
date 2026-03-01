"""Storage layer for aspects, features, and shortcomings."""

import os
import re
import shutil
import yaml
from pathlib import Path
from models import Aspect, Feature, Shortcoming


class AspectStore:
    """Manages storage of aspects, features, and shortcomings in YAML files."""

    def __init__(self, base_path: Path | str | None = None):
        """Initialize the store with a base path for YAML files."""
        if base_path is None:
            base_path = Path(os.environ["SHORTCOMINGS_PATH"])
        else:
            base_path = Path(base_path)

        self.base_path = base_path
        self.aspects_dir = base_path / "aspects"
        self.aspects_dir.mkdir(parents=True, exist_ok=True)

    def _get_aspect_dir(self, aspect_id: str) -> Path:
        """Get the directory path for an aspect."""
        return self.aspects_dir / aspect_id

    def save_aspect(self, aspect: Aspect) -> None:
        """Save an aspect with its features and shortcomings in separate YAML files."""
        aspect_dir = self._get_aspect_dir(aspect.id)

        # Remove existing directory if present to ensure clean state
        if aspect_dir.exists():
            shutil.rmtree(aspect_dir)

        aspect_dir.mkdir(parents=True, exist_ok=True)

        # Save aspect metadata (without features/shortcomings)
        metadata = aspect.model_dump(exclude={"features", "shortcomings"})
        aspect_file = aspect_dir / "aspect.yaml"
        with open(aspect_file, "w") as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

        # Save features in separate files
        features_dir = aspect_dir / "features"
        features_dir.mkdir(exist_ok=True)
        for feature in aspect.features:
            feature_file = features_dir / f"{feature.id}.yaml"
            with open(feature_file, "w") as f:
                yaml.dump(
                    feature.model_dump(mode="json"),
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                )

        # Save shortcomings in separate files
        shortcomings_dir = aspect_dir / "shortcomings"
        shortcomings_dir.mkdir(exist_ok=True)
        for shortcoming in aspect.shortcomings:
            shortcoming_file = shortcomings_dir / f"{shortcoming.id}.yaml"
            with open(shortcoming_file, "w") as f:
                yaml.dump(
                    shortcoming.model_dump(mode="json"),
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                )

    def get_aspect(self, aspect_id: str) -> Aspect | None:
        """Load an aspect from its YAML files."""
        aspect_dir = self._get_aspect_dir(aspect_id)
        aspect_file = aspect_dir / "aspect.yaml"

        if not aspect_file.exists():
            return None

        # Load aspect metadata
        with open(aspect_file) as f:
            data = yaml.safe_load(f)

        # Load features
        features = []
        features_dir = aspect_dir / "features"
        if features_dir.exists():
            for feature_file in features_dir.glob("*.yaml"):
                with open(feature_file) as f:
                    features.append(Feature.model_validate(yaml.safe_load(f)))

        # Load shortcomings
        shortcomings = []
        shortcomings_dir = aspect_dir / "shortcomings"
        if shortcomings_dir.exists():
            for shortcoming_file in shortcomings_dir.glob("*.yaml"):
                with open(shortcoming_file) as f:
                    shortcomings.append(Shortcoming.model_validate(yaml.safe_load(f)))

        data["features"] = features
        data["shortcomings"] = shortcomings
        return Aspect.model_validate(data)

    def list_aspects(self) -> list[Aspect]:
        """List all aspects."""
        aspects = []
        if not self.aspects_dir.exists():
            return aspects

        for aspect_dir in self.aspects_dir.iterdir():
            if aspect_dir.is_dir():
                aspect = self.get_aspect(aspect_dir.name)
                if aspect:
                    aspects.append(aspect)
        return aspects

    def delete_aspect(self, aspect_id: str) -> None:
        """Delete an aspect's directory."""
        aspect_dir = self._get_aspect_dir(aspect_id)
        if aspect_dir.exists():
            shutil.rmtree(aspect_dir)

    def search(self, pattern: str) -> dict:
        """Search for a regex pattern across all aspects, features, and shortcomings.

        Args:
            pattern: Regex pattern to search for

        Returns:
            Dictionary with keys 'aspects', 'features', 'shortcomings' containing matching items
        """
        regex = re.compile(pattern, re.IGNORECASE)
        results = {"aspects": [], "features": [], "shortcomings": []}

        for aspect in self.list_aspects():
            # Search aspect - check all fields
            aspect_str = (
                f"{aspect.id} {aspect.name} {aspect.description} {aspect.user_story}"
            )
            if regex.search(aspect_str):
                results["aspects"].append(aspect)

            # Search features
            for feature in aspect.features:
                feature_str = f"{feature.id} {feature.title} {feature.description} {' '.join(feature.tags)}"
                if regex.search(feature_str):
                    results["features"].append(feature)

            # Search shortcomings
            for shortcoming in aspect.shortcomings:
                shortcoming_str = f"{shortcoming.id} {shortcoming.title} {shortcoming.description} {shortcoming.criticality.value} {' '.join(shortcoming.tags)}"
                if regex.search(shortcoming_str):
                    results["shortcomings"].append(shortcoming)

        return results
