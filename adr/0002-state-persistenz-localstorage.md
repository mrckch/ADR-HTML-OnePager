# ADR-0002: State-Persistenz im localStorage

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Datenhaltung, Persistenz, Schülerergebnisse

## Kontext

Schüler:innen geben in den Onepagern Antworten/Lösungen ein (Eingabefelder, Checkboxen, Notizen). Diese Ergebnisse sollen **erhalten bleiben**, wenn sie die Seite versehentlich schließen, das Gerät neu starten oder am nächsten Tag weiterarbeiten.

Es gibt **keinen Backend-Server**, der Daten speichern könnte (siehe [ADR-0001](0001-single-file-html-architektur.md)).

Randbedingungen:
- Daten gehören dem/der Schüler:in und sollen das Gerät nicht verlassen (Datenschutz)
- Daten sollen geräte-/browserlokal bestehen bleiben
- Bei mehreren Onepagern auf derselben Domain darf es keine Kollisionen geben

## Entscheidung

**`localStorage`** ist der primäre Speicher für Schülerergebnisse.

Konventionen:
- **Ein einziger Storage-Key pro Onepager:** `onepager:<slug>:state` (z. B. `onepager:bruchrechnen-01:state`)
- Inhalt ist ein JSON-Objekt mit dem gesamten Seiten-State
- **Versionierung im State:** `{ "version": 1, "data": { … } }` — damit spätere Schema-Änderungen migriert werden können
- Auto-Save: bei jeder relevanten Eingabe (`input`, `change`) wird der State geschrieben (debounced ~300 ms)
- Beim Laden der Seite: State aus `localStorage` lesen und UI initialisieren

```js
const STORAGE_KEY = 'onepager:bruchrechnen-01:state';
const SCHEMA_VERSION = 1;

function saveState(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: SCHEMA_VERSION, data }));
}

function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    return parsed.version === SCHEMA_VERSION ? parsed.data : null;
  } catch {
    return null;
  }
}
```

## Alternativen

- **`sessionStorage`:** Verworfen — Daten verschwinden beim Schließen des Tabs.
- **IndexedDB:** Overkill für einfache Formular-States; API zu komplex für den Anwendungsfall.
- **Cookies:** Werden bei jedem Request mitgeschickt (unnötig), Größenlimit pro Cookie zu klein.
- **Backend-Speicherung:** Nicht möglich (kein Server) und datenschutzrechtlich problematisch.

## Konsequenzen

**Positiv:**
- Daten bleiben dauerhaft auf dem Gerät, auch nach Browser-Neustart
- Kein Datenschutz-Risiko (Daten verlassen das Gerät nicht)
- Einfache API, synchron, schnell

**Negativ / Trade-offs:**
- Daten gehen verloren bei: Browser-Cache löschen, privater Modus, anderer Browser/Gerät → daher zusätzlich JSON-Export anbieten ([ADR-0003](0003-json-export-import.md))
- iOS Safari kann `localStorage` in seltenen Fällen (z. B. „Intelligent Tracking Prevention") nach 7 Tagen Inaktivität löschen → JSON-Export als Sicherung wichtig
- Größenlimit ca. 5–10 MB pro Origin — für Text reichlich, bei Bildern/Anhängen prüfen

**Folgewirkungen für künftige Onepager:**
- Jeder Onepager bekommt einen eindeutigen Storage-Key (`onepager:<slug>:state`)
- Schema-Version im State immer mitführen
- Schreib- und Lese-Logik fehlertolerant: bei `JSON.parse`-Fehler oder Versions-Mismatch sauber zurückfallen, **nicht** crashen
- Beim ersten Aufruf eines leeren States: leere/Default-UI anzeigen, **nicht** mit Fehler reagieren

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Single-File (kein Backend)
- [ADR-0003](0003-json-export-import.md) — JSON-Export/Import als Backup-Mechanismus
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Reset löscht den localStorage-Eintrag
