from typing import List

from pydantic import BaseModel, Field


class Properties(BaseModel):
    """
    Properties-Objekt, das Metadaten wie Titel, Description, Keywords etc. speichert.
    """

    cclom_general_keyword: List[str] = Field(
        description="keywords",
        serialization_alias="cclom:general_keyword",
        examples=["Energie", "Erhaltung", "Systeme"],
    )
    ccm_collectionshorttitle: List[str] = Field(
        default_factory=lambda: [""],
        description="short-title of the edu-sharing collection",
        serialization_alias="ccm:collectionshorttitle",
        examples=["Energieerhaltung"],
    )
    ccm_educationalcontext: List[str] = Field(
        default_factory=list,
        description="URIs of educational contexts (de: Bildungsstufen)",
        serialization_alias="ccm:educationalcontext",
        examples=[
            "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_1",
            "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
        ],
    )
    ccm_educationalintendedenduserrole: List[str] = Field(
        default_factory=lambda: ["http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher"],
        description="URIs of target group(s) / intended end users of a learning resource",
        serialization_alias="ccm:educationalintendedenduserrole",
        examples=["http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher"],
    )
    ccm_taxonid: List[str] = Field(
        default_factory=list,
        description="URIs of disciplines (de: Schulfaecher)",
        serialization_alias="ccm:taxonid",
        examples=[
            ["http://w3id.org/openeduhub/vocabs/discipline/48005", "http://w3id.org/openeduhub/vocabs/discipline/720"]
        ],
    )
    cm_description: List[str] = Field(
        description="description of the edu-sharing collection",
        serialization_alias="cm:description",
        examples=[
            "Die Energie ist eine der wichtigsten und gleichzeitig schwierigsten Größen der Physik: Ihre Gesamtmenge ändert sich nie, und doch lässt sie sich nicht beliebig nutzen. Sie tritt in vielen verschiedenen Formen auf, die sich ineinander umwandeln lassen. Und sie vereinfacht die Berechnung einer Vielzahl von praktischen und physikalischen Problemen. Gleichzeitig weiß niemand so genau, was Energie letzten Endes eigentlich genau ist."
        ],
    )
    cm_title: List[str] = Field(
        description="title of the edu-sharing collection",
        serialization_alias="cm:title",
        examples=["Gesetze der Energieerhaltung"],
    )

    class Config:
        # settings used for (de-)serialization of the ``Properties``-model (by invoking an alias_generator)
        # see: https://docs.pydantic.dev/latest/concepts/alias/
        # and https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.alias_generator
        populate_by_name = True
