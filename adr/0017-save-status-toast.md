# ADR-0017: Save-Status-Indikator und Toast-Feedback

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** UX-Feedback, Vertrauen in Auto-Save, ARIA

## Kontext

Auto-Save in localStorage ([ADR-0002](0002-state-persistenz-localstorage.md)) ist still: Schüler:innen sehen nicht, ob ihre Eingaben tatsächlich gesichert wurden. Daraus folgen zwei Probleme:

1. **Misstrauen:** „Ist meine Antwort jetzt wirklich gespeichert? Soll ich nochmal exportieren?"
2. **Unsicherheit nach Aktionen** (Export, Import, Reset): Es passiert „etwas", aber ohne sichtbare Quittung wirkt es undeutlich.

Die ursprüngliche `.status`-Box aus dem Boilerplate v1 lebte mitten im Content, wurde leicht übersehen und reservierte Platz, auch wenn sie leer war.

## Entscheidung

**Zwei dedizierte UX-Patterns:**

### 1. Save-Status-Indikator im Topbar

Ein **kleiner farbiger Punkt** plus Label in der Topbar, immer sichtbar.

- **Grün + „Gespeichert"** im Ruhezustand
- **Gold + „Nicht gespeichert …"** sobald sich der State geändert hat, bis Auto-Save abgeschlossen ist (Debounce, ~1,2 s nach letzter Eingabe)
- **Beim Tippen wechselt der Punkt sofort auf Gold** (auch wenn der eigentliche Save erst gleich kommt) — wirkt unmittelbar reaktiv

```html
<span class="save-status" role="status" aria-live="polite">
  <span class="save-dot" id="save-dot"></span>
  <span id="save-label">Gespeichert</span>
</span>
```

```css
.save-status { display: flex; align-items: center; gap: var(--space-2);
               font-size: var(--fs-xs); color: var(--fg-soft); font-style: italic; }
.save-dot    { width: 8px; height: 8px; border-radius: 50%;
               background: var(--green); transition: background .25s; }
.save-dot.dirty { background: var(--gold); }
```

```js
function markDirty() {
  document.getElementById('save-dot').classList.add('dirty');
  document.getElementById('save-label').textContent = 'Nicht gespeichert …';
  clearTimeout(saveTimer);
  saveTimer = setTimeout(commitSave, 1200);
}
function commitSave() {
  saveState(readUI());
  document.getElementById('save-dot').classList.remove('dirty');
  document.getElementById('save-label').textContent = 'Gespeichert';
}
```

### 2. Toast-Notifications für punktuelle Aktionen

Für **abgeschlossene Aktionen** (Export gespeichert, Import geladen, Reset erfolgt, Fehler) wird ein Toast unten rechts eingeblendet und fadet nach 3–4 Sekunden weg.

```html
<div id="toast" role="status" aria-live="polite"></div>
```

```css
#toast {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  background: var(--navy);
  color: #fff;
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--gold);
  box-shadow: var(--shadow-md);
  font-size: var(--fs-sm);
  max-width: 320px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity .25s, transform .25s;
  pointer-events: none;
  z-index: 9999;
}
#toast.show { opacity: 1; transform: translateY(0); }
#toast.toast--error { border-left-color: var(--red); }

@media (prefers-reduced-motion: reduce) {
  #toast { transition: opacity .01ms; transform: none; }
}
```

```js
function showToast(msg, opts = {}) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.toggle('toast--error', opts.kind === 'error');
  el.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => el.classList.remove('show'), opts.duration ?? 3500);
}
```

### Abgrenzung Save-Indikator vs. Toast

- **Save-Indikator** = laufender Zustand („gerade jetzt"): grün/gold, immer sichtbar.
- **Toast** = punktuelle Quittung („das ist gerade passiert"): kommt, verschwindet wieder.

Niemals beide für dasselbe Ereignis verwenden.

## Alternativen

- **Browser-Notification-API:** Verworfen — braucht Berechtigung, Schüler:innen finden das verstörend für Lernmaterial.
- **`alert()` für Quittungen:** Verworfen — blockierend, abrupt, A11y-schwierig.
- **Stiller Auto-Save ohne Indikator** (wie ADR-0002 ursprünglich):  Verworfen — siehe Kontext.
- **„Speichern"-Button (manuell):** Verworfen — Auto-Save ist schon entschieden, manueller Knopf widerspricht dem Modell und bringt eine zweite Wahrheit ins UI.

## Konsequenzen

**Positiv:**
- Schüler:innen sehen jederzeit, ob gespeichert ist → Vertrauen
- Aktionsquittungen sind sichtbar, aber unaufdringlich
- ARIA-live sorgt für Screenreader-Hinweis
- Toast respektiert `prefers-reduced-motion`

**Negativ / Trade-offs:**
- Etwas mehr DOM/CSS/JS im Boilerplate
- Bei langer Antworten-Eingabe steht der Save-Indikator möglicherweise dauerhaft auf Gold — fühlbar, aber kein Bug

**Folgewirkungen für künftige Onepager:**
- `.save-status` **immer** im Topbar
- `#toast` **immer** im DOM (auch wenn anfangs versteckt)
- Alle Aktionen (Export, Import, Reset, Fehler) **immer** mit Toast quittieren
- `aria-live="polite"` an beiden Containern setzen
- Bei `prefers-reduced-motion`: Animationen minimieren (CSS-Regel ist schon im Snippet)

## Verwandte ADRs

- [ADR-0002](0002-state-persistenz-localstorage.md) — Auto-Save-Verhalten
- [ADR-0003](0003-json-export-import.md) — Toast quittiert Export/Import
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Toast quittiert Reset
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — ARIA-live
- [ADR-0022](0022-design-system-v2.md) — Farbtokens
