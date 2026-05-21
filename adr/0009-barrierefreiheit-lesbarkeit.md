# ADR-0009: Barrierefreiheit und Lesbarkeit

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Accessibility, Inklusion, Lesbarkeit

## Kontext

In der Klasse gibt es Schüler:innen mit:
- Leseschwäche / LRS / Legasthenie
- Sehschwächen (Brille, Kontraste, Vergrößerungsbedarf)
- Motorischen Einschränkungen (Touch ungenau, Tastaturnutzung)
- Konzentrationsschwierigkeiten

Die Onepager sollen für **alle** gut nutzbar sein. Ziel: WCAG 2.1 AA als Orientierungsmarke, kein formaler Audit.

## Entscheidung

**1. Semantisches HTML als Grundlage:**
- `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>` korrekt verwenden
- Eine sinnvolle Überschriftenhierarchie (`<h1>` einmalig, dann `<h2>`, `<h3>` …)
- Formulare mit `<label>` (entweder umschließend oder über `for=…`)
- Buttons sind `<button>`, Links sind `<a>` — niemals `<div onclick>`

**2. Sprache und Schreibrichtung:**
```html
<html lang="de">
```

**3. Farbkontraste:**
- Text: mindestens 4.5:1 zum Hintergrund (AA)
- Großtext (≥18pt oder fett ≥14pt): mindestens 3:1
- Farben aus dem Design-System ([ADR-0008](0008-design-system.md)) sind so gewählt, dass sie AA erfüllen — bei Anpassungen prüfen (z. B. WebAIM Contrast Checker)

**4. Fokus-Indikator immer sichtbar:**
```css
*:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```
Niemals `outline: none` ohne Ersatz.

**5. Lesefreundliche Typografie:**
- Zeilenlänge max. ca. 70 Zeichen (`max-width: 65ch` für Fließtext-Container)
- Zeilenhöhe `1.6` für Body-Text ([ADR-0008](0008-design-system.md))
- Schriftgrößen relativ (`rem`) — Browser-Zoom funktioniert
- Linksbündig, nicht Blocksatz (Blocksatz erzeugt unregelmäßige Lücken, schlecht für LRS)

**6. Bilder:**
- **Immer** `alt`-Attribut. Dekorative Bilder: `alt=""`. Sonst beschreibend.
- SVG-Icons: entweder `aria-hidden="true"` (rein dekorativ) oder mit `<title>`-Element/`aria-label`

**7. Touch- und Tastatur-Bedienung:**
- Touch-Targets ≥44×44 px ([ADR-0006](0006-responsives-layout.md))
- Alle interaktiven Elemente per Tab erreichbar
- Logische Tab-Reihenfolge (DOM-Reihenfolge folgt visueller Reihenfolge)
- `Esc` schließt Dialoge ([ADR-0004](0004-reset-funktion-mit-bestaetigung.md))

**8. Dialoge / Modals:**
- `role="dialog" aria-modal="true"`
- Fokus beim Öffnen in den Dialog setzen
- Fokus-Trap: Tab bleibt im Dialog
- Beim Schließen: Fokus zurück auf den auslösenden Button

**9. Reduktion von Bewegung:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**10. Klare Sprache:**
- Anweisungen kurz und konkret
- Fachbegriffe erklären
- Aktive Formulierungen bevorzugen

## Alternativen

- **Eigene LRS-Schrift einbinden (z. B. OpenDyslexic):** Verworfen — externe Schrift widerspricht [ADR-0001](0001-single-file-html-architektur.md). Studienlage ist außerdem uneindeutig. Schüler:innen können bei Bedarf systemweit eine Lese-Schrift einstellen.
- **Eigener Vergrößerungs-Button:** Verworfen — Browser-Zoom (`Strg/Cmd ++`) erfüllt diesen Zweck zuverlässig, wenn das Layout flexibel ist.
- **Hoch-Kontrast-Modus per Button:** Erwogen, aber `prefers-contrast: more` über das Betriebssystem reicht meist.

## Konsequenzen

**Positiv:**
- Onepager sind für ein breiteres Publikum nutzbar
- Tastaturnutzer und Screenreader funktionieren
- Browser-Zoom funktioniert ohne Brüche
- Reduzierte Bewegung respektiert Systemeinstellung

**Negativ / Trade-offs:**
- Mehr Sorgfalt bei Markup und Stil nötig
- Kontrast-Check bei jeder Farbänderung

**Folgewirkungen für künftige Onepager:**
- `<html lang="de">` **immer**
- Semantische Elemente **immer** verwenden
- `*:focus-visible` mit sichtbarem Outline **immer**
- `alt`-Attribut an jedem `<img>`, ggf. leer für dekorative
- Dialoge mit `role="dialog"`, `aria-modal`, Fokus-Trap, `Esc`
- `prefers-reduced-motion`-Block immer mitkopieren
- Vor Veröffentlichung: einmal mit Tab durchsteppen, einmal mit Browser-Zoom 200 % prüfen

## Verwandte ADRs

- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Dialog-A11y
- [ADR-0006](0006-responsives-layout.md) — Touch-Targets, Browser-Zoom
- [ADR-0008](0008-design-system.md) — Farbkontraste, Typografie
