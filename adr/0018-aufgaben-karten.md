# ADR-0018: Aufgaben-Karten — visuelle Struktur

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Layout, didaktische Struktur, Wiedererkennbarkeit

## Kontext

Im Boilerplate v1 war eine Aufgabe ein einfacher Block mit dünnem grauen Rand. Auf einer Seite mit viel Fließtext, Beispielen und Boxen verschwammen die Aufgaben optisch mit allem anderen.

Schüler:innen sollen auf einen Blick sehen:
1. **„Hier ist eine Aufgabe."**
2. **„Welche Nummer hat sie?"**
3. **„Was ist die Frage?"** (Titel)
4. **„Wo trage ich meine Antwort ein?"** (Body, getrennt vom Aufgaben-Kopf)

Vorbild ist das Turtle-Arbeitsblatt: Aufgaben mit goldener Top-Border, getöntem Header, Pille-Badge für die Aufgaben-Nummer und klar abgesetztem Body.

## Entscheidung

Eine **Aufgabe ist eine eigenständige Karte** mit dreigliedrigem Aufbau: Top-Border, Header, Body.

### HTML-Struktur

```html
<article class="aufgabe" data-task-id="1.1">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 1.1</span>
    <h3 class="aufgabe__titel">Quader: Berechne das Volumen</h3>
  </header>
  <div class="aufgabe__body">
    <p>Aufgabentext, Skizzen, Eingabefelder …</p>
  </div>
</article>
```

- `<article>` als semantischer Container (eigenständiger Inhalt)
- `data-task-id` als eindeutige ID, an die andere Module (Lösungs-Reveal, Fortschritt, Quiz) andocken können
- `aufgabe__nr` als **Pille-Badge** mit goldenem Hintergrund — sofortiger visueller Anker
- `aufgabe__titel` als `<h3>` (Serif aus ADR-0022, passt sich in die Heading-Hierarchie ein)
- `aufgabe__body` mit eigenem Padding, klar getrennt vom Header

### CSS

```css
.aufgabe {
  border: 1px solid var(--border);
  border-top: 4px solid var(--gold);
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  margin: var(--space-6) 0;
  background: var(--bg-page);
  overflow: hidden;
  break-inside: avoid;        /* Druck: nicht zerschneiden */
  page-break-inside: avoid;
}

.aufgabe__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-5);
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
}

.aufgabe__nr {
  background: var(--gold);
  color: var(--navy);
  font-weight: 800;
  font-size: var(--fs-sm);
  letter-spacing: 0.04em;
  padding: 2px var(--space-3);
  border-radius: 999px;       /* Pille */
  white-space: nowrap;
}

.aufgabe__titel {
  margin: 0;
  font-family: var(--font-serif);
  font-size: var(--fs-h3);
  color: var(--navy);
  font-weight: 400;
  line-height: 1.3;
  border: 0;                  /* Kein Heading-Unterstrich hier */
  padding: 0;
}

.aufgabe__body { padding: var(--space-5); }
.aufgabe__body > :first-child { margin-top: 0; }
.aufgabe__body > :last-child  { margin-bottom: 0; }

/* Dark Mode kommt automatisch über die Tokens. */
```

### Antwort-Felder innerhalb der Karte

Antwort-Inputs/Textareas heben sich nochmal ab — Cream-Hintergrund, goldener Linksrand:

```css
.aufgabe__body input[type="text"],
.aufgabe__body input[type="number"],
.aufgabe__body textarea {
  background: var(--bg-answer);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
```

### Optional: Status-Indikator pro Aufgabe

Wenn ADR-0012 (Gamification) später Fortschritt anzeigt, kann ein kleines Status-Symbol am Karten-Header andocken:
```html
<span class="aufgabe__status" data-state="done"></span>
```
Wird dort von ADR-0012 spezifiziert; hier nur Platz vorgesehen.

## Alternativen

- **Aufgaben als `<details>`** (einklappbar): Verworfen — Aufgaben sollen *immer* sichtbar sein; einklappbar werden Lösungen ([ADR-0010](0010-loesungs-huerde.md)), nicht die Aufgaben.
- **Aufgaben ohne Top-Border**, nur mit grauem Rahmen: Verworfen — die goldene Top-Border ist der schnellste Erkennungsanker.
- **Aufgaben-Nr nicht als Pille, sondern als Präfix im Titel** („Aufgabe 1.1 — Quader …"): Verworfen — die Pille macht die Nummerierung visuell stärker und einfacher überfliegbar.

## Konsequenzen

**Positiv:**
- Aufgaben sind auf der Seite sofort erkennbar
- Eindeutige `data-task-id` ermöglicht spätere Erweiterungen (Lösungs-Reveal, Fortschritt)
- Karten-Layout wirkt aufgeräumt und wertig
- Druck-freundlich (`break-inside: avoid`)

**Negativ / Trade-offs:**
- Vertikaler Platzverbrauch ist etwas größer als beim alten Block-Layout
- Header-Hintergrund wird beim Standarddruck nicht gefüllt → Pille bleibt aber sichtbar, das reicht

**Folgewirkungen für künftige Onepager:**
- Aufgaben **immer** als `<article class="aufgabe">` strukturieren
- `data-task-id` **immer** vergeben (z. B. `"1.1"`, `"2.3"`, `"quiz-1"`)
- Keine selbst-gebastelten Aufgaben-Container — wer Sonderfälle hat, soll ein neues ADR vorschlagen
- Aufgaben-Body verwendet die Standard-Antwort-Feld-Styles aus diesem ADR

## Verwandte ADRs

- [ADR-0022](0022-design-system-v2.md) — Token-Quelle (Gold, Navy, Border)
- [ADR-0010](0010-loesungs-huerde.md) — Lösungs-Reveal dockt an Karten an (kommt in Phase 2)
- [ADR-0012](0012-gamification.md) — Fortschritt nutzt `data-task-id` (kommt in Phase 2)
- [ADR-0015](0015-inhalts-boxen.md) — Boxen sind keine Karten
