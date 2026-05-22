# Profil: Vokabel-/Wortschatz-Onepager

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager zum **Wortschatz-Training** in Fremdsprachen (Englisch, Französisch, Latein, Spanisch …) oder zum **Fachvokabular-Lernen** (z. B. Begriffe aus Biologie, Geschichte, Musik).

Hauptmechanik: **Karteikarten** — Vorderseite zeigt das Wort/den Begriff, Hinterseite die Übersetzung/Definition. Schüler:innen testen sich selbst, indem sie die Hinterseite **verdecken** und prüfen, ob sie die Übersetzung kennen.

## Typische Merkmale

- **Klassenstufe:** alle Sprach-Lerner ab Grundschule
- **Fachbereich:** Fremdsprachen (Hauptfall), Fachsprachen, Begriffslernen
- **Zeitumfang:** 10–20 Minuten pro Session; Onepager wird wiederholt aufgerufen
- **Ziel-Typ:** Üben, Auswendiglernen, Festigung
- **Gerät:** alle, besonders Smartphone (oft nebenbei genutzt — Bus, Pause)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0006](../adr/0006-responsives-layout.md) | **Smartphone-optimiert** — Vokabel-Lernen passiert oft mobil. Karten müssen einhändig bedienbar sein |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) | „Welche Vokabel kann ich, welche nicht?" wird gespeichert (z. B. mit Marker „weiß ich" / „muss ich noch üben") |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur ist hier **selbst-gesteuert** (Schüler bestätigt selbst, ob er es wusste — kein automatischer Abgleich) |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0018](../adr/0018-aufgaben-karten.md):** keine klassischen Aufgaben-Karten — stattdessen Vokabel-Listen mit Flip-Karten
- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** umgedreht — die „Lösung" (Übersetzung) ist das, was man lernen will. Flip statt Hürde
- **Quiz:** möglich, aber Karteikarten sind die Hauptmechanik
- **Canvas:** nicht relevant

## Spezifische didaktische Entscheidungen

### 1. Karteikarten-Pattern: Flip oder Verdecken

Zwei Standard-Varianten:

**a) Flip-Karte (Karte dreht sich)**

```html
<div class="vokabel-karte" data-state-id="v1">
  <button class="vokabel-flip" data-state="v1-revealed" aria-expanded="false">
    <span class="vokabel-vorderseite">to embark</span>
    <span class="vokabel-rueckseite">an Bord gehen, beginnen</span>
  </button>
</div>
```

Klick toggelt Vorder-/Rückseite. State (revealed: true/false) wird gespeichert — nach Reload sieht man, welche Karten man schon umgedreht hat.

**b) Verdecken-Liste (komplette Liste, Übersetzungen einzeln aufdeckbar)**

```html
<ol class="vokabel-liste">
  <li>
    <span class="vokabel-wort">to embark</span>
    <button class="vokabel-toggle" data-state="v1-revealed" aria-expanded="false">
      Übersetzung zeigen
    </button>
    <span class="vokabel-uebersetzung" hidden>an Bord gehen</span>
  </li>
  …
</ol>
```

Empfehlung: **Flip-Karte für kleine Mengen (≤ 15)**, **Liste für größere Mengen (> 15)**.

### 2. Selbst-Markierung „weiß / weiß noch nicht"

Jede Vokabel bekommt zwei Buttons:

```html
<div class="vokabel-feedback">
  <button data-state="v1-kannt-ich" data-value="true">✓ Wusste ich</button>
  <button data-state="v1-kannt-ich" data-value="false">○ Muss ich noch üben</button>
</div>
```

Schüler:in markiert ehrlich nach dem Aufdecken. Der Onepager kann dann eine **„noch zu üben"-Filter-Ansicht** anbieten.

### 3. Filter-Buttons

Im Topbar oder direkt über der Vokabel-Liste:

| Filter | Anzeige |
|---|---|
| Alle | alle Vokabeln |
| ✓ Kann ich | nur grün markierte |
| ○ Übe ich | nur „noch zu üben" |
| ◯ Unbearbeitet | nur Vokabeln ohne Markierung |

Der Filter-Status wird **nicht persistiert** (default: alle), damit nach Reload alle Vokabeln sichtbar sind.

### 4. Shuffle-Button

Beim Lernen Reihenfolge variieren — Schüler:innen sollen nicht „Position 3" auswendig lernen:

```html
<button id="shuffle">🔀 Reihenfolge mischen</button>
```

JS shuffelt das DOM mit Fisher-Yates. Originale Reihenfolge wird im DOM nicht zerstört (sondern via CSS `order`-Property auf die Listenelemente gesetzt), damit Reset einfach ist.

### 5. Beispielsatz pro Vokabel optional

Vokabeln in Kontext lernen ist effektiver als isolierte Wörter. Eine zusätzliche „Beispielsatz"-Zeile kann optional aufgeklappt werden:

```html
<details class="vokabel-beispiel">
  <summary>Beispielsatz</summary>
  <p><em>The ship will embark at noon.</em></p>
</details>
```

Hier ist `<details>` OK, weil der Beispielsatz keine „Lösung" ist, sondern Bonus-Info.

### 6. Lernrichtung umschaltbar

Manche Schüler:innen wollen erst die Übersetzung sehen und das Wort raten:

```html
<nav class="lern-richtung" role="radiogroup" aria-label="Lernrichtung">
  <label><input type="radio" name="richtung" value="fremd-deutsch" checked> Fremdsprache → Deutsch</label>
  <label><input type="radio" name="richtung" value="deutsch-fremd"> Deutsch → Fremdsprache</label>
</nav>
```

Bei Wechsel werden Vorder-/Rückseite ausgetauscht. Wahl persistiert in localStorage.

### 7. Smartphone-First

Karten sind **groß genug für Einhandbedienung** (mind. 80 px hoch, gut tappbar). Topbar sehr kompakt. Keine Tabellen — Listen.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | optional (eine Zeile genügt: „Diese Vokabeln lernst du") |
| Aufgaben-Karten | nein (Vokabel-Karten haben eigene Struktur) |
| **Vokabel-Karten / -Liste** | **ja, Hauptmechanik** |
| **„Kann ich" / „Üben"-Marker** | **ja** |
| **Filter-Buttons** | **ja** |
| **Shuffle-Button** | ja |
| **Lernrichtung-Wahl** | ja |
| Selbst-Korrektur (`data-expected`) | nein — Schüler:in beurteilt selbst |
| Lösungs-Hürde | nein (Flip ist die „Hürde") |
| Quiz | optional am Ende — als Selbsttest |
| Canvas | nein |
| Fortschrittsbalken | ja, bezogen auf bearbeitete Vokabeln |
| Save-Status | ja |
| Toast | ja |
| JSON-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Englisch · Klasse 7 · Unit 3</span>
    <h1>Vokabeln Unit 3 — Travel & Holidays</h1>
  </header>
  <div class="content">

    <nav class="lern-richtung" role="radiogroup" aria-label="Lernrichtung">
      <label><input type="radio" name="richtung" data-state="richtung" value="en-de" checked> 🇬🇧 → 🇩🇪</label>
      <label><input type="radio" name="richtung" data-state="richtung" value="de-en"> 🇩🇪 → 🇬🇧</label>
    </nav>

    <div class="vokabel-filter" role="group" aria-label="Filter">
      <button data-filter="all"     aria-pressed="true">Alle</button>
      <button data-filter="kannt"   aria-pressed="false">✓ Kann ich</button>
      <button data-filter="uebe"    aria-pressed="false">○ Übe ich</button>
      <button data-filter="neu"     aria-pressed="false">◯ Neu</button>
    </div>

    <button id="shuffle" class="btn">🔀 Reihenfolge mischen</button>

    <ol class="vokabel-liste">
      <li class="vokabel-eintrag" data-vokabel-id="v1">
        <button class="vokabel-flip" data-state="v1-revealed" aria-expanded="false">
          <span class="vokabel-vorderseite">to embark</span>
          <span class="vokabel-rueckseite" hidden>an Bord gehen, beginnen</span>
        </button>
        <details class="vokabel-beispiel">
          <summary>Beispielsatz</summary>
          <p><em>The ship will embark at noon.</em></p>
        </details>
        <div class="vokabel-feedback" role="group">
          <button data-state="v1-marker" data-value="kannt">✓ Wusste ich</button>
          <button data-state="v1-marker" data-value="uebe">○ Übe ich</button>
        </div>
      </li>
      <!-- weitere Vokabeln … -->
    </ol>
  </div>
</article>
```

## Anti-Patterns

- **Vokabel und Übersetzung gleichzeitig sichtbar** → kein Lerneffekt
- **Automatisches Aufdecken nach Zeit** → nimmt Selbst-Steuerung
- **Quiz-Auswertung mit „70 % geschafft"** → erzeugt Druck, Vokabel-Lernen soll niedrig-schwellig sein
- **Tabellen-Layout** → bricht auf Smartphone und ist schlecht touch-bedienbar
- **Lange Wortlisten ohne Mischen** → Schüler:innen lernen Position statt Wort
- **Latein-Stammformen alle in einer Zeile** → besser pro Vokabel-Karte eigene Sektionen für Grundform, Genitiv, Geschlecht etc.

## Verwandte Profile

- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn der Vokabel-Onepager auch eine Reflexions-Zeile am Ende haben soll
- [`profiles/kompetenzraster.md`](kompetenzraster.md) — Für eine grobe Selbst-Einschätzung „Wie sicher fühle ich mich bei Unit-Vokabeln?" am Ende
