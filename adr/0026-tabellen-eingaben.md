# ADR-0026: Tabellen-Eingaben (editierbare Tabellen)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** UI-Pattern, Eingabe-Standards

## Kontext

Mehrere Profile brauchen **tabellarische Eingaben**:

- [Kompetenzraster](../profiles/kompetenzraster.md) — „Ich kann …"-Aussagen mit Skala pro Zeile
- [Statistik](../profiles/statistik.md) — Messreihen mit eigenen Werten
- [Recherche](../profiles/recherche.md) — Vergleich von Quellen
- [Lektüre](../profiles/lektuere.md) — Figurenverzeichnis
- [Erarbeitungsseite](../profiles/erarbeitungsseite.md) — gelegentlich Datenreihen

Bisher hat jedes Profil sein eigenes Tabellen-Pattern dokumentiert. Das ist redundant und führt zu Inkonsistenzen (Mobile-Verhalten, Persistenz-Schema, Druck-Verhalten).

## Entscheidung

Ein **standardisiertes Pattern für editierbare Tabellen** in Onepagern.

### HTML-Struktur

```html
<div class="table-wrapper">
  <table class="data-table">
    <thead>
      <tr>
        <th scope="col">Spalte 1</th>
        <th scope="col">Spalte 2</th>
        <th scope="col">Spalte 3</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Zeile A</th>
        <td><input type="text" data-state="t1-a-2"></td>
        <td><input type="number" data-state="t1-a-3" data-expected="42" data-tolerance="1"></td>
      </tr>
      <tr>
        <th scope="row">Zeile B</th>
        <td><input type="text" data-state="t1-b-2"></td>
        <td><input type="number" data-state="t1-b-3"></td>
      </tr>
    </tbody>
  </table>
</div>
```

**Konventionen:**
- `<table class="data-table">` als Klassen-Marker
- `<th scope="col">` für Spalten-Header, `<th scope="row">` für Zeilen-Header (Accessibility)
- Jede Zelle mit Input bekommt **eindeutiges `data-state`**, Schema `t<tabellen-id>-<zeile>-<spalte>` oder `<aufgaben-id>-<zellen-id>`
- `<input>` direkt in `<td>` — keine Wrapper-Divs für Standard-Eingaben

### CSS-Standard

```css
.table-wrapper { overflow-x: auto; margin: var(--space-3) 0; }
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--fs-sm);
}
.data-table th,
.data-table td {
  border: 1px solid var(--border);
  padding: var(--space-1) var(--space-2);
  text-align: left;
}
.data-table th {
  background: var(--bg-elevated);
  color: var(--navy);
  font-weight: 600;
}
.data-table tbody tr:nth-child(even) { background: var(--bg-info); }
.data-table td input {
  width: 100%; min-width: 60px;
  background: transparent; border: 0;
  font: inherit; color: var(--fg);
  padding: var(--space-1);
  outline: none;
}
.data-table td input:focus {
  background: var(--bg-answer);
  outline: 2px solid var(--gold);
  outline-offset: -2px;
}
```

Inputs in Tabellen sind **dezent gestylt** — kein eigener Hintergrund/Rand, damit die Tabelle als Ganzes sichtbar bleibt. Nur beim Fokus visuell hervorgehoben.

### Mobile-Fallback: Cards

Auf Smartphone-Breite (< 600 px) bricht die Tabelle in **vertikale Cards** um — eine Card pro Zeile:

```css
@media (max-width: 600px) {
  .data-table, .data-table thead, .data-table tbody,
  .data-table tr, .data-table th, .data-table td { display: block; }
  .data-table thead { display: none; }
  .data-table tr {
    background: var(--bg-page);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-3);
    margin-bottom: var(--space-3);
  }
  .data-table th[scope="row"] {
    font-weight: 700;
    color: var(--navy);
    margin-bottom: var(--space-2);
    border: 0; padding: 0;
  }
  .data-table td {
    border: 0;
    padding: var(--space-1) 0;
  }
  .data-table td::before {
    content: attr(data-label) ": ";
    font-weight: 600;
    color: var(--fg-muted);
    display: inline-block;
    min-width: 100px;
  }
}
```

Damit der Mobile-Fallback Spaltennamen anzeigt, bekommen die `<td>` ein `data-label`-Attribut:

```html
<td data-label="Spalte 2"><input type="text" data-state="..."></td>
```

### Live-Summen / Spalten-Aggregate (optional)

Manchmal soll eine Tabelle eine **Summen-Zeile** oder eine **Aggregat-Zelle** haben, die sich live aktualisiert:

```html
<tr class="data-table__summe">
  <th scope="row">Σ</th>
  <td><output data-aggregate="sum" data-aggregate-col="2"></output></td>
  <td><output data-aggregate="sum" data-aggregate-col="3"></output></td>
</tr>
```

JS-Helper:

```js
function updateAggregates(table) {
  table.querySelectorAll('output[data-aggregate]').forEach(out => {
    const col = parseInt(out.dataset.aggregateCol, 10);
    const op = out.dataset.aggregate;
    const cells = table.querySelectorAll(
      `tbody tr:not(.data-table__summe) td:nth-child(${col + 1}) input`
    );
    const values = Array.from(cells)
      .map(el => parseFloat(el.value))
      .filter(v => !isNaN(v));
    let result;
    if (op === 'sum')      result = values.reduce((s, v) => s + v, 0);
    else if (op === 'avg') result = values.length ? values.reduce((s, v) => s + v, 0) / values.length : 0;
    else if (op === 'count') result = values.length;
    else if (op === 'max') result = values.length ? Math.max(...values) : 0;
    else if (op === 'min') result = values.length ? Math.min(...values) : 0;
    out.value = isFinite(result) ? result.toFixed(2).replace(/\.?0+$/, '') : '';
  });
}
table.addEventListener('input', () => updateAggregates(table));
```

Unterstützte Aggregate: `sum`, `avg`, `count`, `max`, `min`. Werden bei jeder Eingabe neu berechnet.

### Druck-Verhalten

```css
@media print {
  .data-table { font-size: 9pt; border: 0.5pt solid #000; }
  .data-table th, .data-table td { border: 0.5pt solid #000; padding: 2pt 4pt; }
  .data-table td input { border: 0; background: transparent; color: #000; }
}
```

Tabellen drucken sauber als A4-Tabelle. Bei langen Tabellen kann `break-inside: avoid` an `tr` gesetzt werden, damit Zeilen nicht zerschnitten werden.

## Alternativen

- **Externes Tabellen-Tool (Handsontable etc.)** — verletzt ADR-0001
- **`contenteditable` statt `<input>`** — komplizierter zu styllen, schlechtere Mobile-Tauglichkeit, schwieriger Persistenz
- **Eigene Tabellen-Komponente in JS** — Overengineering für den Anwendungsfall
- **Tabellen-spezifisches Persistenz-Schema** (verschachteltes `data[t1][a][2]`) — verworfen, flache Keys sind einfacher zu serialisieren

## Konsequenzen

**Positiv:**
- Einheitliches Tabellen-Pattern über alle Profile
- Mobile-Fallback Standard-Verhalten
- Live-Aggregate als optionales Feature
- Druckbar
- Persistenz nahtlos im flachen `data-state`-Schema

**Negativ / Trade-offs:**
- Viele `data-state`-Keys pro Tabelle (eine pro Zelle) — bei 10×5 Tabelle = 50 Keys. Akzeptabel, weil flach speicherbar
- Mobile-Fallback erfordert `data-label`-Attribute (extra Aufwand beim Erstellen)

**Folgewirkungen für künftige Onepager:**
- Profile, die Tabellen nutzen, verweisen auf dieses ADR
- Schema für `data-state`-Keys: `<aufgabe>-<row>-<col>` oder ähnlich konsistent
- `<th scope>` immer setzen für Accessibility
- `data-label` an `<td>`s setzen für Mobile-Fallback

## Verwandte ADRs / Profile

- [profiles/kompetenzraster.md](../profiles/kompetenzraster.md) — Klassischer Anwendungsfall
- [profiles/statistik.md](../profiles/statistik.md) — Datentabellen
- [profiles/recherche.md](../profiles/recherche.md) — Quellen-Vergleichstabelle
- [ADR-0006](0006-responsives-layout.md) — Mobile-First-Anforderung
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — `<th scope>` für Screenreader
