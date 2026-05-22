# Profil: Differenzierungs-Onepager (3 Niveaus)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der **denselben Inhalt in drei Anforderungsniveaus** anbietet — ★ Basis, ★★ Erweitert, ★★★ Experte. Schüler:innen wählen das Niveau, das zu ihrem Lernstand passt, und arbeiten daran. Bei Bedarf können sie wechseln.

Ziel: **Binnen-Differenzierung in heterogenen Klassen** ohne separate Arbeitsblätter ausdrucken zu müssen.

## Typische Merkmale

- **Klassenstufe:** alle, besonders in Gemeinschaftsschulen, Realschulen und integrativen Klassen
- **Fachbereich:** alle, besonders Mathematik, Sprachen, Naturwissenschaften — überall, wo Aufgaben in unterschiedlichen Schwierigkeitsgraden formulierbar sind
- **Zeitumfang:** Einzel- oder Doppelstunde
- **Ziel-Typ:** Übung, Anwendung, gelegentlich Erarbeitung
- **Gerät:** Laptop/Tablet (Smartphone schwierig wegen Tab-Layout)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten **pro Niveau dreimal** vorhanden — gleiche Karten-Struktur, unterschiedlicher Inhalt |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur zentral — Schüler:innen sollen merken, ob das gewählte Niveau passt |
| [ADR-0006](../adr/0006-responsives-layout.md) | Auf Smartphone wird Tab-Layout zu Tabs (vertikal), auf Tablet/Desktop nebeneinander |

## Core-ADRs abweichend oder weniger relevant

- **Lernziele:** **alle drei Niveaus haben die gleichen Lernziele** — dieselbe Sache, anders zugänglich. Das Lernziel-Block bleibt einfach.
- **Canvas:** je nach Fach (Mathe-Skizzen ja), sonst nicht zentral
- **[ADR-0013](../adr/0013-quiz-hardening.md) (Quiz):** nicht typisch — Differenzierung passiert über Aufgaben-Schwierigkeit, nicht über Quiz

## Spezifische didaktische Entscheidungen

### 1. Drei sichtbare Niveau-Stränge, einer aktiv

**Fertig-Snippet:** [`templates/snippets/niveau-tabs-snippet.html`](../templates/snippets/niveau-tabs-snippet.html) — CSS + HTML-Beispiel + JS in einem. Einfach einkopieren.

Die Schüler:in **wählt eines** der drei Niveaus per Tab oder Karten-Auswahl. Die anderen zwei sind sichtbar verfügbar, aber dezenter dargestellt:

```html
<nav class="niveau-tabs" role="tablist" aria-label="Anforderungsniveau wählen">
  <button role="tab" aria-selected="false" data-niveau="basis">★ Basis</button>
  <button role="tab" aria-selected="true"  data-niveau="erweitert">★★ Erweitert</button>
  <button role="tab" aria-selected="false" data-niveau="experte">★★★ Experte</button>
</nav>

<div class="niveau-pane" data-niveau="basis"     hidden>… Basis-Aufgaben …</div>
<div class="niveau-pane" data-niveau="erweitert">… Erweitert-Aufgaben …</div>
<div class="niveau-pane" data-niveau="experte"   hidden>… Experte-Aufgaben …</div>
```

CSS-Snippet:
```css
.niveau-tabs { display: flex; gap: var(--space-2); margin: var(--space-4) 0;
               border-bottom: 2px solid var(--border); }
.niveau-tabs button {
  background: transparent; border: 0; border-bottom: 3px solid transparent;
  padding: var(--space-2) var(--space-4); font: inherit; cursor: pointer;
  color: var(--fg-muted); margin-bottom: -2px;
}
.niveau-tabs button[aria-selected="true"] {
  color: var(--navy); border-bottom-color: var(--gold); font-weight: 600;
}
.niveau-pane[hidden] { display: none; }
```

JS-Snippet:
```js
document.querySelector('.niveau-tabs').addEventListener('click', e => {
  const btn = e.target.closest('button[data-niveau]');
  if (!btn) return;
  const niveau = btn.dataset.niveau;
  document.querySelectorAll('.niveau-tabs button').forEach(b =>
    b.setAttribute('aria-selected', b.dataset.niveau === niveau));
  document.querySelectorAll('.niveau-pane').forEach(p =>
    p.hidden = p.dataset.niveau !== niveau);
  // gewähltes Niveau persistieren
  localStorage.setItem('onepager:<slug>:niveau', niveau);
});
// beim Load wiederherstellen
```

### 2. Sterne als Niveau-Marker — visuell konsistent

Niveaus immer mit `★` / `★★` / `★★★` markiert, nie mit Farben (Grün/Gelb/Rot) — würde stigmatisieren („Ich bin der Rote"). Sterne sind aufsteigend und neutral.

### 3. Gleiches Lernziel, unterschiedliche Anforderung

Alle drei Niveaus zielen auf **dieselbe Kompetenz**, unterscheiden sich nur in:

| Niveau | Aufgaben-Charakter |
|---|---|
| ★ Basis | Mehr Strukturhilfen, konkretere Zahlen, evtl. Lückentext, mehr Hilfen-Stufen |
| ★★ Erweitert | Standard-Aufgaben aus dem Curriculum |
| ★★★ Experte | Transferaufgaben, abstrakte Variablen, offene Problemstellungen, ggf. Mehrschritt-Aufgaben |

**Anti-Pattern:** Drei verschiedene Themen pro Niveau. → Differenzierung muss am selben Lerngegenstand stattfinden.

### 4. Wechsel zwischen Niveaus erlaubt

Schüler:in kann jederzeit das Niveau wechseln. Antworten in anderen Niveaus bleiben gespeichert (eigene `data-state`-Schlüssel pro Niveau).

Vorteil: Wer mit Basis startet und schnell durch ist, kann hochwechseln. Wer bei Experte ins Schwimmen kommt, wechselt zurück — ohne sich „outen" zu müssen.

### 5. Niveau-Wahl wird persistiert

Das zuletzt gewählte Niveau wird im localStorage gespeichert (`onepager:<slug>:niveau`). Beim nächsten Aufruf: dort weitermachen, wo man zuletzt war.

### 6. Lehrkraft-Modus: alle drei Niveaus sichtbar

Mit `?solutions=1` oder `?all-niveaus=1` werden alle drei Niveau-Panes gleichzeitig angezeigt. So kann die Lehrkraft drucken oder einen Überblick haben.

```js
if (new URLSearchParams(location.search).get('all-niveaus') === '1') {
  document.querySelectorAll('.niveau-pane').forEach(p => p.hidden = false);
}
```

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja (am Anfang, gemeinsam für alle Niveaus) |
| **Niveau-Tabs** | **ja, profilspezifisch** |
| Aufgaben-Karten | ja, jeweils dreimal (pro Niveau) |
| Inhalts-Boxen (Tipp) | mehr in Basis-Pane, weniger in Experte-Pane |
| Selbst-Korrektur | ja, pro Niveau eigene `data-expected` |
| Lösungs-Hürde | ja, Standard |
| Quiz | nein |
| Canvas | je nach Fach |
| Fortschrittsbalken | bezogen auf das **gewählte Niveau**, nicht alle drei |
| Save-Status | ja |
| Toast | ja |
| JSON-Export | ja, exportiert alle Niveau-Eingaben + zuletzt gewähltes Niveau |
| Reset | ja, löscht alle drei Niveaus auf einmal mit klarem Hinweis |

## Aufgaben-Pattern (typisch)

```html
<div class="box lernziel">
  <span class="box-title">✦ Was du heute lernst</span>
  Du kannst Brüche addieren und subtrahieren.
</div>

<nav class="niveau-tabs" role="tablist">
  <button role="tab" aria-selected="false" data-niveau="basis">★ Basis</button>
  <button role="tab" aria-selected="true"  data-niveau="erweitert">★★ Erweitert</button>
  <button role="tab" aria-selected="false" data-niveau="experte">★★★ Experte</button>
</nav>

<div class="niveau-pane" data-niveau="basis" hidden>
  <article class="aufgabe" data-task-id="basis-1">
    <header class="aufgabe__header">
      <span class="aufgabe__nr">★ Aufgabe 1</span>
      <h3 class="aufgabe__titel">Berechne 1/4 + 2/4</h3>
    </header>
    <div class="aufgabe__body">
      <p class="hint">Tipp: Bei gleichem Nenner werden nur die Zähler addiert.</p>
      <input data-state="basis-1-a" data-expected-keywords="3/4">
      <span class="feedback" data-feedback-for="basis-1-a"></span>
    </div>
  </article>
</div>

<div class="niveau-pane" data-niveau="erweitert">
  <article class="aufgabe" data-task-id="erweitert-1">
    <header class="aufgabe__header">
      <span class="aufgabe__nr">★★ Aufgabe 1</span>
      <h3 class="aufgabe__titel">Berechne 1/3 + 1/4</h3>
    </header>
    <div class="aufgabe__body">
      <input data-state="erweitert-1-a" data-expected-keywords="7/12">
      <span class="feedback" data-feedback-for="erweitert-1-a"></span>
    </div>
  </article>
</div>

<div class="niveau-pane" data-niveau="experte" hidden>
  <article class="aufgabe" data-task-id="experte-1">
    <header class="aufgabe__header">
      <span class="aufgabe__nr">★★★ Aufgabe 1</span>
      <h3 class="aufgabe__titel">Für welche x gilt: x/6 + 1/4 = 5/12?</h3>
    </header>
    <div class="aufgabe__body">
      <input data-state="experte-1-a" data-expected-keywords="x=1,x = 1">
      <span class="feedback" data-feedback-for="experte-1-a"></span>
    </div>
  </article>
</div>
```

## Anti-Patterns

- **Drei verschiedene Themen pro Niveau** → keine Differenzierung, sondern drei Onepager in einem
- **Farb-Codierung Rot/Gelb/Grün** → stigmatisiert „die Roten"
- **Empfehlung an die Schüler:in, welches Niveau passt** → Schüler:in wählt selbst, das ist Teil der didaktischen Mündigkeit
- **Niveau-Wechsel blockieren** → nimmt Sicherheits-Netz
- **Quiz mit gemischten Niveaus** → die Differenzierung soll spürbar bleiben
- **Lange Theorie-Texte pro Niveau** → die Theorie ist gleich, nur die Aufgaben variieren

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn neuer Inhalt erarbeitet wird, kann eine Erarbeitungsseite auch differenzierte Übungs-Aufgaben enthalten
- [`profiles/loesungszettel.md`](loesungszettel.md) — Wenn das Buch differenzierte Aufgaben enthält, kann der Lösungszettel diese auf Niveau-Tabs spiegeln
