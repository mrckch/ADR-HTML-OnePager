# ADR-0007: Druck- und PDF-Optimierung (A4)

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Druck, PDF-Export, Layout

## Kontext

Onepager werden gelegentlich ausgedruckt — entweder von der Lehrkraft (Klassensatz) oder von Schüler:innen (Hausaufgabe in Papierform). Manche speichern sie auch über den Browser-Druckdialog als PDF.

Häufige Probleme ohne Print-CSS:
- Sticky-Menü erscheint auf jeder Druckseite
- Hintergrundfarben werden nicht gedruckt (Standardverhalten der meisten Browser)
- Schlechte Seitenumbrüche (Überschriften am Seitenende, Tabellen mittendurch geschnitten)
- Hyperlinks zeigen kein Ziel
- Schrift zu groß/klein für A4

## Entscheidung

**1. Eigene `@media print`-Sektion in jedem Onepager:**

```css
@media print {
  /* Seitenformat */
  @page {
    size: A4;
    margin: 1.5cm;
  }

  /* Menü und interaktive Elemente ausblenden */
  .topbar,
  .no-print,
  button {
    display: none !important;
  }

  /* Hintergrund auf weiß, Text auf schwarz */
  body {
    background: #fff;
    color: #000;
    font-size: 11pt;
    line-height: 1.4;
  }

  /* Seitenumbrüche steuern */
  h1, h2, h3 {
    break-after: avoid;
    page-break-after: avoid;
  }
  figure, table, pre {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  /* Links mit URL in Klammern (nur für externe Links) */
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.85em;
    color: #555;
  }

  /* Schülereingaben sichtbar drucken */
  input[type="text"],
  textarea {
    border: 1px solid #000;
    background: #fff;
  }
}
```

**2. Print-spezifische Hilfsklassen** im normalen CSS:
- `.no-print` — wird im Druck ausgeblendet
- `.print-only` — wird **nur** im Druck angezeigt (z. B. „Name: ___________" am Seitenanfang)

**3. Schülerantworten werden mitgedruckt** — Inputs, Checkboxen und Textareas behalten ihre Werte im Druck.

**4. Test:** Vor Veröffentlichung jedes Onepagers einmal die Druckvorschau (`Cmd/Strg+P`) prüfen.

## Alternativen

- **PDF generieren per JS (z. B. jsPDF, html2pdf):** Verworfen — zusätzliche Bibliothek, widerspricht [ADR-0001](0001-single-file-html-architektur.md), Layout-Ergebnisse oft schlechter als Browser-Druck.
- **Print-Stylesheet auslagern:** Verworfen — Single-File-Prinzip.
- **Kein Print-CSS:** Verworfen — Druckergebnis sonst unbrauchbar.

## Konsequenzen

**Positiv:**
- Ausgedrucktes Ergebnis sieht sauber aus
- Speichern als PDF via Browser funktioniert sofort
- Lehrerin/Lehrer kann Schülerantworten ausdrucken (z. B. zur Bewertung)
- Konsistentes Druckbild über alle Onepager

**Negativ / Trade-offs:**
- Etwas Mehrarbeit pro Onepager beim Layout-Check
- Browser-Unterschiede im Druck-Rendering (Safari, Chrome, Firefox unterschiedlich) → vor Veröffentlichung kurz prüfen

**Folgewirkungen für künftige Onepager:**
- `@media print { … }` mit obigem Grundgerüst **immer** vorhanden
- `.topbar` und alle `button`s im Druck ausblenden
- `@page { size: A4; margin: 1.5cm; }` als Default
- Vor Veröffentlichung: Druckvorschau prüfen
- Bei längeren Inhalten: `break-inside: avoid` für zusammengehörige Blöcke

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Single-File (kein externes PDF-Tool)
- [ADR-0005](0005-sticky-menue-ios-safe-area.md) — Sticky-Menü beim Druck ausblenden
- [ADR-0008](0008-design-system.md) — Typografie
