# Profil: Fachwörter-Training

- **Status:** Draft
- **Datum:** 2026-11-19
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Training für die **Fachwörter eines Buchabschnitts oder Themas** (Biologie, Mathematik, Informatik, jedes
Sachfach) im Vokabelstil: Karteikarten zum Lernen, dazu zwei Tests – das passende Fachwort **auswählen** oder es
selbst **schreiben**. Jeder fertige Versuch bleibt im Verlauf, damit die SuS sehen, dass sie besser werden.

Es ist die Fachwörter-Fassung des Profils [Vokabeln](vokabeln.md), aber mit **eigener Blaupause**: Die Seite wird
nicht von Hand gebaut, sondern aus einem Datenblock.

| Wozu | Datei |
|---|---|
| Blaupause | [`templates/fachwoerter-boilerplate.html`](../templates/fachwoerter-boilerplate.html) |
| Prüfen und bauen | [`tools/fachwoerter_bauen.py`](../tools/fachwoerter_bauen.py) |
| Im Browser durchspielen | [`tools/fachwoerter_test.py`](../tools/fachwoerter_test.py) |
| Beispiel | [`examples/fachwoerter-stammzellen-kl9.json`](../examples/fachwoerter-stammzellen-kl9.json) → [`.html`](../examples/fachwoerter-stammzellen-kl9.html) |

**Abgrenzung:** Fremdsprachen-Vokabeln → [Vokabeln](vokabeln.md). Spiel mit Punkten, Level oder Zeit →
[Lernspiel](lernspiel.md). Benoteter Test → nicht als HTML-Seite (die Lösungen stehen im Quelltext).

## Typische Merkmale

- **Klassenstufe:** Sek I
- **Fachbereich:** alle Sachfächer mit Fachsprache
- **Zeitumfang:** 10–15 Minuten je Sitzung, wird mehrmals geöffnet (vor der Arbeit, im Bus)
- **Ziel-Typ:** Fachsprache festigen, Vorbereitung auf Arbeit oder Test
- **Gerät:** Smartphone zuerst, iPad

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0001](../adr/0001-single-file-html-architektur.md) | Eine Datei, nichts nachladen; die Daten stehen als JSON-Block in der Seite |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) | Markierungen, fertige und angefangene Versuche lokal; mit HTML-Share zusätzlich auf dem Server |
| [ADR-0006](../adr/0006-responsives-layout.md) | 390 px ohne waagerechtes Scrollen, Tippflächen ab 44 px |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Rückmeldung immer als Text, nie nur Farbe |
| [ADR-0011](../adr/0011-selbst-korrektur.md) | Karten: Selbsteinschätzung. Tests: automatische Prüfung mit Erklärung |

## Core-ADRs abweichend oder weniger relevant

- **ADR-0012 (Gamification):** keine Punkte, Level, Zeit, Ranglisten. Der Verlauf vergleicht nur mit den eigenen Versuchen.
- **ADR-0013 (Quiz-Härtung):** nicht nötig, die Seite ist zum Üben.
- **ADR-0003 (JSON-Export):** entfällt; einsammeln geht über HTML-Share („Eingaben speichern: einsammeln“).
- **ADR-0018 (Aufgaben-Karten), ADR-0010 (Lösungs-Hürde):** wie bei Vokabeln durch Flip-Karten ersetzt.

## Der Datenblock

Je Seite ändert sich nur eine JSON-Datei. Sie liegt neben der fertigen Seite (`<slug>.json`), damit sich die
Seite neu bauen lässt.

```json
{
  "slug": "fachwoerter-stammzellen-9nwbi09-1",
  "titel": "Fachwörter-Training: Stammzellen",
  "kurz": "Bio · Fachwörter",
  "label": "Biologie · 9nwBI_09 · Stammzellen",
  "quelle": "Natur und Technik S. 330–334",
  "buch": "Natur und Technik",
  "woerter": [
    {
      "id": "v1",
      "wort": "Stammzelle",
      "erklaerung": "Unspezialisierte Zelle, die sich teilen und in verschiedene Zelltypen entwickeln kann.",
      "seiten": "330, 331, 334",
      "frage": "Eine Zelle, die noch nicht spezialisiert ist. Sie kann sich teilen und zu verschiedenen Zelltypen werden.",
      "falsch": ["Embryo", "Zelldifferenzierung", "Klonen"],
      "geprueft": false
    }
  ]
}
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `slug` | ja | eindeutig, klein, ohne Umlaute; Schlüssel des gespeicherten Stands – nach dem Veröffentlichen nicht mehr ändern |
| `titel`, `label`, `quelle`, `kurz`, `buch` | `titel` ja | Kopf der Seite; `buch` steht vor den Seitenzahlen der Karten |
| `testlaenge` | nein | Zahl der Fragen je Versuch; ohne Angabe alle Wörter |
| `woerter[].id` | empfohlen | fest vergeben (`v1` …); an ihr hängen die Markierungen der SuS |
| `wort`, `erklaerung` | ja | Vorder- und Rückseite der Karte; die Erklärung ist auch die Rückmeldung im Test |
| `seiten` | nein | gedruckte Seitenzahlen |
| `frage` | empfohlen | eigene Umschreibung für die Tests, **ohne** das Fachwort oder seinen Wortstamm |
| `falsch` | ja | genau drei falsche Antworten für „Auswählen“ |
| `auch` | nein | weitere Schreibweisen, die bei „Schreiben“ gelten |
| `beispiel` | nein | Beispielsatz, auf der Karte aufklappbar |
| `geprueft` | nein | `false`, wenn der Glossar-Eintrag noch ungeprüft ist – das Bauskript meldet es |
| `stamm_ok` | nein | `true` schaltet die Wortstamm-Prüfung für dieses Wort ab (nur wenn es nicht anders geht) |

## Spezifische didaktische Entscheidungen

1. **Quelle der Wörter ist das Glossar** der Lehrkraft zum Buchabschnitt, nicht freie Erfindung. Ungeprüfte Einträge
   werden beim Bauen gemeldet und vor dem Veröffentlichen angesehen.
2. **Drei Schritte, frei wählbar:** Karten (kennenlernen) → Auswählen (wiedererkennen) → Schreiben (abrufen und
   richtig schreiben). Nichts ist gesperrt.
3. **Falsche Antworten sind echte Alternativen:** Fachwörter aus demselben Thema und derselben Wortart, am besten
   die typische Verwechslung (totipotent – pluripotent – multipotent). Die richtige Antwort darf weder an der
   Länge noch an der Schreibung noch am Wortstamm in der Frage zu erkennen sein. Das prüft das Bauskript; ob
   eine falsche Antwort nicht doch auch stimmt, prüft der Mensch.
4. **Fragen sind Umschreibungen**, nicht die Glossar-Erklärung im Wortlaut. Die Erklärung erscheint danach als
   Rückmeldung – auch bei richtiger Antwort.
5. **Test und Karten hängen zusammen:** Ein im Test nicht gewusstes Wort bekommt die Markierung „Übe ich“; nach der
   Auswertung führt „Nur meine Fehler üben“ direkt zu diesen Karten. Richtige Antworten ändern keine Markierung –
   „Wusste ich“ bleibt Selbsteinschätzung.
6. **Schreiben prüft Buchstaben, nicht Formalien:** Groß-/Kleinschreibung, Bindestrich und Leerzeichen dürfen
   abweichen (die genaue Schreibweise wird dann gezeigt); bis zu zwei falsche Buchstaben geben „Fast“ und zählen
   nicht.
7. **Versuche gehen nicht verloren:** Jeder fertige Versuch steht im Verlauf (Datum, Balken, „x von n“, bester
   Versuch, „Du wirst besser“). Ein angefangener Versuch wird nach jeder Antwort gespeichert und lässt sich
   fortsetzen. „Reset“ löscht nur die Markierungen der Karten.
8. **Kein Druck:** keine Zeit, keine Prozent-Noten, kein Vergleich mit anderen.
9. **Druck:** „Wörterliste“ druckt alle Fachwörter mit Erklärung und Seite.

## HTML-Share

- Freigabe mit „Eingaben speichern“: `weitermachen` (anderes Gerät) oder `einsammeln` (Lehrkraft sieht die Stände).
- Die Seite verwaltet den Stand selbst (`HTMLShare.load/save/submit`); die Klick-Aufzeichnung ist per Meta-Tag aus.
- Gespeichert wird `{v:1, karten, versuche:[{t, art, score, max, falsch}], laufend}`; jedes Ergebnis geht zusätzlich
  als Punktzahl an HTML-Share. In der Lehrkraft-Ansicht (`HTMLShare.readOnly`) steht oben der Verlauf mit „Noch zu
  üben“ je Versuch.
- Ohne HTML-Share (Datei lokal) läuft alles mit `localStorage`.

## Ablauf beim Bauen

1. Fachwörter und Erklärungen aus dem Glossar holen, je Wort `frage` und drei `falsch` schreiben → `<slug>.json`.
2. `python3 tools/fachwoerter_bauen.py <slug>.json -o <slug>.html` – Fehler beheben, Warnungen beheben oder der
   Lehrkraft nennen.
3. `python3 tools/fachwoerter_test.py <slug>.html` – spielt die Seite in Handy-Größe durch.
4. An der Blaupause selbst (CSS, Programm) wird für eine einzelne Seite nichts geändert. Fehlt etwas: Blaupause
   verbessern, dann gilt es für alle.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Flip-Karten, Marker, Filter, Mischen, Lernrichtung | ja (in der Blaupause) |
| Test „Auswählen“ und „Schreiben“ | ja (in der Blaupause) |
| Verlauf der Versuche | ja |
| Save-Status, Toast, Reset | ja |
| Lösungs-Hürde, Gating, Canvas, JSON-Export | nein |

## Anti-Patterns

- **Richtige Antwort ist die längste oder genaueste** – SuS raten nach Form statt nach Inhalt.
- **Wortstamm in der Frage** („Forschung mit Stammzellen“ → Stammzellen-Forschung).
- **Falsche Antworten aus einem anderen Thema** – sie scheiden sofort aus.
- **Mehr als etwa 20 Wörter in einem Test** – lieber `testlaenge` setzen oder zwei Seiten bauen.
- **Erklärungen aus dem Schulbuch abschreiben** – eigene Worte, Buch nur als Seitenverweis.
- **Namen von Schülerinnen und Schülern** in Titel, Daten oder Dateiname.

## Verwandte Profile

- [`profiles/vokabeln.md`](vokabeln.md) – Fremdsprachen, freier Aufbau aus dem Flip-Karten-Snippet
- [`profiles/lernspiel.md`](lernspiel.md) – dieselben Begriffe als Memory oder Challenge
- [`profiles/klausurvorbereitung.md`](klausurvorbereitung.md) – das Training als Baustein vor der Arbeit verlinken
