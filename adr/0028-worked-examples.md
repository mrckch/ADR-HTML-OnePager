# ADR-0028: Worked-Examples-Pattern (Lösungsbeispiele nach Sweller)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** Didaktik, Lehrmethode, Cognitive Load

## Kontext

In der lernpsychologischen Forschung gibt es ein robustes, vielfach repliziertes Ergebnis: **Anfänger:innen profitieren mehr vom Studium durchgerechneter Lösungsbeispiele als vom Selbstlösen von Aufgaben** — vor allem in regelbasierten Domänen wie Mathematik, Physik, Programmierung und Grammatik. Dieser Effekt heißt **„Worked-Example-Effect"** und wurde Anfang der 1980er Jahre von **John Sweller** im Rahmen der **Cognitive Load Theory** beschrieben.

**Kernidee:**

- Beim Selbstlösen einer neuen Aufgabe verbraucht der Anfänger fast den gesamten Arbeitsgedächtnis-Speicher für **„Wie löse ich das jetzt?"** (extraneous cognitive load). Wenig bleibt übrig für **„Welches Schema lerne ich gerade?"** (germane cognitive load).
- Beim Studieren eines fertig gelösten Beispiels entfällt die Such-Belastung. Die ganze Aufmerksamkeit kann auf das **Verstehen der Lösungs-Struktur** gerichtet werden.
- Nach ausreichender Schema-Bildung wird das eigene Problemlösen effektiv.

Wichtige Folgeerkenntnisse (Stand der Forschung):

- **Self-Explanation Prompts** (Renkl, Atkinson): Wenn Lernende neben den Beispielen aktiv erklären, *warum* ein Schritt funktioniert, ist der Effekt nochmal deutlich stärker.
- **Faded Worked Examples** (Renkl & Atkinson): Sequenz aus „voll gelöst" → „teilweise gelöst, Lücken füllen" → „nur Problem". Die schrittweise Reduktion der Hilfen wird **„expertise reversal effect"** vermieden, also dass Beispiele für fortgeschrittene Lernende nicht mehr hilfreich, sondern eher hinderlich werden.
- **Worked Example vor Problem Solving** wirkt besser als „Problem → Beispiel als Korrektur danach".

Bisher kennt unser Repo:
- [ADR-0010 Lösungs-Hürde](0010-loesungs-huerde.md) — Lösung wird absichtlich erschwert
- [profiles/erarbeitungsseite.md](../profiles/erarbeitungsseite.md) — Erarbeitung mit Theorie + Übung

Es fehlt aber **ein expliziter Worked-Example-Workflow** — gerade für Mathe/Physik/Informatik wäre der wertvoll.

## Entscheidung

Wir ergänzen das Repo um ein **Worked-Example-Pattern** mit drei Bausteinen:

1. **ADR-0028** (dieses Dokument) — die Theorie und die didaktischen Prinzipien
2. **`profiles/worked-examples.md`** — Profil, das den Worked-Example-Workflow als Onepager-Struktur empfiehlt
3. **`templates/snippets/worked-example-snippet.html`** — CSS+HTML+JS-Pattern für die Darstellung

### Anatomie eines Worked Example im Onepager

Eine Worked-Example-Sequenz besteht aus **drei Stufen**, die in dieser Reihenfolge im Onepager erscheinen:

```
┌──────────────────────────────────────────────────────┐
│ 📘 LÖSUNGSBEISPIEL (vollständig gezeigt)              │
│                                                       │
│   Aufgabenstellung                                    │
│   Schritt 1: …  ▸ „Warum?" (Self-Explanation)         │
│   Schritt 2: …  ▸ „Warum?"                            │
│   Schritt 3: …  ▸ „Warum?"                            │
│   Ergebnis                                            │
└──────────────────────────────────────────────────────┘
       ↓ direkt anschließend
┌──────────────────────────────────────────────────────┐
│ ✏️ JETZT DU — GELEITET (faded)                        │
│                                                       │
│   Ähnliche Aufgabe                                    │
│   Schritt 1: ___ (Eingabefeld)                        │
│   Schritt 2: ___ (Eingabefeld)                        │
│   Schritt 3: ___ (Eingabefeld)                        │
│   Ergebnis: ___ (mit Selbst-Korrektur)                │
└──────────────────────────────────────────────────────┘
       ↓
┌──────────────────────────────────────────────────────┐
│ 🎯 JETZT DU — ALLEINE                                 │
│                                                       │
│   Analoge Aufgabe                                     │
│   Ergebnis: ___ (mit Selbst-Korrektur, ggf. Lösung)   │
└──────────────────────────────────────────────────────┘
```

Diese **Dreier-Sequenz** ist die kleinste sinnvolle Einheit. Mehrere solche Sequenzen können hintereinander stehen (z. B. für verschiedene Aufgabentypen einer Einheit).

### Self-Explanation-Prompts (Pflicht-Element)

Nach jedem Schritt des vollständigen Beispiels steht eine kleine Frage, die in einem `<details>` aufgeklappt werden kann:

```html
<li>
  <strong>Schritt 1: Identifiziere die Formel</strong>
  → Bei einem Rechteck: A = Länge · Breite
  <details class="we-warum">
    <summary>Warum diese Formel?</summary>
    Die Fläche zählt, wie viele 1m×1m-Quadrate in das Rechteck passen.
    Bei Länge·Breite multiplizieren wir genau diese Anzahl pro Reihe mal
    Anzahl Reihen.
  </details>
</li>
```

Anders als bei der [Lösungs-Hürde](0010-loesungs-huerde.md) ist `<details>` hier **didaktisch passend**, weil Self-Explanation-Prompts **freiwillig** und **kein „spoiler"** sind — sie vertiefen das Verständnis.

### Faded Stufe: Lücken-Eingaben

In der zweiten Stufe sind die Schritte vorgegeben, aber mit Eingabefeldern. Selbst-Korrektur (`data-expected` aus [ADR-0011](0011-selbst-korrektur.md)) gibt direktes Feedback.

```html
<article class="aufgabe we-faded" data-task-id="we-1">
  <header><span class="aufgabe__nr">✏️ Jetzt du</span></header>
  <div class="aufgabe__body">
    <p>Eine Wiese ist 30 m lang und 15 m breit.</p>
    <ol class="we-faded-steps">
      <li>Formel: A = <input type="text" data-state="we-1-formel"
                              data-expected-keywords="Länge,breite,L,B"></li>
      <li>Einsetzen: A = <input data-state="we-1-werte" placeholder="z.B. 30 · 15"></li>
      <li>Rechnen: A = <input type="number" data-state="we-1-ergebnis"
                               data-expected="450"> m²</li>
    </ol>
    <span class="feedback" data-feedback-for="we-1-ergebnis"></span>
  </div>
</article>
```

### Analoge Stufe: Voll selbständig

Die dritte Stufe ist eine **strukturgleiche, aber selbst zu lösende Aufgabe**. Hier gilt die normale [Lösungs-Hürde](0010-loesungs-huerde.md) — Schüler:innen rechnen, prüfen sich selbst, decken bei Bedarf die Lösung auf.

### Forschungsbasis und Quellen

- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning.
- Atkinson, R. K., Derry, S. J., Renkl, A., & Wortham, D. (2000). Learning from examples.
- Renkl, A. (2014). The Worked Examples Principle in Multimedia Learning.
- Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does not work.

Die Methode ist **gut belegt**, gehört zu den **stabilsten Befunden** der Lernforschung. Sie wird in der Schulpraxis aber noch zu selten systematisch eingesetzt.

### Wann Worked Examples einsetzen

**Sehr gut geeignet:**
- Mathematik (Rechenverfahren, Beweise)
- Physik / Chemie (Aufgabenrechnung)
- Programmierung (Code-Muster)
- Sprachen — Grammatik-Strukturen (Satzbau, Konjugationen)
- Geometrie (Konstruktionsschritte)
- Algorithmen / Logik

**Weniger geeignet:**
- Kreative Aufgaben (Schreiben, Gestalten)
- Reflexion und Meinungsbildung
- Offene Diskussionen
- Forschende Recherche

Im Profil [`worked-examples.md`](../profiles/worked-examples.md) ist das genauer ausgeführt.

### Abgrenzung zu „normaler Aufgabe mit Lösung"

| | Normale Aufgabe + Lösungs-Hürde | Worked Example |
|---|---|---|
| Reihenfolge | Problem → eigene Lösung → Reveal | **Beispiel → ähnliche Aufgabe → analoge Aufgabe** |
| Schwerpunkt | Eigenes Problemlösen | **Schema-Verstehen, dann eigenes Lösen** |
| Zielgruppe | Geübte / Vertiefung | **Anfänger:innen / Neu-Einführung** |
| Lösung sichtbar | Erst nach Versuch | **Sofort sichtbar als „so geht's"** |
| Self-Explanation | Optional | **Pflicht-Element** |

## Alternativen

- **Klassische Aufgabe + Lösung-Reveal** (ADR-0010): Verworfen für Anfänger:innen — der Worked-Example-Effekt zeigt, dass es bei neuen Schemas weniger wirksam ist.
- **Reines Problembasiertes Lernen** (problem-based learning): Verworfen für formale Domänen — gegen die robuste Forschungslage. PBL hat seine Stärken bei offenen, kreativen Aufgaben.
- **Direkte Instruktion ohne Beispiel-Studium**: Verworfen — Worked Examples sind besser belegt.

## Konsequenzen

**Positiv:**
- Forschungsbasierte didaktische Methode
- Reduziert kognitive Überlastung bei Anfänger:innen
- Klare Struktur, einfach zu generieren mit KI
- Wirkt besonders gut in formalen Fächern (Mathe, Physik, Informatik)
- Self-Explanation als Pflicht-Element baut auf bekannten Patterns auf

**Negativ / Trade-offs:**
- **Expertise reversal effect**: Für fortgeschrittene Schüler:innen weniger oder gar nicht wirksam → Differenzierung nötig
- Mehr Aufwand beim Erstellen — drei Stufen statt einer
- Kreative Aufgaben passen nicht in dieses Schema
- „Sieht aus wie Spickzettel" — muss in der Lehrkraft-Kommunikation klar sein, dass das Beispiel-Studium pädagogisch ist

**Folgewirkungen für künftige Onepager:**
- Bei Erarbeitung neuer Rechenverfahren: erst ein Worked Example, dann Übung
- Self-Explanation-Prompts via `<details>` standardisieren
- Faded-Aufgabe als Brücke zwischen Beispiel und freier Aufgabe nicht überspringen
- Bei sehr leistungsstarken Lerngruppen: Schritte überspringen oder direkt zur freien Aufgabe

## Verwandte ADRs / Profile

- [profiles/worked-examples.md](../profiles/worked-examples.md) — Profil, das dieses Pattern als Onepager-Struktur umsetzt
- [ADR-0010 Lösungs-Hürde](0010-loesungs-huerde.md) — komplementäres Pattern für eigenes Problemlösen
- [ADR-0011 Selbst-Korrektur](0011-selbst-korrektur.md) — für die Faded-Stufe und analoge Aufgabe
- [profiles/erarbeitungsseite.md](../profiles/erarbeitungsseite.md) — kann Worked Examples in der Erarbeitungs-Phase enthalten
- [profiles/code-uebung.md](../profiles/code-uebung.md) — passt besonders gut zusammen (Code-Worked-Examples)
