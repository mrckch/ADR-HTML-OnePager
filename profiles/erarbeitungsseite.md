# Profil: Erarbeitungsseite mit Lernpfad

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **vollständige Lerneinheit** zu einem neuen Thema. Die Schüler:innen gehen einen **strukturierten Lernpfad** entlang:

1. **Vorwissensaktivierung** — was wissen wir schon?
2. **Erarbeitung** — neues Konzept einführen (Theorie + Beispiele)
3. **Übung** — erste Aufgaben zum direkten Anwenden
4. **Vertiefung** — anspruchsvollere Aufgaben oder Transfer
5. **Quiz** (optional) — Selbst-Kontrolle am Ende

Charakteristisch: **Gating** — Sektionen werden erst freigeschaltet, wenn die vorherige Sektion bearbeitet wurde. Das soll davon abhalten, zu schnell durchzuklicken, und stellt sicher, dass die Aufbau-Logik (Vorwissen → Neues) tatsächlich erlebt wird.

## Typische Merkmale

- **Klassenstufe:** alle, besonders Sek I für neue Themen
- **Fachbereich:** alle — Mathe, Sprachen, Geschichte, NaWi
- **Zeitumfang:** Einzelstunde bis Doppelstunde (komplette Erarbeitung), oder Hausaufgabe vor einer Stunde („Flipped Classroom")
- **Ziel-Typ:** Erarbeitung neuer Inhalte, Vorbereitung, Selbst-Erarbeitung
- **Gerät:** vorwiegend Laptop/Tablet; Smartphone weniger gut wegen Textmenge

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0015](../adr/0015-inhalts-boxen.md) | **Zentral.** Lernziel-, Merke-, Info-, Tipp-Boxen tragen die Erarbeitungs-Theorie. Häufig benutzt. |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Übungs- und Vertiefungs-Aufgaben als Karten |
| [ADR-0010](../adr/0010-loesungs-huerde.md) + [ADR-0011](../adr/0011-selbst-korrektur.md) | Standard-Lösungs-Hürde — nicht so streng wie beim Lösungszettel, aber Standard-zweistufig |
| [ADR-0013](../adr/0013-quiz-hardening.md) | Quiz am Ende als Selbst-Kontrolle |
| [ADR-0012](../adr/0012-gamification.md) | Fortschrittsbalken zeigt Lernpfad-Position |

## Core-ADRs abweichend oder weniger relevant

- **Canvas-Modul:** nur bei Bedarf (z. B. Geometrie). Standard ist Text-/Zahleneingabe.
- **HTML-Export mit eingebettetem State (Phase 3):** weniger zentral — der Onepager ist Arbeits-, kein Abgabe-Material.

## Spezifische didaktische Entscheidungen

### 1. Fester Aufbau in fünf Sektionen

Jede Erarbeitungsseite hat dieselben fünf Sektionen — in dieser Reihenfolge:

```
[Lernziele-Box am Anfang]

§ 1 — Vorwissen aktivieren           (1–2 leichte Aufgaben, oft offene Fragen)
       ↓
§ 2 — Neuer Inhalt: Erarbeitung      (Theorie + Beispiele + erste geleitete Aufgaben)
       ↓
§ 3 — Übungsphase                    (Aufgaben zum direkten Anwenden)
       ↓
§ 4 — Vertiefung / Transfer          (anspruchsvoller, optional, Sternchen-Aufgaben)
       ↓
§ 5 — Quiz / Selbst-Check            (optional, Multiple-Choice mit gehashten Antworten)
```

Wenn eine Sektion nicht passt (z. B. keine Vertiefung möglich), wird sie weggelassen — nicht verschoben oder umbenannt. Die Reihenfolge ist Teil der Profilkennung.

### 2. Gating zwischen Sektionen

Sektionen ab § 2 sind **initial visuell ausgegraut und nicht klickbar**, bis die vorherige Sektion ihr Aufgabe-Minimum erreicht hat:

- Sektion gilt als „bearbeitet", wenn **alle Pflicht-Aufgaben** der Sektion einen nicht-leeren Wert haben (analog ADR-0012 Fortschritts-Logik)
- Optional: zusätzlich ein „Weiter zur nächsten Sektion"-Button am Ende jeder Sektion
- Gating ist **sichtbar** durch:
  - reduzierte Opazität (`opacity: 0.4`)
  - `pointer-events: none` auf den Inhalten
  - ein Schloss-Icon mit Hinweis „Erst die vorige Sektion abschließen"
  - kein scharfes Verbot — wenn die Lehrkraft `?solutions=1` oder `?gate=off` setzt, ist alles offen

**Wichtig — empfehlender Charakter:** Gating ist sanft. Es **hindert**, klickt sich aber **nicht weg**. Ein:e Schüler:in, der/die unbedingt weiterspringen will (z. B. weil Inhalte schon bekannt sind), kann via Lehrkraft eine Freischaltung anfordern. Echte Wegklick-Logik wäre zu rigide.

### Gating-JS-Pattern (kommt mit eigener ADR in einer späteren Phase)

```js
function updateGating() {
  const sections = Array.from(document.querySelectorAll('section[data-step]'));
  let predecessorComplete = true;
  for (const sec of sections) {
    const aufgaben = sec.querySelectorAll('.aufgabe[data-task-id]:not([data-optional])');
    const allFilled = Array.from(aufgaben).every(isAufgabeFilled);
    sec.classList.toggle('is-locked', !predecessorComplete);
    if (!allFilled) predecessorComplete = false;
  }
}
```

```css
section.is-locked {
  opacity: 0.4;
  pointer-events: none;
  position: relative;
}
section.is-locked::before {
  content: "🔒 Erst die vorige Sektion abschließen";
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  background: var(--bg-page);
  border: 1px solid var(--border);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: 600;
}
```

(Wird in einer Phase 3-ADR als Modul ausgelagert.)

### 3. Lernziele am Anfang sind Pflicht

Die `.lernziel`-Box (ADR-0015) ist hier **nicht optional**. Schüler:innen sehen vor der Erarbeitung, was sie am Ende können sollen.

### 4. Theorie-Lasten in `.merke` und `.info`

Der Hauptteil von § 2 ist neuer Inhalt — Definitionen, Beispiele, Erklärungen. Diese leben in:

- `.box.merke` — Definitionen, Regeln, Formeln
- `.box.info` — Hintergrund-Info, „Wusstest du schon?"
- `.box.tipp` — methodische Tipps, „So gehst du vor"

Aufgaben in § 2 sind **geleitet** (Lückentext, kleine Berechnungen mit Hilfsstruktur). Erst in § 3 wird's offen.

### 5. Quiz am Ende mit Hash-Schutz

Wenn ein Quiz dazukommt (empfohlen, aber optional), liegt es **immer in § 5 am Ende**. Es nutzt ADR-0013 mit `data-answer-hash`. Auswertung erst auf Klick auf „Quiz auswerten" (nicht live).

### 6. Fortschrittsbalken zeigt Lernpfad-Position

Standard-Fortschrittsbalken aus ADR-0012, **angereichert** um Sektion-Indikatoren:

```
[●●●●○○○○]  3 / 5 Sektionen
 §1 §2 §3
```

Wenn die Sektion-Anzeige zu viel Platz braucht, reicht die Standard-Anzeige „X / Y Aufgaben". Der Fortschritts-Bezugspunkt ist hier aber **Sektionen**, nicht einzelne Aufgaben.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | **ja, Pflicht am Anfang** |
| Aufgaben-Karten | **ja, viele** |
| Inhalts-Boxen (Merke, Tipp, Info) | **ja, viele** in § 2 |
| Selbst-Korrektur (`data-expected`) | ja, wo eindeutig |
| Lösungs-Hürde (Tipp + Lösung) | ja, Standard-zweistufig |
| Quiz mit gehashten Antworten | ja, am Ende |
| Canvas-Stift-Eingabe | optional, nur bei Bedarf |
| Fortschrittsbalken | **ja, mit Sektion-Anzeige** |
| Sektion-Gating | **ja, profilspezifisch** |
| Save-Status-Indikator | ja |
| Toast-Notifications | ja |
| JSON-Export/Import | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">…</header>
  <div class="content">

    <div class="box lernziel">
      <span class="box-title">✦ Was du heute lernst</span>
      <ul>…</ul>
    </div>

    <section data-step="1">
      <h2>§ 1 — Vorwissen aktivieren</h2>
      <article class="aufgabe" data-task-id="vorwissen-1">…</article>
    </section>

    <section data-step="2">
      <h2>§ 2 — Neuer Inhalt: Erarbeitung</h2>
      <div class="box merke">
        <span class="box-title">📌 Merke</span>
        <p>Definition / Formel / Regel</p>
      </div>
      <p>Erklärtext, Beispiel …</p>
      <article class="aufgabe" data-task-id="erarbeitung-1">…</article>
    </section>

    <section data-step="3">
      <h2>§ 3 — Übungsphase</h2>
      <article class="aufgabe" data-task-id="uebung-1">…</article>
      <article class="aufgabe" data-task-id="uebung-2">…</article>
    </section>

    <section data-step="4">
      <h2>§ 4 — Vertiefung</h2>
      <article class="aufgabe" data-task-id="vertiefung-1" data-optional>…</article>
    </section>

    <section data-step="5">
      <h2>§ 5 — Quiz</h2>
      <div class="quiz-frage" data-quiz-id="q1" data-answer-hash="…">…</div>
    </section>

  </div>
</article>
```

## Anti-Patterns

- **Theorie und Aufgaben durcheinander streuen** → Lernpfad zerfällt
- **Quiz mitten drin statt am Ende** → unterbricht die Erarbeitung
- **Gating ohne „Weiter"-Eskalation** → Schüler, die schon weiter sind, blockieren
- **Lernziele weglassen** → das eigentliche Pfad-Versprechen geht verloren
- **Mehrere `<h1>`** → die Sektion-Überschriften sind `<h2>` (Aufbau)
- **Sektion-Reihenfolge ändern** → die fünf Phasen sind Profil-Identität

## Verwandte Profile

- [`profiles/loesungszettel.md`](loesungszettel.md) — Wenn Theorie schon im Buch steht und nur die Aufgaben begleitet werden
- [`profiles/digitales-arbeitsheft.md`](digitales-arbeitsheft.md) — Wenn handschriftliche Bearbeitung im Vordergrund steht
