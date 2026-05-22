# Profil: Recherche-Auftrag

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der eine **Rechercheaufgabe** strukturiert: Schüler:innen erhalten eine Forschungsfrage, sammeln Quellen, prüfen sie auf Glaubwürdigkeit, notieren Erkenntnisse und schreiben am Ende ein Fazit oder Ergebnis.

Hauptzweck: **methodisches wissenschaftliches Arbeiten** üben — von „eine Frage formulieren" bis „eine Antwort mit Quellen begründen".

## Typische Merkmale

- **Klassenstufe:** Sek I (späte) bis Sek II
- **Fachbereich:** Gesellschaftswissenschaften (Geschichte, Politik, Geographie), Religion, Deutsch (Erörterungen), aber auch NaWi
- **Zeitumfang:** mehrere Stunden bis Tage, oft als Mini-Projekt
- **Ziel-Typ:** Methodenkompetenz, eigenständiges Arbeiten, Quellenkritik
- **Gerät:** Laptop oder Tablet (Recherche im Browser parallel)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0015](../adr/0015-inhalts-boxen.md) | Info-/Tipp-Boxen für methodische Anleitung (z. B. „So prüfst du eine Quelle") |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Karten für die einzelnen Recherche-Schritte |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | **Persistenz kritisch** — Recherche dauert lange und kann unterbrochen werden |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | HTML-Export für Abgabe, da Schüler:in ihre Sammlung mitnimmt |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) + [ADR-0011](../adr/0011-selbst-korrektur.md):** wenig relevant — es gibt selten „die richtige" Antwort bei Recherche
- **Quiz, Canvas:** typischerweise nicht
- **Gamification:** Fortschrittsbalken ja, sonst zurückhaltend

## Spezifische didaktische Entscheidungen

### 1. Klare Recherche-Struktur in fünf Schritten

| Schritt | Inhalt |
|---|---|
| **1. Forschungsfrage** | Was will ich herausfinden? (vorgegeben oder eigene) |
| **2. Quellen sammeln** | Mind. 3–5 Quellen mit URL, Titel, Datum, Glaubwürdigkeits-Einschätzung |
| **3. Notizen pro Quelle** | Was steht in dieser Quelle? Welche Antwort gibt sie auf meine Frage? |
| **4. Synthese** | Was haben die Quellen gemeinsam? Wo widersprechen sie sich? |
| **5. Ergebnis / Fazit** | Meine Antwort auf die Forschungsfrage, mit Quellenbelegen |

Diese Reihenfolge ist Teil der Profil-Identität — sie spiegelt wissenschaftliches Arbeiten.

### 2. Quellen-Eingabe-Pattern

Pro Quelle eine Karte:

```html
<article class="aufgabe quelle" data-task-id="quelle-1">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Quelle 1</span>
    <h3 class="aufgabe__titel">Eintrag</h3>
  </header>
  <div class="aufgabe__body">
    <div class="field">
      <label>Titel</label>
      <input type="text" data-state="q1-titel">
    </div>
    <div class="field">
      <label>URL</label>
      <input type="url" data-state="q1-url" placeholder="https://…">
    </div>
    <div class="field">
      <label>Veröffentlicht am / Autor:in</label>
      <input type="text" data-state="q1-meta">
    </div>
    <div class="field">
      <label>Glaubwürdigkeit (Begründung)</label>
      <textarea data-state="q1-credibility" rows="2"
        placeholder="Warum hältst du diese Quelle für glaubwürdig? Wer steht dahinter?"></textarea>
    </div>
    <div class="field">
      <label>Wichtigste Aussage zur Forschungsfrage</label>
      <textarea data-state="q1-aussage" rows="3"></textarea>
    </div>
  </div>
</article>
```

### 3. Quellenkritik-Tipps in einer eigenen Box

Direkt vor den Quellen-Karten:

```html
<div class="box tipp">
  <span class="box-title">💡 So prüfst du eine Quelle</span>
  <ul>
    <li><strong>Wer:</strong> Wer steht hinter der Seite/dem Artikel? Impressum?</li>
    <li><strong>Wann:</strong> Wann wurde es veröffentlicht? Ist die Info aktuell?</li>
    <li><strong>Warum:</strong> Welches Ziel verfolgt die Quelle? Werbung, Information, Meinungsmache?</li>
    <li><strong>Wie:</strong> Werden Quellen genannt? Belege geliefert?</li>
  </ul>
</div>
```

### 4. URL als klickbarer Link rendern

Eingegebene URLs werden live als Link unter dem Feld angezeigt, damit Schüler:innen sie direkt prüfen können:

```js
document.querySelectorAll('input[type="url"]').forEach(input => {
  const link = document.createElement('a');
  link.className = 'url-preview';
  link.target = '_blank';
  link.rel = 'noopener';
  input.after(link);
  function update() {
    if (input.value) {
      link.href = input.value;
      link.textContent = '→ ' + input.value;
      link.hidden = false;
    } else { link.hidden = true; }
  }
  input.addEventListener('input', update);
  update();
});
```

### 5. Synthese-Sektion mit Vergleichs-Tabelle

In der Synthese-Phase eine Tabellen-Vorlage für den **Vergleich der Quellen**:

```html
<div class="field">
  <label>Vergleich der Quellen</label>
  <table class="quellen-vergleich">
    <thead>
      <tr><th>Aspekt</th><th>Quelle 1</th><th>Quelle 2</th><th>Quelle 3</th></tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Antwort auf die Frage</th>
        <td><textarea data-state="vergleich-1-1" rows="2"></textarea></td>
        <td><textarea data-state="vergleich-1-2" rows="2"></textarea></td>
        <td><textarea data-state="vergleich-1-3" rows="2"></textarea></td>
      </tr>
      <tr>
        <th scope="row">Stimmt überein mit / widerspricht</th>
        <td><textarea data-state="vergleich-2-1" rows="2"></textarea></td>
        …
      </tr>
    </tbody>
  </table>
</div>
```

### 6. Fazit mit Quellen-Pflicht-Hinweis

Im Fazit-Feld eine Hinweis-Box: „Belege deine Antwort mit mindestens zwei Quellen aus deiner Sammlung."

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja (mit Forschungsfrage) |
| Aufgaben-Karten (Quellen-Karten) | **ja, Hauptelement** |
| Inhalts-Boxen (Tipps zur Quellenkritik) | **ja** |
| Selbst-Korrektur | nein (keine richtige Antwort) |
| Lösungs-Hürde | nein |
| Quiz | nein |
| Canvas | optional |
| Fortschrittsbalken | ja |
| Save-Status | **ja, prominent** |
| Toast | ja |
| JSON-Export | ja |
| **HTML-Export** | ja, primärer Abgabeweg |
| Reset-Dialog | ja |

## Anti-Patterns

- **Vorgegebene „richtige" Antwort** → widerspricht dem Recherche-Charakter
- **Quiz am Ende** → Recherche ist kein Multiple-Choice-Thema
- **Zu wenige Quellen** verlangen (1–2) → keine echte Synthese möglich
- **Keine Quellenkritik-Aufforderung** → Schüler:innen kopieren von der ersten Wikipedia-Seite
- **Kein Datums-/Autoren-Feld** → Quellenangaben werden lückenhaft

## Verwandte Profile

- [`profiles/lesetext.md`](lesetext.md) — Wenn die Quellen schon vorgegeben sind und nur ein Text analysiert wird
- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn eher reflektierender Lern-Bezug (z. B. ethische Position) als Recherche
- [`profiles/lektuere.md`](lektuere.md) — Wenn eine längere Quelle (Buch, Aufsatz) als Hauptquelle dient
