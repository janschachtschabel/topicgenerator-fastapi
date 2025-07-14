import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger
from openai import AsyncOpenAI

from src.DTOs.collection import Collection
from src.DTOs.ping import Ping
from src.DTOs.properties import Properties
from src.DTOs.topic_tree_request import TopicTreeRequest
from src.prompts import MAIN_PROMPT_TEMPLATE, SUB_PROMPT_TEMPLATE, LP_PROMPT_TEMPLATE
from src.structured_text_helper import generate_structured_text, generate_structured_text_async

# ToDo: replace / remove unnecessary dependencies
#  - replace "backoff" dependency since its unmaintained / abandonware
#  - replace OpenAI implementation with edu-sharing B.API
#    - define edu-sharing connector class
#  -> as of 2025-02-07 replacing the OpenAI client is no longer a priority since this prototype is intended for
#  quick iteration.

# ToDo: allow dynamic prompt updates
#  - prompts and basic instructions should allow for dynamic updates
#    - e.g. by fetching the prompt string from an edu-sharing node
#    - or via edu-sharing admin-tools

# ToDo: fix variable names and prompt placeholders
#  - either use German as our domain language for everything
#  - or properly translate everything to English

load_dotenv()


def get_openai_key():
    """Liest den OpenAI-API-Key aus den Umgebungsvariablen."""
    return os.getenv("OPENAI_API_KEY", "")


# Erlaubt, dass das Collection-Modell sich selbst referenziert (subcollections)
Collection.model_rebuild()
# ToDo: figure out why model_rebuild() is called here

# ------------------------------------------------------------------------------
# 7) FastAPI App
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Themenbaum Generator API",
    description="""
    ## Themenbaum Generator API

    Diese API ermöglicht die automatische Generierung von strukturierten Themenbäumen für Bildungsinhalte.

    ### Hauptfunktionen

    - **Themenbaumgenerierung**: Erstellt hierarchisch strukturierte Themenbäume mit Haupt-, Unter- und Lehrplanthemen
    - **Bildungskontext** (optional per URI): Falls gewünscht, kann eine Bildungsstufen-URI angegeben werden
    - **Fach (Disziplin)** (optional per URI): Falls gewünscht, kann eine Fach-URI angegeben werden
    - **Metadaten**: Generiert standardisierte Metadaten für jeden Knoten im Themenbaum

    ### Verwendung

    1. Senden Sie eine POST-Anfrage an den `/generate-topic-tree` Endpunkt
    2. Definieren Sie die gewünschten Parameter wie Thema, Anzahl der Themen und optional die URIs für Fach & Kontext
    3. Erhalten Sie einen strukturierten Themenbaum im JSON-Format

    ### Authentifizierung

    Die API verwendet einen OpenAI API-Schlüssel, der über die Umgebungsvariable `OPENAI_API_KEY` bereitgestellt werden muss.
    """,
    version="1.0.0",
    contact={"name": "Themenbaum Generator Support", "email": "support@example.com"},
    license_info={"name": "Proprietär", "url": "https://example.com/license"},
)
# ToDo: set (valid) contact / license information


@app.post(
    "/generate-topic-tree",
    response_model=dict,
    summary="Generiere einen Themenbaum",
    description="""
    Generiert einen strukturierten Themenbaum basierend auf den übergebenen Parametern.

    Der Themenbaum wird in folgender Hierarchie erstellt:
    1. Hauptthemen (z.B. "Mechanik", "Thermodynamik")
    2. Unterthemen (z.B. "Kinematik", "Dynamik")
    3. Lehrplanthemen (z.B. "Gleichförmige Bewegung", "Newtonsche Gesetze")

    Jeder Knoten im Themenbaum enthält:
    - Titel und Kurztitel
    - Beschreibung
    - Schlagworte (Keywords)
    - Standardisierte Metadaten (Properties)

    Optional können URIs für Fach und Bildungsstufe übergeben werden (via ``discipline_uri`` und ``educational_context_uri``). 
    Die URIs von Fach und Bildungsstufe haben **keinen** Effekt auf die Generierung des Themenbaums!
    """,
    responses={
        200: {
            "description": "Erfolgreich generierter Themenbaum",
            "content": {
                "application/json": {
                    "example": {
                        "metadata": {
                            "title": "Physik in Anlehnung an die Lehrpläne der Sekundarstufe 2",
                            "description": "Themenbaum für Physik in der Sekundarstufe II",
                            "created_at": "2025-02-05T11:28:40+01:00",
                            "version": "1.0",
                            "author": "Themenbaum Generator",
                        },
                        "collection": [
                            {
                                "title": "Allgemeines",
                                "shorttitle": "Allg",
                                "properties": {
                                    "cclom:general_keyword": ["allgemein", "grundlagen"],
                                    "ccm:collectionshorttitle": ["Allg"],
                                    "ccm:educationalcontext": [],
                                    "ccm:educationalintendedenduserrole": [
                                        "http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher"
                                    ],
                                    "ccm:taxonid": [],
                                    "cm:description": ["Einführung in ..."],
                                    "cm:title": ["Allgemeines"],
                                },
                                "subcollections": [],
                            }
                        ],
                    }
                }
            },
        },
        500: {
            "description": "Interner Serverfehler",
            "content": {"application/json": {"example": {"detail": "OpenAI API Key nicht gefunden"}}},
        },
    },
    tags=["Themenbaum-Generator"],
)
async def generate_topic_tree(topic_tree_request: TopicTreeRequest):
    """
    Generiert einen strukturierten Themenbaum basierend auf den Eingabeparametern.

    - ``theme``: Hauptthema
    - ``num_main_topics``: Anzahl der Hauptthemen (1 bis 30)
    - ``num_subtopics``: Anzahl der Unterthemen pro Hauptthema (0 bis 20)
    - ``num_curriculum_topics``: Anzahl der Lehrplanthemen pro Unterthema (0 bis 20)
    - ``include_general_topic``: Falls True, fügt ein Hauptthema "Allgemeines" hinzu
    - ``include_methodology_topic``: Falls True, fügt ein Hauptthema "Methodik und Didaktik" hinzu
    - ``discipline_uri``: Falls übergeben, tauchen diese URIs in den ``ccm:taxonid``-Properties auf (hat **keinen** Effekt auf die Generierung)
    - ``educational_context_uri``: Falls übergeben, taucht diese URI in den ``ccm:educationalcontext``-Properties auf (hat **keinen** Effekt auf die Generierung)
    """
    logger.info(
        f"Request received. Starting OpenAI chat completion request with the following settings: {topic_tree_request}"
    )
    # 1) OpenAI-Key holen
    openai_key = get_openai_key()
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API Key nicht gefunden")

    try:
        client = AsyncOpenAI(api_key=get_openai_key())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI-Init-Fehler: {str(e)}")

    try:
        # 2) Spezialanweisungen für Hauptthemen (z.B. Allgemeines, Methodik etc.)
        special_instructions = []
        if topic_tree_request.include_general_topic:
            special_instructions.append("1) Hauptthema 'Allgemeines' an erster Stelle")
        if topic_tree_request.include_methodology_topic:
            special_instructions.append("2) Hauptthema 'Methodik und Didaktik' an letzter Stelle")
        special_instructions = (
            "\n".join(special_instructions) if special_instructions else "Keine besonderen Anweisungen."
        )

        logger.info(f"Generating {topic_tree_request.num_main_topics} main topics ('Hauptthemen') ...")

        # 3) Hauptthemen generieren
        main_topics = await generate_structured_text_async(
            client=client,
            prompt=MAIN_PROMPT_TEMPLATE.format(
                themenbaumthema=topic_tree_request.theme,
                num_main=topic_tree_request.num_main_topics,
                existing_titles="",
                special_instructions=special_instructions,
            ),
            model=topic_tree_request.model,
        )

        if not main_topics:
            raise HTTPException(status_code=500, detail="Fehler bei der Generierung der Hauptthemen")

        logger.info("Received main topics ('Hauptthemen'). Beginning generation of sub topics ('Unterthemen') next.")

        # 4) Unterthemen für jedes Hauptthema asynchron generieren
        sub_topic_tasks = []
        for main_topic in main_topics:
            logger.info(f"Creating subtopic generation task for '{main_topic.title}'")
            prompt = SUB_PROMPT_TEMPLATE.format(
                themenbaumthema=topic_tree_request.theme,
                main_theme=main_topic.title,
                num_sub=topic_tree_request.num_subtopics,
            )
            task = generate_structured_text_async(client=client, prompt=prompt, model=topic_tree_request.model)
            sub_topic_tasks.append(task)

        sub_topics_results = await asyncio.gather(*sub_topic_tasks)

        for i, main_topic in enumerate(main_topics):
            sub_topics = sub_topics_results[i]
            if sub_topics:
                main_topic.subcollections = sub_topics

        # 5) Lehrplanthemen für jedes Unterthema asynchron generieren
        lp_tasks = []
        for main_topic in main_topics:
            for sub_topic in main_topic.subcollections:
                logger.info(f"Creating curriculum generation task for '{sub_topic.title}'")
                prompt = LP_PROMPT_TEMPLATE.format(
                    themenbaumthema=topic_tree_request.theme,
                    main_theme=main_topic.title,
                    sub_theme=sub_topic.title,
                    num_lp=topic_tree_request.num_curriculum_topics,
                )
                task = generate_structured_text_async(client=client, prompt=prompt, model=topic_tree_request.model)
                lp_tasks.append((main_topic, sub_topic, task))

        lp_results = await asyncio.gather(*[task for _, _, task in lp_tasks])

        for i, (main_topic, sub_topic, _) in enumerate(lp_tasks):
            lp_topics = lp_results[i]
            if lp_topics:
                sub_topic.subcollections = lp_topics

        # 6) Properties für alle Knoten nochmal updaten mit den (ggf.) übergebenen URIs
        for main_topic in main_topics:
            main_topic.properties = Properties(
                cm_title=[main_topic.title],
                ccm_collectionshorttitle=[main_topic.shorttitle],
                cm_description=main_topic.properties.cm_description,
                cclom_general_keyword=main_topic.properties.cclom_general_keyword,
                ccm_taxonid=main_topic.properties.ccm_taxonid,
                ccm_educationalcontext=main_topic.properties.ccm_educationalcontext,
            )

            for sub_topic in main_topic.subcollections:
                sub_topic.properties = Properties(
                    cm_title=[sub_topic.title],
                    ccm_collectionshorttitle=[sub_topic.shorttitle],
                    cm_description=sub_topic.properties.cm_description,
                    cclom_general_keyword=sub_topic.properties.cclom_general_keyword,
                    ccm_taxonid=sub_topic.properties.ccm_taxonid,
                    ccm_educationalcontext=sub_topic.properties.ccm_educationalcontext,
                )

                for lp_topic in sub_topic.subcollections:
                    lp_topic.properties = Properties(
                        cm_title=[lp_topic.title],
                        ccm_collectionshorttitle=[lp_topic.shorttitle],
                        cm_description=lp_topic.properties.cm_description,
                        cclom_general_keyword=lp_topic.properties.cclom_general_keyword,
                        ccm_taxonid=lp_topic.properties.ccm_taxonid,
                        ccm_educationalcontext=lp_topic.properties.ccm_educationalcontext,
                    )

        # 7) Finale Daten strukturieren (Metadaten + Collection-Liste)
        final_data = {
            "metadata": {
                "title": topic_tree_request.theme,
                "description": f"Themenbaum für {topic_tree_request.theme}",
                "target_audience": "Lehrkräfte",
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
                "author": "Themenbaum Generator",
            },
            "collection": [topic.to_dict() for topic in main_topics],
        }

        # ToDo: actually return a JSON object (instead of a python dict) as soon as you're done with debugging
        return final_data

    except Exception as e:
        logger.error(f"Unhandled Exception occured while generating topic tree: {e}")
        raise HTTPException(status_code=500, detail=f"Fehler bei der Generierung: {str(e)}")


@app.get(path="/_ping", response_model=Ping, tags=["health check"])
async def ping_endpoint():
    """Ping function for Kubernetes health checks."""
    return Ping(status="ok")


@app.get(path="/", include_in_schema=False)
async def root_endpoint():
    return {
        "message": "Hi there! The API Documentation is available in two formats: "
        "Please take a look at the /docs endpoint (for the Swagger UI) - or - "
        "take a look at the /redoc endpoint for an alternative documentation (by Redoc).",
        "API docs": {"swagger": "/docs", "redoc": "/redoc"},
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
