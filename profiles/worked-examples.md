# Profil: Worked Examples (Lösungsbeispiele)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))
- **Basiert auf:** [ADR-0028 Worked-Examples-Pattern](../adr/0028-worked-examples.md)

## Was ist das?

Ein Onepager, der die **Worked-Examples-Methode** als Hauptstruktur nutzt: Anfänger:innen sehen erst eine **vollständig durchgerechnete Beispielaufgabe** mit Erklärungs-Prompts, lösen dann eine **„gefadete" Aufgabe mit Lücken** und schließlich eine **analoge Aufgabe selbständig**.

Forschungs-Hintergrund: der „Worked-Example-Effect" (Sweller, 1988) zeigt, dass Anfänger:innen besser durch Beispiel-Studium lernen als durch Selbst-Problemlösen. Details in [ADR-0028](../adr/0028-worked-examples.md).

## Typische Merkmale

- **Klassenstufe:** Sek I/II — besonders **wenn ein neues Verfahren eingeführt wird**
- **Fachbereich:** Mathematik, Physik, Chemie, Informatik, Sprachen (Grammatik), Logik
- **Zeitumfang:** 30–60 Min für mehrere Worked-Example-Sequenzen
- **Ziel-Typ:** Einführung neuer Rechenverfahren, Schema-Bildung
- **Gerät:** Laptop oder Tablet (am Smartphone wegen der Schritt-Struktur eher umständlich)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0028](../adr/0028-worked-examples.md) | **Theoretische und didaktische Basis** dieses Profils |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur **zentral** in der Faded-Stufe (Lücken-Eingaben mit `data-expected`) |
| [ADR-0010](../adr/0010-loesungs-huerde.md) | Lösungs-Hürde nur für die **dritte (analoge) Stufe**, nicht für das Worked Example selbst |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Faded und Analog werden als Aufgaben-Karten dargestellt |

## Core-ADRs abweichend oder weniger relevant

- **Quiz:** typischerweise nicht — Worked Examples sind für Verfahren, nicht für Faktenwissen
- **Canvas:** je nach Fach (z. B. bei Geometrie-Worked-Examples sinnvoll)

## Spezifische didaktische Entscheidungen

### 1. Sequenz-Struktur: 1+1+1 oder 2+1+1

Standard ist die **Dreier-Sequenz** (siehe ADR-0028):

```
[📘 Beispiel] → [✏️ Faded] → [🎯 Analog]
```

Für leistungsstärkere Gruppen reicht das. Für schwächere Gruppen empfehlenswert: **zwei Beispiele** (verschiedene Varianten desselben Verfahrens), dann ein Faded, dann eine Analog-Aufgabe:

```
[📘 Beispiel 1] → [📘 Beispiel 2] → [✏️ Faded] → [🎯 Analog]
```

Mehrere Beispiele helfen, das Schema von der konkreten Ausführung zu trennen.

### 2. Visuelle Hierarchie

Die drei Stufen sind visuell deutlich unterschieden:

| Stufe | Marker | Farbe | Gefühl |
|---|---|---|---|
| 📘 Worked Example | Gold-Box mit Gradient | Gold | „Lies und verstehe" |
| ✏️ Faded | Blau-Border-Top auf Aufgaben-Karte | Blau | „Trau dich" |
| 🎯 Analog | Grün-Border-Top auf Aufgaben-Karte | Grün | „Du kannst es" |

Die Farb-Progression Gold → Blau → Grün signalisiert visuell „Schritt für Schritt zur Selbständigkeit".

### 3. Self-Explanation-Prompts sind Pflicht

Jeder Schritt im Worked Example hat ein `<details class="we-warum">` mit einer „Warum?"-Frage:

```html
<li>
  <strong>Schritt 1:</strong> Identifiziere die Formel: A = L · B
  <details class="we-warum">
    <summary>Warum diese Formel?</summary>
    Die Fläche zählt, wie viele 1m×1m-Quadrate in das Rechteck passen.
  </details>
</li>
```

Schüler:innen können selbst entscheiden, ob sie die Erklärung sehen wollen — aber sie ist da. Forschung zeigt: aktives Aufklappen der Erklärung verbessert das Schema-Bilden nochmal deutlich.

**Anti-Pattern**: alle Schritte ohne Erklärung → degeneriert zu „Spickzettel".

### 4. Faded Stufe mit data-expected

Die Lücken-Eingabefelder nutzen die Selbst-Korrektur aus ADR-0011:

```html
<li>
  Formel: A = <input data-state="we-1-formel"
                      data-expected-keywords="Länge,breite,L·B">
</li>
<li>
  Einsetzen: A = <input data-state="we-1-werte"
                         data-expected-keywords="30 · 15">
</li>
<li>
  Berechnen: A = <input type="number" data-state="we-1-ergebnis"
                          data-expected="450" data-tolerance="0.1"> m²
</li>
```

Feedback erscheint **on blur**, nicht live — sonst stresst das blinkende Feedback während des Tippens.

### 5. Analoge Aufgabe ohne Anleitung

Die dritte Stufe ist eine **strukturell gleiche, aber unbeschriftete** Aufgabe. Hier gibt es keine Schritt-Eingaben mehr — die Schüler:in rechnet selbst, gibt das Ergebnis ein, prüft sich selbst, kann bei Bedarf die Lösung aufdecken (Standard ADR-0010).

### 6. Mehrere Sequenzen pro Onepager

Ein Onepager kann **2–4 Worked-Example-Sequenzen** enthalten, die verschiedene Aspekte/Schwierigkeitsgrade abdecken. Beispiel-Reihenfolge in einer „Flächen"-Einheit:

```
Sequenz 1: Rechteck (Standardfall)
Sequenz 2: Quadrat (Spezialfall des Rechtecks)
Sequenz 3: Dreieck (anderes Verfahren)
Sequenz 4: Trapez (anspruchsvoller, ggf. zwei Beispiele)
```

### 7. Lehrer-Modus mit `?solutions=1`

Im Lehrer-Druck-Modus sollten die Faded-Stufen automatisch ausgefüllt werden (zur Kontrolle des Lehrer-Lösungsblattes). Da der Lehrer-Modus aber typischerweise auch nur Pflichtwerte enthält, bleibt das eine pragmatische Implementation: bei Bedarf kann pro Faded-Input ein `data-teacher-value="..."` gesetzt werden, das bei `?solutions=1` als `value` eingefügt wird.

### 8. Fertig-Snippet

Komplettes Pattern in [`templates/snippets/worked-example-snippet.html`](../templates/snippets/worked-example-snippet.html) — CSS + HTML für alle drei Stufen.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja |
| **Worked-Example-Box** (📘 Stufe 1) | **ja, Hauptelement** |
| **Faded Aufgaben-Karten** (✏️ Stufe 2) | **ja** |
| **Analoge Aufgaben-Karten** (🎯 Stufe 3) | **ja** |
| Selbst-Korrektur (data-expected) | **ja, in Stufe 2 und 3** |
| Lösungs-Hürde | nur in Stufe 3 (analog) |
| Quiz | nein |
| Canvas | je nach Fach (z. B. Geometrie-Worked-Examples) |
| Fortschrittsbalken | ja |
| Save-Status | ja |
| Toast | ja |
| JSON/HTML-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathe · Klasse 6 · Flächen</span>
    <h1>Flächenberechnung — wir lernen es Schritt für Schritt</h1>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Was du heute lernst</span>
      Du verstehst, wie man die Fläche eines Rechtecks, Quadrats und Dreiecks
      berechnet — und kannst es selbständig.
    </div>

    <div class="box info">
      <span class="box-title">ℹ️ So lernst du heute</span>
      <p>Jedes Verfahren lernst du in <strong>drei Stufen</strong>:</p>
      <ol>
        <li>📘 Du <strong>liest</strong> ein vollständig gelöstes Beispiel</li>
        <li>✏️ Du <strong>füllst</strong> die Lücken einer ähnlichen Aufgabe</li>
        <li>🎯 Du <strong>löst</strong> eine analoge Aufgabe selbständig</li>
      </ol>
    </div>

    <h2>Sequenz 1: Fläche eines Rechtecks</h2>

    <!-- Stufe 1: Worked Example -->
    <section class="worked-example">
      <span class="we-badge">📘 Lösungsbeispiel</span>
      <h3>Eine Wiese: 25 m lang, 12 m breit. Wie groß ist die Fläche?</h3>
      <ol class="we-steps">
        <li>
          <strong>Formel identifizieren:</strong> Bei einem Rechteck: A = Länge · Breite
          <details class="we-warum">
            <summary>Warum diese Formel?</summary>
            …Erklärung…
          </details>
        </li>
        <li><strong>Einsetzen:</strong> A = 25 m · 12 m</li>
        <li><strong>Berechnen:</strong> A = 300 m²</li>
      </ol>
      <div class="we-answer">Die Wiese ist <strong>300 m²</strong> groß.</div>
    </section>

    <!-- Stufe 2: Faded -->
    <article class="aufgabe we-faded" data-task-id="we-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">✏️ Jetzt du — geleitet</span>
        <h3 class="aufgabe__titel">30 m × 15 m</h3>
      </header>
      <div class="aufgabe__body">
        <ol class="we-faded-steps">…Eingabefelder…</ol>
      </div>
    </article>

    <!-- Stufe 3: Analog -->
    <article class="aufgabe we-analog" data-task-id="we-2">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">🎯 Jetzt du — alleine</span>
        <h3 class="aufgabe__titel">Klassenzimmer: 8 m × 6 m</h3>
      </header>
      <div class="aufgabe__body">…eine Antwort, Lösungs-Reveal optional…</div>
    </article>

    <hr class="page-break-hint">

    <h2>Sequenz 2: Fläche eines Quadrats</h2>
    <!-- analog: Worked Example, Faded, Analog -->
  </div>
</article>
```

## Anti-Patterns

- **Worked Example ohne Self-Explanation-Prompts** → degeneriert zu „Spickzettel", kein Lerneffekt
- **Faded-Stufe überspringen** (direkt von Beispiel zu freier Aufgabe) → zu großer Sprung für Anfänger:innen
- **Nur 1 Worked Example pro Verfahren** bei schwachen Gruppen → ein Beispiel reicht oft nicht für Schema-Bildung
- **Worked Examples bei kreativen Aufgaben** (Aufsatz, Diskussion) → Methodisch unpassend
- **Worked Examples bei Fortgeschrittenen** ohne Differenzierung → „expertise reversal effect"
- **Lösungs-Cipher** im Worked Example → das Beispiel SOLL sichtbar sein, das ist der Punkt

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Kann Worked-Example-Sequenzen in der Erarbeitungs-Phase enthalten
- [`profiles/code-uebung.md`](code-uebung.md) — Worked Examples eignen sich hervorragend für Code-Pattern-Vermittlung
- [`profiles/loesungszettel.md`](loesungszettel.md) — Komplementär: Worked Example einführt, Lösungszettel begleitet beim Üben
- [`profiles/methoden.md`](methoden.md) — Methoden-Onepager können Worked Examples für die Methoden-Anwendung nutzen
