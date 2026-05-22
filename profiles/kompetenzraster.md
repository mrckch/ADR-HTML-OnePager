# Profil: Kompetenzraster / Selbst-Einschätzung

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager als **Selbst-Einschätzungs-Raster**: Eine Tabelle mit „Ich kann …"-Aussagen, daneben eine Skala (Smileys, Sterne, Ampel), auf der die Schüler:in den eigenen Lernstand markiert. Keine Aufgaben — nur Bewertung.

Wird typischerweise **vor und nach einer Einheit** ausgefüllt (Pre/Post-Vergleich) oder regelmäßig zwischendurch, um den Lernfortschritt sichtbar zu machen.

## Typische Merkmale

- **Klassenstufe:** alle, ab Sek I sinnvoll
- **Fachbereich:** alle, besonders in Fächern mit klar formulierbaren Teilkompetenzen
- **Zeitumfang:** 5–10 Minuten zum Ausfüllen
- **Ziel-Typ:** Diagnose, Metakognition, Selbst-Bewertung
- **Gerät:** Laptop oder Tablet; auf Smartphone schwierig (Tabelle wird zu breit)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0006](../adr/0006-responsives-layout.md) | **Tabelle muss mobile-tauglich sein** — auf schmalen Screens umbrechen oder als Cards rendern |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | Persistent über Wochen — Pre/Post-Vergleich braucht Datums-Stempel |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Radio-Buttons müssen tab-bedienbar sein, Smileys haben `aria-label` |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md) / [ADR-0011](../adr/0011-selbst-korrektur.md):** nicht relevant — keine richtige/falsche Antwort
- **[ADR-0018](../adr/0018-aufgaben-karten.md):** keine Aufgaben-Karten — eine große Tabelle ist das Hauptelement
- **Quiz, Canvas, Fortschrittsbalken:** nicht relevant

## Spezifische didaktische Entscheidungen

### 1. Tabelle als zentrales Element

Das Raster ist eine Tabelle mit:
- Zeile pro Kompetenz („Ich kann …")
- Spalten: Skala-Werte + optional „Datum 1" / „Datum 2" für Pre/Post-Vergleich

```html
<table class="kompetenz-raster">
  <thead>
    <tr>
      <th scope="col">Ich kann …</th>
      <th scope="col" colspan="4">Wie sicher fühle ich mich?</th>
      <th scope="col">Notiz</th>
    </tr>
    <tr>
      <th></th>
      <th aria-label="Unsicher">😞</th>
      <th aria-label="Wenig sicher">😐</th>
      <th aria-label="Sicher">🙂</th>
      <th aria-label="Sehr sicher">😀</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">… einfache Prismen erkennen.</th>
      <td><input type="radio" name="k1" data-state="k1" value="1"></td>
      <td><input type="radio" name="k1" data-state="k1" value="2"></td>
      <td><input type="radio" name="k1" data-state="k1" value="3"></td>
      <td><input type="radio" name="k1" data-state="k1" value="4"></td>
      <td><input type="text" data-state="k1-notiz" placeholder="optional"></td>
    </tr>
    <!-- weitere Zeilen … -->
  </tbody>
</table>
```

### 2. Skala bewusst gewählt

Empfohlen: **4er-Skala** (gerade Anzahl, kein neutraler Mittelwert, zwingt zur Tendenz):
- 😞 Unsicher
- 😐 Wenig sicher
- 🙂 Sicher
- 😀 Sehr sicher

Alternativen: Sterne (★, ★★, ★★★, ★★★★) oder Ampel (Rot/Gelb/Grün — 3er-Skala mit Mitte). 5er-Skala vermeiden — neutrale Mitte wird zu oft gewählt.

### 3. Notiz-Spalte optional

Eine kleine Text-Spalte pro Zeile erlaubt freie Notizen („Brauche noch mehr Übung bei …"). Optional — kann weggelassen werden für ein kompakteres Raster.

### 4. Pre/Post-Vergleich

Bei wiederkehrender Nutzung (z. B. „am Anfang und am Ende der Einheit ausfüllen"): zwei Spalten-Gruppen pro Zeile, jeweils mit Datum:

```html
<table class="kompetenz-raster">
  <thead>
    <tr>
      <th scope="col">Ich kann …</th>
      <th colspan="4">Vor der Einheit · <input type="date" data-state="datum-pre"></th>
      <th colspan="4">Nach der Einheit · <input type="date" data-state="datum-post"></th>
    </tr>
    …
  </thead>
  …
</table>
```

Schüler:in füllt am Anfang die linke Hälfte aus, am Ende die rechte — der Fortschritt wird sofort sichtbar.

### 5. Mobile-Fallback: vertikales Card-Layout

Auf Smartphone-Breite wird die Tabelle zu Cards umgebrochen — eine „Karte" pro Kompetenz:

```css
@media (max-width: 600px) {
  .kompetenz-raster, .kompetenz-raster thead, .kompetenz-raster tbody,
  .kompetenz-raster tr, .kompetenz-raster th, .kompetenz-raster td {
    display: block;
  }
  .kompetenz-raster thead { display: none; }
  .kompetenz-raster tr {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--space-3);
    margin-bottom: var(--space-3);
  }
  .kompetenz-raster tr th[scope="row"] {
    font-weight: 600;
    margin-bottom: var(--space-2);
  }
  .kompetenz-raster tr td { display: inline-block; padding: var(--space-1); }
}
```

### 6. Keine Auswertung anzeigen

**Wichtig:** Der Onepager rechnet nicht zusammen („Du hast 70 % erreicht"). Das wäre Bewertung, nicht Selbst-Einschätzung. Die Lehrkraft kann beim Einsammeln (JSON-Export) eine Aggregation machen — der Schüler-Onepager bleibt qualitativ.

### 7. Datenschutz-Hinweis

Sensibles Material. Hinweis-Box am Anfang:

```html
<div class="box info">
  <span class="box-title">ℹ️ Hinweis</span>
  Deine Einschätzung bleibt auf deinem Gerät. Du entscheidest, ob du sie teilst.
</div>
```

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | nein (das Raster IST die Lernziel-Sammlung) |
| Aufgaben-Karten | nein (Tabelle dominiert) |
| Inhalts-Boxen (Info) | ja (für Hinweise zur Nutzung) |
| **Kompetenz-Tabelle** | **ja, Hauptelement** |
| Selbst-Korrektur | nein |
| Lösungs-Hürde | nein |
| Quiz | nein |
| Canvas | nein |
| Fortschrittsbalken | nein |
| Pre/Post-Spalten | optional, sehr empfehlenswert |
| Save-Status | ja |
| Toast | ja |
| JSON-Export | **ja, für Pre/Post-Vergleich und Lehrer-Einsammlung** |
| Reset-Dialog | ja, mit Warnung |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathematik · Klasse 8 · Einheit "Prismen"</span>
    <h1>Wie sicher bin ich? — Selbst-Einschätzung</h1>
  </header>
  <div class="content">

    <div class="box info">
      <span class="box-title">ℹ️ So gehst du vor</span>
      Lies jede „Ich kann …"-Aussage und markiere, wie sicher du dich
      gerade fühlst. Es gibt keine richtige oder falsche Antwort.
    </div>

    <table class="kompetenz-raster">
      <thead>
        <tr><th>Ich kann …</th>
            <th aria-label="Unsicher">😞</th>
            <th aria-label="Wenig sicher">😐</th>
            <th aria-label="Sicher">🙂</th>
            <th aria-label="Sehr sicher">😀</th>
            <th>Notiz</th></tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">… einfache Prismen erkennen und beschreiben.</th>
          <td><input type="radio" name="k1" data-state="k1" value="1"></td>
          <td><input type="radio" name="k1" data-state="k1" value="2"></td>
          <td><input type="radio" name="k1" data-state="k1" value="3"></td>
          <td><input type="radio" name="k1" data-state="k1" value="4"></td>
          <td><input type="text" data-state="k1-notiz" placeholder="optional"></td>
        </tr>
        <!-- weitere Zeilen … -->
      </tbody>
    </table>

    <div class="field" style="margin-top: var(--space-6)">
      <label for="freie-reflexion">Was möchtest du noch lernen oder vertiefen?</label>
      <textarea id="freie-reflexion" data-state="freie-reflexion" rows="3"></textarea>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Automatische Auswertung „Du hast 70 % erreicht"** → wird zum Bewertungsraster, nicht Selbst-Einschätzung
- **Skala mit ungerader Anzahl** (1–5) → neutrale Mitte verleitet zur Vermeidung der Entscheidung
- **Pflicht-Markierung** → Schüler:in darf auch leer lassen (z. B. weil unklar)
- **Aufgaben mitten zwischen Kompetenz-Zeilen** → vermischt Selbst-Einschätzung mit Übung
- **Lange Lernziel-Boxen am Anfang** → das Raster selbst ersetzt die Lernziele
- **Tabelle ohne Mobile-Fallback** → auf Smartphone unbenutzbar

## Verwandte Profile

- [`profiles/reflexionstagebuch.md`](reflexionstagebuch.md) — Strukturell ähnlich (qualitativ, keine Aufgaben), aber narrativ statt tabellarisch
- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Kann am Anfang/Ende ein Kompetenzraster-Element enthalten; als ganzes Profil ist Kompetenzraster geeigneter, wenn die Bewertung der Hauptzweck ist
