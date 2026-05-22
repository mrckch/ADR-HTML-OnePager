# Profil: Lese-/Verständnistext

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der einen **vollständigen Lesetext** (Sachtext, literarischer Auszug, Quelle, Zeitungsartikel) im Zentrum stellt und mit **Verständnis- und Analyse-Aufgaben** flankiert. Schüler:innen lesen den Text in der Seite selbst und arbeiten direkt anschließend daran.

Dieses Profil bringt die einzige Besonderheit, dass der **Inhalt im Onepager selbst gebraucht wird** — ein längerer Textblock, der gut lesbar gestaltet sein muss.

## Typische Merkmale

- **Klassenstufe:** Sek I, Sek II, je nach Textschwierigkeit
- **Fachbereich:** Deutsch, Fremdsprachen (Englisch, Französisch …), Gesellschaftslehre, Geschichte, Politik, Religion, Philosophie
- **Zeitumfang:** Doppelstunde — Lesen + Bearbeitung
- **Ziel-Typ:** Textverständnis, Analyse, Interpretation, Quellenkritik
- **Gerät:** Laptop/Tablet bevorzugt (Smartphone für längere Texte schlecht); auch gedruckt sinnvoll, wenn auf Papier angestrichen werden soll

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0022](../adr/0022-design-system-v2.md) | **Lesetypografie** ist hier zentral: Serif-Body für den Text, größere Zeilenhöhe, max-width 65ch |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben mit **unterschiedlichen Antwortformaten** (Zitat-Eingabe, kurze Antwort, lange Stellungnahme) |
| [ADR-0023](../adr/0023-a4-druck-und-preview.md) | Druck **wichtig** — viele Schüler:innen lesen lieber auf Papier und arbeiten unterstreichend |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Mit Keywords (`data-expected-keywords`), nicht numerisch — Antworten sind sprachlich |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** anwendbar, aber bei Interpretations-Aufgaben oft keine eindeutige Lösung — dann mehr „Beispiel-Lösung" als „die richtige Lösung"
- **Canvas:** meist nicht relevant (Texte werden gelesen, nicht gezeichnet); Ausnahme: Schema-Skizze einer Texterschließungs-Methode
- **Quiz mit gehashten Antworten:** möglich für Verständnis-Multiple-Choice, aber nicht typisch

## Spezifische didaktische Entscheidungen

### 1. Text-Block prominent gestaltet

Der Lesetext steht in einer eigenen **`.text-quelle`**-Box, optisch klar abgegrenzt:

```html
<section class="text-quelle">
  <header class="text-quelle__meta">
    <p><strong>Quelle:</strong> Max Frisch, „Homo Faber" (Erster Bericht, S. 7–9, gekürzt)</p>
  </header>
  <div class="text-quelle__body">
    <p>Wir starteten in La Guardia, New York, mit dreistündiger Verspätung infolge Schneestürmen …</p>
    <p>[weitere Absätze]</p>
  </div>
  <div class="text-quelle__zaehler">
    <span>Zeilen 1–32</span>
  </div>
</section>
```

CSS-Snippet:
```css
.text-quelle {
  border: 1px solid var(--border);
  border-left: 4px solid var(--navy);
  background: var(--bg-page);
  padding: var(--space-5) var(--space-6);
  margin: var(--space-6) 0;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
.text-quelle__meta { font-size: var(--fs-sm); color: var(--fg-muted);
                     border-bottom: 1px solid var(--border-soft);
                     padding-bottom: var(--space-2); margin-bottom: var(--space-3); }
.text-quelle__body { font-family: var(--font-serif);
                     font-size: var(--fs-lg); line-height: 1.7;
                     max-width: 60ch; }
.text-quelle__body p { margin: 0 0 var(--space-3); }
.text-quelle__zaehler { font-size: var(--fs-sm); color: var(--fg-muted);
                        text-align: right; margin-top: var(--space-2); }
```

Lesetext in Serif, etwas größer und mit mehr Zeilenhöhe — wie in einem gedruckten Buch.

### 2. Zeilennummerierung bei längeren Texten

Bei Texten > 30 Zeilen: **Zeilennummern** alle 5 Zeilen einblenden, damit Schüler:innen Zitate per „Z. 7" referenzieren können:

```html
<ol class="zeilen">
  <li>Wir starteten in La Guardia, New York, mit dreistündiger</li>
  <li>Verspätung infolge Schneestürmen, unsere Super-Constellation</li>
  …
</ol>
```

```css
.zeilen { list-style: decimal; padding-left: 3em; counter-reset: line; }
.zeilen li { padding-left: var(--space-2); }
.zeilen li:nth-child(5n) { font-weight: 500; }
```

Beim Druck (`@page`) bleiben Zeilennummern erhalten.

### 3. Aufgaben-Typen mischen

Drei typische Frage-Typen:

| Stufe | Frage-Typ | Beispiel | UI |
|---|---|---|---|
| **Reproduktion** | Verständnisfrage mit kurzer Antwort | „Wann startet das Flugzeug?" | `<input type="text">` mit `data-expected-keywords` |
| **Analyse** | Zitat heraussuchen + Erklärung | „Wo zeigt sich Fabers Distanz zum Geschehen? Zitiere und erkläre." | `<textarea>`, evtl. mit Zitat-Hilfe |
| **Stellungnahme** | Eigene Meinung mit Begründung | „Würdest du in dieser Situation anders reagieren? Begründe." | `<textarea>` ohne Lösungs-Reveal — bewusst offen |

### 4. Zitat-Eingabe-Hilfe

Manche Aufgaben verlangen ein Zitat. Hilfreich: ein dezenter Hinweis „Format: ‚...' (Z. 12)", optional ein „Zitate-Generator" als Hilfsfeld:

```html
<div class="zitat-helper">
  <input type="text" placeholder="Zitat" data-state="z-1-text" />
  <input type="number" placeholder="Z." data-state="z-1-zeile" />
  <span class="zitat-preview"></span>
</div>
```

JS-Snippet:
```js
document.querySelectorAll('.zitat-helper').forEach(z => {
  const t = z.querySelector('input[data-state$="-text"]');
  const l = z.querySelector('input[data-state$="-zeile"]');
  const p = z.querySelector('.zitat-preview');
  function update() { p.textContent = t.value ? `„${t.value}" (Z. ${l.value || '?'})` : ''; }
  t.addEventListener('input', update); l.addEventListener('input', update);
});
```

### 5. „Beispiel-Lösung" statt „die richtige Lösung"

Bei interpretativen Aufgaben wird die Lösung deutlich als **Beispiel-Lösung** markiert — andere Lesarten sind möglich:

```html
<div class="solution-content" data-task-id="..." hidden>
  <p><strong>Eine mögliche Lösung:</strong> Fabers Reaktion auf den Schneesturm zeigt …</p>
  <p class="hint">Andere Deutungen sind möglich, wenn sie sich am Text belegen lassen.</p>
</div>
```

Hervorhebung als „beispielhaft" verändert das Verhältnis: keine „richtige" Antwort, sondern eine Verhandlungsbasis.

### 6. Druck-Optimierung kritisch

Lesetexte werden oft gedruckt — zum Unterstreichen, Markieren, Anstreichen am Rand. Im Print-CSS:

- `.text-quelle` ist gut sichtbar (Border erhalten)
- Zeilennummerierung bleibt
- Schriftgröße der Lesetext-Box etwas größer als Body (z. B. 11pt statt 10.5pt)
- Aufgaben kommen NACH dem Text, damit der Text als zusammenhängender Block lesbar bleibt

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja (am Anfang, knapp) |
| Aufgaben-Karten | **ja, mit gemischten Antwort-Typen** |
| Inhalts-Boxen | sparsam — der Text dominiert |
| **Lesetext-Box (`.text-quelle`)** | **ja, profilspezifisch** |
| Zeilennummerierung | bei Texten > 30 Zeilen empfohlen |
| Selbst-Korrektur (Keywords) | ja, für Reproduktions-Fragen |
| Lösungs-Hürde („Beispiel-Lösung") | ja |
| Quiz | nein (passt nicht zur Texterschließung) |
| Canvas | nein |
| Fortschrittsbalken | ja, optional |
| Save-Status-Indikator | ja |
| Toast-Notifications | ja |
| JSON-Export/Import | ja (Schüler:in kann Bearbeitung mitnehmen) |
| Reset-Dialog | ja |
| Druck-Optimierung | **ja, kritisch** |

## Aufgaben-Pattern (typisch)

```html
<section class="text-quelle">
  <header class="text-quelle__meta">
    <p><strong>Quelle:</strong> Auszug aus … (Z. 1–28)</p>
  </header>
  <ol class="zeilen text-quelle__body">
    <li>Erster Satz des Textes …</li>
    <li>Zweite Zeile …</li>
    …
  </ol>
</section>

<h2>Aufgaben zum Text</h2>

<article class="aufgabe" data-task-id="t-1">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 1 · Verstehen</span>
    <h3 class="aufgabe__titel">Worum geht es im ersten Abschnitt (Z. 1–8)?</h3>
  </header>
  <div class="aufgabe__body">
    <textarea data-state="t-1-text" rows="3"
              data-expected-keywords="Reise,Verspätung,New York" rows="3"></textarea>
    <span class="feedback" data-feedback-for="t-1-text"></span>
  </div>
</article>

<article class="aufgabe" data-task-id="t-2">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 2 · Analysieren</span>
    <h3 class="aufgabe__titel">Wo zeigt sich Fabers Distanz? Zitiere und erkläre.</h3>
  </header>
  <div class="aufgabe__body">
    <textarea data-state="t-2-text" rows="5" placeholder="Zitat („...", Z. ...) + Erklärung"></textarea>
    <div class="reveal-actions">
      <button class="reveal-btn reveal-btn--solution" data-task-id="t-2">🔍 Beispiel-Lösung</button>
    </div>
    <div class="solution-content" data-task-id="t-2" hidden>
      <p><strong>Eine mögliche Lösung:</strong> …</p>
      <p class="hint">Andere Stellen mit anderen Begründungen sind genauso gültig.</p>
    </div>
  </div>
</article>

<article class="aufgabe" data-task-id="t-3">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 3 · Stellung nehmen</span>
    <h3 class="aufgabe__titel">Würdest du in dieser Situation anders reagieren? Begründe.</h3>
  </header>
  <div class="aufgabe__body">
    <textarea data-state="t-3-text" rows="6"
              placeholder="Meine Meinung: … Begründung: …"></textarea>
    <!-- KEIN Reveal — bewusst offen -->
  </div>
</article>
```

## Anti-Patterns

- **Lesetext in normaler Body-Schrift** → wirkt wie Aufgabentext, geht visuell unter
- **Text aufteilen über mehrere Sektionen** → bricht den Lesefluss
- **Keine Zeilennummern bei langen Texten** → Schüler:innen können nicht referenzieren
- **Quiz statt offener Aufgaben** → reduziert komplexe Textarbeit auf Multiple-Choice
- **Eine einzige „richtige Lösung"** bei Interpretationen → erzieht zum Reproduzieren statt zum Denken
- **Schmale Lesetext-Spalte (< 50ch)** → ständige Zeilenumbrüche stören
- **Zu lange Lesetexte (> 60 Zeilen) ohne Pause** → Konzentration fällt ab — besser den Text in 2 Teile aufteilen, dazwischen kurze Verständnisfrage

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn der Text Teil einer breiteren Lerneinheit ist und nicht das Zentrum
- [`profiles/stationenlernen.md`](stationenlernen.md) — Eine Station kann auch ein kurzer Lesetext sein
- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn Eindrücke zum Text frei reflektiert werden sollen
