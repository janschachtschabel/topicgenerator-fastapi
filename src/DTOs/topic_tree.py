from typing import List

from pydantic import BaseModel, Field

from src.DTOs.collection import Collection


class TopicTree(BaseModel):
    """
    Der komplette Themenbaum mit Metadaten und einer Liste von Collections.
    """

    collection: List[Collection]
    metadata: dict = Field(
        default_factory=lambda: {
            "title": "",
            "description": "",
            "target_audience": "",
            "created_at": "",
            "version": "1.0",
            "author": "Themenbaum Generator",
        }
    )

    def to_dict(self) -> dict:
        """
        Konvertiert den gesamten Themenbaum (inkl. Metadaten und Collections) in ein Dictionary.
        """
        return {"metadata": self.metadata, "collection": [c.to_dict() for c in self.collection]}
