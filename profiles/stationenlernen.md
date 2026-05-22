# Profil: Stationenlernen-Station

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **eine einzelne Station** eines Stationen-Lernzirkels (oder einer Lernlandschaft). Mehrere solcher Onepager bilden gemeinsam einen Zirkel — die Schüler:innen rotieren durch die Stationen oder wählen frei, in welcher Reihenfolge sie arbeiten.

Charakteristisch: **kompakt, fokussiert, in begrenzter Zeit bearbeitbar**.

## Typische Merkmale

- **Klassenstufe:** alle, häufig Grundschule und Sek I
- **Fachbereich:** alle
- **Zeitumfang pro Station:** **10–20 Minuten** — bewusst klein, damit ein Zirkel in einer Doppelstunde durchläuft
- **Ziel-Typ:** Übung, Anwendung, manchmal Erarbeitung eines Teilaspekts
- **Gerät:** Tablet (wechselt zwischen Schülern) oder Laptop

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | 1–3 Aufgaben-Karten reichen — bewusst klein gehalten |
| [ADR-0023](../adr/0023-a4-druck-und-preview.md) | Eine Station passt **auf eine A4-Seite** — Daumenregel und didaktische Konvention |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save kritisch, weil Geräte zwischen Schülern wechseln können |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0012](../adr/0012-gamification.md) (Fortschrittsbalken):** weniger relevant — eine Station ist kurz, der Balken füllt sich in 5 Minuten. Optional weglassen.
- **Lernziele:** auf eine **einzige** kompakte Stations-Lernziele-Zeile reduzieren („An dieser Station lernst du …")
- **[ADR-0010](../adr/0010-loesungs-huerde.md) (Lösungs-Hürde):** Standard-Mechanik beibehalten, aber sparsam einsetzen — eine Station hat selten mehr als 2-3 Aufgaben mit Lösungs-Reveal

## Spezifische didaktische Entscheidungen

### 1. Stations-Header statt UE-Label

Statt „Fach · Klasse · Einheit X von Y" steht im Page-Header **„Station N von M · Zeit: ca. 15 Min · Thema: …"** — das Stations-Metadatum ist primär.

```html
<header class="page-header">
  <span class="ue-label">Station 3 von 6 · ca. 15 Min</span>
  <h1>Brüche addieren</h1>
</header>
```

### 2. Eine Station = eine A4-Seite

Daumenregel: Eine Station passt im A4-Druck (`?layout=a4`) auf **eine einzige Seite**. Wenn nicht: Inhalt kürzen, nicht aufteilen — sonst entsteht zwischen Stationen Verwirrung.

Praktisch: 1 Lernziel-Zeile, 1–3 Aufgaben-Karten, optional 1 Merke-Box, dezenter Footer.

### 3. Klare Stations-Eingrenzung

Die Aufgaben einer Station müssen **inhaltlich eng** sein — eine Teilfähigkeit, ein Begriff, ein Verfahren. Wer am gleichen Tag mit verschiedenen Stationen arbeitet, soll wissen, *worauf diese Station zielt*.

Anti-Beispiel: „Station 3: Rechnen" → zu breit. Besser: „Station 3: Bruchaddition mit gleichnamigen Brüchen".

### 4. Übergang zur nächsten Station

Am Ende ein dezenter Hinweis, was als Nächstes kommt:

```html
<div class="box info" style="margin-top: var(--space-8)">
  <span class="box-title">→ Nächste Station</span>
  <p>Wenn du fertig bist: weiter zu <strong>Station 4 — Bruchaddition mit ungleichnamigen Brüchen</strong>.</p>
</div>
```

Bei freiem Lauf (Schüler wählen selbst): „Du kannst zu jeder Station gehen, die noch frei ist."

### 5. Geräte-Wechsel-Verträglichkeit

Stationen werden oft an **festen Geräten** bearbeitet — verschiedene Schüler:innen am selben iPad. Beim ersten Aufruf nach Reset/Klassenwechsel:

- Reset-Dialog mit klarem Hinweis: „Das löscht die Eingaben des/der vorigen Schüler:in"
- JSON-Export-Empfehlung am Ende: „Speicher deine Lösung als Datei, falls du sie noch brauchst"

### 6. Stations-Nummer als Topbar-Element

Statt eines normalen Topbar-Titels: prominent die Stations-Nummer und das Stations-Thema:

```html
<span class="topbar__title">Station 3 · Bruchaddition</span>
```

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box (kompakt) | ja, **eine Zeile** |
| Aufgaben-Karten | ja, **1–3 Stück** |
| Inhalts-Boxen (Merke, Tipp) | sparsam, max. 1–2 |
| Selbst-Korrektur | ja |
| Lösungs-Hürde | ja, Standard |
| Quiz | nein (das passt eher zur Erarbeitungsseite) |
| Canvas | optional |
| Fortschrittsbalken | weniger relevant (Station ist kurz) — kann weg |
| Save-Status-Indikator | ja |
| Toast-Notifications | ja |
| JSON-Export/Import | ja, bei Geräte-Wechsel wichtig |
| Reset-Dialog | ja, mit Geräte-Wechsel-Warnung |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Station 3 von 6 · ca. 15 Min</span>
    <h1>Brüche addieren mit gleichnamigen Nennern</h1>
  </header>
  <div class="content">

    <div class="box lernziel">
      <span class="box-title">✦ An dieser Station</span>
      Du lernst, gleichnamige Brüche zu addieren.
    </div>

    <article class="aufgabe" data-task-id="s3-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Aufgabe 1</span>
        <h3 class="aufgabe__titel">Berechne 2/7 + 3/7</h3>
      </header>
      <div class="aufgabe__body">
        <input data-state="s3-1-a" data-expected="5/7"
               data-expected-keywords="5/7,5÷7">
        <span class="feedback" data-feedback-for="s3-1-a"></span>
        <div class="reveal-actions">
          <button class="reveal-btn reveal-btn--hint" data-task-id="s3-1" data-stage="1">💡 Tipp</button>
          <button class="reveal-btn reveal-btn--solution" data-task-id="s3-1">🔍 Lösung</button>
        </div>
        <div class="hint-content" data-task-id="s3-1" data-stage="1" hidden>
          Bei gleichem Nenner werden die Zähler addiert, der Nenner bleibt.
        </div>
        <div class="solution-content" data-task-id="s3-1" hidden>
          2/7 + 3/7 = (2+3)/7 = <strong>5/7</strong>
        </div>
      </div>
    </article>

    <!-- Maximal 2–3 Aufgaben — Station ist kompakt -->

    <div class="box info">
      <span class="box-title">→ Nächste Station</span>
      <p>Wenn du fertig bist: weiter zu Station 4 — Brüche mit ungleichnamigen Nennern.</p>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Zu viele Aufgaben** (≥ 5) → sprengt das Stationen-Zeitbudget, andere Stationen werden nicht erreicht
- **Mehrseitiger Inhalt** → Station soll auf einer A4-Seite passen
- **Lange Lernzielliste** → eine Zeile reicht
- **Quiz mit vielen Fragen** → das ist nicht der Charakter einer Station
- **Direkte Verlinkung auf andere Stationen** → Schüler:innen sollen physisch zur nächsten Station gehen oder ihren eigenen Plan haben

## Verwandte Profile

- [`profiles/lesetext.md`](lesetext.md) — Wenn die Station ein Sachtext mit Aufgaben ist
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn der Onepager **die ganze Einheit** strukturiert (statt nur eine Teilstation), ist Erarbeitungsseite passend
