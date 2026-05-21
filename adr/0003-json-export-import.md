# ADR-0003: JSON-Export und -Import für Schülerergebnisse

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Persistenz, Backup, Datenportabilität

## Kontext

`localStorage` ist die Primärspeicherung ([ADR-0002](0002-state-persistenz-localstorage.md)), kann aber unter bestimmten Umständen verloren gehen:
- Schüler:in löscht den Browser-Cache
- iOS Safari löscht Storage nach längerer Inaktivität (ITP)
- Wechsel auf ein anderes Gerät / einen anderen Browser
- Lehrkraft möchte Ergebnisse einsammeln (z. B. zur Kontrolle)

## Entscheidung

Jeder Onepager bietet im Top-Menü ([ADR-0005](0005-sticky-menue-ios-safe-area.md)) **Export** und **Import** von Ergebnissen als JSON-Datei.

**Export:**
- Button „Ergebnisse herunterladen" erzeugt eine `.json`-Datei
- Dateiname: `<onepager-slug>__<YYYY-MM-DD>__<HH-MM>.json` (Doppelter Unterstrich als Trenner; keine Doppelpunkte wegen Windows-Dateinamen)
- Inhalt: Identisch zum localStorage-Format (`{ version, data }`) plus Metadaten:

```json
{
  "version": 1,
  "exportedAt": "2026-05-21T10:30:00.000Z",
  "onepager": "bruchrechnen-01",
  "data": { … }
}
```

**Import:**
- Button „Ergebnisse importieren" öffnet einen Datei-Dialog (`<input type="file" accept="application/json,.json">`)
- Beim Import: Datei lesen, validieren (`version` und `onepager`-Slug prüfen), in `localStorage` schreiben, UI neu rendern
- Bei Mismatch (falscher Onepager oder unbekannte Version): freundliche Fehlermeldung, **kein** Datenverlust
- **Vor dem Überschreiben** bestehender Daten: Bestätigungsdialog („Aktuelle Ergebnisse werden überschrieben. Fortfahren?")

## Alternativen

- **PDF-Export der Antworten:** Verworfen — nicht maschinenlesbar, kein Re-Import möglich.
- **Cloud-Sync (Dropbox, Google Drive):** Verworfen — Datenschutz, Komplexität, externe Abhängigkeiten.
- **Copy-to-Clipboard:** Verworfen — zu fehleranfällig bei langen JSONs, schwierig zu speichern.

## Konsequenzen

**Positiv:**
- Schüler:innen haben eine Sicherungskopie
- Wechsel zwischen Geräten möglich (Datei z. B. per AirDrop, Mail, USB-Stick)
- Lehrkraft kann Ergebnisse einsammeln und sichten
- Format ist menschenlesbar und langzeitstabil

**Negativ / Trade-offs:**
- Schüler:innen müssen einmal lernen, wie Export/Import funktioniert
- Auf iOS: Download landet je nach Browser unterschiedlich (Safari: „Downloads"-Ordner in iCloud; Chrome: andere Wege) → kurz erklären

**Folgewirkungen für künftige Onepager:**
- JSON-Export immer mit Schema-Version und `onepager`-Slug-Markierung
- Import muss defensiv validieren — falsches Schema oder falscher Onepager darf **nicht** zu Datenverlust führen
- Vor Import bestehender Daten: Bestätigungsdialog
- Buttons im Sticky-Menü gut sichtbar und touch-freundlich (mindestens 44×44 px)

## Verwandte ADRs

- [ADR-0002](0002-state-persistenz-localstorage.md) — localStorage als Primärspeicher
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Reset
- [ADR-0005](0005-sticky-menue-ios-safe-area.md) — Menü-Position für Buttons
