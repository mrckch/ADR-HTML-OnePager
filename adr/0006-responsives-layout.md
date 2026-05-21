# ADR-0006: Responsives Mobile-First-Layout

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Layout, Responsivität, Touch-Bedienung

## Kontext

Die Schüler:innen öffnen die Onepager auf sehr unterschiedlichen Geräten:
- Smartphones (iOS und Android) — schmal, Touch
- Tablets (oft iPad) — mittlere Breite, Touch
- Laptops / Schul-PCs — breit, Maus/Tastatur

Häufige Probleme:
- Inhalte sind auf dem Smartphone zu klein oder zu breit (horizontaler Scrollbalken)
- Buttons sind zu klein für Touch-Bedienung
- Tabellen brechen unschön um

## Entscheidung

**Mobile-First**: Default-Styles sind für schmale Bildschirme, größere Layouts werden über `@media (min-width: …)` ergänzt.

**1. Viewport korrekt setzen** (auch nötig für Safe-Area, siehe [ADR-0005](0005-sticky-menue-ios-safe-area.md)):
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

**2. Container mit klarer Maximalbreite und seitlichem Padding:**
```css
.container {
  max-width: 800px;
  margin-inline: auto;
  padding-inline: 16px;
}
@media (min-width: 600px) {
  .container { padding-inline: 24px; }
}
```

**3. Breakpoints** (sparsam — nur was wirklich nötig ist):
- `min-width: 600px` — Tablet hochkant
- `min-width: 900px` — Tablet quer / kleiner Laptop
- Keine festen Geräte-Breakpoints; an Inhalt orientieren

**4. Flexible Einheiten:**
- Schriftgrößen in `rem` (für `<html>` `font-size: 100%` belassen, damit Browser-Zoom funktioniert)
- Layouts in `%`, `fr`, `min()`, `max()`, `clamp()` — keine festen `px`-Breiten am Container
- Beispiel: `font-size: clamp(1rem, 2.5vw, 1.125rem);`

**5. Touch-Targets ≥ 44×44 px** für alle Buttons, Links und interaktiven Elemente.

**6. Bilder und Tabellen flexibel:**
```css
img, svg { max-width: 100%; height: auto; }
.table-wrapper { overflow-x: auto; }    /* Tabellen scrollbar in der Box */
```

**7. Keine `100vh`-Container** — auf iOS Safari ist `100vh` größer als der sichtbare Bereich (URL-Leiste). Stattdessen `100dvh` (dynamic viewport height) verwenden, mit `100vh` als Fallback:
```css
.fullscreen { min-height: 100vh; min-height: 100dvh; }
```

## Alternativen

- **Desktop-First mit Skalierung nach unten:** Verworfen — schmale Screens sind die häufigsten, also dort optimieren.
- **Fertiges CSS-Framework (Bootstrap, Tailwind):** Verworfen — externe Abhängigkeit oder zu viel ungenutztes CSS in der Single-File ([ADR-0001](0001-single-file-html-architektur.md)).
- **Fixe Layouts mit Skalierung:** Verworfen — schlecht für Accessibility und Browser-Zoom.

## Konsequenzen

**Positiv:**
- Sieht auf allen Schüler-Geräten anständig aus
- Keine horizontalen Scrollbalken
- Funktioniert mit Browser-Zoom für sehschwächere Schüler:innen
- Touch- und Maus-bedienbar

**Negativ / Trade-offs:**
- Etwas mehr CSS-Sorgfalt nötig
- `100dvh` wird von älteren Browsern nicht unterstützt → Fallback nötig

**Folgewirkungen für künftige Onepager:**
- Mobile-First-CSS schreiben
- Max-Breite `800px` für Lese-Inhalte
- Schriftgrößen relativ (`rem`/`clamp`), nie fix in `px`
- Touch-Targets ≥44 px
- Tabellen in `overflow-x: auto`-Wrapper
- `100dvh` mit `100vh`-Fallback für Vollbild-Sektionen

## Verwandte ADRs

- [ADR-0005](0005-sticky-menue-ios-safe-area.md) — Viewport-Meta-Tag
- [ADR-0008](0008-design-system.md) — Typografie-Skala
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — Touch-Targets und Zoom
