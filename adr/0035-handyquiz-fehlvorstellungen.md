# ADR-0035: Handyquiz mit Distraktoren, die auf Fehlvorstellungen zeigen

- **Status:** Proposed
- **Datum:** 2026-11-24
- **Betrifft:** neue Blaupause (Profil Handyquiz), Quiz-Mechanik, Rückmeldung
- **Ändert nicht:** [ADR-0012](0012-gamification.md), [ADR-0013](0013-quiz-hardening.md) (gilt für Tests, nicht für Selbsttests)

## Kontext

Am Ende einer Stunde soll die Klasse in fünf bis zehn Minuten am **eigenen Handy** prüfen, was sitzt. Die Lehrkraft
braucht dabei keine Rückmeldung, es soll nichts gespeichert werden. Ein gewöhnliches Quiz sagt nur „richtig/falsch“ und
eine Punktzahl. Für das Lernen ist wertvoller, **warum** eine Antwort falsch war: Gute Distraktoren sind keine
beliebigen falschen Antworten, sondern typische **Fehlvorstellungen** des Themas (fachdidaktische Diagnostik, z. B.
„Bei der Zellteilung wird die Erbinformation halbiert“). Wer einen Distraktor wählt, verrät damit eine mögliche
Fehlvorstellung – und wer denselben Denkfehler bei mehreren Fragen zeigt, hat ihn wahrscheinlich wirklich.

## Entscheidung

Eine eigene Blaupause **Handyquiz** (`templates/handyquiz-boilerplate.html`), gefüllt nur über einen JSON-Datenblock
und gebaut mit `tools/handyquiz_bauen.py`, geprüft mit `tools/handyquiz_test.py`. Profil:
[`profiles/handyquiz.md`](../profiles/handyquiz.md).

1. **Fragetypen:** eine richtige Antwort (`eins`), mehrere richtige (`mehr`), wahr/falsch (`wf`) – gemischt in einem Quiz.
2. **Jeder Distraktor zeigt auf eine Fehlvorstellung** (`fv`). Das Bauskript bricht ab, wenn eine falsche Antwort keine
   hat. Bei `wf` trägt die Frage das `fv` der falschen Wahl. Bei `mehr` kann eine richtige Antwort `fv_wenn_fehlt`
   tragen: Wer sie übersieht, zeigt diese Fehlvorstellung.
3. **Fehlvorstellungen sind eigene Einträge** mit `titel` (der Denkfehler in Schülersprache, als „Du dachtest …“) und
   `richtig` (die fachlich richtige Vorstellung in ein bis drei Sätzen). Jede soll von **mindestens zwei Fragen**
   angesteuert werden, sonst warnt das Bauskript.
4. **Rückmeldung:** nach jeder Frage richtig/falsch mit Erklärung und – bei einer falschen Wahl – „Möglicher Denkfehler“
   mit Titel. Am Ende Punktzahl, Prozent und die Liste der Denkfehler, häufigste zuerst: bei zwei oder mehr Fragen
   „das solltest du klären“, bei einer „vielleicht nur verklickt“. Immer als Text, nie nur Farbe (ADR-0009).
5. **Mischen:** Fragen und Antworten bei jedem Start neu; wahr/falsch bleibt in dieser Reihenfolge.
6. **Kein Speichern:** kein localStorage, keine HTML-Share-Speicherung, keine Übermittlung. „Neuer Versuch“ beginnt neu.
7. **Keine Spielmechanik** über das eigene Ergebnis hinaus: keine Zeit, keine Ranglisten, kein Vergleich (ADR-0012).

## Konsequenzen

- Die Qualität steht und fällt mit den Fehlvorstellungen: Sie kommen aus der Fachdidaktik oder der Erfahrung mit der
  Klasse, nicht aus beliebigen falschen Antworten. Das Bauskript erzwingt die Zuordnung, nicht ihre Güte.
- Die Lösungen stehen im Quelltext. Für benotete Tests ist das Format ungeeignet (dann QuizCenter oder ADR-0013).
- Die Lehrkraft sieht nichts. Will sie wissen, welche Denkfehler in der Klasse häufig sind, fragt sie im Plenum nach
  („Wer hatte den Denkfehler …?“) – das Ergebnis bleibt bei den Schülerinnen und Schülern.
