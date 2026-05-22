# Profil: Methoden-/Strategien-Onepager

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der eine **Lernmethode oder Strategie** erklärt — und sie direkt im Anschluss anwenden lässt. Die Schüler:innen lernen also nicht *Inhalte*, sondern *wie man lernt*. Beispiele: SQ3R für Lesetexte, die Mindmap-Methode, Karteikarten-System, Pomodoro-Technik, Strukturlegetechnik, Eselsbrücken-Bauen, „Think-Pair-Share", die Fishbone-Methode für Problemanalyse.

Charakteristisch: **Methodenkompetenz** ist das Lernziel, nicht Inhaltswissen.

## Typische Merkmale

- **Klassenstufe:** Sek I (späte) bis Sek II — Methodenkompetenz wird hier explizit gelehrt
- **Fachbereich:** fächerübergreifend — in „Methodentagen", in Klassenleiterstunden, oder eingebettet in ein Fach
- **Zeitumfang:** 30–60 Min für Erklärung + erste Anwendung
- **Ziel-Typ:** Methodenlernen, Meta-Kompetenz
- **Gerät:** Laptop oder Tablet

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0015](../adr/0015-inhalts-boxen.md) | **Sehr viele** Info-/Tipp-/Merke-Boxen, weil die Methode erklärt werden muss |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten für die Übungs-Anwendung |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur bei Bedarf, aber bei Methoden-Anwendungen oft offen |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md):** für eine Methode gibt es selten *die* Lösung — es geht um Vorgehen
- **Quiz:** möglich, um Methodenwissen abzufragen („Was sind die 5 Schritte von SQ3R?")
- **Canvas:** sehr nützlich für visuelle Methoden (Mindmap, Strukturlegetechnik, Fishbone)
- **Gating / Niveau-Tabs:** typischerweise nicht

## Spezifische didaktische Entscheidungen

### 1. Aufbau in drei Phasen

```
1. Methode kennenlernen      (Theorie, Beschreibung, Beispiel)
   ↓
2. Methode ausprobieren      (geführte Anwendung an einem Beispiel)
   ↓
3. Methode reflektieren      (Wann hilft mir das? Wo nicht?)
```

Diese Reihenfolge ist Teil der Profil-Identität.

### 2. Phase 1: Methode kennenlernen

Eine Mischung aus:
- **Merke-Box** mit der Methode in 3–5 Schritten
- Optional ein Beispiel-Video oder eine Grafik (SVG inline)
- **Info-Box** „Wofür eignet sich diese Methode?"

```html
<div class="box merke">
  <span class="box-title">📌 SQ3R — Die 5 Schritte</span>
  <ol>
    <li><strong>Survey</strong> — Text überfliegen, Struktur erkennen</li>
    <li><strong>Question</strong> — Fragen ans Material formulieren</li>
    <li><strong>Read</strong> — Sorgfältig lesen, Fragen im Hinterkopf</li>
    <li><strong>Recite</strong> — Mit eigenen Worten wiedergeben</li>
    <li><strong>Review</strong> — Wiederholen, vernetzen</li>
  </ol>
</div>

<div class="box info">
  <span class="box-title">ℹ️ Wofür diese Methode?</span>
  Besonders hilfreich bei <strong>Sachtexten</strong> in Schule und Studium —
  z. B. wenn du dich auf eine Klausur vorbereitest oder einen Wikipedia-Artikel
  durcharbeitest.
</div>
```

### 3. Phase 2: Methode ausprobieren

Schüler:innen wenden die Methode an einem **konkreten Beispiel** an. Pro Methoden-Schritt eine Aufgabe-Karte:

```html
<article class="aufgabe" data-task-id="sq3r-survey">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Schritt 1: Survey</span>
    <h3 class="aufgabe__titel">Überfliege den Beispieltext</h3>
  </header>
  <div class="aufgabe__body">
    <p>Wirf einen Blick auf den Beispieltext unten. Achte nur auf Überschriften, fettgedruckte Wörter und Bilder. (Max. 1 Minute.)</p>
    <textarea data-state="sq3r-survey-eindruck" rows="2"
      placeholder="Erster Eindruck — worum geht es?"></textarea>
  </div>
</article>

<article class="aufgabe" data-task-id="sq3r-question">
  …
</article>
```

Der **Beispieltext** kann inline im Onepager stehen (wie bei [Lesetext](lesetext.md)) oder ein externer Link sein.

### 4. Phase 3: Methode reflektieren

Am Ende eine **Reflexions-Sektion**:

| Frage | Eingabetyp |
|---|---|
| Wie fandest du die Methode? | Smiley-Skala |
| Wann würdest du sie wieder anwenden? | Textarea |
| Wann würdest du sie NICHT anwenden? | Textarea |
| Was hat dir gefehlt / war unklar? | Textarea |

Dieses Phase-3-Element ist wichtig: **Methodenlernen ohne Reflexion** bleibt oberflächlich.

### 5. Methoden-Karte als Referenz

Ergänzend zum Lernpfad gibt es eine **kompakte „Methoden-Karte"** zum Speichern — die Schüler:innen können sie später als Spickzettel für die Anwendung im Alltag nutzen:

```html
<div class="box merke methoden-karte">
  <span class="box-title">📇 Methoden-Karte: SQ3R</span>
  <ol>
    <li>S — Survey: Überfliegen</li>
    <li>Q — Question: Fragen formulieren</li>
    <li>R — Read: Lesen</li>
    <li>R — Recite: Wiedergeben</li>
    <li>R — Review: Wiederholen</li>
  </ol>
  <p class="hint">Drucke diese Karte mit „PDF speichern" und nutze sie beim Lernen!</p>
</div>
```

Hinweis am Ende, dass per PDF-Export eine handliche Druckversion entsteht.

### 6. Optional: Mehrere Methoden auf einem Onepager

Eine „Methodensammlung" kann mehrere Methoden enthalten — dann ist jede Methode in einer eigenen `<details>`-Sektion eingeklappt, vergleichbar mit dem [Lektüre](lektuere.md)-Profil.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box (Methodenkompetenz) | ja |
| Aufgaben-Karten (Übungs-Anwendung) | ja |
| Inhalts-Boxen (Merke, Info, Tipp) | **ja, viele** |
| Selbst-Korrektur | optional |
| Lösungs-Hürde | optional, weniger zentral |
| Quiz | optional (Methodenwissen abfragen) |
| Canvas | bei visuellen Methoden (Mindmap, Strukturlegetechnik) |
| Fortschrittsbalken | optional |
| Save-Status | ja |
| Toast | ja |
| JSON/HTML-Export | ja |
| **PDF-Export-Snippet** | **ja, für die druckbare Methoden-Karte** |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

Siehe oben, Phase 1 / 2 / 3. Hier eine kompakte Vorstellung des Strukturschemas:

```html
<header class="page-header">
  <span class="ue-label">Methodentag · Klasse 9</span>
  <h1>Methode: SQ3R — Sachtexte effizient verstehen</h1>
</header>

<div class="content">
  <div class="box lernziel">
    <span class="box-title">✦ Was du lernst</span>
    Die SQ3R-Methode kennen und auf einen Sachtext anwenden können.
  </div>

  <h2>1. Die Methode kennenlernen</h2>
  <div class="box merke">…SQ3R in 5 Schritten…</div>
  <div class="box info">…wofür hilfreich…</div>

  <h2>2. Methode ausprobieren</h2>
  <!-- Beispieltext + 5 Aufgaben (eine pro Methodenschritt) -->

  <h2>3. Reflektieren</h2>
  <!-- Smiley-Skala + offene Fragen -->

  <h2>Methoden-Karte zum Mitnehmen</h2>
  <div class="box merke methoden-karte">…</div>
</div>
```

## Anti-Patterns

- **Nur Theorie, keine Anwendung** → die Methode bleibt abstrakt
- **Anwendung ohne Reflexion** → keine Transfer-Wirkung
- **Methode komplex und Onepager überladen** → besser pro Methode ein eigener Onepager
- **Quiz statt Anwendung** → testet Methodenwissen, nicht Methodenkönnen
- **Keine Methoden-Karte am Ende** → die Schüler:innen haben nichts „Greifbares" zum Mitnehmen

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn die Methode Teil einer größeren Unterrichtseinheit ist
- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Wenn der Fokus auf Reflexion über die eigene Lernpraxis liegt
- [`profiles/kompetenzraster.md`](kompetenzraster.md) — Für Methodenkompetenz-Selbst-Einschätzung („Welche Methoden kann ich anwenden?")
