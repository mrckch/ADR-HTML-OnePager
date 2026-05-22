# ADR-0020: HTML-Export mit eingebettetem State

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** Schüler-Lehrer-Übergabe, Datenportabilität, Eltern-Einsicht

## Kontext

[ADR-0003](0003-json-export-import.md) bietet bereits JSON-Export/-Import. Das funktioniert, hat aber zwei praktische Reibungspunkte:

1. **Lehrer-Workflow ist umständlich:** Lehrkraft öffnet den Onepager im Browser, klickt „Laden", wählt die JSON-Datei aus jedem Schüler einzeln, schaut hin, klickt sich durch — pro Schüler:in eine Aktion. Bei 28 Schüler:innen sind das 28 Lade-Aktionen.
2. **Eltern und Schüler ohne IT-Kenntnis können JSON-Import nicht intuitiv:** „Was ist eine .json-Datei?" — bei Eltern (z. B. bei Tag der offenen Tür: „Schau mal, was mein Kind gemacht hat") wird das zur Hürde.

**Vorbild:** Im Turtle-Beispiel-Arbeitsblatt (das die Designinspiration für Boilerplate v2 war) gab es einen HTML-Export, der den State **direkt in die Datei einbettet**. Doppelklick auf die HTML — alle Antworten und Zeichnungen sind sofort sichtbar, ohne Import.

## Entscheidung

Zusätzlich zum bestehenden JSON-Export ([ADR-0003](0003-json-export-import.md)) gibt es einen **HTML-Export**, der eine selbsttragende `.html`-Datei erzeugt: der Onepager mit eingebettetem State.

### Mechanismus

```js
function exportHTML() {
  commitSave();  // Sicherstellen, dass localStorage aktuell ist

  // 1. Aktuellen State aus localStorage einsammeln (alle Keys mit STORAGE_KEY-Prefix)
  const stateRaw = localStorage.getItem(STORAGE_KEY);
  if (!stateRaw) {
    showToast('Noch nichts zum Speichern.', { kind: 'error' });
    return;
  }

  // 2. Injektions-Script bauen, das den State beim Öffnen wiederherstellt
  const inject = `<script id="embedded-state" type="application/json">${
    escapeForScript(stateRaw)
  }</script>`;

  // 3. Den aktuellen DOM-Baum klonen und Topbar-Button "HTML speichern" markieren
  //    damit der Empfänger nicht versucht, noch einmal zu exportieren
  const cloneHtml = document.documentElement.outerHTML
    // Marker für „diese Datei ist ein Export"
    .replace('<head>', `<head>\n${inject}`)
    // Optional: Hinweis-Banner im Topbar
    .replace('class="topbar"', 'class="topbar topbar--exported"');

  // 4. Als Datei speichern
  const blob = new Blob(['<!DOCTYPE html>\n', cloneHtml], { type: 'text/html;charset=utf-8' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  const ts   = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 16);
  const name = (document.getElementById('meta-name')?.value || 'schueler').replace(/[^a-zA-Z0-9_-]/g, '_');
  a.href = url;
  a.download = `${ONEPAGER_SLUG}__${name}__${ts}.html`;
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
  showToast('HTML-Datei mit Antworten gespeichert.');
}

function escapeForScript(s) {
  return s.replace(/<\/script>/gi, '<\\/script>');  // verhindert vorzeitiges Script-Ende
}
```

### Wiederherstellung beim Öffnen der exportierten Datei

Im Standard-Init-Script des Boilerplates wird zuerst geprüft, ob ein `<script id="embedded-state">` existiert:

```js
const embedded = document.getElementById('embedded-state');
if (embedded) {
  try {
    const stateRaw = embedded.textContent;
    // In localStorage schreiben — damit alle Standard-Funktionen normal arbeiten
    localStorage.setItem(STORAGE_KEY, stateRaw);
    showToast('Eingebetteter Stand geladen.');
  } catch {}
}
const initial = loadState();
writeUI(initial);
applyRevealedState(initial._revealed || {});
// … weiter wie bisher
```

Vorteil: der Empfänger (Lehrkraft, Eltern, der/die Schüler:in selbst auf anderem Gerät) öffnet die Datei per Doppelklick → der gesamte State wird automatisch in den lokalen localStorage gespielt → alle Eingaben sind sichtbar.

### Dateigröße

- Reiner Text + UI-State: ~5–20 KB extra zur HTML-Datei
- Mit Canvas-Zeichnungen (ADR-0019): pro Canvas etwa 50–300 KB als PNG-Base64
- Realistische Größen:
  - Onepager ohne Canvas: ~80 KB
  - Onepager mit 2–3 Canvases: ~200–800 KB
  - Onepager mit vielen vollgemalten Canvases: bis ~2 MB

Diese Datei kann per Mail, Messenger oder Teams problemlos versendet werden.

### Topbar-Hinweis in exportierter Datei

Optional ein dezenter Hinweis-Banner, wenn die Datei aus einem Export stammt:

```css
.topbar--exported::after {
  content: "📎 Eingebettete Antworten geladen";
  font-size: var(--fs-xs);
  color: var(--gold);
  margin-left: var(--space-3);
}
```

So sieht die Empfänger:in sofort, dass diese Datei besondere Inhalte trägt.

### Beziehung zu JSON-Export

JSON-Export und HTML-Export bestehen **parallel**:

| Format | Wann | Workflow |
|---|---|---|
| **JSON** | Geräte-Wechsel, Backup, Re-Import | „Speichern" als `.json` → später „Laden" |
| **HTML** | Abgabe an Lehrkraft, Eltern, Mitschüler | „Als HTML mit Antworten" → Empfänger öffnet Datei |

Der Topbar bekommt einen zusätzlichen Button „HTML speichern" neben „Speichern" (= JSON):

```html
<button data-action="export-html">📎 HTML</button>
```

### Sicherheit / Datenschutz

- **Der HTML-Export enthält ALLES**: alle Antworten, Reflexionen, Zeichnungen, aufgedeckte Lösungen, Kompetenz-Selbst-Einschätzungen
- Bei sensiblen Profilen (Reflexionstagebuch, Kompetenzraster): Bestätigungs-Modal mit explizitem Hinweis vor Export:

> „Diese Datei enthält **alle deine Eingaben** — auch persönliche Reflexionen.
> Bist du sicher, dass du sie teilen möchtest?"

Bei Datenschutz-unkritischen Profilen (Lösungszettel, Übung): kein Extra-Modal nötig.

### Größen-Warnung

Bei sehr großen Exports (> 5 MB): Warnung im Modal, optional Anbieten, Canvas-Daten zu reduzieren oder JSON statt HTML zu wählen.

## Alternativen

- **Nur JSON-Export beibehalten:** Verworfen — Lehrer- und Eltern-Workflow zu umständlich.
- **PDF-Export statt HTML:** Phase 3 hat auch PDF-Export (ADR-0021), aber PDF ist statisch — kein Hover-Effekt, kein Canvas-Vergrößern, keine Interaktion mit aufgedeckten Lösungen. HTML behält die Interaktivität.
- **Backend-Upload zu einem Server:** Verworfen — kein Backend, Datenschutz, Komplexität.
- **HTML mit ZIP-Anhang für Canvas:** Verworfen — Browser-Download kann keine ZIPs erzeugen ohne JS-Library, Datei-Magic zerbricht.
- **State direkt in URL hash (`#state=...`):** funktioniert für kleine States, scheitert spätestens bei Canvas-Daten (URL-Länge-Limit der Browser ~2000–8000 Zeichen).

## Konsequenzen

**Positiv:**
- Lehrkraft-Workflow stark vereinfacht — Datei anklicken statt Import-Dialog
- Eltern-tauglich — Doppelklick reicht
- Selbsterklärendes Format: jeder kann eine HTML-Datei öffnen
- Single-File-Prinzip erhalten — auch der Export ist selbsttragend
- Funktioniert offline, ohne Account, ohne Server

**Negativ / Trade-offs:**
- Doppelter Export-Weg → Topbar wird voller, etwas mehr UX-Komplexität
- Dateigröße bei Canvas-haltigen Onepagern erheblich (siehe oben)
- Schüler-Verlust-Risiko: wer den Export verschickt UND lokal löscht, ist nur noch im Empfänger-HTML drin. Reset-Modal sollte vor Löschung warnen
- Empfänger:in muss aufpassen: Wenn sie selbst Eingaben macht, überschreibt sie die Schüler-Eingaben. Daher: in exportierter Datei standardmäßig den Topbar-„Reset"-Button **ausgrauen** oder mit Warnung versehen

**Folgewirkungen für künftige Onepager:**
- Boilerplate enthält den HTML-Export-Mechanismus standardmäßig
- Profile, die viel Canvas nutzen ([digitales Arbeitsheft](../profiles/digitales-arbeitsheft.md)), empfehlen den HTML-Export als primären Übergabeweg
- Sensible Profile (Reflexionstagebuch, Kompetenzraster) verwenden ein Bestätigungs-Modal vor Export
- Erkennung „Diese Datei ist ein Export" beim Öffnen → optional Topbar-Hinweis-Banner

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Single-File auch für Export
- [ADR-0002](0002-state-persistenz-localstorage.md) — State-Schema, das embedded wird
- [ADR-0003](0003-json-export-import.md) — JSON-Variante bleibt bestehen
- [ADR-0019](0019-canvas-stift-modul.md) — Canvas-PNG geht mit
- [ADR-0021](0021-pdf-export-inline.md) — PDF als Alternative für statische Übergabe
- [profiles/digitales-arbeitsheft.md](../profiles/digitales-arbeitsheft.md) — Empfiehlt HTML-Export als Hauptübergabe
