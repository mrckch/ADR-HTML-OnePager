# ADR-0027: Datum/Zeit-Eingaben

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** UI-Pattern, Eingabe-Standards, Mobile-Tauglichkeit

## Kontext

Mehrere Profile brauchen **Datum- oder Zeit-Eingaben**:

- [Reflexionstagebuch](../profiles/reflexionstagebuch.md) — Datum pro Eintrag
- [Lektüre-Tagebuch](../profiles/lektuere.md) — Datum pro Kapitel-Eintrag
- [Hausaufgaben](../profiles/hausaufgaben.md) — Abgabe-Termin
- [Kompetenzraster](../profiles/kompetenzraster.md) — Pre-/Post-Datum
- [Recherche](../profiles/recherche.md) — Veröffentlichungsdatum pro Quelle
- [Lernportfolio](../profiles/lernportfolio.md) — Datum pro Eintrag

Bisher hat jedes Profil eigene Lösungen gewählt — mal `<input type="date">`, mal `<input type="text" placeholder="TT.MM.JJJJ">`, mal versteckt im Header. Das ist inkonsistent.

## Entscheidung

**`<input type="date">` als Standard** mit klar definiertem Verhalten.

### HTML-Pattern

```html
<div class="field">
  <label for="datum-eintrag">Datum</label>
  <input type="date" id="datum-eintrag" data-state="datum-eintrag">
</div>
```

### Browser-natives Date-Picker — bewusst gewählt

- **iOS Safari**: zeigt Roll-Picker (gut für Touch)
- **Android Chrome**: zeigt Material-Date-Picker
- **Desktop**: Native Picker (Browser-abhängig, aber konsistent erlebt)

Wir verwenden **nicht** ein eigenes Date-Picker-Widget. Gründe:
- Native ist barrierefrei (Screenreader, Tastaturbedienung)
- Lokalisiert (deutsche Wochentage, deutsche Monatsnamen)
- Touch-optimiert auf Mobil-Geräten
- Externe Libs wie Flatpickr würden ADR-0001 verletzen

### Format und Persistenz

`input type="date"` speichert intern **immer im ISO-Format `YYYY-MM-DD`** — unabhängig von der Anzeige im Browser. Das ist auch das, was wir in den localStorage schreiben. Vorteile:

- Sortierbar als String
- Kompatibel mit `new Date('2026-05-22')`
- Eindeutig (kein Tag/Monat-Verwechslungs-Risiko)

### Standard-Verhalten beim Default

#### „Heute" als Default vorausfüllen (optional)

Manche Profile (Hausaufgabe, Reflexion) wollen **„Heute" beim ersten Aufruf vorausfüllen**. Pattern:

```js
// Beim Init, nach loadState():
document.querySelectorAll('input[type="date"][data-default="today"]').forEach(el => {
  if (!el.value) {
    el.value = new Date().toISOString().slice(0, 10);
    saveState();
  }
});
```

HTML:
```html
<input type="date" data-state="eintrag-datum" data-default="today">
```

#### Bei Hausaufgabe: Abgabe-Datum vorgegeben

Manche Datum-Felder sind **nicht editierbar** — z. B. die von der Lehrkraft vorgegebene Abgabe-Frist:

```html
<div class="meta-field">
  <label>Abgabe bis</label>
  <input type="date" value="2026-05-30" readonly aria-readonly="true">
</div>
```

`readonly` statt `disabled`, damit der Wert im Tab-Reading-Flow bleibt.

### Zeit-Eingaben (selten)

`<input type="time">` für Uhrzeit-Felder — selten gebraucht, aber selbe Logik:
- 24-Stunden-Format intern (`HH:MM`)
- Browser-natives Widget
- Locale-abhängige Anzeige

### Datum + Zeit kombiniert

`<input type="datetime-local">` existiert, hat aber zwei Schwächen:
- Inkonsistente Browser-Implementierungen
- Hat keine Zeitzone-Info

Empfehlung: **getrennte Felder** für Datum und Zeit, wenn beide gebraucht werden.

### Anzeige-Formatierung

Wenn das Datum **angezeigt** wird (z. B. „Eintrag vom 22. Mai 2026"), nutzen wir `toLocaleDateString('de-DE')`:

```js
function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso + 'T00:00:00');
  return d.toLocaleDateString('de-DE', { day: 'numeric', month: 'long', year: 'numeric' });
}
// 2026-05-22 → "22. Mai 2026"
```

Speichern bleibt ISO, Anzeige ist lokalisiert.

### Druck-Verhalten

Im Druck wird der Datum-Wert sichtbar, aber das Picker-Widget verschwindet:

```css
@media print {
  input[type="date"] {
    border: 0;
    background: transparent;
    color: #000;
    /* Native picker-Buttons ausblenden */
    -webkit-appearance: none;
    appearance: none;
  }
}
```

In den meisten Browsern erscheint der Wert dann als Text. Bei Bedarf kann ein zusätzlicher `<span>` daneben das Datum lokalisiert ausgeben.

### Spezialfall: Pre/Post-Datum im Kompetenzraster

Im Kompetenzraster gibt es **zwei Datum-Felder** (vor und nach der Einheit):

```html
<div class="meta-row">
  <div class="meta-field">
    <label>Vor der Einheit</label>
    <input type="date" data-state="datum-pre" data-default="today">
  </div>
  <div class="meta-field">
    <label>Nach der Einheit</label>
    <input type="date" data-state="datum-post">
    <!-- KEIN data-default="today" — wird erst beim 2. Aufruf gesetzt -->
  </div>
</div>
```

Das zweite Datum bleibt leer, bis die Schüler:in es manuell setzt — Lehrkraft kann dann beim Auswerten sehen, wann post gemacht wurde.

## Alternativen

- **Eigenes Date-Picker-Widget bauen** — überflüssig, native reicht
- **External Lib (Flatpickr, Pikaday)** — verletzt ADR-0001
- **Text-Input mit Format-Parsing** — fehleranfälliger, schlechtere Mobile-UX
- **HTML5 Date-Format auf de-DE umstellen** — nicht möglich, ISO ist verpflichtend

## Konsequenzen

**Positiv:**
- Konsistentes Datum-Pattern über alle Profile
- Touch- und Tastatur-optimiert dank nativen Pickern
- Sortier- und vergleichbar im ISO-Format
- Lokalisiert in der Anzeige
- Kein externes JS

**Negativ / Trade-offs:**
- Native Picker variieren visuell zwischen Browsern
- `datetime-local` nicht zuverlässig — wir vermeiden es
- Pre-Filled „Today" braucht JS, kein reines HTML

**Folgewirkungen für künftige Onepager:**
- Datum-Felder immer als `<input type="date">`, nie als Text
- `data-default="today"` für Felder, die mit heute vorbelegt werden sollen
- Anzeige via `toLocaleDateString('de-DE', …)` wenn formatiert nötig
- ISO-Format (`YYYY-MM-DD`) als Persistenz-Wert
- `readonly` (nicht `disabled`) für nicht-editierbare Daten

## Verwandte ADRs / Profile

- [profiles/reflexionstagebuch.md](../profiles/reflexionstagebuch.md) — Datum pro Eintrag
- [profiles/hausaufgaben.md](../profiles/hausaufgaben.md) — Abgabe-Termin
- [profiles/kompetenzraster.md](../profiles/kompetenzraster.md) — Pre/Post-Datum
- [profiles/lektuere.md](../profiles/lektuere.md) — Lese-Datum pro Kapitel
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — native Inputs sind a11y-freundlich
