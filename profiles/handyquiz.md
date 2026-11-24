# Profil: Handyquiz

- **Status:** Draft
- **Datum:** 2026-11-24
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md)); Mechanik: [ADR-0035](../adr/0035-handyquiz-fehlvorstellungen.md)

## Was ist das?

Ein **kurzer Selbsttest am eigenen Handy**, meist in den letzten fünf bis zehn Minuten einer Stunde: 8–12 Fragen,
gemischt aus „eine Antwort richtig“, „mehrere richtig“ und „wahr oder falsch“. Jede falsche Antwort zeigt auf eine
typische **Fehlvorstellung**; am Ende sehen die Schülerinnen und Schüler ihre Punktzahl und die Denkfehler, die ihnen
vielleicht passiert sind – mit der richtigen Vorstellung daneben. Nichts wird gespeichert, die Lehrkraft sieht nichts.

| Wozu | Datei |
|---|---|
| Blaupause | [`templates/handyquiz-boilerplate.html`](../templates/handyquiz-boilerplate.html) |
| Prüfen und bauen | [`tools/handyquiz_bauen.py`](../tools/handyquiz_bauen.py) |
| Im Browser durchspielen | [`tools/handyquiz_test.py`](../tools/handyquiz_test.py) |
| Beispiel | [`examples/handyquiz-mitose-kl10.json`](../examples/handyquiz-mitose-kl10.json) → [`.html`](../examples/handyquiz-mitose-kl10.html) |

**Abgrenzung:** Fachwörter üben → [Fachwörter-Training](fachwoerter.md). Spiel mit Punkten, Level oder Zeit →
[Lernspiel](lernspiel.md). Benoteter Test oder Lehrkraft will Ergebnisse sehen → QuizCenter, nicht HTML.
Quiz als Etappe einer Erarbeitung → [Erarbeitungsseite](erarbeitungsseite.md).

## Typische Merkmale

- **Klassenstufe:** Sek I/II
- **Fachbereich:** alle, besonders wo es bekannte Fehlvorstellungen gibt (Naturwissenschaften, Mathematik)
- **Zeitumfang:** 5–10 Minuten, Stundenende oder Stundenbeginn (Wiederholung)
- **Ziel-Typ:** Selbstkontrolle, Diagnose eigener Denkfehler
- **Gerät:** **Smartphone** (auch ohne Schul-Tablet), Link per Messenger

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0035](../adr/0035-handyquiz-fehlvorstellungen.md) | **Definiert dieses Profil** – Distraktoren → Fehlvorstellungen, Rückmeldung, Mischen, kein Speichern |
| [ADR-0001](../adr/0001-single-file-html-architektur.md) | Eine Datei, Daten als JSON-Block in der Seite |
| [ADR-0006](../adr/0006-responsives-layout.md) | 390 px ohne waagerechtes Scrollen, Tippflächen ab 52 px |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Richtig/falsch als Text und Zeichen, nicht nur Farbe |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Automatische Prüfung mit Erklärung nach jeder Frage |

## Core-ADRs abweichend oder weniger relevant

- **ADR-0002/0003/0017/0020 (Persistenz, Export):** entfallen – nichts wird gespeichert (ADR-0035, Punkt 6).
- **ADR-0012 (Gamification):** nur das eigene Ergebnis (Punkte, Prozent) am Ende; keine Zeit, keine Ranglisten.
- **ADR-0013 (Quiz-Härtung):** nicht nötig, Selbsttest. Lösungen stehen im Quelltext.
- **ADR-0007/0023 (Druck):** entfällt.

## Der Datenblock

```json
{
  "slug": "quiz-mitose-bio10-01",
  "titel": "Quiz: Mitose",
  "kurz": "Bio · Quiz Mitose",
  "label": "Biologie · Klasse 10 · Zellteilung",
  "fehlvorstellungen": {
    "fv-halbieren": {
      "titel": "Du dachtest, bei der Teilung wird die Erbinformation halbiert.",
      "richtig": "Jede Tochterzelle bekommt die vollständige Erbinformation – beim Menschen wieder 46 Chromosomen."
    }
  },
  "fragen": [
    { "id": "m2", "typ": "eins", "frage": "… Wie viele Chromosomen hat jede Tochterzelle?",
      "optionen": [ {"text": "46", "richtig": true}, {"text": "23", "fv": "fv-halbieren"}, {"text": "92", "fv": "fv-verdopplung"} ] },
    { "id": "m3", "typ": "wf", "frage": "Die Tochterzellen sind erbgleich.", "wahr": true, "fv": "fv-tochter",
      "erklaerung": "Optional: ein Satz, der nach dem Prüfen erscheint." },
    { "id": "m7", "typ": "mehr", "frage": "Was passiert in der Prophase?",
      "optionen": [ {"text": "Chromosomen werden sichtbar.", "richtig": true, "fv_wenn_fehlt": "fv-chromosom"},
                    {"text": "Die Zelle schnürt sich durch.", "fv": "fv-phasen"} ] }
  ]
}
```

Regeln, die `handyquiz_bauen.py` prüft (Fehler brechen ab, Warnungen sind zu beheben oder bewusst hinzunehmen):

- `eins`: 3–5 Antworten, genau eine richtig. `mehr`: mindestens zwei richtige und eine falsche. `wf`: `wahr` und `fv`.
- **Jede falsche Antwort hat ein `fv`**, das es in `fehlvorstellungen` gibt; richtige Antworten haben keins.
- Warnung: Fehlvorstellung an nur einer Frage, nicht benutzt; ein Fragetyp fehlt; richtige Antwort ist auffällig die längste.

## Spezifische didaktische Entscheidungen

1. **Erst die Fehlvorstellungen, dann die Fragen.** Vier bis sieben typische Denkfehler des Themas sammeln
   (Fachdidaktik, Schulbuch, eigene Erfahrung), dann Fragen bauen, deren Distraktoren genau diese Denkfehler sind.
2. **Jede Fehlvorstellung an mindestens zwei Fragen.** Erst die Wiederholung macht die Diagnose belastbar – einmal
   kann ein Verklicken sein, und so sagt es die Ergebnisseite auch.
3. **Titel in Schülersprache** („Du dachtest, …“), **Richtig-Satz kurz** und fachlich sauber.
4. **Keine Fangfragen**, keine doppelten Verneinungen; Distraktoren gleich lang und gleich plausibel.
5. **Fehlvorstellungen nicht beschämend formulieren** – es sind normale Zwischenschritte beim Lernen.
6. **Link per Messenger** zum Stundenende; die Seite braucht kein Konto.

## Anti-Patterns

- **Beliebige falsche Antworten** („12“, „Telophase“ ohne Grund) – dann gibt es keine Diagnose.
- **Eine Fehlvorstellung für alles** – die Ergebnisseite sagt dann nichts.
- **Zu lang:** mehr als 12 Fragen passen nicht in zehn Minuten.
- **Als Test benutzen** – die Lösungen stehen im Quelltext; für Noten das QuizCenter.

## Verwandte Profile

- [`profiles/fachwoerter.md`](fachwoerter.md) – gleiche Bauweise (Blaupause + Datenblock), für Fachwörter
- [`profiles/lernspiel.md`](lernspiel.md) – Üben mit Spielmechanik
- [`profiles/praesentation.md`](praesentation.md) – häufiges Gespann: Foliensatz vorn, Handyquiz am Ende
