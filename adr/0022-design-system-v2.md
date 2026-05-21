# ADR-0022: Aktualisiertes Design-System (Editorial)

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Styling, Typografie, Farben, visuelle Identität
- **Ersetzt:** [ADR-0008](0008-design-system.md)

## Kontext

Das ursprüngliche Design-System aus ADR-0008 hatte einen sehr technisch/UI-getriebenen Look: kühles Blau auf Reinweiß mit System-Sans als Standardschrift. In der Praxis wirkte das auf Schüler:innen wenig „Lehrmaterial" und mehr „App" — und damit weniger einladend für längere Lerneinheiten.

Vorbild für die Aktualisierung ist ein selbst erstelltes Arbeitsblatt (UE3 Sequenz), das durch warme, editorial wirkende Farben und einen Serif-Sans-Mix deutlich besser angenommen wurde:

- Tiefes Navy für Überschriften und Topbar
- Gold als wärmender Akzent
- Off-White-Hintergrund („Papier-Anmutung")
- Serif für Überschriften (Lehrbuch-Feeling), Sans für den Lesetext
- Antwortfelder mit Cream-Hintergrund und goldener Linkskante (klar sichtbar als „hier schreibst du")

## Entscheidung

Ein neuer Satz von **CSS-Custom-Properties** ersetzt die Tokens aus ADR-0008. Alle Onepager (und das Boilerplate) verwenden diese Tokens.

```css
:root {
  /* --- Farben (Light Mode) --- */
  --navy:          #1a2340;   /* Hauptakzent: Überschriften, Topbar */
  --navy-soft:     #2a3a5a;   /* Body-Text auf hellem Grund, weniger hart */
  --gold:          #E8A838;   /* Wärmender Akzent: Aufgaben-Border, Antwort-Linksrand */
  --blue:          #4A90D9;   /* Sekundär: Info-Boxen, Links */
  --green:         #1a6b45;   /* Erfolg / Success */
  --red:           #C0645A;   /* Warnung / Danger (gedämpft, nicht knallig) */

  --bg:            #F5F2EB;   /* Off-White — Seiten-Hintergrund (Papier) */
  --bg-page:       #FFFFFF;   /* Die "Seite" selbst (Container) */
  --bg-elevated:   #FFFBF0;   /* Karten-Header, leicht warm */
  --bg-info:       #EEF4FB;   /* Info-Box-Hintergrund */
  --bg-answer:     #FFFDF5;   /* Antwort-Felder, „Schreibflächen" */
  --bg-code:       #0D1117;   /* Code-Boxen, GitHub-Dark */

  --fg:            #1a1a1a;   /* Primärtext */
  --fg-muted:      #555a60;   /* Hinweise, Captions */
  --fg-soft:       #8a9ab8;   /* Sehr dezent, Meta-Labels auf Navy */

  --border:        #D8D0C4;   /* Warmer grauer Rand */
  --border-soft:   #E8E2D6;   /* Noch dezenter */

  /* --- Typografie --- */
  --font-serif:    ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-sans:     -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                   "Helvetica Neue", Arial, sans-serif,
                   "Apple Color Emoji", "Segoe UI Emoji";
  --font-mono:     ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
                   "Liberation Mono", monospace;

  --fs-base:       15px;       /* Etwas kleiner als 16px — wirkt "gesetzter" */
  --fs-sm:         13px;
  --fs-xs:         11px;
  --fs-lg:         17px;
  --fs-h3:         18px;
  --fs-h2:         22px;
  --fs-h1:         clamp(24px, 4vw, 32px);

  --lh-body:       1.65;       /* Etwas luftiger als 1.6 */
  --lh-heading:    1.25;

  /* --- Abstände (4-px-Skala) --- */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px;
  --space-4: 16px; --space-5: 20px; --space-6: 24px;
  --space-8: 32px; --space-10: 40px;

  /* --- Radien & Schatten --- */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 10px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 4px 16px rgba(0,0,0,.10);
  --shadow-lg: 0 12px 48px rgba(0,0,0,.20);
}

/* Dark Mode — warme Anmutung beibehalten */
@media (prefers-color-scheme: dark) {
  :root {
    --navy:        #6c84c4;
    --navy-soft:   #aab8d8;
    --gold:        #E8A838;
    --blue:        #6FB0E8;
    --green:       #5DBA85;
    --red:         #E29083;

    --bg:          #15171a;
    --bg-page:     #1d2024;
    --bg-elevated: #25282c;
    --bg-info:     #1a2230;
    --bg-answer:   #25241a;
    --bg-code:     #0D1117;

    --fg:          #e8eaed;
    --fg-muted:    #a8aeb6;
    --fg-soft:     #7a8090;

    --border:      #3a3a3a;
    --border-soft: #2a2a2a;
  }
}
```

### Typografie-Anwendung

```css
body {
  font-family: var(--font-sans);
  font-size:   var(--fs-base);
  line-height: var(--lh-body);
  color:       var(--fg);
  background:  var(--bg);
}

/* Überschriften in Serif — Lehrbuch-Feeling */
h1, h2, h3, .serif {
  font-family: var(--font-serif);
  font-weight: 400;        /* Serif braucht selten Bold */
  line-height: var(--lh-heading);
  color: var(--navy);
}
h1 { font-size: var(--fs-h1); }
h2 { font-size: var(--fs-h2); border-bottom: 3px solid var(--gold); padding-bottom: var(--space-2); }
h3 { font-size: var(--fs-h3); }

code, .code { font-family: var(--font-mono); }
```

### „Seiten"-Container

Anders als bei ADR-0008 sitzt der Inhalt nicht direkt auf dem Body-Hintergrund, sondern in einem **abgesetzten weißen Container mit Schatten**, der wie ein Blatt Papier auf einem Schreibtisch wirkt:

```css
.page {
  max-width: 860px;
  margin: var(--space-8) auto var(--space-10);
  background: var(--bg-page);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}
```

Auf mobilen Geräten (`max-width: 720px`) entfallen Margin und Shadow, der Container füllt die Bildschirmbreite.

## Alternativen

- **Tailwind CSS / Bootstrap:** Weiterhin verworfen — selbe Begründung wie in ADR-0008 (externe Abhängigkeit oder zu viel ungenutztes CSS).
- **Beim alten ADR-0008-System bleiben:** Verworfen — die warme Palette wirkt für Lernmaterial nachweislich angenehmer.
- **Google Fonts (DM Serif Display, DM Sans):** Verworfen — externe Abhängigkeit, verletzt ADR-0001. System-Serif-Stack ist auf allen modernen OS ansprechend (Georgia auf Windows, Charter/New York auf macOS/iOS).
- **Eigene Schrift inline einbetten (z. B. via Base64-WOFF2):** Erwogen, aber 30–80 kB pro Schnitt summieren sich; System-Schriften sind „gut genug".

## Konsequenzen

**Positiv:**
- Wärmere, einladendere Optik — wirkt wie Lehrmaterial, nicht wie App
- Klare Lese-Hierarchie durch Serif-Headings
- Antwortfelder visuell sofort als „Schreibflächen" erkennbar (Cream-Hintergrund)
- Dunkelmodus respektiert die warme Anmutung
- Weiterhin keine externen Schriften nötig

**Negativ / Trade-offs:**
- System-Serifen variieren zwischen Plattformen (Windows: Georgia, macOS/iOS: Charter/New York, Android: oft kein guter Serif → fällt auf Times zurück). Variation ist hinnehmbar; alle modernen Systeme haben einen brauchbaren Serif.
- `--fs-base: 15px` statt 16px ist marginal kleiner; Browser-Zoom funktioniert weiterhin, weil andere Größen relativ in `px` definiert sind (nicht in `rem`, aber Skalierung folgt der Browser-Zoom-Logik).

**Folgewirkungen für künftige Onepager:**
- Token-Block aus diesem ADR **immer** im `<style>` am Anfang
- Keine willkürlichen Farb-/Abstandswerte — immer Tokens
- Überschriften standardmäßig in Serif
- Dark-Mode-Block immer mitkopieren
- Antwort-Felder (Inputs, Textareas) mit `background: var(--bg-answer)` und linkem goldenen Akzent

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Keine externen Fonts (Bestätigung)
- [ADR-0008](0008-design-system.md) — **Ersetzt durch dieses ADR**
- [ADR-0015](0015-inhalts-boxen.md) — Box-System nutzt diese Tokens
- [ADR-0017](0017-save-status-toast.md) — Toast und Save-Indikator nutzen diese Tokens
- [ADR-0018](0018-aufgaben-karten.md) — Aufgaben-Karten nutzen Gold-Border
