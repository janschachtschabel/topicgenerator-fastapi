# Changelog

## [Unreleased] - 2025-07-14

### Hinzugefügt

- **Asynchrone Verarbeitung**: Die Kernlogik zur Generierung von Themenbäumen wurde von einem sequenziellen auf einen parallelen Ansatz umgestellt, um die Gesamt-Performance deutlich zu verbessern.

### Geändert

- **`src/DTOs/topic_tree_request.py`**:
  - Das Standard-LLM-Modell wurde von `gpt-4o-mini` auf `gpt-4.1-mini` geändert.

- **`src/structured_text_helper.py`**:
  - **Zeile 7**: `AsyncOpenAI` wurde importiert, um asynchrone API-Anfragen zu ermöglichen.
  - **Zeilen 81-132**: Die neue asynchrone Funktion `generate_structured_text_async` wurde implementiert. Sie ist eine asynchrone Version der bestehenden `generate_structured_text`-Funktion und verwendet `await`, um auf die Antwort der OpenAI-API zu warten.
  - **Zeilen 125-132**: Das Fehler-Handling in der asynchronen Funktion wurde angepasst. Bei Fehlern wird eine leere Liste zurückgegeben, um zu verhindern, dass ein einzelner fehlerhafter Aufruf alle anderen parallelen Anfragen in `asyncio.gather` abbricht.

- **`main.py`**:
  - **Zeilen 1, 8, 15**: Import von `asyncio`, `AsyncOpenAI` und `generate_structured_text_async`.
  - **Zeile 140**: Die Endpunkt-Funktion `generate_topic_tree` wurde zu einer asynchronen Funktion (`async def`) geändert.
  - **Zeile 159**: Der `OpenAI`-Client wurde durch den `AsyncOpenAI`-Client ersetzt.
  - **Zeile 176**: Der erste Aufruf zur Generierung der Hauptthemen wurde auf `await` umgestellt.
  - **Zeilen 188-231**: Die sequenziellen `for`-Schleifen zur Generierung von Unterthemen und Lehrplanthemen wurden durch parallele Logik mit `asyncio.gather` ersetzt. Tasks werden erstellt, parallel ausgeführt und die Ergebnisse anschließend den korrekten Eltern-Knoten zugeordnet.

- **`src/prompts.py`**:
  - **Zeilen 6-52**: Die `BASE_INSTRUCTIONS` wurden umfassend überarbeitet, um die Anweisungen für die KI zu präzisieren und zu vereinfachen.
  - **Zeilen 22-35**: Die Regeln für `FÄCHERFAMILIE` wurden klarer strukturiert und die Formatierungshinweise optimiert.
  - **Zeilen 36-41**: Die Anweisungen zur `BILDUNGSSTUFE` wurden vereinfacht und der Hinweis auf die automatische Anpassung verdeutlicht.
  - **Zeilen 42-45**: Die Regel zur `ANZAHL DER KATEGORIEN` wurde präzisiert, um eine natürliche Struktur zu fördern.
  - **Fix**: Explizite JSON-Formatierungsbeispiele und die Fehlerbehandlungs-Sektion wurden entfernt, um den Prompt zu straffen und die Anweisungen auf die Kernregeln zu fokussieren.

- **`pyproject.toml`**:
  - **Zeile 7**: Die Anforderung an die Python-Version (`requires-python`) wurde von `">=3.13"` auf `">=3.12"` geändert, um die Kompatibilität mit der Systemumgebung sicherzustellen.
