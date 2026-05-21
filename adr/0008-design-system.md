# ADR-0008: Konsistentes Design-System

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Styling, Typografie, Farben, Konsistenz

## Kontext

Bisher variieren Schriftarten, Farben und Abstände zwischen den Onepagern. Schüler:innen, die mehrere Materialien bearbeiten, erleben das als unruhig und unprofessionell. Auch ich selbst muss bei jedem neuen Onepager wieder neu nachdenken — das kostet Zeit und führt zu Inkonsistenzen.

## Entscheidung

**Ein verbindliches Design-System als CSS-Custom-Properties** am `:root` jedes Onepagers. Das System ist klein und an System-Schriften/-Farben orientiert, damit es plattform-nativ wirkt und keine externen Ressourcen braucht.

```css
:root {
  /* --- Farben (Light Mode) --- */
  --bg:           #ffffff;
  --bg-elevated:  #f8f9fa;
  --fg:           #1a1a1a;
  --fg-muted:     #555a60;
  --border:       #d8dce0;

  --primary:      #1e6feb;     /* Aktion / Fokus */
  --primary-fg:   #ffffff;
  --success:      #2e8b57;
  --warning:      #b46b00;
  --danger:       #b00020;

  /* --- Typografie --- */
  --font-sans:    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                  "Helvetica Neue", Arial, sans-serif,
                  "Apple Color Emoji", "Segoe UI Emoji";
  --font-mono:    ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;

  --fs-base:      1rem;        /* 16px */
  --fs-sm:        0.875rem;
  --fs-lg:        1.125rem;
  --fs-h3:        1.25rem;
  --fs-h2:        1.5rem;
  --fs-h1:        2rem;

  --lh-body:      1.6;
  --lh-heading:   1.25;

  /* --- Abstände (4-px-Skala) --- */
  --space-1:      4px;
  --space-2:      8px;
  --space-3:      12px;
  --space-4:      16px;
  --space-6:      24px;
  --space-8:      32px;
  --space-12:     48px;

  /* --- Radien & Schatten --- */
  --radius-sm:    4px;
  --radius-md:    8px;
  --radius-lg:    12px;
  --shadow-sm:    0 1px 2px rgba(0,0,0,.06);
  --shadow-md:    0 4px 12px rgba(0,0,0,.08);
}

/* Dark Mode: Schüler:innen, die ihr Gerät auf dunkel haben */
@media (prefers-color-scheme: dark) {
  :root {
    --bg:          #15171a;
    --bg-elevated: #1d2024;
    --fg:          #e8eaed;
    --fg-muted:    #a8aeb6;
    --border:      #2c3036;
    --primary:     #4d8fff;
  }
}

body {
  font-family: var(--font-sans);
  font-size: var(--fs-base);
  line-height: var(--lh-body);
  color: var(--fg);
  background: var(--bg);
}

h1 { font-size: var(--fs-h1); line-height: var(--lh-heading); }
h2 { font-size: var(--fs-h2); line-height: var(--lh-heading); }
h3 { font-size: var(--fs-h3); line-height: var(--lh-heading); }
```

**Verbindliche Regeln:**
- **Keine externen Schriftarten** (Google Fonts, Adobe Fonts) — siehe [ADR-0001](0001-single-file-html-architektur.md)
- Schriftgrößen in `rem` (Browser-Zoom funktioniert)
- Abstände immer über `--space-*`-Tokens, keine willkürlichen `px`-Werte
- Farben immer über `--*`-Tokens, keine Inline-Hex-Codes
- Dark Mode wird per `prefers-color-scheme` mitgeliefert, **kein** manueller Toggle

## Alternativen

- **Tailwind CSS:** Verworfen — externe Abhängigkeit oder zu viel ungenutztes CSS in der Single-File.
- **CSS-Framework (Bootstrap, Bulma):** Verworfen — selber Grund.
- **Pico.css o. ä. minimal CSS:** Erwogen, aber selbst die ~10 kB widersprechen dem Single-File-Prinzip nicht — könnte später als Alternative geprüft werden. Aktuell: eigenes Mini-System.

## Konsequenzen

**Positiv:**
- Alle Onepager wirken wie aus einem Guss
- Schnellere Erstellung neuer Onepager (Tokens kopieren, Inhalte einfüllen)
- Dark Mode automatisch
- Keine externen Abhängigkeiten

**Negativ / Trade-offs:**
- Tokens müssen pro Onepager mitkopiert werden (Single-File)
- Anpassungen am System bedeuten: jeden bestehenden Onepager updaten oder Inkonsistenz akzeptieren

**Folgewirkungen für künftige Onepager:**
- Token-Block **immer** im `<style>` am Anfang einbauen (am besten als kopierbares Snippet vorhalten)
- Keine willkürlichen Farb-/Abstandswerte — immer Tokens
- Dark-Mode-Block immer mitkopieren
- Bei Schriftgrößen `clamp()` für fluide Skalierung erwägen (siehe [ADR-0006](0006-responsives-layout.md))

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Keine externen Fonts
- [ADR-0006](0006-responsives-layout.md) — Fluide Typografie
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — Kontraste, Schriftgrößen
