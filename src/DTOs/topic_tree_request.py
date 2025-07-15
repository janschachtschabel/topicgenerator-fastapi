from typing import Optional, List

from pydantic import BaseModel, Field


class TopicTreeRequest(BaseModel):
    """
    Request-Modell für die Generierung eines Themenbaums.
    Hierüber kommen Parameter wie Thema, Anzahl an Hauptthemen,
    Anzahl an Unterthemen und Anzahl an Lehrplanthemen.

    'discipline_uri' und 'educational_context_uri' sind optional und haben keinen Effekt auf die Generierung.
    Falls sie mitgegeben werden, landen sie als (hard-coded) URIs in den Metadaten.
    """

    theme: str = Field(
        ...,
        description="Das Hauptthema des Themenbaums",
        examples=["Physik in Anlehnung an die Lehrpläne der Sekundarstufe 2"],
    )
    num_main_topics: int = Field(5, ge=1, le=30, description="Anzahl der zu generierenden Hauptthemen", examples=[5])
    num_subtopics: int = Field(3, ge=0, le=20, description="Anzahl der Unterthemen pro Hauptthema", examples=[3])
    num_curriculum_topics: int = Field(
        2, ge=0, le=20, description="Anzahl der Lehrplanthemen pro Unterthema", examples=[2]
    )
    include_general_topic: bool = Field(
        False, description="Wenn True, wird 'Allgemeines' als erstes Hauptthema eingefügt", examples=[True, False]
    )
    include_methodology_topic: bool = Field(
        False,
        description="Wenn True, wird 'Methodik und Didaktik' als letztes Hauptthema eingefügt",
        examples=[True, False],
    )

    discipline_uri: Optional[List[str]] = Field(
        None,
        description="Optionale URIs für den Fachbereich.",
        examples=[["http://w3id.org/openeduhub/vocabs/discipline/460"]],
    )
    educational_context_uri: Optional[List[str]] = Field(
        None,
        description="Optionale URIs für die Bildungsstufe.",
        examples=[
            [
                "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
            ]
        ],
    )

    model: str = Field("gpt-4.1-mini", description="Das zu verwendende OpenAI-Sprachmodell", examples=["gpt-4.1-mini"])
