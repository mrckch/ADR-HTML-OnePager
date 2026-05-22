# Profil: Lernportfolio (Advanced)

- **Status:** Accepted — Profil-Skizze, Implementation als Folgephase
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

> ⚠️ **Advanced-Profil**: Anders als die anderen Profile braucht das Lernportfolio eine **erweiterte Persistenz-Strategie** (mehrere Sessions, datums-basierte Einträge). Diese ist im aktuellen Boilerplate noch nicht standardisiert. Profil-Doku bleibt deshalb bewusst auf konzeptioneller Ebene — Implementation folgt mit einer eigenen ADR.

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
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | **Persistenz absolut kritisch**, plus erweitertes Schema (siehe unten) |
| [ADR-0019](../adr/0019-canvas-stift-modul.md) | Canvas-Einträge möglich (Skizzen, Mindmaps zu einem Thema) |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | **Regelmäßige HTML-Exporte als Backup**, evtl. monatlich |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save-Status besonders prominent |

## Erweiterte Persistenz-Konzepte (Skizze, noch nicht implementiert)

Anders als die bisherigen Profile, die einen flachen State haben, braucht das Lernportfolio:

1. **Liste von Einträgen** statt fester Felder
2. **Datums-Stempel pro Eintrag**
3. **Eintrags-Typen** (Text-Notiz, Reflexion, Skizze, Quelle, …)
4. **„Neuen Eintrag anlegen"-Mechanik** statt fester HTML-Vorlage

Schema-Skizze:

```js
{
  version: 1,
  data: {
    eintraege: [
      { id: "e1", datum: "2026-05-22", typ: "reflexion", inhalt: "...", tags: ["mathe", "geometrie"] },
      { id: "e2", datum: "2026-05-29", typ: "skizze",    inhalt: "data:image/png;base64,...", tags: ["bio"] },
      …
    ],
    profil: { name: "...", klasse: "...", start: "2026-02-01" }
  }
}
```

Implementierungsaufwand: ein **Eintrags-Modul** mit dynamischem DOM-Aufbau, dazu CRUD-UI (anlegen, bearbeiten, löschen). Das ist eine **eigene ADR** wert — voraussichtlich **ADR-0025: Liste-basierte Persistenz für Lernportfolio**.

## Spezifische didaktische Entscheidungen (konzeptionell)

### 1. Drei Eintrags-Typen

| Typ | Inhalt |
|---|---|
| **Reflexion** | Freier Text — „Was habe ich gelernt? Was war schwer?" |
| **Lernprodukt** | Eine Skizze, ein Aufsatz, eine Mindmap — als Canvas oder als längerer Text |
| **Quelle / Notiz** | Link, Zitat, Beleg, „dort habe ich es gelesen" |

### 2. Tags pro Eintrag

Schüler:in kann jeden Eintrag mit **Tags** versehen (z. B. „mathe", „klasse-8", „experiment", „bestehen"). Filter macht das Portfolio durchsuchbar.

### 3. Profil-Header am Anfang

Statt der typischen Aufgaben-Struktur: ein **persönliches Profil** am Anfang:

```html
<header class="portfolio-header">
  <h1>Mein Lernportfolio</h1>
  <p>Anna · Klasse 8a · seit 01.02.2026</p>
  <p class="stats">23 Einträge · 5 Tags · letzter Eintrag: 22.05.2026</p>
</header>
```

### 4. Zeitleiste statt Sektion-Struktur

Einträge sind chronologisch sortiert (neuester zuerst oder ältester zuerst — Schüler:in wählt). Visuell wie eine Timeline.

### 5. HTML-Export als „Jahresbuch"

Am Ende des Schuljahres exportiert die Schüler:in das Portfolio als HTML — wird zum bleibenden Erinnerungsstück. Mit dem PDF-Export-Snippet ([ADR-0021](../adr/0021-pdf-export-inline.md)) entsteht ein druckbares Jahres-Heft.

### 6. Datenschutz besonders sensibel

Ein Lernportfolio kann sehr persönliche Inhalte enthalten. Hinweise:
- **Default: privat** — nur Schüler:in sieht es
- Lehrkraft sieht NUR, wenn explizit per HTML-Export geteilt
- Reset-Dialog mit **doppelter Bestätigung** und Warnung „Das Werk eines ganzen Halbjahres wird gelöscht"
- HTML-Export-Reminder: alle paar Wochen, mit Hinweis „auf USB-Stick oder iCloud sichern"

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Profil-Header | ja |
| **Liste-basierte Einträge** (in Folgephase) | **ja, Hauptmechanik** |
| Tags / Filter | ja |
| Aufgaben-Karten | nein (Einträge sind individuell, nicht aufgabenartig) |
| Canvas-Modul | ja (für Skizzen-Einträge) |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | nein |
| Lösungs-Hürde | nein |
| Quiz | nein |
| Fortschrittsbalken | optional, eher als „X Einträge bisher" |
| Save-Status | **ja, prominent** |
| Toast | ja |
| JSON-Export | ja |
| **HTML-Export** | **ja, regelmäßig empfohlen** |
| Reset-Dialog | ja, mit **doppelter Bestätigung** |

## Empfohlener Workflow (auch ohne fertiges Modul)

Bis das volle Listen-Persistenz-Modul kommt, kann das Profil **provisorisch** als Erweiterung des [Reflexionstagebuch-Profils](reflexionstagebuch.md) realisiert werden:

- Vorab eine **feste Anzahl von Eintrags-Slots** (z. B. 30) im HTML anlegen
- Jeder Slot hat Datum, Typ-Dropdown, Inhalts-Textarea, Tags-Input
- Schüler:in nutzt die Slots der Reihe nach

Das ist hässlich, aber funktioniert.

## Anti-Patterns

- **Strenge Aufgabenstruktur erzwingen** → Lernportfolio ist offen, nicht aufgabengetrieben
- **Pflicht-Mindestanzahl von Einträgen** → erzeugt Pflichtgefühl, das gegen die Idee arbeitet
- **Bewertung durch die Lehrkraft** (Noten auf einzelne Einträge) → tötet Authentizität
- **Lehrer-Einsicht ohne Schüler-Zustimmung** → Datenschutz-Verletzung
- **Kein HTML-Export-Reminder** → wochenlange Arbeit kann verloren gehen

## Verwandte Profile

- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Strukturell verwandt, aber kürzer und reiner reflektierend
- [`profiles/lektuere.md`](lektuere.md) — Verwandt durch lange Lebensdauer, aber an ein Buch gebunden
- [`profiles/kompetenzraster.md`](kompetenzraster.md) — Komplementär: Raster für quantitative Selbst-Einschätzung, Portfolio für qualitative Sammlung

## Status der Implementation

| Aspekt | Status |
|---|---|
| Konzept dokumentiert | ✅ |
| Vereinfachte Variante (feste Slots) machbar | ✅ — als Erweiterung Reflexionstagebuch |
| Listen-basierte Persistenz | ⏳ Folgephase (ADR-0025 geplant) |
| Eintrags-Typen / Tags / Filter | ⏳ Folgephase |
| Spezifisches Snippet | ⏳ Folgephase |

Wenn du dieses Profil dringend brauchst: melde dich per Issue, dann priorisieren wir die Implementierung.
