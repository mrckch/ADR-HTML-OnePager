# ADR-0025: Lernportfolio-Persistenz (Liste-basiertes Schema)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** Persistenz, Lernportfolio-Profil

## Kontext

Das bisherige State-Schema aus [ADR-0002](0002-state-persistenz-localstorage.md) ist **flach**:

```json
{ "version": 1, "data": { "a-1": "60", "a-2": "antwort", "meta-name": "Anna" } }
```

Das funktioniert hervorragend für die meisten Profile, weil die Felder im HTML vorgegeben sind und sich nicht zur Laufzeit ändern. Beim **Lernportfolio**-Profil ([profiles/lernportfolio.md](../profiles/lernportfolio.md)) versagt das Modell aber:

- Schüler:innen sammeln über Wochen/Monate **beliebig viele** Einträge
- Jeder Eintrag hat Datum, Typ, Tags, Inhalt — also strukturierte Sub-Daten
- Anzahl der Einträge ist nicht vorab bekannt

Die provisorische „Feste-Slots"-Variante (8 vorgegebene Slots) ist eine Krücke und limitiert die Schüler:innen. Eine ordentliche Implementation braucht ein **listen-basiertes Schema**.

## Entscheidung

Das State-Schema wird auf **Version 2** angehoben und um einen optionalen `_eintraege`-Array erweitert. Das flache Schema bleibt für alle anderen Profile unverändert — `_eintraege` ist eine zusätzliche, optionale Struktur.

### Schema v2

```json
{
  "version": 2,
  "data": {
    "meta-name": "Anna",
    "profil-klasse": "8a",
    "_eintraege": [
      {
        "id": "e1717238400000",
        "datum": "2026-05-22",
        "typ": "reflexion",
        "titel": "Erste Mathearbeit",
        "inhalt": "Ich habe heute gemerkt, dass ich beim Bruchrechnen…",
        "tags": ["mathe", "klassenarbeit"]
      },
      {
        "id": "e1717324800000",
        "datum": "2026-05-25",
        "typ": "lernprodukt",
        "titel": "Mindmap zu Photosynthese",
        "inhalt": "data:image/png;base64,iVBOR…",
        "tags": ["bio", "skizze"]
      }
    ]
  }
}
```

### Eintrags-Typen

Drei Typen, klar voneinander unterschieden:

| Typ | `inhalt`-Format | UI-Element |
|---|---|---|
| `reflexion` | Plain text | `<textarea>` |
| `lernprodukt` | Plain text **oder** Base64-PNG (Canvas) | `<textarea>` oder Canvas-Snippet |
| `quelle` | URL + Notiztext (als JSON-String) | Strukturierter Input |

Pro Eintrag kann der Typ **nicht** wechseln, sobald er angelegt ist — sonst geht der `inhalt` verloren. Beim Anlegen entscheidet die Schüler:in einmalig.

### IDs

`id` ist ein Timestamp-basierter String (z. B. `e<unix-ms>`). Vorteile:
- Eindeutig genug für ein einzelnes Lernportfolio
- Reihenfolge-erhaltend (Sortierung nach `id` = chronologisch)
- Keine UUID-Lib nötig (siehe [ADR-0001](0001-single-file-html-architektur.md))

### CRUD-Operationen

```js
function addEintrag(typ, titel) {
  const id = 'e' + Date.now();
  const eintrag = { id, datum: today(), typ, titel: titel || '', inhalt: '', tags: [] };
  state._eintraege = state._eintraege || [];
  state._eintraege.push(eintrag);
  saveState();
  renderEintraege();
  return id;
}
function removeEintrag(id) {
  state._eintraege = state._eintraege.filter(e => e.id !== id);
  saveState();
  renderEintraege();
}
function updateEintrag(id, patch) {
  const e = state._eintraege.find(x => x.id === id);
  if (e) Object.assign(e, patch);
  saveState();
}
function getEintraege({ tag, typ } = {}) {
  let list = state._eintraege || [];
  if (tag) list = list.filter(e => e.tags.includes(tag));
  if (typ) list = list.filter(e => e.typ === typ);
  return list.sort((a, b) => b.datum.localeCompare(a.datum));  // neueste zuerst
}
```

### Schema-Migration v1 → v2

Beim Laden eines alten Onepagers mit Schema v1:

```js
function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return defaultState();
  const parsed = JSON.parse(raw);
  if (parsed.version === 1) return migrateV1toV2(parsed);
  if (parsed.version === 2) return parsed;
  return defaultState();
}

function migrateV1toV2(old) {
  // Schema v1 hat kein _eintraege — v2 hat es optional. Migration ist trivial:
  return { version: 2, data: { ...old.data, _eintraege: old.data._eintraege || [] } };
}
```

Da das `_eintraege`-Feld **additiv** ist, kostet die Migration nichts. Onepager, die das Feld nicht brauchen, ignorieren es einfach.

### Dynamisches DOM-Rendering

Anders als bei allen anderen Profilen, wo HTML-Felder statisch im Markup stehen, wird die Eintragsliste **zur Laufzeit gerendert**:

```js
function renderEintraege() {
  const container = document.getElementById('eintraege-liste');
  const filterTag = document.body.dataset.tagFilter || null;
  const items = getEintraege({ tag: filterTag });
  container.innerHTML = items.map(e => `
    <article class="eintrag" data-id="${e.id}">
      <header>
        <span class="datum">${formatDate(e.datum)}</span>
        <span class="typ-badge typ-${e.typ}">${typLabel(e.typ)}</span>
        <input type="text" class="titel" value="${escapeHtml(e.titel)}" data-field="titel">
        <button class="remove" aria-label="Eintrag löschen">×</button>
      </header>
      <textarea data-field="inhalt" rows="4">${escapeHtml(e.inhalt)}</textarea>
      <input type="text" class="tags" value="${e.tags.join(', ')}"
             placeholder="Tags (kommagetrennt)" data-field="tags">
    </article>
  `).join('');
}
```

Edit-Events landen via Event-Delegation am Container. Bei jeder Änderung: `updateEintrag(id, {feld: wert})`.

### Tag-Filter und Übersicht

Tags werden zur Suche/Filterung verwendet. Über den Einträgen ein Filter-UI:

```html
<div class="tag-filter">
  <button data-tag="">Alle (23)</button>
  <button data-tag="mathe">mathe (8)</button>
  <button data-tag="bio">bio (5)</button>
  …
</div>
```

Tags werden aus allen vorhandenen Einträgen automatisch eingesammelt (mit Häufigkeit).

### Datenschutz und Größe

Ein Lernportfolio kann groß werden — gerade mit Canvas-Lernprodukten (Skizzen). Daraus folgen drei Hinweise:

1. **localStorage hat 5–10 MB Limit pro Origin.** Bei 30 Einträgen mit je einer 100 KB Skizze ist man bei ~3 MB — noch unter dem Limit, aber spürbar. Im Reset-Dialog explizit warnen.
2. **HTML-Export-Reminder** (regelmäßig sichern) ist hier doppelt wichtig. Das Profil empfiehlt monatliches Sichern.
3. **JSON-Export ist primärer Übergabe-Mechanismus**, weil HTML-Export bei vielen Einträgen die Datei groß macht.

## Alternativen

- **IndexedDB statt localStorage:** Mächtiger (kein Größenlimit, strukturierte Queries), aber asynchron, komplexer. Für ein Single-File-HTML zu schwer. Verworfen.
- **Verschachteltes Schema (Map statt Array):** Hätte O(1)-Zugriff per ID, aber Sortier-Reihenfolge geht verloren. Verworfen.
- **Mehrere Speicher-Keys (`onepager:<slug>:eintrag:<id>`):** Verworfen — bricht das Pro-Onepager-State-Modell.
- **Sub-Schema-Version für `_eintraege`:** Erwogen, aber Overkill. Wenn das Eintrags-Schema sich ändert, bumpen wir die Hauptversion.

## Konsequenzen

**Positiv:**
- Lernportfolio kann jetzt beliebig viele Einträge aufnehmen
- Schema bleibt rückwärtskompatibel (v1 → v2 ist trivial)
- Andere Profile sind nicht betroffen
- Tag-Filter und chronologische Sortierung funktionieren ohne weitere Strukturen

**Negativ / Trade-offs:**
- Dynamisches Rendering bricht das „HTML ist Single Source"-Prinzip — der State bestimmt jetzt mit, was im DOM ist
- HTML-Export wird bei vielen Einträgen sehr groß
- Komplexer als andere Profile — höhere Schwelle für KI-Generierung
- Migration-Logik muss im Boilerplate verankert sein

**Folgewirkungen für künftige Onepager:**
- Schema-Version-Check beim Laden: `version === 2` oder Migration aus `version === 1`
- Wenn ein Profil dynamische Listen braucht, lehnt es sich an dieses Pattern an
- Snippet `templates/snippets/lernportfolio-eintraege-snippet.html` ist der Referenz-Code

## Verwandte ADRs / Profile

- [ADR-0002](0002-state-persistenz-localstorage.md) — Basis-Persistenz, hier auf v2 angehoben
- [ADR-0019](0019-canvas-stift-modul.md) — Canvas-Einträge nutzen Base64-PNG im `inhalt`-Feld
- [ADR-0020](0020-html-export-eingebetteter-state.md) — Embedded-State funktioniert mit beiden Schema-Versionen
- [profiles/lernportfolio.md](../profiles/lernportfolio.md) — Hauptkonsument dieses Schemas
