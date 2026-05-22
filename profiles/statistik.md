# Profil: Statistik / Datenanalyse

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager mit **eingebetteten Daten** (Tabelle oder kleine Datenreihe), an denen Schüler:innen statistische Berechnungen üben: Mittelwert, Median, Modalwert, Häufigkeit, Spannweite, Standardabweichung, …

Die Daten kommen aus realen Kontexten (Klassennotenverteilung, Niederschlag-Statistik, Sport-Ergebnisse) und werden im Onepager **direkt sichtbar als Tabelle** dargestellt — plus optional ein Säulendiagramm (Inline-SVG, kein externes Chart-Lib).

## Typische Merkmale

- **Klassenstufe:** Sek I (Jahrgang 6/7 — Mittelwert) bis Sek II (Stochastik)
- **Fachbereich:** Mathematik (primär), aber auch Naturwissenschaften (Messwerte), Geographie (Klimadaten), Geschichte (Demografie)
- **Zeitumfang:** Doppelstunde
- **Ziel-Typ:** Übung, Anwendung statistischer Methoden
- **Gerät:** Laptop, Tablet

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten neben/unter der Datentabelle |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | **Zentral** — Berechnungen werden numerisch geprüft (`data-expected` + `data-tolerance`) |
| [ADR-0010](../adr/0010-loesungs-huerde.md) | Lösungs-Hürde mit Rechenweg-Erklärung |

## Core-ADRs abweichend oder weniger relevant

- **Quiz:** möglich für Begriffe („Was ist der Median?"), aber nicht zentral
- **Canvas:** optional, z. B. für Box-Plot per Hand
- **Lösungs-Cipher:** Standard-Reveal ist passender — die Antwort selbst ist die Zahl, der **Rechenweg** ist die eigentliche Lösung

## Spezifische didaktische Entscheidungen

### 1. Daten als HTML-Tabelle vor den Aufgaben

Die Daten leben **sichtbar im Onepager** als HTML-Tabelle. Nicht als CSV-Anhang, nicht als externe Datei.

```html
<table class="daten-tabelle" id="noten">
  <thead>
    <tr><th>Note</th><th>Anzahl</th></tr>
  </thead>
  <tbody>
    <tr><td>1</td><td class="num">3</td></tr>
    <tr><td>2</td><td class="num">7</td></tr>
    …
  </tbody>
</table>
```

CSS macht die Tabelle lesbar (Zebra-Streifen, rechtsbündige Zahlen). Snippet: [`templates/snippets/statistik-tabelle-snippet.html`](../templates/snippets/statistik-tabelle-snippet.html).

### 2. Optional Säulendiagramm aus der Tabelle

Aus derselben Tabelle wird per JS ein **Inline-SVG-Säulendiagramm** gerendert. Das ist:
- Vollständig im Browser, ohne externe Lib
- Skalierbar (resp. responsive)
- Kein Tracking, kein externes Asset

```html
<div class="saeulen-diagramm" data-saeulen="noten">
  <svg viewBox="0 0 400 220" role="img" aria-label="Notenverteilung"></svg>
</div>
```

Das Script aus dem Snippet erkennt `data-saeulen` und befüllt die SVG aus den Tabellenzeilen.

### 3. Numerische Selbst-Korrektur ist Pflicht

Jede Berechnungs-Aufgabe hat `data-expected` mit passender `data-tolerance`:

```html
<input type="number" data-state="mw" step="0.01"
       data-expected="2.85" data-tolerance="0.05">
<span class="feedback" data-feedback-for="mw"></span>
```

Die Toleranz ist nötig, weil:
- Schüler:innen runden unterschiedlich
- Komma vs. Punkt als Dezimaltrenner
- Klassenmittelwerte sind oft 2-stellige Brüche

Default für Mathe-Mittelwert: `tolerance="0.05"` reicht meistens.

### 4. Lehrer-Helper für richtige Werte (in Konsole)

Im Snippet ist ein kleiner Helper eingebaut, der das richtige Ergebnis für die Lehrkraft berechnet:

```js
// In der Browser-Konsole:
statHelper.mittelwert('noten')   // → 2.85
statHelper.summe('noten')        // → 27
```

So muss die Lehrkraft den Mittelwert nicht selbst von Hand ausrechnen, sondern kopiert ihn direkt in `data-expected`.

### 5. Lösung enthält den Rechenweg

Beim Reveal sieht die Schüler:in nicht nur die Zahl, sondern den **Weg**:

```html
<div class="solution-content" data-task-id="..." hidden>
  <p>Schritte:</p>
  <p>Summe = 1·3 + 2·7 + 3·9 + 4·5 + 5·2 + 6·1 = 80</p>
  <p>Anzahl = 3 + 7 + 9 + 5 + 2 + 1 = 27</p>
  <p>Mittelwert = 80 / 27 = <strong>2.96</strong> (gerundet auf 2 Nachkommastellen)</p>
</div>
```

Das ist wichtiger als das Ergebnis — Statistik ist ein „Wie kommt das zustande?"-Fach.

### 6. Mehrere Aufgaben zur selben Tabelle

Ein Onepager hat typischerweise **eine Tabelle, mehrere Aufgaben** dazu:

| Aufgabe | Berechnung |
|---|---|
| 1 | Anzahl der Werte |
| 2 | Summe |
| 3 | Mittelwert |
| 4 | Median |
| 5 | Modalwert |
| 6 | Spannweite |

Schüler:in scrollt zwischen Tabelle und Aufgaben — Tabelle bleibt oben sichtbar (oder per CSS sticky).

### 7. Reale Daten verwenden

Best Practice: keine ausgedachten Zahlen, sondern **echte Daten** verwenden, die auch im Lehrplan vorkommen:
- Klassennotenverteilung
- Klima-Daten der Wetterdienst-Webseite
- Sport-Statistiken
- Bevölkerungsdaten
- Umfrage-Ergebnisse

Quelle in der Tabellen-Caption nennen.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja |
| **Daten-Tabelle** | **ja, Hauptelement** |
| **Säulendiagramm** (Inline-SVG) | optional, sehr empfehlenswert |
| Aufgaben-Karten | ja |
| Selbst-Korrektur (`data-expected` numerisch) | **ja, sehr wichtig** |
| Lösungs-Hürde mit Rechenweg | **ja** |
| Quiz | optional (Begriffsabfrage) |
| Canvas | optional (z. B. eigenen Box-Plot zeichnen) |
| Fortschrittsbalken | ja |
| Save-Status | ja |
| Toast | ja |
| JSON/HTML-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathematik · Klasse 7 · Statistik</span>
    <h1>Notenverteilung in unserer Klasse auswerten</h1>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Was du heute lernst</span>
      Du berechnest Mittelwert, Median und Modalwert einer Datenreihe.
    </div>

    <h2>Die Daten</h2>
    <p>Notenverteilung der letzten Klassenarbeit (n = 27):</p>

    <div class="daten-wrapper">
      <table class="daten-tabelle" id="noten">
        <thead>
          <tr><th>Note</th><th>Anzahl</th></tr>
        </thead>
        <tbody>
          <tr><td>1</td><td class="num">3</td></tr>
          <tr><td>2</td><td class="num">7</td></tr>
          <tr><td>3</td><td class="num">9</td></tr>
          <tr><td>4</td><td class="num">5</td></tr>
          <tr><td>5</td><td class="num">2</td></tr>
          <tr><td>6</td><td class="num">1</td></tr>
        </tbody>
      </table>
    </div>

    <div class="saeulen-diagramm" data-saeulen="noten">
      <svg viewBox="0 0 400 220" role="img" aria-label="Säulendiagramm"></svg>
    </div>

    <h2>Aufgaben</h2>

    <article class="aufgabe" data-task-id="anzahl">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">1</span>
        <h3 class="aufgabe__titel">Wie viele Schüler:innen sind es insgesamt?</h3>
      </header>
      <div class="aufgabe__body">
        <input type="number" data-state="anzahl-a" data-expected="27" step="1">
        <span class="feedback" data-feedback-for="anzahl-a"></span>
      </div>
    </article>

    <article class="aufgabe" data-task-id="mittelwert">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">2</span>
        <h3 class="aufgabe__titel">Berechne den Mittelwert</h3>
      </header>
      <div class="aufgabe__body">
        <p>Tipp: Multipliziere jede Note mit ihrer Anzahl, addiere alles und teile durch die Gesamtzahl.</p>
        <input type="number" data-state="mw-a" data-expected="2.96"
               data-tolerance="0.05" step="0.01">
        <span class="feedback" data-feedback-for="mw-a"></span>
        <div class="reveal-actions">
          <button class="reveal-btn reveal-btn--solution" data-task-id="mittelwert">🔍 Rechenweg</button>
        </div>
        <div class="solution-content" data-task-id="mittelwert" hidden>
          <p>Summe der gewichteten Noten:</p>
          <p>1·3 + 2·7 + 3·9 + 4·5 + 5·2 + 6·1 = 3 + 14 + 27 + 20 + 10 + 6 = 80</p>
          <p>Mittelwert = 80 / 27 ≈ <strong>2,96</strong></p>
        </div>
      </div>
    </article>

    <!-- weitere Aufgaben zum selben Datensatz … -->
  </div>
</article>
```

## Anti-Patterns

- **Daten als CSV-Anhang** → nicht single-file
- **Externe Chart-Library** (Chart.js, D3) → externes JS, widerspricht ADR-0001
- **Ohne `data-tolerance` bei Mittelwerten** → Rundungs-Unterschiede führen zu Frust
- **„Richtig/falsch" ohne Rechenweg** → Statistik braucht den Lösungs-WEG
- **Tabellen ohne Mobile-Wrapper** → bricht auf Smartphone unschön um (Wrapper ist im Snippet)
- **Ausgedachte Zahlen** → wirkt künstlich; reale Daten sind besser

## Verwandte Profile

- [`profiles/lesetext.md`](lesetext.md) — Analoge Logik, aber mit Text statt Datentabelle
- [`profiles/code-uebung.md`](code-uebung.md) — Wenn die statistische Berechnung als Code-Aufgabe (Python) gestellt wird
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn ein neues Konzept erarbeitet wird, kann die Daten-Tabelle Teil davon sein
