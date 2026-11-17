# ADR-0031: Design-System v3 „Signal" (Bildschirm- und Projektions-Flächen)

- **Status:** Accepted
- **Datum:** 2026-11-17
- **Betrifft:** Design-Tokens, Typografie, Komponenten-Konventionen, Gültigkeitsbereich
- **Ersetzt nicht:** [ADR-0022](0022-design-system-v2.md) — v2 bleibt für Arbeitsblatt-Kontexte gültig

## Kontext

Das Design-System **v2 „Editorial"** ([ADR-0022](0022-design-system-v2.md), zuvor [ADR-0008](0008-design-system.md)) ist für sein Medium gebaut: ein **Arbeitsblatt**, das auf Papier oder im A4-Layout am Tablet gelesen wird. Navy `#1a2340` auf Creme `#F5F2EB`, Serif-Überschriften, Gold `#E8A838` als 3-px-Akzentlinie, Radius 10 px, Schriftgrad 15 px. Das funktioniert: gedruckt wirkt es wie ein gutes Schulbuch, und alle Demos plus beide Boilerplates sind darin konsistent.

Mit `UEBERSICHT.html` ist aber ein Seitentyp entstanden, dessen Medium **nicht** Papier ist: eine Übersichtsseite über den Baukasten, die am Bildschirm gelesen, gescrollt und gefiltert wird. Dort trägt die Editorial-Palette nicht — Creme und Serif lesen sich auf einer Webseite mit Filter-Chips, Karten-Grid und Hero-Fläche wie ein Fremdkörper, und die zarten Gold-Linien verschwinden auf großen Flächen.

Deshalb wurde für diese Seite ein zweites Token-Set gebaut: **v3 „Signal"**. Es existiert seit Commit `d783d82` produktiv, der Datei-Kommentar von `UEBERSICHT.html` verweist bereits auf „ADR-0031 (Design-System v3 Signal)" — **diese ADR fehlte jedoch**. Ein undokumentiertes Design-System auf genau einer Seite ist ein Wartungsrisiko: der nächste Seitentyp erfindet entweder ein viertes System oder greift zu v2 und passt nicht zu seinem Medium.

Mit dem Präsentations-Profil ([ADR-0032](0032-praesentations-variante.md)) kommt genau so ein Seitentyp dazu: eine Fläche, die **projiziert** wird. Hier ist v3 nicht nur Geschmack, sondern funktional überlegen — kräftige Vollflächen und harte Kontraste überleben einen Beamer in einem nicht ganz dunklen Klassenraum, Creme wird an der Wand zu Grau.

## Entscheidung

**v3 „Signal" wird als eigenständiges, benanntes Design-System festgeschrieben** — mit einem klar begrenzten Gültigkeitsbereich. Es ersetzt v2 **nicht**, sondern tritt daneben.

### Gültigkeitsbereich — welches System wann?

| Medium | System | Seitentypen |
|---|---|---|
| **Papier / A4** — wird gedruckt oder im A4-Layout gelesen | **v2 „Editorial"** ([ADR-0022](0022-design-system-v2.md)) | `onepager-boilerplate.html`, `infoseite-boilerplate.html`, alle Aufgaben- und Info-Profile |
| **Bildschirm** — wird gescrollt, gefiltert, navigiert | **v3 „Signal"** | `UEBERSICHT.html` und künftige Übersichts-/Navigationsseiten |
| **Projektion** — wird an die Wand geworfen | **v3 „Signal"** | `praesentation-boilerplate.html` ([ADR-0032](0032-praesentations-variante.md)) |

**Harte Regel: eine Seite nutzt genau ein System.** Kein Mischen von Navy/Gold und Blau/Orange in derselben Datei — das ist der häufigste Weg, wie zwei Design-Systeme zu einem Brei werden.

**Bestehende Dateien werden nicht migriert.** Die beiden Boilerplates und alle Demos bleiben v2. Eine Migration wäre ein eigener, großer Umbau (jedes Druck- und Dark-Layout neu prüfen) und ist nicht Teil dieser Entscheidung.

### Tokens

```css
:root{
  /* Signal-Blau — Primäraktion, Links, Karten-Oberkante */
  --blue:       #0C5ADB;
  --blue-dark:  #0A49B0;
  --blue-deep:  #00247E;
  --blue-wash:  #EAF1FE;

  /* Marken-Fläche — Topbar, Hero, Footer, Titelfolie */
  --brand-surface:#00247E;
  --on-brand:   #FFFFFF;
  --on-accent:  #FFFFFF;

  /* Signal-Orange — Akzent, Kicker, Fokus, Schrittmarken. Sparsam! */
  --orange:     #FF5E14;
  --orange-wash:#FFF0E9;

  --ink:        #1B1A1A;   /* Überschriften */
  --ink-2:      #353535;   /* Fließtext */
  --muted:      #6E7076;   /* Sekundär, Meta */

  --bg:         #FFFFFF;
  --bg-alt:     #F4F6FA;   /* abgesetzte Abschnitte / Folienfläche */
  --bg-card:    #FFFFFF;
  --border:     #E1E6EF;
  --border-2:   #CBD4E3;   /* kräftiger, für 2-px-Rahmen */

  --shadow:     0 1px 2px rgba(16,24,40,.04), 0 8px 24px rgba(16,24,40,.06);
  --shadow-lift:0 2px 4px rgba(16,24,40,.06), 0 16px 40px rgba(16,24,40,.12);

  --radius: 4px;      /* flach — v2 nutzte 10px */
  --radius-lg: 8px;
  /* Pillen (Chips, Tags, Eyebrow) immer 999px */
}
```

### Typografie

| Rolle | Festlegung |
|---|---|
| **Display** (h1–h4, Buttons, Labels) | `--font-display`: `"Rajdhani", "Oswald", "Segoe UI Variable Display", "Segoe UI Semibold", "Segoe UI", system-ui, …` — Gewicht **700**, `line-height: 1.1`, `letter-spacing: -.01em` bei Headlines |
| **Fließtext** | `--font-sans`: `"Open Sans", "Segoe UI", system-ui, …` — `line-height: 1.65` |
| **Labels / Kicker / Buttons** | Display 700, `text-transform: uppercase`, `letter-spacing: .14em–.2em`, klein (`.74rem–.92rem`) |
| **Serif** | **entfällt** — v3 hat keine Serif-Rolle. Das ist der auffälligste Bruch zu v2 |

**Keine Webfonts** ([ADR-0001](0001-single-file-html-architektur.md)): Rajdhani und Open Sans werden benannt, aber nicht geladen. Wo sie lokal installiert sind, greifen sie; sonst übernimmt die System-Kette. Der Look muss **mit der Fallback-Kette funktionieren** — darum ist die Wirkung über Gewicht, Laufweite und Versalien gebaut, nicht über eine spezifische Schriftzeichnung.

### Komponenten-Konventionen

- **Eyebrow / Kicker** — Versal-Label über der Headline, orange bzw. auf Marken-Fläche in weiß mit `rgba`-Rahmen und orangem Punkt davor.
- **Karte** — `1px` Rahmen plus **`3px` Oberkante in Blau**, Radius 4 px, dezenter Schatten, beim Hover `translateY(-3px)`.
- **Hervorhebungs-Box** — `--blue-wash` mit `3px` linker Blau-Kante; Titelzeile als Versal-Label in Blau. (Entspricht funktional den Inhalts-Boxen aus [ADR-0015](0015-inhalts-boxen.md), nur in Signal-Formensprache.)
- **Chips / Tags** — Pille, `2px` Rahmen; aktiv = Blau gefüllt mit `--on-accent`.
- **Buttons** — `.btn--primary` orange gefüllt, `.btn--ghost` transparent mit Rahmen; beide Display, Versalien, Radius 4 px.
- **Fokus** — `outline: 3px solid var(--orange); outline-offset: 2px` ([ADR-0009](0009-barrierefreiheit-lesbarkeit.md)). Orange ist der Fokus-Kanal; deshalb wird Orange im Inhalt **sparsam** eingesetzt.
- **Orange-Budget** — Orange markiert, es dekoriert nicht: Kicker, Fokus, aktive Schrittmarke, maximal ein Primär-Button pro Ansicht.

### Dark Mode

```css
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){ /* dunkles Token-Set */ }
}
```

Automatik nach OS-Einstellung mit `data-theme="light"` als Notausgang. **Ausnahme Projektion:** Das Präsentations-Template dreht diese Logik um ([ADR-0032](0032-praesentations-variante.md), Entscheidung 7) — projizierte Flächen rendern unabhängig vom OS hell, Dunkel ist dort eine bewusste Wahl der Lehrkraft, keine Automatik.

## Alternativen

- **v2 für alles, auch Bildschirm und Projektion:** Konsistent, aber am falschen Medium: Creme-Flächen werden am Beamer grau, Serif-Überschriften und Haarlinien tragen auf Projektionsdistanz nicht. Verworfen.
- **v2 durch v3 ersetzen und alles migrieren:** Ein System statt zwei — aber ein großer Umbau mit Prüfaufwand bei jedem Druck- und Dark-Layout, und v3 ist für A4-Druck nicht erprobt. Verworfen (bleibt als separate Option offen).
- **v3 undokumentiert in `UEBERSICHT.html` lassen:** Der Status quo. Führt dazu, dass jeder neue Seitentyp improvisiert. Verworfen — genau deshalb gibt es diese ADR.
- **v3 nur als Profil-Empfehlung statt Core-ADR:** Profile dürfen Core-Entscheidungen laut [ADR-0024](0024-schichten-modell-profile.md) nicht ersetzen. Ein zweites Token-Set ist eine Core-Frage. Verworfen.

## Konsequenzen

**Positiv:**
- Das produktiv genutzte v3 ist dokumentiert; die Referenz in `UEBERSICHT.html` zeigt jetzt auf eine existierende ADR.
- Neue Seitentypen haben eine **Medien-Regel** statt einer Geschmacksfrage: Papier → v2, Bildschirm/Projektion → v3.
- Projektionsflächen bekommen die Kontraste, die sie brauchen.
- v2-Bestand bleibt unangetastet — kein Risiko an den geprüften Druck-Layouts.

**Negativ / Trade-offs:**
- **Zwei Design-Systeme zu pflegen.** Eine Farbänderung muss bewusst einem System zugeordnet werden. Mitigation: die Medien-Regel und das Mischverbot.
- **Der Baukasten sieht nicht mehr einheitlich aus** — ein Arbeitsblatt (Navy/Gold/Serif) und der Foliensatz zur selben Stunde (Blau/Orange/Display) sind sichtbar zwei Welten. Akzeptiert, weil Medium und Leseabstand unterschiedlich sind; wer Einheitlichkeit höher gewichtet, migriert v2 → v3 (eigener Umbau).
- **Drift-Risiko:** v3 lebt in `UEBERSICHT.html` und im Präsentations-Template parallel (kontrollierte Duplikation wie in [ADR-0030](0030-statische-infoseiten.md) beschlossen). Token-Blöcke bei Änderungen in **beiden** Dateien nachziehen.

**Folgewirkungen:**
- Der KI-Workflow ([AI_GUIDE.md](../AI_GUIDE.md)) fragt bei neuen Seitentypen nach dem **Medium** und wählt daraus das System.
- `CHECKLIST.md` prüft: „genau ein Design-System pro Datei, nicht gemischt?"
- Eine künftige v2→v3-Migration bekommt ihre eigene ADR; diese hier nimmt sie nicht vorweg.

## Verwandte ADRs

- [ADR-0022](0022-design-system-v2.md) — v2 „Editorial", weiterhin gültig für Arbeitsblatt-Kontexte
- [ADR-0001](0001-single-file-html-architektur.md) — Grund für den Verzicht auf Webfonts
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — Fokus-Kanal, Kontrastanforderungen
- [ADR-0015](0015-inhalts-boxen.md) — Inhalts-Boxen, in v3 als Blue-Wash-Variante
- [ADR-0032](0032-praesentations-variante.md) — erster Konsument von v3 mit eigener Dark-Mode-Ausnahme
