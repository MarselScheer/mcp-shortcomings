"""Pydantic models for aspects, features, and shortcomings."""

from enum import Enum
from pydantic import BaseModel, Field


class Criticality(str, Enum):
    """Criticality level for shortcomings."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Feature(BaseModel):
    """A feature of an aspect."""

    id: str
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)


class Shortcoming(BaseModel):
    """A shortcoming of an aspect."""

    id: str
    title: str
    description: str
    criticality: Criticality
    tags: list[str] = Field(default_factory=list)
    depends_on_others: bool = False


class Aspect(BaseModel):
    """An aspect of the project."""

    id: str
    name: str
    description: str
    user_story: str
    features: list[Feature] = Field(default_factory=list)
    shortcomings: list[Shortcoming] = Field(default_factory=list)
