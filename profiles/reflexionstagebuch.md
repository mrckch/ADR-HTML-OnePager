# Profil: Reflexionstagebuch / Lerntagebuch

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **Lerntagebuch** — am Ende einer Stunde, einer Einheit oder eines Projekts. Die Schüler:innen halten schriftlich fest, was sie gelernt haben, was schwer war, was sie noch brauchen. Es geht nicht um „richtig oder falsch", sondern um **Metakognition**: das eigene Lernen sichtbar machen und reflektieren.

## Typische Merkmale

- **Klassenstufe:** alle, je nach Sprach- und Schreibfähigkeit angepasst
- **Fachbereich:** alle Fächer
- **Zeitumfang:** 10–20 Minuten am Ende einer Stunde/Einheit, oder als wiederkehrendes Element (wöchentlich, projektbegleitend)
- **Ziel-Typ:** Reflexion, Metakognition, Selbst-Beobachtung
- **Gerät:** Laptop oder Tablet (auch Smartphone möglich — kurze Texte)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0015](../adr/0015-inhalts-boxen.md) | `.lernziel` am Anfang erinnert an die Lernziele der Einheit |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Jede Reflexionsfrage in eigener Karte (`.aufgabe`-Klasse passt strukturell, auch wenn es nicht „Aufgaben" sind) |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | Persistenz **kritisch** — verlorene Reflexionen sind nicht reproduzierbar |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save-Status muss zuverlässig sein und prominent |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** irrelevant — es gibt keine Lösungen
- **[ADR-0011](../adr/0011-selbst-korrektur.md) (Selbst-Korrektur):** irrelevant — keine richtigen/falschen Antworten
- **[ADR-0013](../adr/0013-quiz-hardening.md) (Quiz):** nein
- **[ADR-0012](../adr/0012-gamification.md) (Fortschrittsbalken):** nein — würde unter Druck setzen, Reflexion soll freiwillig wirken

## Spezifische didaktische Entscheidungen

### 1. Keine „richtig/falsch"-Mechanik überhaupt

Es gibt keine `data-expected`, keine Lösungs-Hürde, kein Quiz, kein Reveal-Button. Jede Eingabe ist akzeptiert. Eine wertfreie Atmosphäre ist Voraussetzung für ehrliche Selbst-Reflexion.

### 2. Drei Frage-Typen sind die Standard-Mischung

| Typ | Beispiel | UI-Element |
|---|---|---|
| **Offene Reflexionsfrage** | „Was war heute am schwersten?" | `<textarea>` |
| **Skalen-Selbsteinschätzung** | „Wie sicher fühlst du dich beim Thema X?" | Skala 1–5 (Sterne) oder Smileys (😞 / 😐 / 🙂 / 😀) |
| **Multiple-Choice Selbst-Auswahl** | „Welche dieser Strategien hast du heute verwendet?" | Checkboxes (mehrere möglich) |

Mischung wirkt — reine Textareas ermüden, reine Skalen sind oberflächlich.

### 3. Smileys / Skalen als Skala-Eingabe

Statt klassischer Radio-Buttons werden Smileys als Skalen-Element verwendet:

```html
<div class="skala" role="radiogroup" aria-label="Wie sicher fühlst du dich?">
  <label><input type="radio" name="sicher-x" data-state="sicher-x" value="1"> 😞</label>
  <label><input type="radio" name="sicher-x" data-state="sicher-x" value="2"> 😐</label>
  <label><input type="radio" name="sicher-x" data-state="sicher-x" value="3"> 🙂</label>
  <label><input type="radio" name="sicher-x" data-state="sicher-x" value="4"> 😀</label>
</div>
```

CSS-Snippet:
```css
.skala { display: flex; gap: var(--space-3); margin: var(--space-2) 0; }
.skala label { display: flex; flex-direction: column; align-items: center;
               font-size: 28px; cursor: pointer;
               padding: var(--space-2); border-radius: var(--radius-md); }
.skala label:has(input:checked) { background: var(--bg-info); }
.skala input { position: absolute; opacity: 0; }
```

### 4. Datum-Header pro Eintrag

Bei wiederkehrender Nutzung („jeden Freitag schreibst du ins Lerntagebuch") bekommt jeder Eintrag ein Datum-Feld, das automatisch heute vor-eingetragen wird:

```html
<input type="date" id="eintrag-datum" data-state="eintrag-datum">
```

Beim ersten Laden: wenn leer, mit `new Date().toISOString().slice(0,10)` vorbefüllen.

### 5. Privatsphäre-Hinweis

Reflexion ist sensibel. Im Topbar oder einer dezenten Info-Box ein Hinweis:

> Deine Einträge bleiben lokal auf deinem Gerät. Sie werden nicht automatisch an die Lehrkraft geschickt. Wenn du möchtest, kannst du sie exportieren und teilen — aber nur, wenn du das aktiv tust.

### 6. Keine Auswertungs-Quittung über Toast

Toast „Stimmt!" oder ähnliches wäre fehl am Platz. Save-Toasts bleiben (gespeichert.), aber keine Bewertungs-Sprache.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja (am Anfang als Erinnerung) |
| Aufgaben-Karten | ja (pro Reflexionsfrage) |
| Inhalts-Boxen (Info, Tipp) | sparsam, höchstens 1× Info „So funktioniert das Tagebuch" |
| Selbst-Korrektur | **nein** |
| Lösungs-Hürde | **nein** |
| Quiz | **nein** |
| Canvas-Stift-Eingabe | optional (für skizzierte Reflexionen, z. B. „Stimmungs-Wetter") |
| Fortschrittsbalken | **nein** (würde unter Druck setzen) |
| Skalen / Smileys | **ja, Hauptmechanik neben Textareas** |
| Save-Status-Indikator | **ja, prominent** |
| Toast-Notifications | ja (nur für Save/Export/Reset) |
| JSON-Export/Import | ja — Schüler:in kann Tagebuch über Halbjahre hinweg mitnehmen |
| Reset-Dialog | ja, mit besonderer Warnung („Du löschst deine gesamte Reflexion!") |

## Aufgaben-Pattern (typisch)

```html
<article class="aufgabe" data-task-id="ref-1">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Reflexion 1</span>
    <h3 class="aufgabe__titel">Was war heute am schwersten?</h3>
  </header>
  <div class="aufgabe__body">
    <textarea data-state="ref-1-text" rows="4"
              placeholder="Heute war für mich am schwersten …"></textarea>
  </div>
</article>

<article class="aufgabe" data-task-id="ref-2">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Reflexion 2</span>
    <h3 class="aufgabe__titel">Wie sicher fühlst du dich beim Thema "Bruchrechnen"?</h3>
  </header>
  <div class="aufgabe__body">
    <div class="skala" role="radiogroup" aria-label="Sicherheit">
      <label><input type="radio" name="sicher-bruch" data-state="sicher-bruch" value="1"> 😞</label>
      <label><input type="radio" name="sicher-bruch" data-state="sicher-bruch" value="2"> 😐</label>
      <label><input type="radio" name="sicher-bruch" data-state="sicher-bruch" value="3"> 🙂</label>
      <label><input type="radio" name="sicher-bruch" data-state="sicher-bruch" value="4"> 😀</label>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Quiz, Lösungen, „richtig/falsch"-Mechanik** → zerstört die wertfreie Atmosphäre
- **Pflichtfelder oder Mindestlänge** → Reflexion soll freiwillig sein
- **Fortschrittsbalken** → vermittelt „du musst noch X reflektieren!"
- **Bunte Gamification** → unpassend, Reflexion ist ein ernster Moment
- **Direkte Übermittlung an Lehrkraft** → Datenschutz, Vertrauen. Wenn Lehrkraft eingebunden werden soll: bewusst per Export

## Verwandte Profile

- [`profiles/kompetenzraster.md`](kompetenzraster.md) — strukturierter, mit „Ich kann …"-Aussagen statt offener Fragen
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — kann eine „Reflexion am Ende"-Sektion enthalten, aber als ganzes Profil ist Reflexionstagebuch geeigneter, wenn Reflexion der Hauptzweck ist
