# ADR-0029: Audio-Aufnahmen via MediaRecorder API

- **Status:** Accepted
- **Datum:** 2026-05-27
- **Betrifft:** Erweiterte Eingabe-Modalitäten, optional

## Kontext

Bisher kann ein Onepager Eingaben nur als **Text** (`<input>`, `<textarea>`) oder als **Zeichnung** ([ADR-0019](0019-canvas-stift-modul.md)) entgegennehmen. Für einige Einsatzszenarien wäre eine **Audio-Aufnahme** wertvoll:

- **Sprachen**: Aussprache üben — Schüler:in spricht ein Wort/Satz, hört sich selbst, vergleicht
- **Lernportfolio**: Reflexion „lauter denken" — manche Schüler:innen formulieren mündlich besser als schriftlich
- **Differenzierung**: Schüler:innen mit Schreib-Schwierigkeiten (LRS) können sich audio-äußern
- **Lesetext**: Hör-Verstehen-Übung — Schüler:in spricht eine Zusammenfassung
- **Fremdsprache**: Sprach-Tagebuch — kurze tägliche Sprach-Aufnahmen
- **Musik**: Rhythmus-Übungen, Singen, Instrumental-Aufnahmen

Die Web-Plattform bietet dafür die **MediaRecorder API** — seit ~2017 in allen modernen Browsern verfügbar (Chrome, Firefox, Safari ab 14.1, Edge). Sie kann Audio (und Video) aufnehmen, ohne externe Library, ohne Plugin.

## Entscheidung

Wir definieren ein **optionales Audio-Aufnahme-Modul**, das per Snippet (`templates/snippets/audio-aufnahme-snippet.html`) in einen Onepager integriert werden kann. Es ist **nicht Teil des Boilerplate** — denn es ist nicht universell sinnvoll, und es bringt einige besondere Anforderungen (Permission, Speicher-Verbrauch) mit, die nicht jedes Profil tragen muss.

### Browser-API

```js
async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
  const chunks = [];
  recorder.ondataavailable = e => chunks.push(e.data);
  recorder.onstop = () => {
    const blob = new Blob(chunks, { type: 'audio/webm' });
    saveAudio(blob);
    stream.getTracks().forEach(t => t.stop()); // Mic-LED ausschalten
  };
  recorder.start();
  return recorder;
}
```

### Encoding-Format

Wir nutzen **`audio/webm` (Opus-Codec)**. Begründung:

| Format | Browser-Support | Größe | Qualität |
|---|---|---|---|
| `audio/webm; codecs=opus` | Chrome, Firefox, Edge, Safari 14.1+ | klein (~6 KB/s) | gut bis sehr gut |
| `audio/mp4; codecs=mp4a.40.2` | Safari, manche Chrome | mittel | gut |
| `audio/wav` | universell | sehr groß (~88 KB/s) | maximal |

Opus ist der **kleinste** und genügend qualitativ — für 1 Minute Sprache ~360 KB statt 5 MB als WAV. Fallback-Logik via `MediaRecorder.isTypeSupported()`:

```js
const MIME = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
  ? 'audio/webm;codecs=opus'
  : MediaRecorder.isTypeSupported('audio/mp4')
  ? 'audio/mp4'
  : '';
```

### Persistenz

Aufnahmen werden als **Base64-Data-URL** im State gespeichert — wie Canvas-Bilder ([ADR-0019](0019-canvas-stift-modul.md)). Das integriert sich nahtlos mit:

- **localStorage** ([ADR-0002](0002-state-persistenz-localstorage.md))
- **JSON-Export** ([ADR-0003](0003-json-export-import.md))
- **HTML-Export mit eingebettetem State** ([ADR-0020](0020-html-export-eingebetteter-state.md))
- **Lernportfolio-Einträge** ([ADR-0025](0025-lernportfolio-persistenz.md))

```js
function blobToDataUrl(blob) {
  return new Promise(resolve => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}
```

### Speicher-Limits — strikte Obergrenzen

Audio frisst Speicher schnell. **Standard-Limit: 60 Sekunden pro Aufnahme.** Der Recorder beendet automatisch:

```js
const MAX_DURATION_MS = 60_000;
setTimeout(() => recorder.state === 'recording' && recorder.stop(), MAX_DURATION_MS);
```

Im UI wird die Restzeit angezeigt. Bei `localStorage`-Quota-Überschreitung beim Speichern: Toast mit Hinweis, Aufnahme verwerfen.

### Permission-Handling

`getUserMedia({ audio: true })` zeigt die **Browser-Permission-Prompt**. Mögliche Fehler:

| Fehler | Bedeutung | Reaktion |
|---|---|---|
| `NotAllowedError` | Nutzer:in hat abgelehnt | Toast: „Mikrofon-Zugriff abgelehnt. In Browser-Einstellungen erlauben." |
| `NotFoundError` | Kein Mikrofon vorhanden | Toast: „Kein Mikrofon gefunden." |
| `NotReadableError` | Mikrofon belegt | Toast: „Mikrofon wird gerade von anderer App benutzt." |
| Sonstiges | — | Toast: „Audio-Aufnahme nicht möglich." |

**Datenschutz-Wichtig**: Das Mikrofon-LED (bei Laptops) und Browser-Indikator zeigen die Aufnahme an. Wir stellen sicher, dass `stream.getTracks().forEach(t => t.stop())` nach Aufnahme-Ende läuft, sonst bleibt das LED an.

### UI-Pattern

```
┌─────────────────────────────────────────┐
│  🎤 Audio-Aufnahme                       │
│                                          │
│  [● Aufnahme starten]                    │
│                                          │
│  Bestehende Aufnahme:                    │
│  ▶ ▶▶ 0:34 / 1:00     [🗑 Löschen]      │
└─────────────────────────────────────────┘
```

Während Aufnahme:
```
│  ● 0:12 / 1:00 (max)    [■ Stop]        │
│  ◉ ◉ ◉ ◉ ◉ ◉ ◉           ← Pegel-Visualisierung │
```

### Pegel-Visualisierung (optional)

Mit der **Web Audio API** lässt sich der Eingangspegel anzeigen — visuelles Feedback hilft Schüler:innen, dass das Mikrofon funktioniert:

```js
const audioCtx = new AudioContext();
const source = audioCtx.createMediaStreamSource(stream);
const analyser = audioCtx.createAnalyser();
analyser.fftSize = 256;
source.connect(analyser);

function tick() {
  const data = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(data);
  const avg = data.reduce((a, b) => a + b, 0) / data.length;
  updateMeter(avg / 128); // 0..2
  if (recording) requestAnimationFrame(tick);
}
```

### Browser-Kompatibilität

| Browser | Min-Version | Anmerkung |
|---|---|---|
| Chrome (Desktop + Android) | 49+ | volle Unterstützung |
| Firefox | 25+ | volle Unterstützung |
| Safari (macOS + iOS) | **14.1+** | **iOS 14.1+ erforderlich** |
| Edge | 79+ | Chromium-basiert |

Auf iOS < 14.1 und in alten Browsern: **Graceful Degradation** — das Snippet zeigt einen Hinweis „Audio nicht unterstützt" und das Feld wird auf Text-only zurückgesetzt.

```js
if (!navigator.mediaDevices || !window.MediaRecorder) {
  showFallback('🔇 Audio-Aufnahme in diesem Browser nicht möglich. Bitte Text-Antwort.');
}
```

### Beispiel-Integration im Lernportfolio

Audio-Eintrag ist ein **neuer Typ** zusätzlich zu reflexion/lernprodukt/quelle:

```js
// In _eintraege-Schema (ADR-0025):
{
  id: "e1717238400000",
  datum: "2026-05-27",
  typ: "audio",
  titel: "Aussprache 'thoroughly'",
  inhalt: "data:audio/webm;base64,GkXfo59ChoEBQveBAULygQ…",
  tags: ["englisch", "aussprache"]
}
```

Im UI wird statt `<textarea>` ein `<audio controls>` Element gerendert.

## Alternativen

- **Externe Audio-Library** (z. B. RecordRTC): Mehr Features (Pause, Konvertierung), aber widerspricht [ADR-0001](0001-single-file-html-architektur.md). MediaRecorder ist genug. Verworfen.
- **Server-Upload statt localStorage**: Erfordert Backend. Widerspricht dem Single-File-Modell. Verworfen.
- **Nur WAV-Format**: Universell, aber zu groß für sinnvolle Speicherung. Verworfen.
- **Audio in IndexedDB statt localStorage**: Mehr Platz, aber asynchron und komplex. Bei 60s/Aufnahme reicht localStorage. Verworfen.
- **Streaming statt File**: MediaRecorder kann beides; File-Modell ist einfacher. Streaming verworfen.

## Konsequenzen

**Positiv:**
- Neue Eingabe-Modalität ohne externe Abhängigkeit
- Integriert sich nahtlos in bestehende Persistenz (Base64 wie Canvas)
- Sprachen-, Inklusions-, Reflexions-Szenarien gewinnen Möglichkeit
- Native Browser-API — kein Tracking, keine externe URL

**Negativ / Trade-offs:**
- iOS < 14.1 nicht unterstützt — Fallback nötig
- Mikrofon-Permission erzeugt zusätzlichen UX-Schritt
- Audio frisst Speicher: bei vielen Aufnahmen schnell am localStorage-Limit
- Datenschutz-sensibel — Schüler-Stimme als Daten im Browser

**Folgewirkungen:**
- Profile, die das Snippet nutzen, **müssen** dokumentieren: Permission-Prompt erwarten, max. 60s, lokale Speicherung
- Bei Lernportfolio-Integration: neuer Eintrags-Typ `audio` (additiv zum Schema v2)
- Reset-Dialog muss erwähnen, dass auch Audio-Aufnahmen gelöscht werden
- HTML-Export wird mit Audio größer — JSON-Export bevorzugen

## Verwandte ADRs / Profile

- [ADR-0019](0019-canvas-stift-modul.md) — analoges Muster für Bild-Eingabe (Base64-PNG)
- [ADR-0002](0002-state-persistenz-localstorage.md) — Audio landet im Standard-State
- [ADR-0025](0025-lernportfolio-persistenz.md) — Audio als Eintrags-Typ
- [profiles/vokabeln.md](../profiles/vokabeln.md) — Aussprache-Üben
- [profiles/lernportfolio.md](../profiles/lernportfolio.md) — Audio-Reflexionen
- [profiles/differenzierung.md](../profiles/differenzierung.md) — Inklusion bei LRS
