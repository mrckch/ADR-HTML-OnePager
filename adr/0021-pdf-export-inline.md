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

### Export-Mechanik

```js
async function exportPDF() {
  if (typeof html2canvas === 'undefined' || typeof window.jspdf === 'undefined') {
    showToast('PDF-Modul nicht geladen.', { kind: 'error' });
    return;
  }
  commitSave();

  // Topbar/Modals beim Rendern ausblenden (sollen nicht ins PDF)
  document.body.classList.add('pdf-rendering');

  try {
    const canvas = await html2canvas(document.querySelector('.page'), {
      scale: 2,                    // höhere Auflösung
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false
    });

    const { jsPDF } = window.jspdf;
    const imgData = canvas.toDataURL('image/jpeg', 0.92);
    const pdfW = 210; // A4-Breite in mm
    const pdfH = (canvas.height / canvas.width) * pdfW;

    // Wenn das Bild höher als eine A4-Seite ist → in Seiten aufteilen
    const pageH = 297;
    const pdf = new jsPDF({ unit: 'mm', format: 'a4', orientation: 'portrait' });

    if (pdfH <= pageH) {
      pdf.addImage(imgData, 'JPEG', 0, 0, pdfW, pdfH, '', 'FAST');
    } else {
      // Vertikales Aufteilen auf mehrere A4-Seiten
      let position = 0;
      const heightLeft = pdfH;
      let remaining = heightLeft;
      while (remaining > 0) {
        pdf.addImage(imgData, 'JPEG', 0, position, pdfW, pdfH, '', 'FAST');
        remaining -= pageH;
        if (remaining > 0) { pdf.addPage(); position -= pageH; }
      }
    }

    const name = (document.getElementById('meta-name')?.value || 'schueler')
                  .replace(/[^a-zA-Z0-9_-]/g, '_');
    const date = new Date().toISOString().slice(0, 10);
    pdf.save(`${ONEPAGER_SLUG}__${name}__${date}.pdf`);

    showToast('PDF gespeichert.');
  } catch (err) {
    console.warn(err);
    showToast('PDF-Export fehlgeschlagen: ' + err.message, { kind: 'error' });
  } finally {
    document.body.classList.remove('pdf-rendering');
  }
}

// CSS-Begleitregel
// body.pdf-rendering .topbar,
// body.pdf-rendering .modal,
// body.pdf-rendering #toast { display: none !important; }
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
