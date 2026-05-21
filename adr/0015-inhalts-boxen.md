# ADR-0015: Inhalts-Boxen — visuelle Strukturierung

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Layout, Lesbarkeit, didaktische Struktur

## Kontext

Lerntexte sind anstrengend zu lesen, wenn alles wie Fließtext aussieht. Schüler:innen sollen auf den ersten Blick erkennen können:

- *„Aha, das ist ein Merksatz, das muss ich mir behalten."*
- *„Das ist ein Tipp — wenn ich nicht weiterkomme, hilft mir das."*
- *„Das ist eine Warnung — hier passiert leicht ein Fehler."*

Wenn jede Lehrkraft sich eigene Box-Stile ausdenkt, wirkt der Onepager unruhig und verlangt von der/dem Lesenden, das Schema neu zu lernen. Ein **fester, kleiner Satz von Boxtypen** mit konsistentem Look löst das.

## Entscheidung

Fünf verbindliche Box-Typen, alle mit einheitlichem Aufbau:
- Links farbiger Rand (4 px)
- Heller getönter Hintergrund
- Kleiner Uppercase-Header mit Icon
- Body-Text in normaler Größe

Farben kommen aus den Tokens von [ADR-0022](0022-design-system-v2.md).

| Klasse | Zweck | Farbe |
|---|---|---|
| `.lernziel` | „Was du heute lernst …" | Blau (`--blue`) |
| `.merke`    | Merksatz, Formel, Definition | Gold (`--gold`) |
| `.info`     | Zusätzliche Information / Hinweis | Blau (`--blue`, dezenter Hintergrund) |
| `.tipp`     | Hilfestellung, wenn ein:e Schüler:in nicht weiterkommt | Grün (`--green`) |
| `.warn`     | Warnung vor häufigen Fehlern | Rot (`--red`) |

### CSS-Grundgerüst

```css
.box {
  border: 1px solid var(--border-soft);
  border-left-width: 4px;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: var(--space-3) var(--space-5);
  margin: var(--space-4) 0;
  font-size: var(--fs-base);
}
.box > .box-title {
  display: block;
  font-size: var(--fs-sm);
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

.lernziel { background: var(--bg-info); border-left-color: var(--blue); }
.lernziel > .box-title { color: var(--blue); }

.merke    { background: #FFFBF0; border-left-color: var(--gold); }
.merke    > .box-title { color: var(--navy); }   /* Gold auf Gold wäre unleserlich */

.info     { background: var(--bg-info); border-left-color: var(--blue); }
.info     > .box-title { color: var(--blue); }

.tipp     { background: #F0F8F2; border-left-color: var(--green); }
.tipp     > .box-title { color: var(--green); }

.warn     { background: #FDF1EF; border-left-color: var(--red); }
.warn     > .box-title { color: var(--red); }

/* Dark Mode — Hintergründe nochmal dezent überschreiben */
@media (prefers-color-scheme: dark) {
  .merke { background: #2a2310; }
  .tipp  { background: #14241a; }
  .warn  { background: #2a1814; }
}
```

### HTML-Verwendung

```html
<div class="box lernziel">
  <span class="box-title">✦ Was du heute lernst</span>
  <ul>
    <li>…</li>
  </ul>
</div>

<div class="box merke">
  <span class="box-title">📌 Merke</span>
  <p>V = G · h (Volumen = Grundfläche · Höhe)</p>
</div>

<div class="box tipp">
  <span class="box-title">💡 Tipp</span>
  <p>Drehwinkel = 360° ÷ Anzahl Ecken</p>
</div>

<div class="box warn">
  <span class="box-title">⚠️ Achtung</span>
  <p>Die Reihenfolge der Anweisungen ist entscheidend!</p>
</div>
```

### Icon-Konventionen

Ein Icon pro Box-Titel, immer das gleiche pro Box-Typ:

| Box | Icon |
|---|---|
| `.lernziel` | ✦ |
| `.merke`    | 📌 |
| `.info`     | ℹ️ oder ✦ |
| `.tipp`     | 💡 |
| `.warn`     | ⚠️ |

Icons sind reine Unicode-Emojis (keine Icon-Fonts, kein externer Asset).

## Alternativen

- **Kein Box-System, freier Stil:** Verworfen — führt zu Inkonsistenz und mehr Aufwand pro Onepager.
- **Mehr Box-Typen** (z. B. `.zitat`, `.beispiel`, `.frage`): Bewusst auf 5 begrenzt. Wer mehr Differenzierung braucht, soll Inhalt in Aufgaben-Karten ([ADR-0018](0018-aufgaben-karten.md)) packen.
- **Boxen ohne farbigen Linksrand**, nur mit Tönung: Verworfen — der Linksrand ist der schnellste visuelle Hinweis und gut sichtbar auch in s/w-Druck.

## Konsequenzen

**Positiv:**
- Schüler:innen erkennen Inhaltstypen auf einen Blick
- Lehrkräfte müssen pro Onepager nur 5 Typen kennen, nicht neu designen
- Druckbar (Linksrand bleibt sichtbar in s/w)
- Wiederverwendbar als kopierbares Snippet

**Negativ / Trade-offs:**
- Box-CSS muss pro Onepager mitkopiert werden (Single-File, ADR-0001)
- Hintergrundfarben werden beim Standarddruck nicht automatisch gedruckt → Linksrand übernimmt die Erkennbarkeit

**Folgewirkungen für künftige Onepager:**
- Nur diese 5 Box-Klassen verwenden, keine eigenen erfinden
- Jede Box hat genau einen `.box-title` mit Icon
- Bei Bedarf neue Box-Typen erst via neuem ADR ergänzen
- Box-Hintergründe in Dark-Mode-Block mitpflegen

## Verwandte ADRs

- [ADR-0022](0022-design-system-v2.md) — Token-Quelle für alle Farben
- [ADR-0018](0018-aufgaben-karten.md) — Aufgaben sind keine Boxen, sondern eigene Karten
