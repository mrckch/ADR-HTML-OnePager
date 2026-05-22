# ADR-0019: Canvas-Stift-Modul

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** Eingabe-Mechanik, iPad-Tauglichkeit, Handschrift

## Kontext

Für mehrere Profile (insbesondere [digitales Arbeitsheft](../profiles/digitales-arbeitsheft.md), aber auch optional für Erarbeitungsseite und Vokabel-Profil) brauchen Schüler:innen die Möglichkeit, **handschriftlich** zu schreiben oder zu zeichnen — Rechnungen, Skizzen, Konstruktionen, Notizen.

Anforderungen:
- Funktioniert mit **Apple Pencil**, normalem Touch (Finger), Maus und Trackpad
- iPad-tauglich: kein versehentliches Scrollen beim Zeichnen
- Tools: Stift mit verschiedenen Farben und Größen, Radierer, „Alles löschen"
- State wird gespeichert (localStorage als PNG-Base64), bleibt nach Reload erhalten
- Optionaler Hintergrund: Lineatur, Karo, Punkt-Raster, plain
- Single-File, kein externes JS (siehe [ADR-0001](0001-single-file-html-architektur.md))

Bisherige Onepager hatten kein einheitliches Canvas-Pattern — jeder hat ad hoc etwas gebaut. Das soll vereinheitlicht werden.

## Entscheidung

Ein wiederverwendbares **Canvas-Modul** mit HTML-Struktur, CSS und JS-Helpern, das per Snippet in jeden Onepager kopiert werden kann. Das Modul ist Teil des Boilerplate, lässt sich aber per Kommentar-Fences komplett entfernen, wenn ein Profil es nicht braucht.

### HTML-Struktur

```html
<div class="canvas-wrap">
  <div class="canvas-tools" role="toolbar" aria-label="Zeichen-Werkzeuge">
    <button type="button" class="canvas-tool" data-tool="pen"     aria-pressed="true">✏ Stift</button>
    <button type="button" class="canvas-tool" data-tool="eraser"  aria-pressed="false">⬜ Radierer</button>
    <span class="canvas-colors">
      <button class="canvas-color" data-color="#1a2340" style="background:#1a2340" aria-label="Navy"></button>
      <button class="canvas-color" data-color="#C0645A" style="background:#C0645A" aria-label="Rot"></button>
      <button class="canvas-color" data-color="#1a6b45" style="background:#1a6b45" aria-label="Grün"></button>
      <button class="canvas-color" data-color="#000000" style="background:#000000" aria-label="Schwarz"></button>
    </span>
    <span class="canvas-sizes">
      <button class="canvas-size" data-size="2" aria-pressed="false">●</button>
      <button class="canvas-size" data-size="4" aria-pressed="true">⬤</button>
      <button class="canvas-size" data-size="8" aria-pressed="false">⬛</button>
    </span>
    <button type="button" class="canvas-clear">🗑 Löschen</button>
  </div>
  <canvas data-state="aufgabe-3-zeichnung"
          data-background="karo-5mm"
          width="760" height="480"></canvas>
</div>
```

- Eine Toolbar pro Canvas
- `data-state="..."` macht das Canvas Teil des Standard-Persistenz-Systems ([ADR-0002](0002-state-persistenz-localstorage.md))
- `data-background="..."` (optional): `plain`, `lineatur`, `karo-5mm`, `punkt-raster`
- Mehrere Canvas-Instanzen pro Seite möglich (z. B. pro Aufgabe eine)

### Pointer-Events statt separater Mouse/Touch-Handler

Pointer-Events sind seit Jahren breit unterstützt und kapseln Maus, Touch und Stift uniform:

```js
canvas.addEventListener('pointerdown', start);
canvas.addEventListener('pointermove', draw);
canvas.addEventListener('pointerup',   end);
canvas.addEventListener('pointercancel', end);
canvas.addEventListener('pointerleave', end);
```

Vorteile:
- Ein Code-Pfad für alle Eingabegeräte
- `event.pointerType` unterscheidet `"mouse"`, `"pen"`, `"touch"`
- `event.pressure` (0–1) für druckempfindliche Stifte (Apple Pencil)

### `touch-action: none` ist Pflicht

Sonst scrollt iPad-Safari mit, statt zu zeichnen:

```css
.canvas-wrap canvas { touch-action: none; }
```

### Apple-Pencil-Druck (optional)

Wenn `event.pointerType === 'pen'` und `event.pressure > 0`:

```js
const lineWidth = baseSize * (0.5 + e.pressure);
```

Andernfalls Standard-Größe. Pressure-Sensitivität ist ein Plus, keine Pflicht — funktioniert ohne, wird mit besser.

### State-Persistenz: `toDataURL` → localStorage

Pro `pointerup` (= nach jedem Stiftzug) wird der Canvas-Inhalt als PNG-Base64 in localStorage gespeichert:

```js
function saveCanvas(cv) {
  const key = cv.dataset.state;
  if (!key) return;
  const dataUrl = cv.toDataURL('image/png');
  // Wird in den Standard-State eingespeist und über STORAGE_KEY persistiert
  // (siehe Hauptmodul ADR-0002)
}
function loadCanvas(cv, dataUrl) {
  const ctx = cv.getContext('2d');
  if (!dataUrl) { clearCanvas(cv); return; }
  const img = new Image();
  img.onload = () => ctx.drawImage(img, 0, 0);
  img.src = dataUrl;
}
```

Integration: `readUI()` und `writeUI()` (aus dem Hauptmodul) berücksichtigen Canvas-Elemente extra:

```js
// in readUI:
document.querySelectorAll('canvas[data-state]').forEach(cv => {
  data[cv.dataset.state] = cv.toDataURL('image/png');
});
// in writeUI:
document.querySelectorAll('canvas[data-state]').forEach(cv => {
  if (data[cv.dataset.state]) loadCanvas(cv, data[cv.dataset.state]);
  else clearCanvas(cv);
});
```

### Hintergrund-Pattern via CSS

Lineatur und Raster werden **nicht** auf den Canvas selbst gezeichnet (sonst löschen sie sich mit), sondern als CSS-Background unter dem transparenten Canvas:

```css
canvas[data-background="lineatur"] {
  background-image: repeating-linear-gradient(
    transparent, transparent 23px, var(--border-soft) 23px, var(--border-soft) 24px);
  background-size: 100% 24px;
}
canvas[data-background="karo-5mm"] {
  background-color: #fff;
  background-image:
    linear-gradient(to right,  var(--border-soft) 1px, transparent 1px),
    linear-gradient(to bottom, var(--border-soft) 1px, transparent 1px);
  background-size: 18.9px 18.9px;  /* ~5mm bei 96 DPI */
}
canvas[data-background="punkt-raster"] {
  background-image: radial-gradient(var(--border) 1px, transparent 1.5px);
  background-size: 16px 16px;
}
canvas[data-background="plain"], canvas:not([data-background]) {
  background: #fff;
}
```

Im Dark-Mode wirken die Pattern dezent durch — bei Bedarf können Lehrer:innen für ihr Profil Anpassungen machen.

### „Alles löschen" mit Bestätigung

Versehentliches Wegklicken einer fertigen Skizze ist schmerzhaft. Daher: Bestätigungs-Modal analog zu [ADR-0004](0004-reset-funktion-mit-bestaetigung.md).

```js
function clearCanvasWithConfirm(cv) {
  if (cv.dataset.empty === 'true') { return; }   // Wenn leer, einfach durchlaufen
  // Bestätigungs-Modal öffnen (eigenes oder geteilt mit reset-Modal)
}
```

### Mehrere Canvases pro Seite

Jedes Canvas hat eindeutiges `data-state` und eigene Toolbar (Toolbar-Klick-Events werden per `closest('.canvas-wrap')` an das jeweilige Canvas gebunden).

### CSS-Mindestmaße

- **Höhe**: mindestens 240 px für kurze Notizen, 400–600 px für Skizzen/Konstruktionen
- **Tool-Buttons**: mindestens 40×40 px (Touch-tauglich)
- **Farb-Swatches**: 28×28 px

### Druck-Verhalten

Beim Drucken wird das Canvas als statisches PNG ausgegeben (Browser-Default für `<canvas>`). Toolbar wird ausgeblendet:

```css
@media print {
  .canvas-tools { display: none !important; }
  canvas { border: 0.5pt solid #000; max-width: 100%; }
}
```

Wichtig: weil Canvas-Inhalte beim Drucken nicht reflowen, sind sehr breite Canvases bei A4-Druck problematisch. Empfehlung: Canvas-Breite ≤ 760 px halten (passt in A4-Inhaltsbereich von ~700 px bei 18mm Rand).

## Alternativen

- **SVG statt Canvas:** Vektorbasiert, sieht beim Druck besser aus, aber für freihändige Zeichnungen mit Tausenden Pfaden wird das DOM riesig. Verworfen.
- **Externes Drawing-Lib (Fabric.js, Paper.js):** Mächtiger, aber 100–500 KB extra. Für die hier nötige Funktionalität overkill. Verworfen.
- **Apple Pencil ScribbleKit / iOS Notes Integration:** iOS-spezifisch, nur Safari. Nicht plattform-portabel. Verworfen.
- **HTML5 Form-Field „handwriting"-Eingabe:** Existiert nicht standardisiert. Verworfen.
- **Touch- und Mouse-Events getrennt** (statt Pointer-Events): Doppelter Code-Pfad, anfälliger. Verworfen.

## Konsequenzen

**Positiv:**
- Einheitliches Canvas-Pattern für alle Onepager
- Apple Pencil mit Druck-Empfindlichkeit (wenn Browser unterstützt)
- Touch + Mouse + Pen über einen Code-Pfad
- Hintergründe via CSS, ohne Canvas-Pixel zu „verbrauchen"
- Persistenz nahtlos im bestehenden State-System

**Negativ / Trade-offs:**
- Canvas-Inhalte sind raster (PNG) — beim großen Zoom verschwommen
- Canvas-PNG-Base64 ist platzhungrig: ein 760×480-Canvas mit komplexem Inhalt ≈ 100–300 KB Base64. Bei mehreren Canvases pro Onepager schnell 1–2 MB im localStorage
- localStorage-Limit (5–10 MB) kann bei vielen Canvases erreicht werden → in Profil-Doku darauf hinweisen
- Keine Undo-Funktion (zu komplex für die Skala dieses Repos). Schüler löschen und beginnen neu

**Folgewirkungen für künftige Onepager:**
- Canvas-Sektionen mit eindeutigen `data-state`-IDs (z. B. `aufgabe-3-zeichnung`)
- Höhen großzügig wählen, mind. 240 px
- Druckverhalten testen: lange Canvases werden vertikal beschnitten — ggf. mehrere kleinere Canvases statt eines großen
- Bei mehr als 5 Canvases pro Onepager: localStorage-Last im Blick behalten

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Kein externes JS für Drawing
- [ADR-0002](0002-state-persistenz-localstorage.md) — Canvas-PNG geht in den Standard-State
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — „Alles löschen" mit Bestätigung
- [ADR-0007](0007-druck-pdf-optimierung.md) + [ADR-0023](0023-a4-druck-und-preview.md) — Druck-Verhalten von Canvas
- [ADR-0020](0020-html-export-eingebetteter-state.md) — HTML-Export enthält Canvas-PNGs eingebettet
- [profiles/digitales-arbeitsheft.md](../profiles/digitales-arbeitsheft.md) — Hauptkonsument dieses Moduls
