# Profil: Concept Map / Mindmap

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, bei dem Schüler:innen ein **Begriffsnetz** aufbauen — entweder als Mindmap, Concept Map oder semantisches Netz. Vorgegebene Begriffe werden auf einer Zeichenfläche **platziert und verbunden**, die Verbindungen werden mit dem Stift gezeichnet. Schüler:innen machen Wissensbeziehungen sichtbar.

Hauptzweck: **Wissen vernetzen statt linear sammeln** — gerade in Fächern mit komplexen Begriffsbeziehungen (Biologie, Geschichte, Politik, Religion) wertvoll.

## Typische Merkmale

- **Klassenstufe:** alle, besonders Sek I/II
- **Fachbereich:** Biologie (z. B. Ökosysteme), Geschichte (Ursachen-Wirkungs-Geflechte), Politik (Akteure), Religion (Begriffsfelder), aber auch Mathe und Sprachen
- **Zeitumfang:** 30–60 Min
- **Ziel-Typ:** Erarbeitung von Strukturen, Vernetzung, Sicherung
- **Gerät:** **iPad mit Apple Pencil** ideal — geht aber auch mit Maus oder Touch

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0019](../adr/0019-canvas-stift-modul.md) | Canvas-Modul ist die **Verbindungs-Zeichenfläche** — Knoten kommen als HTML-Layer darüber |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | Persistenz wichtig — Knoten-Positionen und Canvas-Inhalt werden zusammen gespeichert |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | HTML-Export mit eingebetteter Concept Map (inkl. Knoten-Positionen und Zeichnung) |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** Concept Maps haben selten *eine* richtige Lösung. Wenn überhaupt: eine „Beispiel-Concept-Map" am Ende, optional als Bild
- **Quiz:** nicht typisch
- **Selbst-Korrektur:** nicht für die Concept Map; bei begleitenden Verständnisfragen schon

## Spezifische didaktische Entscheidungen

### 1. Knoten-Schicht über dem Canvas

Vorgegebene Begriffe leben als **HTML-Buttons in einem Layer ÜBER dem Canvas**. Der Stift zeichnet auf dem Canvas darunter Verbindungslinien. Vorteile:

- Knoten bleiben lesbar (HTML-Text, kein Pixel)
- Knoten können verschoben werden, ohne die Verbindungen zu zerstören (Verbindungen sind nur Pixel auf dem Canvas — werden neu gezeichnet)
- Knoten-Positionen werden eigenständig persistiert

```
┌─────────────────────────────────┐
│  Begriffe (Pool):               │
│  [Photosynthese] [Chlorophyll]  │
│  [CO₂] [O₂] [Sonnenlicht]       │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│                                 │
│     ┌─[Chlorophyll]─┐           │
│     │       │       │           │
│   [CO₂]  [Photo-]  [O₂]         │
│            synthese             │
│                                 │
└─────────────────────────────────┘
```

### 2. Begriffspool vor der Karte

Über (oder neben) der Map ein **Pool mit den vorgegebenen Begriffen** — die Schüler:in zieht sie auf die Karte. Doppelklick legt einen Knoten zurück in den Pool. So bleibt die Aufgabe halbgesteuert: die Begriffe sind gegeben, die Anordnung und Verbindungen offen.

### 3. Verbindungs-Zeichnung mit dem Stift

Das Canvas-Modul aus [ADR-0019](../adr/0019-canvas-stift-modul.md) wird unverändert genutzt — Schüler:in zieht Striche zwischen Knoten. Optional: Beschriftung der Verbindung mit kleinem Text (handschriftlich oder als Inline-Eingabe daneben).

### 4. Begleit-Aufgaben rund um die Map

Zusätzlich zur Map:

- **Vorab**: „Welche Beziehung vermutest du zwischen X und Y?" (Hypothese)
- **Danach**: „Erkläre in 3 Sätzen, was deine Concept Map zeigt"
- **Reflexion**: „Welche Verbindung war für dich überraschend?"

Diese kommen als normale Aufgaben-Karten neben/unter der Map.

### 5. Fertig-Snippet

Das komplette Pattern liegt als kopierbares Snippet in [`templates/snippets/concept-map-snippet.html`](../templates/snippets/concept-map-snippet.html). Es setzt voraus, dass das Canvas-Modul aus dem Boilerplate aktiv ist.

### 6. Mobile-Tauglichkeit

Auf Smartphone schwer bedienbar (Knoten und Verbindungen brauchen Platz). Optional Hinweis im Header: „Diese Aufgabe funktioniert am besten am Tablet oder Laptop." Mindestbreite des Canvas: 600 px.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja |
| Aufgaben-Karten (Begleit-Aufgaben) | ja |
| **Concept-Map-Snippet** | **ja, Hauptmechanik** |
| Canvas-Modul aus Boilerplate | ja (Voraussetzung) |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | nur bei Begleit-Aufgaben |
| Lösungs-Hürde | optional, „Beispiel-Map" am Ende |
| Quiz | nein |
| Fortschrittsbalken | optional |
| Save-Status | **ja, prominent** |
| Toast | ja |
| JSON-Export | ja |
| **HTML-Export** | **ja, mit Knoten-Positionen** |
| Reset-Dialog | ja, mit starker Warnung |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Biologie · Klasse 8 · Photosynthese</span>
    <h1>Wie hängt alles zusammen?</h1>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Was du heute machst</span>
      Du baust ein Concept Map zur Photosynthese und zeigst die
      Beziehungen zwischen den wichtigsten Begriffen.
    </div>

    <div class="box info">
      <span class="box-title">ℹ️ So gehst du vor</span>
      <ol>
        <li>Ziehe die Begriffe aus dem Pool auf die Karte</li>
        <li>Verbinde sie mit dem Stift</li>
        <li>Beschrifte die Verbindungen (z. B. „braucht", „entsteht")</li>
      </ol>
    </div>

    <div class="concept-map">
      <div class="concept-map__pool" id="cm-pool">
        <span class="concept-map__pool-label">Begriffe</span>
        <button class="knoten is-pool" data-cm-id="n1">Photosynthese</button>
        <button class="knoten is-pool" data-cm-id="n2">Chlorophyll</button>
        <button class="knoten is-pool" data-cm-id="n3">CO₂</button>
        <button class="knoten is-pool" data-cm-id="n4">O₂</button>
        <button class="knoten is-pool" data-cm-id="n5">Sonnenlicht</button>
        <button class="knoten is-pool" data-cm-id="n6">Glukose</button>
        <button class="knoten is-pool" data-cm-id="n7">Wasser</button>
      </div>
      <div class="canvas-wrap" style="position: relative">
        <canvas data-state="cm-zeichnung" width="760" height="520"></canvas>
        <div class="knoten-layer" data-cm-state="cm-knoten"></div>
      </div>
    </div>

    <article class="aufgabe" data-task-id="cm-erklaerung">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Erklärung</span>
        <h3 class="aufgabe__titel">Beschreibe deine Concept Map in 3 Sätzen</h3>
      </header>
      <div class="aufgabe__body">
        <textarea data-state="cm-erklaerung-text" rows="4"></textarea>
      </div>
    </article>
  </div>
</article>
```

## Anti-Patterns

- **Zu viele Knoten (> 15)** → unübersichtlich, schwer zu vernetzen
- **Lösungs-Map zeigen, bevor Schüler:in selbst denkt** → keine eigene Vernetzung
- **Concept Map ohne begleitende Erklärungs-Aufgabe** → Schüler:in sieht das eigene Werk nicht reflektiert
- **Ohne vorgegebene Begriffe** → wird zu offen; mit Pool ist die Aufgabe besser fokussiert
- **Verbindungen nicht beschriften** → Beziehungstypen bleiben unklar (z. B. „braucht" vs. „entsteht")
- **Statt Canvas Mind-Mapping-Library einbinden** → externe Abhängigkeit, verletzt ADR-0001

## Verwandte Profile

- [`profiles/digitales-arbeitsheft.md`](digitales-arbeitsheft.md) — Verwandt durch Canvas-Eingabe, aber ohne strukturierte Knoten
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Eine Concept Map kann Teil einer größeren Erarbeitung sein, z. B. in der Sicherungs-Phase
- [`profiles/lektuere.md`](lektuere.md) — Eine Concept Map zu den Figurenbeziehungen eines Romans ist ein typischer Einsatz
