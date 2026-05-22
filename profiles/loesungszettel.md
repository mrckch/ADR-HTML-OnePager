# Profil: Lösungszettel zum Schulbuch

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager, der als **digitaler Lösungs- und Hilfsbegleiter** zu einem gedruckten Schulbuch dient. Die Schüler:innen arbeiten weiterhin im Heft an den Aufgaben, der Onepager liefert gestufte Hilfen und überprüft die Lösung. Die vollständige Lösung kommt erst nach Erfolg oder ausreichendem Bemühen ans Licht.

## Typische Merkmale

- **Klassenstufe:** Sek I, Sek II — überall, wo mit gedrucktem Buch gearbeitet wird
- **Fachbereich:** alles, was buchbasiert ist — Mathe besonders typisch
- **Zeitumfang:** passend zu einem Buchkapitel / einer Doppelstunde / Hausaufgabe
- **Ziel-Typ:** Übung, Selbst-Diagnose, Hausaufgabenbegleiter
- **Gerät:** vorwiegend Laptop oder Tablet; Smartphone möglich, da Eingaben kurz sind

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0010](../adr/0010-loesungs-huerde.md) | Lösungs-Hürde ist die Kern-Mechanik des Profils — hier mit **zusätzlicher Verschärfung** (siehe unten) |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Selbst-Korrektur via `data-expected` / `data-expected-keywords` ist die Standard-Eingangsprüfung jeder Aufgabe |
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten tragen einen **Buchverweis** statt einer fortlaufenden Nummer (z. B. „📖 S. 47 · Aufg. 3a") |
| [ADR-0007](../adr/0007-druck-pdf-optimierung.md) + [ADR-0023](../adr/0023-a4-druck-und-preview.md) | Selten gedruckt (Schüler arbeitet am Gerät neben dem Buch), aber wenn doch: Lehrer-Lösungsblatt via `?solutions=1` |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0013](../adr/0013-quiz-hardening.md) (Quiz):** meist nicht relevant — keine Multiple-Choice. Es gibt eine offene Aufgabe pro Aufgabe.
- **[ADR-0012](../adr/0012-gamification.md) (Gamification):** nur Fortschrittsbalken im Topbar; keine Sektion-Abschluss-Banner, keine Animationen. Der Onepager soll nicht ablenken.
- **Lernziel-Box (ADR-0015):** meist weggelassen — die Lernziele stehen im Buch.

## Spezifische didaktische Entscheidungen

### 1. Aufgabentext NICHT im Onepager wiederholen

Die Aufgabe steht im Buch. Der Onepager zeigt:
- den **Buchverweis** im Aufgaben-Header („📖 S. 47 · Aufg. 3")
- optional eine **sehr kurze Erinnerung** (1 Zeile), worum es geht — z. B. „Volumen berechnen"
- KEIN vollständiger Aufgabentext

Begründung: Sonst schauen Schüler:innen aus Bequemlichkeit nur in den Onepager und ignorieren das Buch — die intendierte Doppelmedium-Arbeit fällt weg.

### 2. Verschärfte Lösungs-Hürde mit Cipher

Standard-ADR-0010 schaltet die Lösung per Bestätigungs-Modal frei. Im Lösungszettel-Profil ist das zu schwach. Stattdessen:

**Zweistufige Hilfen vor der Lösung:**

| Stufe | Inhalt |
|---|---|
| Hilfe 1 (Hinweis) | Leichter Anstoß: „Welche Formel könnte hier passen?" |
| Hilfe 2 (Methode) | Methodisch konkreter: „Berechne zuerst die Grundfläche, dann V = G · h" |

Volle Lösung wird durch einen **XOR-Cipher** verschlüsselt, bei dem die **richtige Antwort als Schlüssel** dient. Konsequenz:

- **Schüler tippt richtige Antwort ein** → Lösung wird mit der eingegebenen Antwort entschlüsselt → Lösungs-Erklärung erscheint (Lösungsweg, Erinnerungs-Schritte, „warum es so funktioniert")
- **Schüler tippt falsche Antwort ein** → Entschlüsselung gibt Müll → Toast „Stimmt noch nicht — schau dir die Hilfen an"
- **Source-Code-Anzeige** → man sieht nur den verschlüsselten Cipher; ohne Schlüssel unbrauchbar

Die „Lösung" ist hier nicht das **Ergebnis** (das hat der Schüler ja), sondern der **Weg dorthin**: Rechen-Schritte, Vergleich mit der eigenen Methode, kurze Begründung. Didaktisch wertvoller als die nackte Zahl.

#### Code-Snippet: Lösungs-Cipher

Das Boilerplate stellt `window.solutionCipher.encrypt(text, key)` und `decrypt(cipher, key)` bereit. Beim Erstellen eines neuen Lösungszettels:

```js
// In der Browser-Konsole, einmal pro Aufgabe:
solutionCipher.encrypt("V = a · b · h = 5 · 3 · 4 = 60 cm³", "60")
//  → "aGVsbG8K..."  (Base64-String)
```

Den Base64-String ins HTML kopieren:

```html
<article class="aufgabe" data-task-id="s47-a3">
  …
  <input type="number" data-state="s47-a3" data-answer-hash="…" />
  <div class="solution-content"
       data-task-id="s47-a3"
       data-solution-cipher="aGVsbG8K..."
       hidden></div>
</article>
```

### 3. Lösungs-Button erst spät freigeschaltet

Der „🔍 Lösung anzeigen"-Button ist initial **deaktiviert**. Er wird aktiv, sobald **eines** der folgenden erfüllt ist:

- Die Selbst-Korrektur meldet „✓ richtig" (dann wird der Button zu „🎯 Lösungsweg anzeigen" — der Schüler hat es geschafft und kann den Weg sehen)
- ODER: 3 Fehlversuche **und** beide Hilfen wurden geöffnet (dann wird der Button aktiv, aber Klick öffnet ein Bestätigungs-Modal nach ADR-0010)

Wenn beide Hilfen nicht angesehen wurden und die Eingabe wiederholt falsch: der Button bleibt deaktiviert mit Tooltip „Schau dir erst Hilfe 1 und Hilfe 2 an".

### 4. Lehrkraft-Eskalation bewusst eingeplant

Wenn ein:e Schüler:in die Aufgabe wirklich nicht schafft (auch mit beiden Hilfen nicht), führt der Weg nicht über einen versteckten „Notfall"-Klick zur Lösung, sondern zur **Lehrkraft**. Anzeige in der Aufgabe:

> Wenn du nicht weiterkommst: frag die Lehrkraft. Lösung freischalten geht erst nach drei Versuchen mit beiden Hilfen.

Das ist didaktische Absicht — die Lehrkraft bleibt im Spiel.

### 5. `?solutions=1` für Lehrer-Druck

URL-Parameter `?solutions=1` (ADR-0010) zeigt:
- alle Hilfen
- ein zusätzliches Lösungs-Klartext-Feld pro Aufgabe (aus einem versteckten `<script type="application/json" id="teacher-solutions">`-Block)
- ideal für ausgedruckte Lehrer-Lösungsblätter

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | meist nein (steht im Buch) |
| Aufgaben-Karten | **ja, mit Buchverweis im Header** |
| Inhalts-Boxen (Merke, Tipp, Warn) | sparsam, höchstens ein Merke-Kasten pro Kapitel |
| Selbst-Korrektur (`data-expected`) | **ja, Pflicht** für jede Aufgabe mit eindeutiger Antwort |
| Lösungs-Hürde (Tipp + Lösung) | **ja, verschärft** (siehe oben) |
| Quiz mit gehashten Antworten | nein |
| Canvas-Stift-Eingabe | nein |
| Fortschrittsbalken | ja (zeigt Bearbeitungsfortschritt) |
| Save-Status-Indikator | ja |
| Toast-Notifications | ja |
| JSON-Export/Import | ja (für Geräte-Wechsel) |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="aufgabe" data-task-id="s47-a3">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">📖 S. 47 · Aufg. 3a</span>
    <h3 class="aufgabe__titel">Volumen berechnen</h3>
    <span class="aufgabe__status" data-status="empty"></span>
  </header>
  <div class="aufgabe__body">
    <div class="field">
      <label for="s47-a3-v">Dein Ergebnis (in cm³)</label>
      <input type="number" id="s47-a3-v" data-state="s47-a3-v"
             data-expected="60" data-tolerance="0.01"
             data-answer-hash="0b8810cc"
             inputmode="decimal" step="0.01">
      <span class="feedback" data-feedback-for="s47-a3-v"></span>
    </div>

    <div class="reveal-actions">
      <button class="reveal-btn reveal-btn--hint"  data-task-id="s47-a3" data-stage="1">💡 Hilfe 1</button>
      <button class="reveal-btn reveal-btn--hint"  data-task-id="s47-a3" data-stage="2">💡 Hilfe 2</button>
      <button class="reveal-btn reveal-btn--solution" data-task-id="s47-a3" disabled>🔍 Lösung</button>
    </div>

    <div class="hint-content" data-task-id="s47-a3" data-stage="1" hidden>
      Welche Formel verbindet Grundfläche und Höhe zu Volumen?
    </div>
    <div class="hint-content" data-task-id="s47-a3" data-stage="2" hidden>
      G ist die Fläche der unteren Seite. Berechne erst G, dann V = G · h.
    </div>
    <div class="solution-content"
         data-task-id="s47-a3"
         data-solution-cipher="aGVsbG8KdGV4dA=="
         hidden></div>
  </div>
</article>
```

## Anti-Patterns

- **Aufgabentext aus dem Buch ins HTML kopieren** → Schüler verlieren den Bezug zum Buch, urheberrechtlich heikel
- **Lösung im Klartext im DOM** → Source-Code-Anzeige spoilert alles
- **Lösungs-Button von Anfang an aktiv** → Hürde wirkungslos
- **Bunte Gamification, Sektion-Abschluss-Banner** → unpassend für Lösungszettel-Charakter
- **Quiz-Charakter** → der Onepager ist Begleiter, kein Test
- **Lernziel-Box** → die Lernziele stehen schon im Buch

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn die Theorie nicht im Buch steht, sondern erarbeitet wird, ist die Erarbeitungsseite das passende Profil.
- [`profiles/digitales-arbeitsheft.md`](digitales-arbeitsheft.md) — Wenn die Schüler:innen direkt im Onepager rechnen sollen (handschriftlich), ist das Arbeitsheft passend.
