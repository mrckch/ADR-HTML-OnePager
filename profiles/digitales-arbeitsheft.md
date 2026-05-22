# Profil: Digitales Arbeitsheft (iPad mit Stift)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der wie ein **klassisches Arbeitsheft** strukturiert ist: vollständige Aufgaben mit großzügigen Schreibflächen, in denen Schüler:innen **handschriftlich am iPad mit Apple Pencil** (oder mit der Tastatur) arbeiten. Der Onepager **ersetzt** das Papier-Arbeitsheft, nicht das Lehrbuch.

Lösungen sind **initial nicht enthalten** — die Selbst-Kontrolle erfolgt durch die Lehrkraft beim Einsammeln oder durch Vergleich im Plenum.

## Typische Merkmale

- **Klassenstufe:** alle, primär Sek I (wo iPads im Klassensatz verbreitet sind)
- **Fachbereich:** Mathematik (Skizzen, Rechnungen), Naturwissenschaften (Versuchsprotokolle), Sprachen (offene Aufgaben), Geographie (Karten beschriften)
- **Zeitumfang:** Einzelstunde bis mehrwöchiges Heft-Kapitel
- **Ziel-Typ:** Übung, Anwendung, Bearbeitung
- **Gerät:** primär **iPad mit Apple Pencil**, sekundär andere Tablets mit Stift

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0019] (Canvas-Modul, *in Phase 3*) | **Zentral.** Das ganze Profil steht und fällt mit funktionierender Stift-Eingabe pro Aufgabe |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0017](../adr/0017-save-status-toast.md) | Auto-Save ist **kritisch**, weil handschriftlicher Inhalt nicht nachgeschrieben werden kann. Save-Status muss prominent sein |
| [ADR-0003](../adr/0003-json-export-import.md) + [ADR-0020] (HTML-Export, *in Phase 3*) | Schüler:innen müssen ihr Werk **mitnehmen** können — JSON-Export (mit Canvas-Daten als Base64) oder HTML-Export mit eingebettetem State |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten, aber mit **großzügigerem Body** — die Schreibfläche braucht Platz |
| [ADR-0023](../adr/0023-a4-druck-und-preview.md) | A4-Vorschau und Druck wichtig, wenn das Heft am Schuljahresende auch physisch existieren soll |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** irrelevant — es gibt keine Lösungen im Schüler-Onepager.
- **[ADR-0011](../adr/0011-selbst-korrektur.md) (Selbst-Korrektur):** irrelevant für handschriftliche Eingabe. Bei zusätzlichen Tipp-Feldern (z. B. Vokabel-Eingabe) optional.
- **[ADR-0013](../adr/0013-quiz-hardening.md) (Quiz):** meist nicht relevant.
- **[ADR-0012](../adr/0012-gamification.md) (Fortschrittsbalken):** „Aufgabe bearbeitet" über Canvas-Inhalt schwer messbar. Meist weggelassen.

## Spezifische didaktische Entscheidungen

### 1. Canvas-Schreibfläche pro Aufgabe

Jede Aufgabe hat eine eigene **Stift-Schreibfläche** als zentrales Eingabeelement. Die Fläche ist:

- mindestens **240 px hoch** (für kurze Antworten), bei Mathe-/Skizzen-Aufgaben **400–600 px**
- mit **Stift-/Radierer-Tool**, **mehreren Farben** (≥ 4 Standardfarben) und **Größenregler** (3 Stiftgrößen)
- **Touch-action: none**, damit das iPad nicht versehentlich scrollt während des Zeichnens
- mit **Apple-Pencil-Unterstützung** (`pointerType === "pen"` → andere Linienbreite, Druck-Sensitivität optional)

Das Canvas-Modul kommt in Phase 3 mit [ADR-0019]. Bis dahin: Profil dokumentiert die Anforderung, Boilerplate enthält noch keinen fertigen Canvas-Helper.

### 2. Lineatur / Karo-Hintergrund optional

Je nach Fach kann der Canvas-Hintergrund eine Lineatur tragen:

| Hintergrund | Verwendung |
|---|---|
| Plain (weiß) | Universal |
| Linien (Heftlineatur) | Sprachen, Aufsatz, Notizen |
| Karo (5 mm) | Mathe-Rechnungen, Geometrie-Skizzen |
| Punkt-Raster | Skizzen, Konzept-Maps |

Empfehlung: per CSS-Background-Image oder SVG-Pattern auf das Canvas-Element, damit es beim Zeichnen nicht „mitwischt".

### 3. Aufgaben sind vollständig im Onepager

Anders als beim Lösungszettel-Profil: hier steht der **vollständige Aufgabentext** im Onepager. Es gibt kein paralleles Buch. Der Onepager ist die Single-Source-of-Truth für diese Stunde / dieses Kapitel.

### 4. Save-Status besonders prominent

Auto-Save (ADR-0017) bleibt aktiv, aber der Indikator wird **größer und auffälliger** dargestellt — z. B. mit zusätzlichem Hinweis „Letzter Stand: 14:23" neben dem Status-Punkt. Handschriftliche Arbeit verloren zu haben ist deutlich schmerzhafter als ein verlorenes Texteingabe-Feld.

Empfehlung: zusätzlich `window.beforeunload`-Schutz, falls Auto-Save-Debounce noch nicht durch ist.

### 5. JSON-Export enthält Canvas als Base64

`exportJSON()` muss die Canvas-Inhalte als `data:image/png;base64,...` mit-exportieren, sonst geht beim Geräte-Wechsel die Handschrift verloren. Pattern:

```js
function readUI() {
  const data = {};
  // … andere Felder …
  document.querySelectorAll('canvas[data-state]').forEach(cv => {
    data[cv.dataset.state] = cv.toDataURL('image/png');
  });
  return data;
}
```

### 6. HTML-Export (ADR-0020, Phase 3) ist die *empfohlene* Übergabe an die Lehrkraft

Die Schüler:innen senden ihr Heft als **selbst-tragende HTML-Datei mit eingebettetem State** an die Lehrkraft. Die Lehrkraft öffnet die HTML im Browser, sieht alle Antworten und Zeichnungen sofort — kein Import-Schritt nötig. (Detail in ADR-0020 in Phase 3.)

### 7. Druckbarkeit am Schuljahresende

Wenn das Schul-Heft am Ende auch in Papierform vorliegen soll: die A4-Vorschau (ADR-0023) zeigt das Druckbild. Canvas-Inhalte werden mit `<img src="…">` im Druck dargestellt (die Browser können `canvas.toDataURL`-Bilder drucken).

Voraussetzung: jeder Onepager ist auch im Print-CSS stimmig — gerade bei vielen großen Canvases muss man Umbrüche (`.page-break-hint`) bewusst setzen.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja (am Anfang) |
| Aufgaben-Karten | **ja, mit größerem Body** |
| Inhalts-Boxen (Merke, Tipp, Warn) | ja, häufiger Merke-Box (Definition vor Aufgabe) |
| Selbst-Korrektur (`data-expected`) | nein (Handschrift) — Ausnahme: ergänzende Tipper-Felder |
| Lösungs-Hürde (Tipp + Lösung) | nein (keine Lösungen) |
| Quiz mit gehashten Antworten | nein |
| **Canvas-Stift-Eingabe** | **ja, Hauptmechanik** |
| Fortschrittsbalken | optional |
| Save-Status-Indikator | **ja, prominent** |
| Toast-Notifications | ja |
| JSON-Export/Import | **ja, mit Canvas-Base64** |
| HTML-Export | **ja, empfohlen für Lehrer-Übergabe** (Phase 3) |
| Reset-Dialog | ja, mit besonderer Warnung („auch deine Zeichnungen!") |

## Aufgaben-Pattern (typisch)

```html
<article class="aufgabe" data-task-id="3.2">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 3.2</span>
    <h3 class="aufgabe__titel">Konstruiere ein gleichseitiges Dreieck mit Seitenlänge 6 cm</h3>
  </header>
  <div class="aufgabe__body">
    <p>Verwende Lineal und Zirkel. Beschrifte die Eckpunkte mit A, B, C.</p>

    <!-- Stift-Eingabe-Bereich (Canvas-Modul, Phase 3) -->
    <div class="canvas-wrap">
      <div class="canvas-tools">
        <button data-tool="pen">✏ Stift</button>
        <button data-tool="eraser">⬜ Radierer</button>
        <span class="color-swatches">…</span>
        <button data-canvas-action="clear">🗑 Löschen</button>
      </div>
      <canvas data-state="3.2-zeichnung"
              data-background="karo-5mm"
              width="760" height="480"></canvas>
    </div>

    <!-- Optional: ergänzendes Text-/Erklärungsfeld -->
    <div class="field">
      <label for="3.2-text">Erklärung deiner Konstruktion (optional)</label>
      <textarea id="3.2-text" data-state="3.2-text" rows="3"></textarea>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Kleine Schreibflächen (< 200 px)** → der Stift trifft nicht zuverlässig, Schüler frustriert
- **`touch-action: auto` auf Canvas** → iPad scrollt mit, statt zu zeichnen
- **Auto-Save nur alle 5 s** → bei Apple-Pencil-Strichen kann viel verloren gehen. Pro Stiftzug speichern (oder mindestens bei jedem `pointerup`)
- **JSON-Export ohne Canvas-Base64** → Schüler verlieren beim Geräte-Wechsel ihre Zeichnungen
- **Lösungen im Schüler-Onepager** → unpassend; wenn nötig, separates Lehrer-Dokument
- **Quiz-/Multiple-Choice-Charakter** → der Onepager soll handschriftliches Arbeiten fördern

## Verwandte Profile

- [`profiles/loesungszettel.md`](loesungszettel.md) — Wenn das Buch im Spiel ist und der Onepager Lösungs-Begleiter ist
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn Theorie + Aufgaben mit Lernpfad-Charakter zusammenkommen
