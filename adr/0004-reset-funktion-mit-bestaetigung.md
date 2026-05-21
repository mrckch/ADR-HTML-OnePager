# ADR-0004: Reset-Funktion mit Bestätigungsdialog

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** UX, Persistenz, Schülerbedienung

## Kontext

Schüler:innen sollen die Möglichkeit haben, einen Onepager **komplett zurückzusetzen** — z. B. um eine Aufgabe noch einmal von vorne zu bearbeiten, oder wenn die Lehrkraft eine Übung neu starten lässt.

Risiko: Versehentlicher Klick darf nicht alle Ergebnisse zerstören.

## Entscheidung

Im Sticky Top-Menü ([ADR-0005](0005-sticky-menue-ios-safe-area.md)) gibt es einen **Reset-Button** mit folgenden Eigenschaften:

1. **Optisch deutlich, aber nicht knallrot.** Nicht der primäre Button; ggf. als Icon mit Label, sekundäre Farbe.
2. **Zweistufiger Bestätigungsdialog** vor dem Löschen:
   - Frage: „Möchtest du wirklich alle deine Eingaben zurücksetzen? Diese Aktion kann nicht rückgängig gemacht werden."
   - Hinweis: „Tipp: Du kannst vorher deine Ergebnisse als JSON-Datei speichern."
   - Buttons: **„Abbrechen"** (primär, vorausgewählt) und **„Zurücksetzen"** (sekundär/destruktiv)
3. **Eigener Dialog**, nicht `window.confirm()` — der native Dialog auf iOS ist nicht stylebar und wirkt unprofessionell. Stattdessen ein eigenes Modal mit Backdrop, das tastatur- und screenreader-freundlich ist (`role="dialog"`, `aria-modal="true"`, Fokus-Trap).
4. **Beim Bestätigen:** `localStorage.removeItem(STORAGE_KEY)` + Seite neu rendern (Default-State).
5. **Kein automatischer Reload** der Seite — flackerfrei reagieren.

## Alternativen

- **Kein Reset-Button:** Verworfen — Schüler:innen wollen das, und sie würden sonst den Browser-Cache löschen (was alle Onepager auf dieser Domain treffen würde).
- **`window.confirm()`:** Verworfen — auf iOS nicht stylebar, optisch hässlich, keine A11y-Kontrolle.
- **Undo-Funktion statt Reset:** Verworfen — Komplexität in Single-File-HTML zu hoch, Schüler:innen verstehen Reset besser.
- **Reset ohne Bestätigung:** Verworfen — versehentlicher Klick zerstört Arbeit.

## Konsequenzen

**Positiv:**
- Schüler:innen können bewusst neu starten
- Versehentliches Löschen wird durch Bestätigungsdialog verhindert
- Konsistentes UX-Pattern über alle Onepager

**Negativ / Trade-offs:**
- Eigener Modal-Dialog muss in jedem Onepager vorhanden sein (kopierbares Snippet)
- Fokus-Management und Tastatur-Bedienung muss korrekt implementiert sein

**Folgewirkungen für künftige Onepager:**
- Reset-Button **immer** im Sticky-Menü, sekundär gestylt
- **Immer** Bestätigungsdialog mit Hinweis auf JSON-Export
- Dialog mit Fokus-Trap, `Esc` zum Schließen, Klick auf Backdrop schließt (= Abbrechen)
- Nach Reset: kein Reload, sondern UI auf Default-State rendern

## Verwandte ADRs

- [ADR-0002](0002-state-persistenz-localstorage.md) — localStorage
- [ADR-0003](0003-json-export-import.md) — JSON-Export als Vorab-Sicherung
- [ADR-0005](0005-sticky-menue-ios-safe-area.md) — Menüposition
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — Dialog-Accessibility
