# ADR-0005: Sticky Top-Menü mit iOS Safe-Area-Beachtung

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Navigation, iOS-Kompatibilität, UX

## Kontext

Jeder Onepager hat ein Top-Menü mit zentralen Aktionen (Export, Import, Reset, ggf. weitere). Dieses Menü soll **immer sichtbar** sein, auch beim Scrollen, damit Schüler:innen jederzeit speichern oder zurücksetzen können.

Problem auf iOS Safari (und iOS Chrome, das WebKit nutzt):
- iOS hat eine **Status-/Notch-/Dynamic-Island-Zone** am oberen Bildschirmrand
- Ohne Safe-Area-Beachtung wird der oberste Bereich der Seite **vom System überdeckt** — Buttons werden unklickbar oder unsichtbar
- Die URL-Leiste in Safari kann ein- und ausgeblendet werden (beim Scrollen), was die effektive Viewport-Höhe ändert
- `position: fixed` und `position: sticky` verhalten sich auf iOS gelegentlich unerwartet, insbesondere bei aufgeklappter Tastatur

## Entscheidung

**1. Sticky-Top-Menü mit `position: sticky` am Top-Container, nicht `position: fixed` am Body.**

Konkret: Das Menü ist ein `<header>` direkt am Anfang des Hauptcontainers mit `position: sticky; top: 0; z-index: 100;`. Das verhält sich auf iOS robuster und ist barriereärmer.

**2. iOS Safe-Area-Inset via `env(safe-area-inset-top)` respektieren.**

Im `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

Im CSS:
```css
body {
  /* Safe-Area-Reserve, damit Inhalt nicht in die Notch/Statusleiste rutscht */
  padding-top: env(safe-area-inset-top, 0px);
  padding-left: env(safe-area-inset-left, 0px);
  padding-right: env(safe-area-inset-right, 0px);
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg);
  /* Schatten erst beim Scroll, optisch ruhiger */
  border-bottom: 1px solid var(--border);
  min-height: 56px;          /* Touch-Target */
  padding: 8px 16px;
}

.topbar button {
  min-height: 44px;          /* Apple HIG: 44pt min */
  min-width: 44px;
}
```

**3. Menü nicht direkt am oberen Rand**, sondern mit `padding-top: env(safe-area-inset-top)` am `<body>`. Damit gleitet der Inhalt nicht unter die iOS-Statusleiste.

**4. Druck-Verhalten:**
```css
@media print {
  .topbar { display: none; }
}
```
Das Menü wird im Ausdruck nicht gedruckt ([ADR-0007](0007-druck-pdf-optimierung.md)).

**5. Optional bei langen Onepagern:** Sticky-Menü beim Hochscrollen einblenden, beim Runterscrollen ausblenden (hide-on-scroll-down). Nur einbauen, wenn nötig — Default ist immer sichtbar.

## Alternativen

- **`position: fixed`:** Verworfen — iOS hat hier in der Vergangenheit Probleme gemacht, insbesondere bei eingeblendeter Tastatur.
- **Bottom-Menü:** Verworfen — wird durch iOS Safari-URL-Leiste am unteren Rand verdeckt, schwer mit `env(safe-area-inset-bottom)` korrekt zu platzieren.
- **Hamburger-Menü:** Verworfen für die Hauptaktionen (Export/Import/Reset) — diese sollen ein-Klick erreichbar sein. Wenn später mehr Aktionen dazukommen, kann ein „Mehr"-Menü ergänzt werden.

## Konsequenzen

**Positiv:**
- Menü ist auf allen Geräten sichtbar und korrekt platziert
- Keine Überdeckung durch iOS-Statusleiste/Notch
- Touch-Targets sind groß genug (≥44 px)
- Im Ausdruck unsichtbar

**Negativ / Trade-offs:**
- `viewport-fit=cover` ist Pflicht — sonst kein Safe-Area-Inset
- Bei vielen Buttons muss das Layout responsiv schrumpfen (Icons statt Text auf kleinen Screens)

**Folgewirkungen für künftige Onepager:**
- `<meta name="viewport" … viewport-fit=cover>` **immer** setzen
- `env(safe-area-inset-*)` **immer** am `<body>` als Padding
- `.topbar` als `position: sticky; top: 0`, nicht `fixed`
- Touch-Targets ≥44×44 px
- `@media print { .topbar { display: none; } }`

## Verwandte ADRs

- [ADR-0003](0003-json-export-import.md) — Buttons im Menü
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Reset im Menü
- [ADR-0006](0006-responsives-layout.md) — Responsives Verhalten
- [ADR-0007](0007-druck-pdf-optimierung.md) — Menü beim Druck ausblenden
