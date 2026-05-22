# ADR-0023: A4-Druck-Layout und A4-Preview-Modus

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Druck, Layout, Lehrkraft-Workflow

## Kontext

[ADR-0007](0007-druck-pdf-optimierung.md) hat Druck schon als Anforderung definiert, aber das praktische Druckbild war suboptimal:

- Container-Padding in `px` → für A4 viel zu groß
- Schriftgrößen in `px` → werden beim Drucken nicht ideal skaliert
- `.page-break-hint` war nur ein visueller Editor-Hinweis, **kein echter** Seitenumbruch
- Goldene/cremefarbene Hintergründe verschwenden Tinte auf S/W-Druckern
- Keine Vorschau-Möglichkeit auf dem Bildschirm, bevor man druckt

Resultat: Lehrkräfte hatten beim physischen Ausdruck (Klassensatz Papier) ein schiefes, zu großes, schlecht umbrochenes Ergebnis. Workflows, die in PDF-Apps wie GoodNotes landen, kaschieren das, aber spätestens am Drucker fällt es auf.

## Entscheidung

Zwei zusammengehörige Maßnahmen:

### 1. Print-CSS aggressiv auf A4 trimmen

Im `@media print`-Block:

- **`@page { size: A4 portrait; margin: 18mm; }`** — gängiges Arbeitsblatt-Maß
- **Alle Schriftgrößen in pt:** h1 18pt, h2 14pt, h3 12pt, Body 10.5pt, hint/code 9pt
- **Container ohne eigenes Padding:** `.page` und `.content` haben in `@media print` `padding: 0` — das Margin macht `@page`
- **Monochrome:** alle Hintergründe weiß, alle Texte schwarz, alle Borders schwarz. Kein Gold-Akzent — der wird auf S/W-Druckern grau und auf Farbdruckern verschwendet Tinte
- **Aufgaben:** 1.5pt schwarze Top-Border, 0.5pt schwarze restliche Borders
- **`.page-break-hint`:** wird zu **echtem Seitenumbruch** (`break-after: page; page-break-after: always`)
- **`orphans: 3; widows: 3`** — verhindert einsame Zeilen am Seitenanfang/-ende
- **`break-inside: avoid`** für `.aufgabe`, `.box`, `.quiz-frage`, `figure`, `table`, `.field`, `.hint-content`, `.solution-content` — kein Zerschneiden
- **Topbar, Modals, Toast, Reveal-Buttons, Feedback-Spans, Save-Status, Progress** komplett ausblenden
- **Lösungen drucken nur, wenn vorher aufgedeckt** (oder `?solutions=1` für Lehrer-Druck — bereits in [ADR-0010](0010-loesungs-huerde.md) festgelegt)
- **A-tags mit URL ausdrucken** für externe Quellen: `a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 8pt; color: #444; }`

### 2. A4-Preview-Modus auf dem Bildschirm

Damit Lehrkräfte vor dem Drucken sehen, was sie bekommen, gibt es einen **Bildschirm-Vorschau-Modus**, der das Print-Layout 1:1 simuliert.

**Aktivierung:**
- URL-Parameter `?layout=a4` → bei Seitenaufruf aktiv
- Topbar-Button **„🖨 A4-Vorschau"** togglet via `body.classList.toggle('a4-preview')` und aktualisiert die URL (`history.replaceState`)

**Visuelles Verhalten (`body.a4-preview`):**
- Body bekommt grauen Hintergrund (`#888`), Padding oben/unten 1cm
- `.page` wird auf **`width: 210mm; min-height: 297mm; padding: 18mm`** gesetzt
- `box-shadow: 0 4px 24px rgba(0,0,0,.4)` simuliert „Blatt auf grauem Schreibtisch"
- **Alle Print-CSS-Regeln werden gespiegelt** — gleiche Schriftgrößen (pt), gleiche Schwarz/Weiß-Behandlung, gleiche Borders
- `.page-break-hint` wird zu einem sichtbaren Trenner mit Text „↓ neue A4-Seite ↓" zwischen Seiten
- Topbar bleibt sichtbar (außerhalb der „Seite") für den Toggle-Button
- Modals/Toast funktionieren weiter

**Versprechen:** Was du im A4-Preview siehst, ist exakt das, was beim Druck rauskommt — abgesehen vom Toolbar-Chrome, das beim echten Druck weg ist.

### 3. Toggle-Button im Topbar

Ein zusätzlicher Button neben „Zurücksetzen", außen am linken Aktions-Cluster:

```html
<button type="button" class="tb-btn tb-btn--preview" data-action="preview"
        title="A4-Druck-Vorschau ein-/ausschalten">
  🖨 <span class="label">A4-Vorschau</span>
</button>
```

JS toggle-Logik:
```js
function setA4Preview(on) {
  document.body.classList.toggle('a4-preview', on);
  const btn = document.querySelector('[data-action="preview"]');
  if (btn) {
    btn.querySelector('.label').textContent = on ? 'Vorschau aus' : 'A4-Vorschau';
    btn.title = on ? 'A4-Vorschau verlassen' : 'A4-Druck-Vorschau ein-/ausschalten';
  }
  const url = new URL(location.href);
  if (on) url.searchParams.set('layout', 'a4'); else url.searchParams.delete('layout');
  history.replaceState(null, '', url);
}
```

Beim Initialisieren: `setA4Preview(new URLSearchParams(location.search).get('layout') === 'a4');`

## Alternativen

- **Bei status quo bleiben** (ADR-0007 wie es war): Verworfen — Druckbild ist messbar schlecht.
- **JS-basierte „Word-Style"-Multipage-Vorschau** (Content auf mehrere A4-DIVs aufteilen): Verworfen — extrem komplex, Layout muss live umgemessen werden, fehleranfällig. Stattdessen: ein langer A4-breiter Container + sichtbare Umbruchmarkierungen.
- **Farbig drucken** (Gold/Cream/Navy beibehalten): Verworfen — Schul-S/W-Drucker liefern oft grau-bräunliches Ergebnis, Farbdruck verschwendet Tinte. Wer Color-PDF braucht: Phase-3 PDF-Export ([ADR-0021]) wird Farbe behalten.
- **Externes Print-Stylesheet** (separate Datei): Verworfen — verletzt [ADR-0001](0001-single-file-html-architektur.md).
- **mm statt pt:** Erwogen — pt ist im Druck-Kontext idiomatischer und kompatibler mit Word-Konventionen, an die Lehrkräfte gewöhnt sind.

## Konsequenzen

**Positiv:**
- Sauberes A4-Druckbild ohne Nachbearbeitung
- Echte, kontrollierbare Seitenumbrüche (`.page-break-hint`)
- A4-Vorschau auf dem Bildschirm — Lehrkraft weiß vorher, was kommt
- Tintenfreundlich (Monochrome statt Hintergrundflächen)
- A4-Preview-URL teilbar (`?layout=a4`)

**Negativ / Trade-offs:**
- Mehr CSS im `@media print`-Block + zusätzliche Preview-Regeln (~80 Zeilen)
- A4-Preview muss alle Print-CSS-Anpassungen spiegeln — bei Änderungen beide Stellen pflegen (Lösung: gemeinsamer Selektor `@media print, body.a4-preview`)
- Lehrkräfte müssen lernen, dass `?layout=a4` existiert (README + CHECKLIST helfen)

**Folgewirkungen für künftige Onepager:**
- `.page-break-hint` **bewusst** einsetzen — etwa zwischen Stundenabschnitten
- Beim Erstellen: **immer** einmal mit `?layout=a4` prüfen, bevor verteilt wird (steht auch in CHECKLIST.md)
- Bei langen Aufgaben: lieber zwei kleinere Aufgaben-Karten, damit `break-inside: avoid` nicht in Konflikt mit der Seitengröße gerät
- Bilder und SVGs auf < 100% Breite halten, sonst Druckumbruch unschön

## Verwandte ADRs

- [ADR-0007](0007-druck-pdf-optimierung.md) — Ursprüngliche Druck-Entscheidung, hier konkretisiert/ergänzt
- [ADR-0010](0010-loesungs-huerde.md) — `?solutions=1` für Lehrer-Druck mit allen Lösungen
- [ADR-0021] (Phase 3, geplant) — PDF-Export wird farbig sein, baut aber auf diesem Druck-Layout auf
