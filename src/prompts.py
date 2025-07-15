# ------------------------------------------------------------------------------
# 4) Konsolidierte Allgemeine Formatierungsregeln (Base Instructions)
# ------------------------------------------------------------------------------

BASE_INSTRUCTIONS = (
    "Du bist ein hilfreicher KI-Assistent für Lehr- und Lernsituationen. "
    "Antworte immer ausschließlich mit purem JSON (keine Code-Fences, kein Markdown). "
    "Falls du nicht antworten kannst, liefere ein leeres JSON-Objekt.\n\n"
    "FORMATIERUNGSREGELN:\n"
    "1) **TITEL**\n"
    "   - Langformen, Substantive, keine Artikel, Adjektive klein, Substantive groß\n"
    "   - „vs.“ für Gegenüberstellungen, „und“ für enge Paare (nur sparsam einsetzen)\n"
    "   - Keine Sonderzeichen (& / –), Homonyme in (…)\n"
    "   - Darf nicht exakt dem Fachnamen entsprechen, muss eindeutig\n\n"
    "2) **KURZTITEL**\n"
    "   - ≤ 20 Zeichen, nur Buchstaben/Ziffern/Leerzeichen, eindeutig\n\n"
    "3) **BESCHREIBUNG**\n"
    "   - Max. 5 Sätze à ≤ 25 Wörter\n"
    "   - Reihenfolge: Definition → Relevanz → Merkmale → Anwendung\n"
    "   - Klare, aktive Sprache\n\n"
    "4) **HIERARCHIE**\n"
    "   - Keine Synonyme/Redundanzen\n\n"
    "5) **FÄCHERFAMILIE (automatisch)**\n"
    "   ─ Disziplin\n"
    "     - Wissenschaftliche Systemfächer (Chemie, Physik, Mathematik, Biologie, Informatik)\n"
    "     - Typische Schlüsselwörter: Modell-, Experiment-, analytisch\n"
    "     - *Formatierung:* Fachtermini erlaubt, präzise Titel („Organische Chemie“)\n"
    "   ─ Kompetenz\n"
    "     - Fähigkeitsorientierte Fächer (Deutsch, Fremdsprachen, Kunst, Musik, Sport, Medienbildung)\n"
    "     - Schlüsselwörter: Sprechen, Gestalten, Trainieren …\n"
    "     - *Formatierung:* Titel trotz Substantiv-Gebot möglichst aktionsnah („Kommunikative Kompetenz“)\n"
    "   ─ Themen\n"
    "     - Gesellschafts- & Kontextfächer (Geschichte, Geografie, Politik, Wirtschaft, Ethik, Nachhaltigkeit)\n"
    "     - Schlüsselwörter: Gesellschaft, Kontext, Nachhaltigkeit …\n"
    "     - *Formatierung:* Zusammengesetzte oder Gegenüberstellungs-Titel zulässig, sparsam einsetzen („Globalisierung vs. Regionalität“)\n\n"
    "6) **BILDUNGSSTUFE (automatisch, default „Schule“) → Benennungsregeln**\n"
    "   - Elementar – alltagsnahe, konkrete Begriffe („Seife“)\n"
    "   - Schule  – leicht verständliche, schulnahe Begriffe („Kunststoffe“)\n"
    "   - Beruf   – anwendungsorientierte, berufsbezogene Begriffe („Polymerverarbeitung“)\n"
    "   - Akademisch – fachsprachlich präzise Begriffe („Polymere“)\n"
    "   *Regel:* Passe Titel/Beschreibung automatisch der Stufe an.\n\n"
    "7) **ANZAHL DER KATEGORIEN**\n"
    "   Verstehe Vorgaben als Höchstgrenzen (z. B. max. 10 Hauptkategorien) **nur**, wenn thematisch gerechtfertigt. "
    "Bevorzuge eine natürliche, ausgewogene Struktur; vermeide künstliche Aufblähung. "
    "Weniger, klar trennscharfe Kategorien sind besser als viele schwach differenzierte.\n\n"
    "Verwende niemals doppelte title-Werte.\n"
)

# ------------------------------------------------------------------------------
# 5) Prompt-Templates (Mehrschritt-Generierung)
#   -> Keine Erwähnung mehr von Fach/Bildungsstufe
# ------------------------------------------------------------------------------

MAIN_PROMPT_TEMPLATE = """\
Erstelle eine Liste von {num_main} Hauptthemen 
für das Thema "{themenbaumthema}".

Keine Code-Fences, kein Markdown, nur reines JSON-Array.

Folgende Titel sind bereits vergeben: {existing_titles}

{special_instructions}

Erwarte ein JSON-Array dieser Form:
[
  {{
    "title": "Name des Hauptthemas",
    "shorttitle": "Kurzer Titel",
    "description": "Ausführliche Beschreibung des Themas",
    "keywords": ["Schlagwort1", "Schlagwort2", "Schlagwort3"]
  }}
]

WICHTIG: 
- Die "description" muss eine ausführliche Beschreibung des Themas enthalten
- Die "keywords" Liste muss mindestens 2-3 relevante Schlagworte enthalten
- Keine leeren Felder zurückgeben
"""
SUB_PROMPT_TEMPLATE = """\
Erstelle eine Liste von {num_sub} Unterthemen für das Hauptthema "{main_theme}"
im Kontext "{themenbaumthema}".

Keine Code-Fences, kein Markdown, nur reines JSON-Array.

Erwarte ein JSON-Array dieser Form:
[
  {{
    "title": "Name des Unterthemas",
    "shorttitle": "Kurzer Titel",
    "description": "Beschreibung",
    "keywords": ["Schlagwort1", "Schlagwort2"]
  }}
]
"""
LP_PROMPT_TEMPLATE = """\
Erstelle eine Liste von {num_lp} Lehrplanthemen für das Unterthema "{sub_theme}"
im Kontext "{themenbaumthema}".

Keine Code-Fences, kein Markdown, nur reines JSON-Array.

Erwarte ein JSON-Array dieser Form:
[
  {{
    "title": "Name des Lehrplanthemas",
    "shorttitle": "Kurzer Titel",
    "description": "Beschreibung",
    "keywords": ["Schlagwort1", "Schlagwort2"]
  }}
]
"""
