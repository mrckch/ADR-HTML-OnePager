# Profil: Klausur-/Klassenarbeitsvorbereitung

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein **Repetitorium-Onepager** vor einer Klassenarbeit oder Klausur. Schüler:innen üben gezielt die Themen, die in der Prüfung drankommen. Charakteristisch: Aufgaben sind mit **Themen-Tags** versehen, haben **Schwierigkeitsgrad-Marker** und sind so strukturiert, dass die/der Schüler:in schnell sehen kann, welche Themen bereits sicher sitzen und welche noch geübt werden müssen.

## Typische Merkmale

- **Klassenstufe:** Sek I, Sek II
- **Fachbereich:** alle, besonders Mathe, NaWi, Sprachen
- **Zeitumfang:** 60–120 Min Bearbeitungszeit, kann auch über mehrere Tage verteilt werden
- **Ziel-Typ:** Repetitorium, Diagnose, gezielte Wiederholung
- **Gerät:** Laptop oder Tablet

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Karten mit zusätzlichen **Themen-Tags** und **Schwierigkeitsgrad-Marker** im Header |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | **Zentral** — Schüler:in muss schnell wissen, ob die Antwort stimmt, ohne erst die Lösung aufzudecken |
| [ADR-0010](../adr/0010-loesungs-huerde.md) | Lösungs-Hürde mit Standard-Tipp + Lösung. Lösung kommt schneller als beim Lösungszettel — die Klausur ist nahe |
| [ADR-0012](../adr/0012-gamification.md) | **Fortschrittsbalken zentral** — visualisiert, wie viel schon geübt ist |

## Core-ADRs abweichend oder weniger relevant

- **Quiz (ADR-0013):** optional am Ende, als Selbst-Check, aber nicht zentral
- **Canvas:** nur bei Fächern mit Skizzen/Konstruktionen relevant
- **Lernziele:** **die Klausur-Themen** sind das Lernziel — Lernziel-Box listet die Themen auf

## Spezifische didaktische Entscheidungen

### 1. Themen-Tags pro Aufgabe

Jede Aufgabe-Karte trägt im Header ein oder mehrere Themen-Tags:

```html
<article class="aufgabe" data-task-id="bruch-add-1" data-thema="bruchrechnen">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">Aufgabe 1</span>
    <span class="thema-tag">Bruchrechnen</span>
    <span class="schwierigkeit" aria-label="mittel">★★</span>
    <h3 class="aufgabe__titel">Brüche addieren</h3>
  </header>
  …
</article>
```

CSS-Snippet für die Tags:

```css
.thema-tag {
  background: var(--bg-info);
  color: var(--blue);
  font-size: var(--fs-xs);
  font-weight: 600;
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.schwierigkeit { color: var(--gold); font-size: var(--fs-sm); letter-spacing: 0.05em; }
```

### 2. Themen-Filter

Eine Toolbar oben am Onepager filtert Aufgaben nach Thema:

```html
<div class="themen-filter" role="group">
  <button data-thema="all"        aria-pressed="true">Alle Themen</button>
  <button data-thema="bruchrechnen" aria-pressed="false">Bruchrechnen</button>
  <button data-thema="dezimal"      aria-pressed="false">Dezimalzahlen</button>
  <button data-thema="prozent"      aria-pressed="false">Prozentrechnung</button>
</div>
```

JS: Klick auf einen Filter blendet alle Aufgaben aus, deren `data-thema` nicht passt. Schüler:in kann gezielt ein Thema durchüben.

### 3. Schwierigkeitsgrad-Marker

Sternchen-Skala wie bei Niveau-Tabs, aber **per Aufgabe**:

| Sterne | Bedeutung |
|---|---|
| ★ | Basis — sollte sitzen |
| ★★ | Standard — Klausur-Niveau |
| ★★★ | Herausforderung — Note 1 |

### 4. Fortschritt **pro Thema** statt nur gesamt

Statt dem üblichen Fortschrittsbalken (alle Aufgaben gesamt) eine kleine Übersicht pro Thema:

```html
<div class="themen-fortschritt">
  <div class="thema-stat" data-thema="bruchrechnen">
    <span class="thema-name">Bruchrechnen</span>
    <span class="thema-bar"><span class="thema-fill" style="width: 60%"></span></span>
    <span class="thema-zahl">3 / 5</span>
  </div>
  …
</div>
```

JS aktualisiert die Bars laufend.

### 5. „Ich fühle mich sicher"-Markierung

Pro Themenbereich (nicht pro Aufgabe) ein Selbst-Einschätzungs-Element:

```html
<label class="thema-sicher">
  <input type="checkbox" data-state="sicher-bruchrechnen">
  Bei <strong>Bruchrechnen</strong> fühle ich mich sicher
</label>
```

Schüler:in markiert nach Bearbeitung selbst — dient als persönlicher Anker („Hier muss ich nichts mehr machen") und als Übersicht („Wo bin ich noch unsicher?").

### 6. „Bonus"-Aufgaben für Note 1

Mit `data-bonus` oder `data-schwierigkeit="3"` markierte Aufgaben werden in einer **eigenen Bonus-Sektion am Ende** gesammelt — wer Note 1 will, übt hier.

### 7. Kein Druck, kein „Score"

Trotz Klausur-Kontext: **kein Punkte-Score, keine Note-Vorhersage**. Der Onepager soll Sicherheit geben, nicht zusätzlichen Stress.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box (Klausur-Themen) | ja |
| **Themen-Filter** | **ja, profilspezifisch** |
| Aufgaben-Karten mit Thema+Schwierigkeit | ja |
| Selbst-Korrektur | **ja, sehr wichtig** |
| Lösungs-Hürde (Standard) | ja |
| Quiz am Ende | optional, als Selbst-Check |
| Canvas | je nach Fach |
| **Fortschritt pro Thema** | **ja, statt globalem Fortschritt** |
| Save-Status | ja |
| Toast | ja |
| JSON/HTML-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<header class="page-header">
  <span class="ue-label">Mathematik · Klasse 8 · Klausurvorbereitung</span>
  <h1>Was kommt in der Klassenarbeit dran?</h1>
</header>

<div class="content">
  <div class="box lernziel">
    <span class="box-title">✦ Klausurthemen</span>
    <ul>
      <li>Bruchrechnen (addieren, subtrahieren, multiplizieren)</li>
      <li>Dezimalzahlen (umrechnen, vergleichen)</li>
      <li>Prozentrechnung (Grundaufgaben)</li>
    </ul>
  </div>

  <div class="themen-filter" role="group">
    <button data-thema="all"          aria-pressed="true">Alle</button>
    <button data-thema="bruchrechnen" aria-pressed="false">Brüche</button>
    <button data-thema="dezimal"      aria-pressed="false">Dezimal</button>
    <button data-thema="prozent"      aria-pressed="false">%</button>
  </div>

  <article class="aufgabe" data-task-id="bruch-1" data-thema="bruchrechnen">
    <header class="aufgabe__header">
      <span class="aufgabe__nr">1</span>
      <span class="thema-tag">Brüche</span>
      <span class="schwierigkeit">★★</span>
      <h3 class="aufgabe__titel">Addition mit ungleichnamigen Brüchen</h3>
    </header>
    <div class="aufgabe__body">
      <p>Berechne 1/3 + 1/4 als Bruch.</p>
      <input data-state="bruch-1-a" data-expected-keywords="7/12">
      <span class="feedback" data-feedback-for="bruch-1-a"></span>
      <div class="reveal-actions">…</div>
    </div>
  </article>

  <!-- weitere Aufgaben, gemischt nach Themen … -->

  <div class="thema-sicher-block">
    <h3>Wie sicher bist du?</h3>
    <label class="thema-sicher">
      <input type="checkbox" data-state="sicher-bruchrechnen">
      Bruchrechnen sitzt
    </label>
    <label class="thema-sicher">
      <input type="checkbox" data-state="sicher-dezimal">
      Dezimalzahlen sitzen
    </label>
    <label class="thema-sicher">
      <input type="checkbox" data-state="sicher-prozent">
      Prozentrechnung sitzt
    </label>
  </div>
</div>
```

## Anti-Patterns

- **Score / Notenvorhersage** → erzeugt zusätzlichen Stress, didaktisch fragwürdig
- **Aufgaben nur einer Schwierigkeit** → Differenzierung fehlt
- **Keine Themen-Tags** → Filter funktioniert nicht, gezielte Übung schwer
- **Zu wenig Aufgaben pro Thema** (< 3) → Ergebnis nicht aussagekräftig
- **Lösung sofort sichtbar** (Klartext) → Schüler:innen schauen rein, statt zu rechnen
- **Quiz statt offene Aufgaben** als Hauptmechanik → Klausur ist meist offen, also üben

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn vor der Klausur ein Thema NEU erarbeitet werden soll. Klausurvorbereitung setzt voraus, dass die Inhalte schon bekannt sind.
- [`profiles/lerntheke.md`](lerntheke.md) — Wenn Schüler:innen Aufgaben **frei wählen** sollen (z. B. nach Schwäche), passt die Lerntheke besser
- [`profiles/kompetenzraster.md`](kompetenzraster.md) — Eine ergänzende Kompetenzraster-Selbsteinschätzung am Anfang/Ende hilft, gezielt zu üben
