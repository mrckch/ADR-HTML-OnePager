# Profil: Lerntheke / Selbstdifferenzierung

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **Aufgaben-Pool**: 8–15 Aufgaben, aus denen Schüler:innen **selbst auswählen**, was sie wann bearbeiten. Mit Markierungen für **Pflicht** (alle bearbeiten), **Wahl** (mind. X aus Y) und **Vertiefung** (für Schnelle / Interessierte). Selbstgesteuertes Arbeiten in eigener Reihenfolge und eigenem Tempo.

Im Unterschied zum **Differenzierungs-Onepager** (drei parallele Niveaus für *die gleiche* Aufgabe) bietet die Lerntheke **viele verschiedene Aufgaben** mit unterschiedlichen Anforderungen.

## Typische Merkmale

- **Klassenstufe:** alle, besonders Sek I/II
- **Fachbereich:** alle, häufig Mathe, NaWi, Sprachen
- **Zeitumfang:** Doppelstunde bis mehrere Stunden
- **Ziel-Typ:** Übung, Anwendung, selbstgesteuertes Lernen
- **Gerät:** Laptop, Tablet

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Karten **mit Typ-Marker** (Pflicht/Wahl/Vertiefung) und Status-Buttons |
| [ADR-0010](../adr/0010-loesungs-huerde.md) + [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur und Lösungs-Hürde — Standard |
| [ADR-0012](../adr/0012-gamification.md) | Fortschritts-Anzeige **gewichtet nach Pflicht-Anteil** |

## Core-ADRs abweichend oder weniger relevant

- **Quiz:** typischerweise nicht
- **Canvas:** je nach Fach optional
- **Gating:** **nicht**, weil Selbst-Steuerung der Kern ist

## Spezifische didaktische Entscheidungen

### 1. Drei Aufgaben-Typen

| Typ | Marker | Bedeutung |
|---|---|---|
| **Pflicht** | ⊕ rot | Müssen ALLE bearbeitet werden |
| **Wahl** | ⊙ gold | Eine Auswahl davon — Lehrkraft sagt z. B. „3 aus 5" |
| **Vertiefung** | ⊛ blau | Optional, für Schnelle und Interessierte |

Visuell unterscheiden sich die Karten an der **Top-Border-Farbe** (statt der einheitlichen goldenen). So sehen Schüler:innen auf einen Blick, welcher Aufgaben-Typ es ist.

### 2. Filter-Toolbar oben

Eine Toolbar oberhalb der Aufgaben mit Filter-Buttons:

```html
<div class="lerntheke-toolbar">
  <div class="lerntheke-filter">
    <button data-lt-filter="all"        aria-pressed="true">Alle</button>
    <button data-lt-filter="pflicht"    aria-pressed="false">⊕ Pflicht</button>
    <button data-lt-filter="wahl"       aria-pressed="false">⊙ Wahl</button>
    <button data-lt-filter="vertiefung" aria-pressed="false">⊛ Vertiefung</button>
    <button data-lt-filter="offen"      aria-pressed="false">Offen</button>
    <button data-lt-filter="erledigt"   aria-pressed="false">✓ Erledigt</button>
  </div>
  <span class="lerntheke-stats">3 / 5 Pflicht erledigt</span>
</div>
```

Schüler:in fokussiert sich auf einen Typ oder filtert auf „offen".

### 3. Status pro Aufgabe: erledigt / übersprungen

Am Ende jeder Aufgabe **zwei Buttons**:
- ✓ **Erledigt** — Aufgabe als bearbeitet markieren
- ⤳ **Übersprungen** — bewusst nicht bearbeitet (z. B. weil zu schwer oder schon klar)

Die Auswahl bleibt persistiert. Beim Filter „Offen" verschwinden alle, die einen Status haben.

### 4. Fortschritt gewichtet nach Pflicht

Der Standard-Fortschrittsbalken aus ADR-0012 zeigt für die Lerntheke etwas Spezielles: **„X / Y Pflicht erledigt"** statt „X / Y Aufgaben bearbeitet". Pflicht ist das, was wirklich zählt.

Wenn man auch Wahl-Aufgaben tracken will: zwei Zähler nebeneinander.

### 5. Reihenfolge ist frei

Anders als bei der **Erarbeitungsseite** (Gating) gibt es **kein** Schloss. Schüler:in entscheidet, in welcher Reihenfolge sie arbeitet — Lerntheke ist explizit „selbstgesteuert".

### 6. Lerntheke-Übersicht am Anfang

Eine Info-Box, die Erwartungen klar macht:

```html
<div class="box info">
  <span class="box-title">ℹ️ Lerntheke — so funktioniert's</span>
  <ul>
    <li><strong>⊕ Pflicht-Aufgaben</strong>: musst du alle bearbeiten</li>
    <li><strong>⊙ Wahl-Aufgaben</strong>: bearbeite mindestens 3 von 5</li>
    <li><strong>⊛ Vertiefung</strong>: optional, wenn du schon fertig bist</li>
    <li>Du wählst die Reihenfolge selbst</li>
  </ul>
</div>
```

Die genauen Zahlen (3 aus 5 etc.) gibt die Lehrkraft an.

### 7. Fertig-Snippet

Komplettes Pattern in [`templates/snippets/lerntheke-snippet.html`](../templates/snippets/lerntheke-snippet.html) — Toolbar, Filter-Logik, Status-Buttons, Statistik.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja, mit klaren Auswahl-Vorgaben |
| **Lerntheke-Toolbar** | **ja, Hauptelement** |
| Aufgaben-Karten mit Typ-Marker | **ja** |
| **Status-Buttons pro Aufgabe** | **ja** |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | ja |
| Lösungs-Hürde | ja, Standard |
| Quiz | nein |
| Canvas | optional |
| **Fortschritt gewichtet nach Pflicht** | **ja** |
| Save-Status | ja |
| Toast | ja |
| JSON/HTML-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathematik · Klasse 7 · Lerntheke</span>
    <h1>Bruchrechnung üben — wähle selbst</h1>
  </header>

  <div class="content">
    <div class="box info">
      <span class="box-title">ℹ️ So funktioniert's</span>
      <ul>
        <li><strong>⊕ Pflicht</strong> (alle bearbeiten)</li>
        <li><strong>⊙ Wahl</strong> (mindestens 2 aus 3)</li>
        <li><strong>⊛ Vertiefung</strong> (optional)</li>
      </ul>
    </div>

    <div class="lerntheke-toolbar">
      <div class="lerntheke-filter">
        <button data-lt-filter="all"        aria-pressed="true">Alle</button>
        <button data-lt-filter="pflicht"    aria-pressed="false">⊕ Pflicht</button>
        <button data-lt-filter="wahl"       aria-pressed="false">⊙ Wahl</button>
        <button data-lt-filter="vertiefung" aria-pressed="false">⊛ Vertiefung</button>
        <button data-lt-filter="offen"      aria-pressed="false">Offen</button>
      </div>
      <span class="lerntheke-stats">
        <strong id="lt-erledigt-count">0</strong> / <span id="lt-pflicht-count">0</span> Pflicht erledigt
      </span>
    </div>

    <article class="aufgabe" data-task-id="lt-1" data-typ="pflicht">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">P1</span>
        <span class="typ-badge" data-typ="pflicht">Pflicht</span>
        <h3 class="aufgabe__titel">Brüche mit gleichem Nenner addieren</h3>
      </header>
      <div class="aufgabe__body">
        <p>Berechne 2/5 + 1/5</p>
        <input data-state="lt-1-a" data-expected-keywords="3/5">
        <span class="feedback" data-feedback-for="lt-1-a"></span>
        <div class="reveal-actions">…</div>
        <div class="aufgabe-status">
          <button data-state="lt-1-status" data-state-value="ja">✓ Erledigt</button>
          <button data-state="lt-1-status" data-state-value="uebersprungen">⤳ Übersprungen</button>
        </div>
      </div>
    </article>

    <article class="aufgabe" data-task-id="lt-2" data-typ="wahl">…</article>
    <article class="aufgabe" data-task-id="lt-3" data-typ="wahl">…</article>
    <article class="aufgabe" data-task-id="lt-4" data-typ="vertiefung">…</article>
  </div>
</article>
```

## Anti-Patterns

- **Alle Aufgaben als „Pflicht"** → keine Selbst-Differenzierung
- **Keine Zahlangaben für Wahl-Aufgaben** („wähle einige") → Schüler:innen wissen nicht, was erwartet wird
- **Status-Buttons ohne „Übersprungen"-Option** → Schüler:innen müssen zuende rechnen, auch wenn sie's schon können
- **Gating einbauen** → widerspricht dem Lerntheke-Prinzip
- **Zu wenige Aufgaben** (< 5) → keine echte Auswahl
- **Zu viele** (> 15) → unübersichtlich

## Verwandte Profile

- [`profiles/differenzierung.md`](differenzierung.md) — Differenzierung über 3 Niveaus *eines* Aufgaben-Sets; Lerntheke über *viele* Aufgaben mit Typ-Wahl
- [`profiles/klausurvorbereitung.md`](klausurvorbereitung.md) — Hat ebenfalls Themen-Filter, aber mit klar vorgegebener Übung
- [`profiles/stationenlernen.md`](stationenlernen.md) — Stationen sind physisch verteilt; Lerntheke ist „alles auf einem Blatt"
