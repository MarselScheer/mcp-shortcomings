"""Storage layer for aspects, features, and shortcomings."""

import yaml
from pathlib import Path
from models import Aspect


class AspectStore:
    """Manages storage of aspects, features, and shortcomings in YAML files."""

    def __init__(self, base_path: Path):
        """Initialize the store with a base path for YAML files."""
        self.base_path = base_path
        self.aspects_dir = base_path / "aspects"
        self.aspects_dir.mkdir(parents=True, exist_ok=True)

    def _get_aspect_file(self, aspect_id: str) -> Path:
        """Get the file path for an aspect."""
        return self.aspects_dir / f"{aspect_id}.yaml"

    def save_aspect(self, aspect: Aspect) -> None:
        """Save an aspect to a YAML file."""
        file_path = self._get_aspect_file(aspect.id)
        with open(file_path, "w") as f:
            yaml.dump(
                aspect.model_dump(mode="json"),
                f,
                default_flow_style=False,
                sort_keys=False,
            )

    def get_aspect(self, aspect_id: str) -> Aspect | None:
        """Load an aspect from its YAML file."""
        file_path = self._get_aspect_file(aspect_id)
        if not file_path.exists():
            return None
        with open(file_path) as f:
            data = yaml.safe_load(f)
            return Aspect.model_validate(data)

    def list_aspects(self) -> list[Aspect]:
        """List all aspects."""
        aspects = []
        for file_path in self.aspects_dir.glob("*.yaml"):
            with open(file_path) as f:
                data = yaml.safe_load(f)
                aspects.append(Aspect.model_validate(data))
        return aspects

    def delete_aspect(self, aspect_id: str) -> None:
        """Delete an aspect's YAML file."""
        file_path = self._get_aspect_file(aspect_id)
        file_path.unlink()
