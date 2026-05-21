# ADR-0012: Gamification — sanft, nicht-kompetitiv

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Motivation, UX, Didaktik

## Kontext

Gamification kann Engagement erhöhen — oder das Gegenteil bewirken. Klassische Spielelemente (Punkte, Levels, Streaks, Ranglisten) erzeugen oft genau die Belastung, die wir bei Schüler:innen *vermeiden* wollen: Wettkampfdruck, Angst vor dem Verlust einer Serie, Frust über schlechtes Abschneiden im Vergleich.

Trotzdem brauchen längere Onepager (z. B. 3-4 Unterrichtsstunden, 15-25 Aufgaben) **visuelle Orientierung**: Wo stehe ich? Was habe ich schon geschafft? Was kommt noch?

## Entscheidung

Wir bauen **drei sanfte, nicht-kompetitive** Gamification-Elemente ein:

### 1. Fortschrittsbalken im Topbar

Direkt unter oder neben dem Save-Status: eine schmale Anzeige „X / Y bearbeitet".

```html
<span class="progress" aria-label="Fortschritt">
  <span class="progress__bar"><span class="progress__fill" id="progress-fill"></span></span>
  <span class="progress__label" id="progress-label">0 / 0</span>
</span>
```

```css
.progress { display: flex; align-items: center; gap: var(--space-2);
            font-size: var(--fs-xs); color: var(--fg-soft); }
.progress__bar { width: 80px; height: 6px; background: rgba(255,255,255,.15);
                 border-radius: 999px; overflow: hidden; }
.progress__fill { display: block; height: 100%; width: 0%;
                  background: linear-gradient(90deg, var(--blue), var(--green));
                  transition: width .4s; }
```

**Berechnung:** Jede `.aufgabe`-Karte mit `data-task-id` zählt. Eine Aufgabe gilt als „bearbeitet", wenn **mindestens ein** Eingabefeld innerhalb der Karte einen nicht-leeren Wert hat (`value !== '' && checked !== false`).

Keine Bewertung „richtig/falsch" — bearbeitet zählt unabhängig von der Korrektheit. Ziel ist *Bewegung*, nicht *Perfektion*.

### 2. Sektion-Abschluss-Marker

Wenn **alle Aufgaben einer `<section>` (oder zwischen zwei `<h2>`) bearbeitet sind**, erscheint ein kleines visuelles Lob direkt unter der Sektion:

```html
<div class="abschnitt-fertig" hidden>
  🎉 Abschnitt geschafft!
</div>
```

```css
.abschnitt-fertig {
  text-align: center;
  background: linear-gradient(135deg, var(--bg-info), var(--bg-elevated));
  border: 1px solid var(--gold);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-5);
  font-weight: 600;
  color: var(--navy);
  margin: var(--space-5) 0;
  transition: opacity .4s, transform .4s;
}
```

Per JS wird das Element sichtbar geschaltet, wenn die Sektion vollständig ist. Bei `prefers-reduced-motion` ohne Transition.

### 3. Status-Punkt am `.aufgabe__header`

Optional pro Aufgabe ein kleiner Punkt, der visualisiert: leer / in Arbeit / bearbeitet:

```html
<header class="aufgabe__header">
  <span class="aufgabe__nr">Aufgabe 1.1</span>
  <h3 class="aufgabe__titel">Titel</h3>
  <span class="aufgabe__status" data-status="empty" aria-label="leer"></span>
</header>
```

```css
.aufgabe__status {
  width: 12px; height: 12px;
  border-radius: 50%;
  border: 2px solid var(--border);
  margin-left: auto;
  background: transparent;
}
.aufgabe__status[data-status="filled"] { background: var(--green); border-color: var(--green); }
```

Per JS aktualisiert sobald Felder innerhalb der Karte sich ändern.

### Was wir NICHT machen

| Element | Warum nicht |
|---|---|
| **Streaks** („Du hast 5 Tage in Folge gelernt!") | Erzeugt Verlust-Angst, wenn der Streak reißt. |
| **Ranglisten** (intern oder klassenweit) | Stigmatisiert Schwächere. Lernen ≠ Wettkampf. |
| **Zeit-Druck** (Countdown, Stoppuhr) | Hat im Lern-Setting nichts verloren außer in expliziten Quiz-Aufgaben. |
| **Punkte/XP-System** | Kann auf den ersten Blick motivierend wirken — führt aber dazu, dass Schüler:innen für Punkte arbeiten statt zu verstehen. |
| **Sterne / Bewertungen** (3-Sterne-Pro-Aufgabe) | Selbe Falle wie XP. |
| **Achievement-Pop-ups** mit Konfetti-Animation | Zu groß, zu unterbrechend. Sektion-Abschluss-Marker reicht. |

## Alternativen

- **Gar keine Gamification** (Status quo Phase 1): Verworfen — fehlende Orientierung auf langen Onepagern.
- **Volle Gamification** (Punkte, Levels, Streaks): Verworfen — siehe „Was wir NICHT machen".
- **Nur Fortschrittsbalken, kein Sektion-Marker:** Erwogen — Sektion-Marker fühlt sich für kurze Onepager (≤ 3 Aufgaben) übertrieben an. Lösung: Sektion-Marker nur ab `≥ 3 Aufgaben pro Sektion` aktivieren.

## Konsequenzen

**Positiv:**
- Schüler:innen sehen ihren Fortschritt, ohne unter Druck zu geraten
- Sektion-Abschluss wirkt als kleines Erfolgserlebnis
- Keine Verlust-Angst, keine Konkurrenz
- A11y: ARIA-Label und keine Bewegung bei `prefers-reduced-motion`

**Negativ / Trade-offs:**
- „Bearbeitet" ≠ „richtig" — Schüler:innen könnten den Balken füllen, indem sie Quatsch eintragen. Akzeptabel, weil die Selbst-Korrektur (ADR-0011) dieses Risiko abfedert.
- Etwas mehr JS-Logik

**Folgewirkungen für künftige Onepager:**
- Topbar **immer** mit `.progress`-Container (auch wenn nur 3 Aufgaben — der Balken ist dezent)
- Jede `<section>` zwischen `<h2>`-Tags optional mit `<div class="abschnitt-fertig" hidden>` enden
- Aufgaben-Status-Punkt im `.aufgabe__header` ist optional, aber empfohlen
- Kein anderes Gamification-Element ohne neues ADR

## Verwandte ADRs

- [ADR-0017](0017-save-status-toast.md) — Topbar-Bereich, in dem der Fortschrittsbalken sitzt
- [ADR-0018](0018-aufgaben-karten.md) — Aufgaben-Karten als Zähleinheit
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — `prefers-reduced-motion`
