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
- [templates/onepager-boilerplate.html](templates/onepager-boilerplate.html) — Sofort einsetzbares Single-File-HTML-Template, das alle ADRs umsetzt
- [CHECKLIST.md](CHECKLIST.md) — Pre-Publish-Checkliste zum Abhaken vor Veröffentlichung jedes Onepagers

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
| [0008](adr/0008-design-system.md) | Konsistentes Design-System | Superseded by [0022](adr/0022-design-system-v2.md) |
| [0009](adr/0009-barrierefreiheit-lesbarkeit.md) | Barrierefreiheit und Lesbarkeit | Accepted |
| [0010](adr/0010-loesungs-huerde.md) | Lösungs-Hürde (gestufter Reveal: Tipp + Lösung) | Accepted |
| [0011](adr/0011-selbst-korrektur.md) | Selbst-Korrektur statt nur Lösungsvergleich | Accepted |
| [0012](adr/0012-gamification.md) | Gamification (sanft, nicht-kompetitiv) | Accepted |
| [0013](adr/0013-quiz-hardening.md) | Quiz-Hardening (Antworten nicht im Klartext) | Accepted |
| [0015](adr/0015-inhalts-boxen.md) | Inhalts-Boxen (Merke, Tipp, Achtung …) | Accepted |
| [0017](adr/0017-save-status-toast.md) | Save-Status-Indikator und Toast-Feedback | Accepted |
| [0018](adr/0018-aufgaben-karten.md) | Aufgaben-Karten — visuelle Struktur | Accepted |
| [0022](adr/0022-design-system-v2.md) | Aktualisiertes Design-System (Editorial) | Accepted |

## ADR-Status

| Status | Bedeutung |
|---|---|
| **Proposed** | Vorgeschlagen, noch nicht endgültig |
| **Accepted** | Aktiv gültig, wird angewendet |
| **Deprecated** | Nicht mehr gültig, aber noch nicht ersetzt |
| **Superseded by ADR-XXXX** | Durch neuere Entscheidung ersetzt |

## Schnellstart mit dem Boilerplate

1. [templates/onepager-boilerplate.html](templates/onepager-boilerplate.html) herunterladen oder kopieren
2. Im `<script>`-Block die Konstante `ONEPAGER_SLUG` auf einen eindeutigen Wert setzen (z. B. `'bruchrechnen-kl6-01'`)
3. `<title>`, `<h1>` und das UE-Label (Fach · Klasse · Einheit) anpassen
4. Lernziele in der `.lernziel`-Box eintragen
5. Aufgaben-Karten (`<article class="aufgabe">`) kopieren und mit Inhalten füllen
6. Jedes Eingabefeld bekommt ein eindeutiges `data-state="…"`
7. Vor Veröffentlichung [CHECKLIST.md](CHECKLIST.md) durchgehen

Das Boilerplate v2.1 (Stand 2026-05-21) bringt zusätzlich die didaktischen
Patterns aus Phase 2 mit: Lösungs-Hürde mit Tipp+Lösung ([ADR-0010](adr/0010-loesungs-huerde.md)),
Selbst-Korrektur via `data-expected` ([ADR-0011](adr/0011-selbst-korrektur.md)),
sanfter Fortschrittsbalken ([ADR-0012](adr/0012-gamification.md)) und
gehashte Quiz-Antworten ([ADR-0013](adr/0013-quiz-hardening.md)).

**Lehrer-Druck mit Lösungen:** Hänge `?solutions=1` an die URL — alle Tipps
und Lösungen werden sofort sichtbar.

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
