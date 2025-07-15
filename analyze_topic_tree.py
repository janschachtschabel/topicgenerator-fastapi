import json
import argparse

def analyze_tree(collections):
    """
    Zählt die Anzahl der Kategorien auf jeder Ebene des Themenbaums.

    Args:
        collections (list): Eine Liste von Collection-Objekten (als Dictionaries).

    Returns:
        tuple: Ein Tupel mit der Anzahl der Hauptthemen, Unterthemen und Lehrplanthemen.
    """
    num_main_topics = len(collections)
    num_sub_topics = 0
    num_curriculum_topics = 0

    for main_topic in collections:
        if 'subcollections' in main_topic and main_topic['subcollections']:
            num_sub_topics += len(main_topic['subcollections'])
            for sub_topic in main_topic['subcollections']:
                if 'subcollections' in sub_topic and sub_topic['subcollections']:
                    num_curriculum_topics += len(sub_topic['subcollections'])

    return num_main_topics, num_sub_topics, num_curriculum_topics

def print_ascii_tree(collections, prefix=""):
    """
    Gibt den Themenbaum als ASCII-Struktur aus, die nur die Titel enthält.

    Args:
        collections (list): Eine Liste von Collection-Objekten (als Dictionaries).
        prefix (str): Das Präfix für die aktuelle Ebene der Baumstruktur.
    """
    for i, item in enumerate(collections):
        is_last = i == len(collections) - 1
        print(prefix + ('└── ' if is_last else '├── ') + item['title'])
        if 'subcollections' in item and item['subcollections']:
            new_prefix = prefix + ('    ' if is_last else '│   ')
            print_ascii_tree(item['subcollections'], new_prefix)

def main():
    """
    Hauptfunktion zum Laden der JSON-Datei und zur Ausführung der Analyse.
    """
    parser = argparse.ArgumentParser(description="Analysiert eine JSON-Datei mit einem Themenbaum.")
    parser.add_argument(
        'filename',
        nargs='?',
        default='topic_tree_result.json',
        help="Der Name der JSON-Datei, die analysiert werden soll. Standard: 'topic_tree_result.json'"
    )
    args = parser.parse_args()

    try:
        with open(args.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{args.filename}' wurde nicht gefunden.")
        print("Bitte stellen Sie sicher, dass die Datei existiert und der Pfad korrekt ist.")
        return
    except json.JSONDecodeError:
        print(f"Fehler: Die Datei '{args.filename}' enthält kein gültiges JSON.")
        return

    if 'collection' not in data:
        print(f"Fehler: Der Schlüssel 'collection' wurde in der Datei '{args.filename}' nicht gefunden.")
        return

    collections = data['collection']

    # Analyse der Kategorien
    main_topics, sub_topics, curriculum_topics = analyze_tree(collections)
    print(f"--- Analyse für: {args.filename} ---")
    print(f"Anzahl Hauptkategorien (Ebene 1): {main_topics}")
    print(f"Anzahl Unterkategorien (Ebene 2): {sub_topics}")
    print(f"Anzahl Lehrplanthemen (Ebene 3): {curriculum_topics}")
    print("---------------------------------"
          "\n")

    # ASCII-Baum ausgeben
    print("--- ASCII Themenbaum ---")
    print_ascii_tree(collections)
    print("------------------------")

if __name__ == "__main__":
    main()
