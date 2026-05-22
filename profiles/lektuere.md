# Profil: Lektüre-/Buchtagebuch

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **Begleiter zu einem ganzen Buch** — einem Roman, einer längeren Erzählung, einem Sachbuch oder einer Lektüre, die über mehrere Wochen im Unterricht behandelt wird. Schüler:innen dokumentieren ihre Lese-Erfahrung **kapitelweise**: Zusammenfassung, Zitate, Charakteranalysen, eigene Gedanken.

Im Unterschied zum **Lesetext**-Profil (das einen einzelnen kurzen Text analysiert) begleitet dieses Profil eine **lange, kontinuierliche Lese-Erfahrung**.

## Typische Merkmale

- **Klassenstufe:** Sek I (späte) bis Sek II
- **Fachbereich:** Deutsch (primär), Englisch, Französisch (fremdsprachliche Lektüre), gelegentlich Geschichte/Religion
- **Zeitumfang:** **Wochen bis Monate** — wiederkehrender Einsatz, kapitelweise Eintrag
- **Ziel-Typ:** Begleitung, Reflexion, Vorbereitung Erörterung/Klausur
- **Gerät:** Laptop, Tablet — wird über lange Zeit genutzt

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | **Persistenz absolut kritisch** — wochenlange Arbeit darf nicht verloren gehen |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save-Status besonders prominent |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Karten pro Kapitel — Kapitel ist die Struktur-Einheit |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | HTML-Export als Sicherung empfohlen alle paar Wochen |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) + [ADR-0011](../adr/0011-selbst-korrektur.md):** wenig relevant — Lektüre ist offenes, interpretatives Arbeiten
- **Quiz, Canvas, Gating, Niveau-Tabs:** typischerweise nicht

## Spezifische didaktische Entscheidungen

### 1. Buch-Header am Anfang

Anders als bei einem stundenbasierten Onepager: hier hat der Onepager einen klaren **Buch-Bezug**, der vorne dauerhaft sichtbar bleibt:

```html
<header class="page-header">
  <span class="ue-label">Deutsch · Klasse 10 · Lektüre</span>
  <h1>Friedrich Dürrenmatt, „Der Besuch der alten Dame"</h1>
  <p class="buch-meta">
    Drama (1956) · Suhrkamp Verlag · 144 Seiten
  </p>
</header>
```

### 2. Sektion pro Kapitel / Akt / Teil

Statt einer flachen Aufgabenliste: **eine Sektion pro Strukturelement** des Buches.

```html
<section data-kapitel="1">
  <h2>1. Akt: Die Ankunft</h2>
  … Fragen, Karten, Reflexionen …
</section>

<section data-kapitel="2">
  <h2>2. Akt: Das Angebot</h2>
  …
</section>
```

Jede Sektion kann eingeklappt werden, damit der Onepager nicht zu lang wirkt:

```html
<details class="kapitel" open>
  <summary><h2>1. Akt: Die Ankunft</h2></summary>
  … Inhalt …
</details>
```

`<details>` ist hier OK (anders als bei Lösungen), weil es um **Übersichtlichkeit** geht, nicht um Anti-Spoiler.

### 3. Wiederkehrende Frage-Typen pro Kapitel

Pro Kapitel die immer gleichen Sektionen — wirkt strukturierend:

| Sektion | Inhalt |
|---|---|
| **Zusammenfassung** (2–3 Sätze) | Was passiert in diesem Kapitel? |
| **Wichtige Zitate** (Zitat-Helper aus Lesetext-Profil) | 1–3 Zitate mit Seitenangabe und Erklärung |
| **Charakter-Entwicklung** | Wie verändern sich die Figuren? |
| **Meine Gedanken** | Was hat dich beeindruckt, irritiert, gestört? |
| **Offene Fragen** | Was möchtest du im Unterricht besprechen? |

Die Lehrkraft entscheidet, welche dieser Sektionen pro Lektüre gewünscht sind.

### 4. Übergreifende Sektionen am Ende

Nach den Kapiteln gibt es **buchübergreifende Sektionen**:

- **Figurenverzeichnis** — Tabelle mit allen wichtigen Figuren
- **Themen und Motive** — wiederkehrende Motive, die durch das Buch ziehen
- **Aufbau** — Spannungskurve, Höhepunkt, Wendepunkte
- **Mein Fazit** — eine Seite Reflexion über das ganze Buch
- **Bewertung** — Sterne, Smiley, freier Kommentar

### 5. Datums-Stempel pro Eintrag

Da die Lektüre über Wochen geht, lohnt sich ein Datum-Feld pro Kapitel-Sektion:

```html
<input type="date" data-state="k1-datum">
<small class="hint">Wann hast du das Kapitel gelesen?</small>
```

Beim Wieder-Reinkommen sieht die Schüler:in, wann sie zuletzt aktiv war.

### 6. HTML-Export-Reminder

Da die Daten über Wochen wachsen, sollte die Schüler:in regelmäßig sichern. Eine Hinweis-Box am Anfang oder Ende:

```html
<div class="box tipp">
  <span class="box-title">💡 Regelmäßig sichern</span>
  Klicke alle paar Wochen oben rechts auf „📎 HTML" und speichere die Datei.
  So gehst du auf Nummer sicher, falls dein Browser den Speicher löscht.
</div>
```

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Buch-Meta-Header | ja (Titel, Autor, Form, Verlag, Seitenzahl) |
| Kapitel-Sektionen | **ja, Hauptstruktur** |
| Aufgaben-Karten pro Kapitel-Sektion | ja |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | nein |
| Lösungs-Hürde | nein |
| Quiz | nein |
| Canvas | optional (z. B. Skizzen zur Figurenkonstellation) |
| Fortschrittsbalken | optional (kapitelweise) |
| Save-Status | **ja, prominent** |
| Toast | ja |
| JSON-Export | ja |
| **HTML-Export** | **ja, mehrfach im Verlauf** |
| Reset-Dialog | ja, mit **besonders starker Warnung** |

## Aufgaben-Pattern (typisch)

```html
<header class="page-header">
  <span class="ue-label">Deutsch · Klasse 10 · Lektüre</span>
  <h1>Friedrich Dürrenmatt, „Der Besuch der alten Dame"</h1>
</header>

<div class="content">
  <div class="box tipp">
    <span class="box-title">💡 So nutzt du dieses Lese-Tagebuch</span>
    <ul>
      <li>Trage nach jedem Akt deine Gedanken ein</li>
      <li>Speichere regelmäßig (HTML-Export) — die Lektüre dauert mehrere Wochen</li>
      <li>Nutze die Notizen für die Erörterung/Klausur am Ende</li>
    </ul>
  </div>

  <details class="kapitel" open>
    <summary><h2>1. Akt: Die Ankunft</h2></summary>

    <article class="aufgabe" data-task-id="k1-zusammenfassung">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Zusammenfassung</span>
        <h3 class="aufgabe__titel">Was passiert im 1. Akt?</h3>
      </header>
      <div class="aufgabe__body">
        <textarea data-state="k1-zusammenfassung-text" rows="3"></textarea>
      </div>
    </article>

    <article class="aufgabe" data-task-id="k1-zitate">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Zitate</span>
        <h3 class="aufgabe__titel">Wichtige Stellen mit Seitenangabe</h3>
      </header>
      <div class="aufgabe__body">
        <textarea data-state="k1-zitate" rows="4"
          placeholder='"Zitat..." (S. 12) — Erklärung: ...'></textarea>
      </div>
    </article>

    <article class="aufgabe" data-task-id="k1-gedanken">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Reflexion</span>
        <h3 class="aufgabe__titel">Meine Gedanken</h3>
      </header>
      <div class="aufgabe__body">
        <textarea data-state="k1-gedanken" rows="4"
          placeholder="Was hat dich beim Lesen beschäftigt?"></textarea>
        <input type="date" data-state="k1-datum">
      </div>
    </article>
  </details>

  <details class="kapitel">
    <summary><h2>2. Akt: Das Angebot</h2></summary>
    …
  </details>

  <!-- … weitere Akte … -->

  <h2>Figuren</h2>
  <table class="figuren">
    <thead>
      <tr><th>Figur</th><th>Rolle</th><th>Mein Eindruck</th></tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Claire Zachanassian</th>
        <td><input data-state="figur-claire-rolle"></td>
        <td><textarea data-state="figur-claire-eindruck" rows="2"></textarea></td>
      </tr>
      <!-- … -->
    </tbody>
  </table>

  <h2>Mein Fazit</h2>
  <article class="aufgabe" data-task-id="fazit">
    <div class="aufgabe__body">
      <textarea data-state="fazit-text" rows="6"
        placeholder="Hat dir das Buch gefallen? Was hast du gelernt?"></textarea>
    </div>
  </article>
</div>
```

## Anti-Patterns

- **Wenige große Textfelder ohne Struktur** → Schüler:innen wissen nicht, was reingehört
- **Quiz / „richtig oder falsch"** → Lektüre ist interpretatives Arbeiten
- **Kein Hinweis auf regelmäßige HTML-Sicherung** → wochenlange Arbeit kann verloren gehen
- **Alle Kapitel auf einer Seite ohne `<details>`** → wird unübersichtlich nach 5–10 Kapiteln
- **Keine Figurenliste/Themen-Sektion** → die übergreifenden Aspekte fehlen

## Verwandte Profile

- [`profiles/lesetext.md`](lesetext.md) — Für einen einzelnen Text statt eines ganzen Buches
- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn der Schwerpunkt auf reiner Reflexion liegt, nicht auf Strukturarbeit
- [`profiles/recherche.md`](recherche.md) — Für rein sachorientierte Lektüre (z. B. einen Aufsatz für eine Erörterung)
