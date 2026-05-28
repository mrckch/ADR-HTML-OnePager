# Profil: Info-Seite

- **Status:** Accepted
- **Datum:** 2026-05-28
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

> 📄 **Statische Variante** — nutzt das schlanke Template [`templates/infoseite-boilerplate.html`](../templates/infoseite-boilerplate.html), **nicht** das große `onepager-boilerplate.html`. Grundlage: [ADR-0030](../adr/0030-statische-infoseiten.md).

## Was ist das?

Eine **reine Informationsseite** — sie erklärt etwas, sammelt aber **nichts** ein. Keine Aufgaben, keine Eingabefelder, keine gespeicherten Ergebnisse. Zielgruppe sind je nach Inhalt **Eltern, Schüler:innen und/oder Lehrkräfte**.

Im Unterschied zu allen anderen Profilen gibt es hier **keine Persistenz**: kein „Ergebnisse sichern", kein Save-Status, kein Reset, kein JSON-Export. Die Seite ist zustandslos und damit maximal robust.

Typische Einsätze:
- **Elterninformation** — Klassenfahrt, Elternabend, neue Regeln, Materiallisten
- **Schüler-Info** — Bewertungskriterien, Prüfungsablauf, Methodenübersicht, Lerntipps
- **Lehrer-Handreichung** — Curriculum-Übersicht, Vertretungsregeln, Konzeptpapiere
- **Aushänge** — Hausordnung, Förderangebote, Ansprechpartner-Listen, FAQ

## Typische Merkmale

- **Klassenstufe:** alle / nicht klassenstufengebunden
- **Fachbereich:** fächerübergreifend, oft Organisation/Klassenleitung
- **Zeitumfang:** dauerhaft — wird über Wochen/Monate immer wieder aufgerufen
- **Ziel-Typ:** Information / Orientierung (kein Lernziel im engeren Sinn)
- **Gerät:** alle — Smartphone (Eltern lesen unterwegs), Laptop, **Druck/PDF** (Aushang, Verteilung)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0030](../adr/0030-statische-infoseiten.md) | **Definiert dieses Profil** — statische Variante ohne Persistenz |
| [ADR-0015](../adr/0015-inhalts-boxen.md) | Inhalts-Boxen (merke/info/tipp/warn) sind das **zentrale** Gestaltungsmittel |
| [ADR-0023](../adr/0023-a4-druck-und-preview.md) + [ADR-0007](../adr/0007-druck-pdf-optimierung.md) | Info-Seiten werden **oft gedruckt / als PDF verschickt** → Druck-Layout zählt besonders |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Eltern jeden Alters lesen mit → Kontrast, Schriftgröße, Tastaturnavigation wichtig |
| [ADR-0022](../adr/0022-design-system-v2.md) | Einheitlicher Look mit den Arbeitsblättern der Schule |

## Core-ADRs abweichend oder weniger relevant

- **ADR-0002 (localStorage):** entfällt komplett — die Seite speichert nichts.
- **ADR-0003 (JSON-Export/Import):** entfällt — es gibt keine Eingaben zum Exportieren.
- **ADR-0004 (Reset-Dialog):** entfällt — nichts zurückzusetzen.
- **ADR-0017 (Save-Status/Toast):** entfällt — kein Zustand, keine Statusanzeige.
- **ADR-0020 (HTML-Export mit State):** entfällt — die Datei ist ohnehin selbsttragend; zum Teilen einfach die `.html` weitergeben.
- **ADR-0010/0011/0012/0013/0018/0019:** entfallen — keine Aufgaben, Quiz, Selbst-Korrektur, Gamification, Canvas.

## Spezifische didaktische / gestalterische Entscheidungen

1. **„Stand:"-Datum im Header** — Info-Seiten veralten. Ein sichtbares Datum macht die Aktualität sofort klar. Bei jeder Änderung mitführen.
2. **Inhaltsverzeichnis / Sprungmarken** — bei längeren Seiten ein `.toc`-Block mit Anker-Links zu den Abschnitten. Eltern springen gezielt zu „Kosten" oder „Termine".
3. **Eckdaten-Tabelle** (`.fakten`) — „Termin / Ort / Kosten / Ansprechpartner" als kompakte Zwei-Spalten-Tabelle. Schneller erfassbar als Fließtext.
4. **Boxen statt Aufgaben** — Hervorhebungen laufen über `.box`-Varianten: `info` (Kernaussage), `merke` (Wichtiges), `tipp` (Empfehlung), `warn` (unbedingt beachten).
5. **Footer mit Kontakt** — Ansprechpartner, E-Mail, ggf. Schul-Impressum. Eltern brauchen einen Rückkanal.
6. **Klare Adressierung** — im Kategorie-Label sofort sagen, an wen sich die Seite richtet („Elterninformation · Klasse 7").

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Inhalts-Boxen (Merke, Info, Tipp, Warn) | **ja, zentral** |
| Inhaltsverzeichnis / Sprungmarken | ja (bei längeren Seiten) |
| „Stand:"-Datum | **ja** |
| Eckdaten-Tabelle (`.fakten`) | optional, oft nützlich |
| Footer mit Kontakt/Quelle | ja |
| A4-Druck + Vorschau | ja |
| Lernziel-Box | nein (kein Lernziel) |
| Aufgaben-Karten | **nein** |
| Selbst-Korrektur (`data-expected`) | **nein** |
| Lösungs-Hürde | **nein** |
| Quiz | **nein** |
| Canvas-Stift-Eingabe | **nein** |
| Fortschrittsbalken | **nein** |
| Save-Status-Indikator | **nein** |
| Toast-Notifications | **nein** |
| JSON-/HTML-Export/Import | **nein** |
| Reset-Dialog | **nein** |

## Struktur-Pattern (typisch)

Kein `.aufgabe`-Block, sondern Abschnitte mit Sprungmarken, Boxen und Tabellen:

```html
<nav class="toc" aria-label="Inhalt dieser Seite">
  <span class="toc__title">Auf dieser Seite</span>
  <ol>
    <li><a href="#termine">Termine &amp; Ablauf</a></li>
    <li><a href="#kosten">Kosten</a></li>
    <li><a href="#packliste">Was mitzunehmen ist</a></li>
  </ol>
</nav>

<section id="termine">
  <h2>Termine &amp; Ablauf</h2>
  <table class="fakten">
    <tr><th>Abfahrt</th><td>Mo, 15.06. · 08:00 Uhr · Bushaltestelle Schule</td></tr>
    <tr><th>Rückkehr</th><td>Fr, 19.06. · ca. 16:00 Uhr</td></tr>
  </table>
  <div class="box info">
    <span class="box-title">ℹ️ Kurz gesagt</span>
    <p>Fünf Tage Schullandheim, Schwerpunkt Teambildung.</p>
  </div>
</section>
```

## Anti-Patterns

- **Eingabefelder einbauen** → dann ist es keine Info-Seite mehr; nimm das große Boilerplate und ein passendes Profil.
- **„Ergebnisse sichern"-Button** → es gibt keine Ergebnisse; verwirrt die Lesenden.
- **Kein Stand-Datum** → veraltete Infos wirken unseriös und führen zu Rückfragen.
- **Wand aus Fließtext** → ohne Boxen, Sprungmarken und Tabellen wird die Info nicht erfasst.
- **Fehlender Kontakt** → Eltern/Schüler:innen haben keine Rückfrage-Möglichkeit.

## Verwandte Profile

- [`profiles/methoden.md`](methoden.md) — erklärt eine Methode, hat aber einen Anwendungs-/Reflexionsteil mit Eingaben; Info-Seite ist rein erklärend
- [`profiles/lesetext.md`](lesetext.md) — präsentiert ebenfalls Text, koppelt ihn aber an Aufgaben
- [`profiles/flipped-classroom.md`](flipped-classroom.md) — Vorbereitungsmaterial, aber mit Aufgaben dazu
