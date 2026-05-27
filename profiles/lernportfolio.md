# Profil: Lernportfolio

- **Status:** Accepted — Implementation verfügbar via ADR-0025
- **Datum:** 2026-05-22 (Status-Update: 2026-05-27)
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

> ✅ **Implementiert**: Listen-basierte Persistenz ist seit [ADR-0025](../adr/0025-lernportfolio-persistenz.md) als Schema v2 verfügbar. Snippet: [`templates/snippets/lernportfolio-eintraege-snippet.html`](../templates/snippets/lernportfolio-eintraege-snippet.html). Demo: [`examples/lernportfolio-halbjahr.html`](../examples/lernportfolio-halbjahr.html).

## Was ist das?

Ein Onepager als **persönliches Lernportfolio** — eine Sammelmappe, die Schüler:innen über eine längere Zeit (Wochen, Monate, ganzes Halbjahr) führen. Im Unterschied zum [Reflexionstagebuch](reflexionstagebuch.md) (das primär reflektierend ist) und zum [Lektüre-Tagebuch](lektuere.md) (das einem konkreten Buch folgt), ist das Lernportfolio:

- **frei strukturierbar** — Schüler:in entscheidet, was reinkommt
- **langlebig** — über Halbjahre, ganze Schuljahre
- **sammelnd** — Texte, Skizzen, Reflexionen, Bilder, Quellen — alles, was gelernt wurde

Typisch eingesetzt in:
- **„Mein Lernweg" in Klassen 5-10** (Halbjahres-Portfolio)
- **Sprachen-Portfolio** (was habe ich in Englisch dazugelernt?)
- **Wahlpflicht-Projekten** (z. B. Sportler-Portfolio, Theater-Portfolio)
- **Berufsorientierung** in Sek I (späte)

## Typische Merkmale

- **Klassenstufe:** alle (besonders Sek I)
- **Fachbereich:** alle, häufig in Klassenleitung-/Tutoren-Kontext
- **Zeitumfang:** **Wochen bis ganze Schuljahre**
- **Ziel-Typ:** Sammeln, Reflektieren, Wachstum sichtbar machen
- **Gerät:** Laptop oder Tablet — wird über lange Zeit immer wieder geöffnet

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0025](../adr/0025-lernportfolio-persistenz.md) | **Persistenz absolut kritisch**, Schema v2 mit `_eintraege`-Array |
| [ADR-0003](../adr/0003-json-export-import.md) | Primärer Übergabe-Mechanismus statt großer HTML-Exports |
| [ADR-0019](../adr/0019-canvas-stift-modul.md) | Canvas-Einträge möglich (Skizzen, Mindmaps zu einem Thema) |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | **Regelmäßige HTML-Exporte als Backup**, evtl. monatlich |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save-Status besonders prominent |

## Persistenz-Schema (ADR-0025)

Der Standard-State wird um ein optionales `_eintraege`-Array erweitert:

```js
{
  version: 2,
  data: {
    // Meta-Felder (wie in v1)
    name: "Anna", klasse: "8a", start: "2026-02-01",
    // Liste der Einträge (neu in v2)
    _eintraege: [
      { id: "e1717238400000", datum: "2026-05-22", typ: "reflexion",
        titel: "Erste Mathearbeit", inhalt: "…", tags: ["mathe", "klassenarbeit"] },
      { id: "e1717324800000", datum: "2026-05-25", typ: "lernprodukt",
        titel: "Mindmap Photosynthese", inhalt: "data:image/png;base64,…", tags: ["bio"] }
    ]
  }
}
```

Migration v1 → v2 ist **additiv und trivial** — bestehende Onepager funktionieren weiter. Details in [ADR-0025](../adr/0025-lernportfolio-persistenz.md).

## Spezifische didaktische Entscheidungen

### 1. Drei Eintrags-Typen

| Typ | Inhalt | UI-Element |
|---|---|---|
| **Reflexion** | Freier Text — „Was habe ich gelernt? Was war schwer?" | `<textarea>` |
| **Lernprodukt** | Eine Skizze, ein Aufsatz, eine Mindmap | `<textarea>` oder Canvas-Snippet |
| **Quelle / Notiz** | Link, Zitat, Beleg, „dort habe ich es gelesen" | Strukturierter Input |

Pro Eintrag kann der Typ **nicht** nachträglich gewechselt werden — siehe ADR-0025.

### 2. Tags pro Eintrag

Jeder Eintrag kann mit **Tags** versehen werden (z. B. „mathe", „klasse-8", „experiment", „bestehen"). Der Tag-Filter über der Liste zeigt Tags **mit Häufigkeit** und macht das Portfolio durchsuchbar.

### 3. Profil-Header am Anfang

Statt der typischen Aufgaben-Struktur: ein **persönliches Profil** am Anfang (Name, Klasse, Start-Datum) sowie eine Statistik-Zeile aus den Einträgen:

```
📊 23 Einträge · 5 Tags · letzter Eintrag: 22.05.2026
```

### 4. Chronologische Sortierung

Einträge sind standardmäßig **neueste zuerst** sortiert — der letzte Lernschritt steht oben.

### 5. HTML-Export als „Jahresbuch"

Am Ende des Schuljahres exportiert die Schüler:in das Portfolio als HTML — wird zum bleibenden Erinnerungsstück. Mit dem PDF-Export-Snippet ([ADR-0021](../adr/0021-pdf-export-inline.md)) entsteht ein druckbares Jahres-Heft.

### 6. Datenschutz besonders sensibel

Ein Lernportfolio kann sehr persönliche Inhalte enthalten. Hinweise:
- **Default: privat** — nur Schüler:in sieht es
- Lehrkraft sieht NUR, wenn explizit per HTML-Export geteilt
- Reset-Dialog mit **doppelter Bestätigung** und Warnung „Das Werk eines ganzen Halbjahres wird gelöscht"
- HTML-Export-Reminder: alle paar Wochen, mit Hinweis „auf USB-Stick oder iCloud sichern"

### 7. Speicher-Limits beachten

Bei vielen Canvas-Lernprodukten kann die `localStorage`-Größe (5–10 MB) ein Limit werden. Empfehlungen:
- Skizzen komprimieren (Canvas in moderater Auflösung)
- Regelmäßiger JSON-Export
- Bei sehr großen Portfolios: monatlich „abschließen" und als HTML archivieren

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Profil-Header | ja |
| **Liste-basierte Einträge** (Snippet `lernportfolio-eintraege-snippet.html`) | **ja, Hauptmechanik** |
| Tags / Filter | ja (im Snippet enthalten) |
| Aufgaben-Karten | nein (Einträge sind individuell, nicht aufgabenartig) |
| Canvas-Modul | ja (für Skizzen-Einträge) |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | nein |
| Lösungs-Hürde | nein |
| Quiz | nein |
| Fortschrittsbalken | optional, eher als „X Einträge bisher" |
| Save-Status | **ja, prominent** |
| Toast | ja |
| JSON-Export | **ja, primärer Übergabe-Mechanismus** |
| **HTML-Export** | **ja, regelmäßig empfohlen** |
| Reset-Dialog | ja, mit **doppelter Bestätigung** |

## Implementations-Hinweis

Das Snippet `templates/snippets/lernportfolio-eintraege-snippet.html` enthält:
- CSS für Toolbar, Tag-Filter, Eintrags-Karten (mit Typ-Farben)
- CRUD-Funktionen `addEintrag()`, `removeEintrag()`, `updateEintrag()`, `getEintraege()`
- `renderEintraege()` mit Tag-Filter und chronologischer Sortierung
- Event-Delegation für Input-Felder und Lösch-Buttons
- Schema-Migration v1 → v2

Vollständige Demo: [`examples/lernportfolio-halbjahr.html`](../examples/lernportfolio-halbjahr.html).

## Anti-Patterns

- **Strenge Aufgabenstruktur erzwingen** → Lernportfolio ist offen, nicht aufgabengetrieben
- **Pflicht-Mindestanzahl von Einträgen** → erzeugt Pflichtgefühl, das gegen die Idee arbeitet
- **Bewertung durch die Lehrkraft** (Noten auf einzelne Einträge) → tötet Authentizität
- **Lehrer-Einsicht ohne Schüler-Zustimmung** → Datenschutz-Verletzung
- **Kein HTML-Export-Reminder** → wochenlange Arbeit kann verloren gehen
- **Eintrags-Typ nachträglich ändern** → Inhalt geht verloren (siehe ADR-0025)

## Verwandte Profile

- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Strukturell verwandt, aber kürzer und reiner reflektierend
- [`profiles/lektuere.md`](lektuere.md) — Verwandt durch lange Lebensdauer, aber an ein Buch gebunden
- [`profiles/kompetenzraster.md`](kompetenzraster.md) — Komplementär: Raster für quantitative Selbst-Einschätzung, Portfolio für qualitative Sammlung

## Status der Implementation

| Aspekt | Status |
|---|---|
| Konzept dokumentiert | ✅ |
| Listen-basierte Persistenz (ADR-0025) | ✅ |
| Eintrags-Typen / Tags / Filter | ✅ |
| Spezifisches Snippet | ✅ `lernportfolio-eintraege-snippet.html` |
| Demo | ✅ `examples/lernportfolio-halbjahr.html` |
| Schema-Migration v1 → v2 | ✅ Im Snippet implementiert |
