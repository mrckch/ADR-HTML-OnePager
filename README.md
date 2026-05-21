# ADR — HTML-Onepager für den Unterricht

Eine Sammlung von **Architecture Decision Records (ADRs)** für HTML-Onepager, die im schulischen Kontext erstellt und an Schüler:innen verteilt werden.

Das Repository ist eine **Vorlage**: Du kannst es forken, einzelne ADRs übernehmen oder dich davon inspirieren lassen, wenn du selbst HTML-Materialien für den Unterricht baust.

## Hintergrund

HTML-Onepager als digitales Handout (per Link verteilt, im Browser geöffnet) haben viele Vorteile: schnell verteilbar, auf jedem Gerät lauffähig, interaktiv möglich. Beim wiederholten Erstellen tauchen aber dieselben Fragen immer wieder auf: Wie speichern wir Schülerergebnisse? Wie sieht das auf dem iPhone aus? Was passiert beim Ausdrucken?

Hier sind die Antworten dokumentiert — als bewusste, begründete Entscheidungen.

## Was sind ADRs?

Ein **Architecture Decision Record** ist eine kurze Markdown-Datei pro Entscheidung. Sie hält fest:

- **Kontext** — Worum geht es, welches Problem liegt vor?
- **Entscheidung** — Was wurde konkret entschieden?
- **Alternativen** — Was wurde sonst noch erwogen?
- **Konsequenzen** — Was bedeutet das für künftige Arbeit?

So bleibt nachvollziehbar, *warum* etwas so gebaut wird wie es gebaut wird — auch Monate später oder für andere Personen.

## Verteilungs-Annahme

Die hier dokumentierten Entscheidungen gehen davon aus, dass die Onepager **auf einem Webhoster liegen und per Link verteilt werden**. Schüler:innen öffnen sie im Browser auf Smartphone (oft iOS), Tablet oder Laptop. Es gibt kein Backend, keine Build-Pipeline, kein eingeloggtes Nutzerkonto.

Wenn dein Setup anders ist (z. B. lokal verteilte Dateien, Moodle-Einbettung, eigener Server), prüfe die ADRs entsprechend.

## Aufbau

- [adr/](adr/) — Alle Entscheidungen, je eine Markdown-Datei pro Entscheidung
- [adr/template.md](adr/template.md) — Vorlage für neue ADRs
- [adr/0001-…](adr/) ff. — Die einzelnen Entscheidungen, fortlaufend nummeriert

## Übersicht der Entscheidungen

| Nr. | Titel | Status |
|---|---|---|
| [0001](adr/0001-single-file-html-architektur.md) | Single-File-HTML-Architektur | Accepted |
| [0002](adr/0002-state-persistenz-localstorage.md) | State-Persistenz im localStorage | Accepted |
| [0003](adr/0003-json-export-import.md) | JSON-Export und -Import für Schülerergebnisse | Accepted |
| [0004](adr/0004-reset-funktion-mit-bestaetigung.md) | Reset-Funktion mit Bestätigungsdialog | Accepted |
| [0005](adr/0005-sticky-menue-ios-safe-area.md) | Sticky Top-Menü mit iOS Safe-Area-Beachtung | Accepted |
| [0006](adr/0006-responsives-layout.md) | Responsives Mobile-First-Layout | Accepted |
| [0007](adr/0007-druck-pdf-optimierung.md) | Druck- und PDF-Optimierung (A4) | Accepted |
| [0008](adr/0008-design-system.md) | Konsistentes Design-System | Accepted |
| [0009](adr/0009-barrierefreiheit-lesbarkeit.md) | Barrierefreiheit und Lesbarkeit | Accepted |

## ADR-Status

| Status | Bedeutung |
|---|---|
| **Proposed** | Vorgeschlagen, noch nicht endgültig |
| **Accepted** | Aktiv gültig, wird angewendet |
| **Deprecated** | Nicht mehr gültig, aber noch nicht ersetzt |
| **Superseded by ADR-XXXX** | Durch neuere Entscheidung ersetzt |

## Wie du dieses Repo nutzen kannst

**Als Inspiration** — ADRs lesen, einzelne Entscheidungen für eigene Projekte übernehmen, andere verwerfen.

**Als Fork** — Repository forken, ADRs an den eigenen Kontext anpassen, weitere Entscheidungen ergänzen. Deine Forks dürfen, müssen aber nicht hierher zurückverlinken.

**Mitwirken** — Verbesserungsvorschläge per Issue oder Pull Request sind willkommen. Bitte begründe Vorschläge so, dass sie zum ADR-Format passen (Kontext, Alternativen, Konsequenzen).

## Neue ADR anlegen

1. [adr/template.md](adr/template.md) kopieren
2. Nächste freie Nummer vergeben (4-stellig, z. B. `0010-…`)
3. Dateinamen kebab-case (`0010-thema-der-entscheidung.md`)
4. Eintrag in die Übersicht oben ergänzen

## Lizenz

Dieses Werk steht unter der [Creative Commons Namensnennung 4.0 International Lizenz (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.de).

Du darfst die Inhalte teilen, anpassen und auch kommerziell nutzen — solange du die ursprüngliche Quelle nennst. Siehe [LICENSE](LICENSE) für den vollständigen Lizenztext.
