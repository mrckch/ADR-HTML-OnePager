# ADR-0021: PDF-Export mit inline html2canvas + jsPDF

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** PDF-Export, Lehrer-Workflow, GoodNotes-Integration
- **Abhängigkeit:** [ADR-0001 Amendment](0001-single-file-html-architektur.md) — Inline-Bibliotheken erlaubt

## Kontext

Browser-natives Drucken (`Strg/Cmd + P` → „Als PDF speichern") funktioniert mit dem überarbeiteten Druck-CSS ([ADR-0023](0023-a4-druck-und-preview.md)) inzwischen ordentlich. Es bleibt aber ein Pferdefuß:

**Canvas-Inhalte werden vom Browser-Druck nicht zuverlässig wiedergegeben.** Mal werden sie als gerasterte Bilder gedruckt, mal sind sie leer, mal merkwürdig skaliert. Bei Onepagern mit Stift-Eingabe (Profil [digitales Arbeitsheft](../profiles/digitales-arbeitsheft.md)) ist das ein Killer.

**Vorbild Turtle-Arbeitsblatt:** Dort gab es einen pixelgenauen PDF-Export via `html2canvas` (rendert das ganze DOM in ein Canvas) + `jsPDF` (verpackt Canvas-Bilder in eine PDF-Datei). Ergebnis: PDF sieht 1:1 aus wie der Bildschirm — inklusive aller Canvas-Zeichnungen. Schüler:innen können das PDF in **GoodNotes** importieren und dort weiterarbeiten.

Diese Mechanik will ich verfügbar machen — **aber nur optional**, weil sie zwei externe Bibliotheken benötigt.

## Entscheidung

**PDF-Export ist ein optionales Modul**, das per Snippet in einen Onepager kopiert wird, wenn er gebraucht wird. Es wird **nicht** standardmäßig im `templates/onepager-boilerplate.html` mitgeliefert, weil die Bibliotheken zusammen ca. **400 KB minified** wiegen — zu viel Overhead für Onepager, die kein PDF brauchen.

### Bibliotheks-Wahl

| Lib | Version | Größe (min) | Lizenz |
|---|---|---|---|
| **html2canvas** | 1.4.1 | ~47 KB | MIT |
| **jsPDF** | 2.5.1 | ~350 KB (umd.min) | MIT |

Beide unter MIT — mit unserer CC-BY-4.0 (Repository-Lizenz) und der Verwendung in pädagogischem Material kompatibel. Lizenz-Header beider Libs **muss erhalten bleiben** (steht so im jeweiligen Minified-Code).

### Aktivierung per Inline-Einbettung

Per [ADR-0001 Amendment](0001-single-file-html-architektur.md) ist das Inline-Einbinden externer Bibliotheken zulässig, solange die Datei single-file bleibt:

```html
<!-- ===== PDF-EXPORT-LIBS (inline, ca. 400 KB) ===== -->
<script>/*! html2canvas v1.4.1 — MIT License — https://html2canvas.hertzen.com */
(function(global, factory) { ... }) /* ~47 KB minified */
</script>
<script>/*! jsPDF v2.5.1 — MIT License — https://github.com/parallax/jsPDF */
(function(global, factory) { ... }) /* ~350 KB minified */
</script>
<!-- ===== /PDF-EXPORT-LIBS ===== -->
```

Die echten Inline-Codes stehen in **`templates/snippets/pdf-export-snippet.html`** als kopierbarer Block. Die Lehrkraft (oder KI) holt sich die Libs einmal per `curl` und fügt sie als großen Block in den Onepager ein.

### Export-Mechanik mit Seitenumbruch-Awareness

Der naive Ansatz (das gerenderte Canvas in 297-mm-Stücke schneiden) zerschneidet Aufgaben-Karten an beliebigen Stellen. Stattdessen respektiert das Modul die `<hr class="page-break-hint">`-Marker aus [ADR-0023](0023-a4-druck-und-preview.md):

1. **Vor dem Render** alle `.page-break-hint`-Elemente und ihre Y-Positionen einsammeln (per `getBoundingClientRect()`)
2. **html2canvas** rendert das gesamte `.page`-Element
3. **Segments bauen**: jeder Bereich zwischen zwei Markern (bzw. vom Anfang/Ende bis zum nächsten Marker) wird ein Segment
4. **Pro Segment** eine neue PDF-Seite: das Segment-Bild wird auf A4-Breite skaliert
5. **Wenn ein Segment länger als 297 mm ist**: weitere Unterteilung in A4-Stücke (Notfall — Autor:in hätte einen weiteren `.page-break-hint` setzen sollen)

Damit landen Aufgaben-Karten nicht über zwei Seiten verteilt, sofern die Marker passend gesetzt sind.

CSS-Begleitregel: `body.pdf-rendering .page-break-hint { border-top-color: transparent !important; }` und `body.pdf-rendering .page-break-hint::after { display: none !important; }` — damit die Marker im PDF nicht als gestrichelter Strich oder als „↓ neue A4-Seite ↓"-Text auftauchen, aber **ihre Höhe behalten**, damit die Positionsmessung stimmt.

Vollständiger Code: siehe [`templates/snippets/pdf-export-snippet.html`](../templates/snippets/pdf-export-snippet.html).

### Pseudocode des Splitting-Algorithmus

```js
// 1. Positionen sammeln (in CSS-Pixeln, relativ zu target)
const breakBounds = breaks.map(b => {
  const r = b.getBoundingClientRect();
  return { top: r.top - targetTop, bottom: r.bottom - targetTop };
});

// 2. html2canvas (scale=2 für höhere Auflösung)
const canvas = await html2canvas(target, { scale: 2, ... });

// 3. Umrechnen auf Canvas-Pixel und Segments bauen
const realScale = canvas.height / target.height;
const segments = [];
let cursor = 0;
for (const bb of breakBounds) {
  if (bb.top * realScale > cursor) {
    segments.push({ start: cursor, end: bb.top * realScale });
  }
  cursor = bb.bottom * realScale;
}
if (cursor < canvas.height) {
  segments.push({ start: cursor, end: canvas.height });
}

// 4. Pro Segment eine PDF-Seite (oder mehrere bei zu langen Segmenten)
for (const seg of segments) {
  let segCursor = seg.start;
  while (segCursor < seg.end) {
    const chunkPx = Math.min(seg.end - segCursor, maxChunkPxFor297mm);
    // Temp-Canvas mit nur diesem Chunk, dann pdf.addImage + pdf.addPage
    segCursor += chunkPx;
  }
}
```

### Progress-Modal während des Renderns

Der Rendervorgang dauert auf älteren Geräten ein paar Sekunden — ein einfaches Modal mit Fortschritts-Anzeige verhindert „Hängt die App?"-Gefühl:

```html
<div id="pdf-progress" class="modal" hidden>
  <div class="modal__panel">
    <h2>📄 PDF wird erstellt …</h2>
    <p>Einen Moment Geduld. Bei vielen Zeichnungen kann das ein paar Sekunden dauern.</p>
    <div class="progress-bar"><div class="progress-fill" id="pdf-progress-fill"></div></div>
  </div>
</div>
```

Modal wird zu Beginn von `exportPDF()` geöffnet, am Ende geschlossen.

### A4-Vorschau-Modus mit PDF-Export koppeln

Bevor die Lehrkraft auf „PDF speichern" klickt, sollte sie im [A4-Vorschau-Modus](0023-a4-druck-und-preview.md) geprüft haben, dass das Layout passt. Beim Klick auf „PDF speichern" wird vorübergehend die A4-Vorschau aktiviert, falls noch nicht:

```js
async function exportPDF() {
  const wasPreview = document.body.classList.contains('a4-preview');
  if (!wasPreview) setA4Preview(true);
  await new Promise(r => requestAnimationFrame(r));  // Layout sich setzen lassen
  // … html2canvas-Aufruf …
  if (!wasPreview) setA4Preview(false);
}
```

### GoodNotes-Integration

Eine PDF-Datei kann in GoodNotes (iPad) importiert werden — sie wird zu einer beschriftbaren Seite. Der Workflow für Lehrer:innen:

1. Onepager fertig bauen
2. `?layout=a4` einschalten, prüfen
3. „PDF speichern" klicken
4. PDF in GoodNotes importieren
5. Mit Apple Pencil annotieren, verteilen

Für Schüler:innen:

1. Im Onepager arbeiten (auch mit Canvas-Zeichnungen)
2. „PDF speichern" klicken
3. PDF in GoodNotes weiter beschriften (z. B. eigene Anmerkungen, Markierungen)
4. Oder per AirDrop, Mail, Teams abgeben

### Beziehung zu anderen Export-Wegen

| Format | Wann | Eigenschaft |
|---|---|---|
| **JSON** ([ADR-0003](0003-json-export-import.md)) | Wieder-Import, Backup, Geräte-Wechsel | Maschinen-lesbar, kompakt, nur State |
| **HTML** ([ADR-0020](0020-html-export-eingebetteter-state.md)) | Übergabe an Lehrkraft oder Eltern, später wieder bearbeiten | Doppelklick öffnet, voll interaktiv |
| **PDF** (dieses ADR) | Druck, GoodNotes-Integration, Archivierung | Pixelgenau, statisch, ausdruckbar |

Drei Wege — drei Zwecke. Sie konkurrieren nicht, ergänzen einander.

## Alternativen

- **Browser-natives Drucken reicht:** Verworfen — Canvas-Inhalte unzuverlässig im Druck.
- **PDF-Lib selbst schreiben:** Verworfen — PDF-Format ist komplex, Vektorisierung von Canvas extrem aufwendig.
- **html2pdf.js (Wrapper-Lib):** Wrappt html2canvas + jsPDF. Spart Code, aber weniger Kontrolle über Render-Optionen. Eine valide Variante — könnte als Sub-Variante dokumentiert werden, wir bleiben aber bei html2canvas + jsPDF separat.
- **Server-Side-PDF (Puppeteer, weasyprint):** Bräuchte Backend. Verstößt gegen ADR-0001 Kern. Verworfen.
- **CDN-Link statt Inline:** Würde ADR-0001 verletzen. Verworfen.
- **PDF-Modul standardmäßig im Boilerplate:** Verworfen — 400 KB extra für Onepager, die kein PDF brauchen, ist Verschwendung. Daher optional per Snippet.

## Konsequenzen

**Positiv:**
- Pixelgenaues PDF inkl. Canvas-Zeichnungen
- GoodNotes-tauglich (iPad)
- Single-File-Prinzip durch Inline-Libs erhalten
- Offline-fähig (CDN-frei)
- Lehrer:innen können Klassensätze als PDF archivieren

**Negativ / Trade-offs:**
- 400 KB extra pro Onepager mit PDF-Modul (in Bytes — beim Hosting irrelevant, beim mobilen Erst-Laden spürbar bei langsamer Verbindung)
- html2canvas hat bekannte Schwächen: CSS-Gradienten, einige Filter, oder dynamische Inhalte werden nicht perfekt gerendert
- Bei sehr großen Onepagern (viele Seiten) kann der Render einige Sekunden dauern
- jsPDF erzeugt JPEG-eingebettete PDFs — bei Texten verlustbehaftet (bei `quality 0.92` aber kaum sichtbar)
- Lizenz-Header der Libs müssen erhalten bleiben

**Folgewirkungen für künftige Onepager:**
- Bei Bedarf: Snippet aus `templates/snippets/pdf-export-snippet.html` einkopieren
- Vorher überlegen: Brauche ich wirklich PDF, oder reicht HTML-Export?
- Wenn ja: einmal `curl` für die Libs, dann Block in HTML einfügen
- Im A4-Vorschau-Modus prüfen, bevor PDF erstellt wird

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Amendment ermöglicht das überhaupt
- [ADR-0019](0019-canvas-stift-modul.md) — PDF-Export ist erst durch Canvas-Inhalte richtig wertvoll
- [ADR-0020](0020-html-export-eingebetteter-state.md) — Alternative Übergabe
- [ADR-0023](0023-a4-druck-und-preview.md) — A4-Vorschau ist Voraussetzung für gutes Layout
