# Profil: Hausaufgaben-Auftrag

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der **strukturierte Hausaufgaben** auf einem Blatt bündelt. Schüler:innen bekommen den Link mit nach Hause (oder erhalten ihn schon in der Stunde) und bearbeiten die Aufgaben zu Hause. Wenn sie wieder online sind oder am nächsten Tag, können sie ihre Bearbeitung in der Schule fortsetzen oder abgeben.

Mischform zwischen **Lösungszettel** (Aufgaben-Hilfen, aber nicht alle Lösungen sofort) und **digitalem Arbeitsheft** (Aufgaben sind vollständig im Onepager).

## Typische Merkmale

- **Klassenstufe:** alle
- **Fachbereich:** alle
- **Zeitumfang:** 20–60 Min Bearbeitungszeit zu Hause
- **Ziel-Typ:** Übung, Vertiefung, Anwendung
- **Gerät:** Laptop oder Tablet zu Hause, später ggf. in der Schule

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Klare Aufgaben-Karten — die Hauptstruktur |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | Persistenz **wichtig**, weil zwischen mehreren Sessions (Zuhause → Schule) gearbeitet wird |
| [ADR-0010](../adr/0010-loesungs-huerde.md) | Lösungs-Hürde — Schüler:innen sollen erst denken, dann gucken |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur, damit Schüler:in selbst merkt, ob die Lösung stimmt |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | HTML-Export ist sinnvoller Abgabeweg (Lehrkraft öffnet Datei und sieht die Bearbeitung) |

## Core-ADRs abweichend oder weniger relevant

- **Quiz, Canvas, Gating, Niveau-Tabs:** je nach Aufgabe optional, aber nicht zentral
- **Lernziele:** kurz und knapp — Hausaufgaben haben meist ein eng umrissenes Ziel

## Spezifische didaktische Entscheidungen

### 1. Meta-Felder am Anfang

Zusätzlich zu Name/Klasse/Datum:
- **Aufgabe gestellt am:** (von Lehrkraft im Onepager vorgegeben oder Text)
- **Abzugeben bis:** (sichtbarer Termin)
- **Geschätzte Bearbeitungszeit:** „ca. 30 Min" im Header

```html
<div class="meta-row">
  <div class="meta-field">…Name…</div>
  <div class="meta-field">…Klasse…</div>
  <div class="meta-field"><label>Abgabe bis</label><span>Fr., 24.05.2026</span></div>
</div>
```

### 2. Übergabe-Modus bewusst auswählen

Drei sinnvolle Workflows — eine sollte die Lehrkraft pro Onepager kommunizieren:

| Übergabe-Modus | Schüler-Aktion | Lehrer-Aktion |
|---|---|---|
| **HTML-Export** | „HTML mit Antworten" speichern → per Mail/Teams an Lehrkraft | Datei öffnen, alle Eingaben sichtbar |
| **JSON-Export** | „JSON" speichern → in der Stunde laden | In der Stunde am Schüler-Gerät öffnen |
| **Mündlich/Heft** | Onepager nur als Hilfe, eigentliche Lösung ins Heft | Heft abgeben wie immer |

Empfehlung: HTML-Export, weil am bequemsten. Der Onepager kann eine **Hinweis-Box** am Ende enthalten, die den gewünschten Übergabeweg dokumentiert.

### 3. Lösungs-Hürde: Standard, aber etwas strenger

Anders als beim Lösungszettel-Profil ist hier der **Schüler ohne Lehrkraft-Aufsicht** unterwegs. Empfehlung:

- Tipp 1 sofort verfügbar
- Tipp 2 nach Klick
- Lösung NUR nach Eingabe einer Antwort verfügbar (Standard-Modal aus ADR-0010 reicht aus — Cipher ist Overkill)

### 4. Kein Quiz am Ende

Ein Quiz am Ende einer Hausaufgabe gibt der/dem Schüler:in das Gefühl, „bewertet" zu werden. Hausaufgabe = Übung, nicht Test.

Wenn Selbst-Test gewünscht: **Kompetenzraster** am Ende (zwei oder drei „Ich kann …"-Zeilen mit Smiley-Skala) ist sanfter als Quiz.

### 5. Abgabe-Hinweis prominent

Am Ende des Onepagers eine **deutliche Box**:

```html
<div class="box info" style="margin-top: var(--space-8)">
  <span class="box-title">📤 So gibst du die Hausaufgabe ab</span>
  <ol>
    <li>Klicke oben rechts auf <strong>„📎 HTML"</strong></li>
    <li>Sende die heruntergeladene Datei per Mail an: …</li>
    <li>Abgabe-Frist: <strong>Fr., 24.05.2026 — 18 Uhr</strong></li>
  </ol>
</div>
```

### 6. „Wann hast du wie lange gebraucht?"-Frage am Ende

Eine kurze Reflexionsfrage am Schluss, freiwillig:

> Wie lange hast du tatsächlich für diese Hausaufgabe gebraucht? Welche Aufgabe war am schwersten?

Hilft der Lehrkraft, das Aufgabenpensum für die nächste Hausaufgabe einzuschätzen — und der/dem Schüler:in, das eigene Lerntempo zu reflektieren.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja, knapp |
| Aufgaben-Karten | **ja, klar nummeriert** |
| Inhalts-Boxen | sparsam |
| Selbst-Korrektur | ja |
| Lösungs-Hürde (Tipp + Lösung) | ja, Standard |
| Quiz | nein |
| Canvas | optional |
| Fortschrittsbalken | ja (Schüler:in sieht, wie viel noch zu tun ist) |
| Save-Status | ja (kritisch — Bearbeitung über mehrere Sessions) |
| Toast | ja |
| **JSON-Export** | ja |
| **HTML-Export** | **ja, primärer Abgabeweg** |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathe · Klasse 7 · Hausaufgabe zu UE 4</span>
    <h1>Bruchrechnung üben</h1>
    <div class="meta-row">
      <div class="meta-field"><label>Name</label><input data-state="meta-name"></div>
      <div class="meta-field"><label>Abgabe bis</label><span>Fr., 24.05.</span></div>
      <div class="meta-field"><label>Dauer</label><span>ca. 30 Min</span></div>
    </div>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Ziel</span>
      Brüche mit gleichen und ungleichen Nennern addieren.
    </div>

    <article class="aufgabe" data-task-id="ha-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Aufgabe 1</span>
        <h3 class="aufgabe__titel">Berechne 1/4 + 2/4</h3>
      </header>
      <div class="aufgabe__body">
        <input data-state="ha-1-a"
               data-expected-keywords="3/4">
        <span class="feedback" data-feedback-for="ha-1-a"></span>
        <div class="reveal-actions">
          <button class="reveal-btn reveal-btn--hint" data-task-id="ha-1">💡 Tipp</button>
          <button class="reveal-btn reveal-btn--solution" data-task-id="ha-1">🔍 Lösung</button>
        </div>
        <div class="hint-content" data-task-id="ha-1" hidden>
          Bei gleichem Nenner addierst du nur die Zähler.
        </div>
        <div class="solution-content" data-task-id="ha-1" hidden>
          1/4 + 2/4 = (1+2)/4 = <strong>3/4</strong>
        </div>
      </div>
    </article>

    <!-- weitere Aufgaben … -->

    <div class="box info" style="margin-top: var(--space-8)">
      <span class="box-title">📤 So gibst du die HA ab</span>
      <ol>
        <li>Klicke oben rechts auf <strong>„📎 HTML"</strong></li>
        <li>Schick die Datei an deine Lehrkraft</li>
      </ol>
    </div>

    <div class="field">
      <label for="reflexion">Wie lange hast du wirklich gebraucht? Was war schwer? (optional)</label>
      <textarea id="reflexion" data-state="reflexion" rows="2"></textarea>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Quiz mit Note am Ende** → Hausaufgabe ist keine Prüfung
- **Lösungen sofort sichtbar** → keine Übung mehr, nur Abschreiben
- **Aufgaben ohne Hilfen** → Schüler:in ohne Aufsicht steht alleine da
- **Zu viele Aufgaben** (> 5–6) → die geschätzte Bearbeitungszeit von 30 Min wird gesprengt
- **HTML-Export ohne Hinweis-Box** → Schüler:innen finden den Abgabeweg nicht
- **Kein Lernziel** → Schüler:in weiß nicht, worauf es ankommt

## Verwandte Profile

- [`profiles/loesungszettel.md`](loesungszettel.md) — Wenn Aufgaben aus dem Buch kommen und nur die Hilfen/Lösungen im Onepager liegen
- [`profiles/digitales-arbeitsheft.md`](digitales-arbeitsheft.md) — Wenn die Hausaufgabe Stift-Eingabe braucht (Konstruktionen, Skizzen)
- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn die Hausaufgabe rein reflektierend ist
