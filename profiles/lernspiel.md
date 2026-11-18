# Profil: Lernspiel

- **Status:** Draft
- **Datum:** 2026-11-18
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md)); die Grenzen der Spielmechanik sind Core ([ADR-0033](../adr/0033-lernspiele.md))

## Was ist das?

Ein kurzes Spiel am Bildschirm zum Üben und Wiederholen: Escape-Room, Zielscheibe, Level-Abenteuer, Memory oder
60-Sekunden-Challenge. Die SuS lösen eine Aufgabe nach der anderen und bekommen sofort Rückmeldung. Anders als ein
Onepager ist es kein Arbeitsblatt: kein Druck, keine Mappe, kein Export. Es gibt einen Spielzustand.

## Typische Merkmale

- **Klassenstufe:** Sek I (5–10), einfache Formen auch Grundschule
- **Fachbereich:** alle, besonders Mathematik (Rechnen), Naturwissenschaften und Sprachen (Begriffe, Paare)
- **Zeitumfang:** 5–20 Minuten: Einstieg, Übungsphase, Wiederholung vor der Arbeit, „für Schnelle“
- **Ziel-Typ:** Übung, Festigung, Automatisieren, Wiederholung
- **Gerät:** Smartphone, Tablet, Laptop; kein Druck

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0033](../adr/0033-lernspiele.md) | **Zentral.** Erlaubte und verbotene Spielmechaniken, Pflicht-Tipp, Ende ohne Abwertung |
| [ADR-0031](../adr/0031-design-system-v3-signal.md) | Design v3 „Signal“, weil Bildschirmfläche; Orange nur für den einen Primär-Knopf und den Fokus |
| [ADR-0001](../adr/0001-single-file-html-architektur.md) | Eine Datei, nichts nachladen – läuft in HTML-Share und offline |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Rückmeldung als Text, nie nur Farbe; große Tippflächen (≥ 48 px); reduzierte Bewegung |
| [ADR-0006](../adr/0006-responsives-layout.md) | Muss bei 390 px Breite ohne waagerechtes Scrollen gehen; Frage und Antworten ohne Scrollen sichtbar |

## Core-ADRs abweichend oder weniger relevant

- **ADR-0012 (Gamification):** hier durch ADR-0033 erweitert – Punkte je Runde, Level, Zeit nur in der Challenge.
- **ADR-0022 (Design v2):** nicht verwendet; v3 statt v2, kein Mischen.
- **ADR-0002/0003/0004 (Persistenz, Export, Reset):** nur Spielstand oder Bestwert lokal; kein JSON-Export, kein Reset-Dialog.
- **ADR-0007/0023 (Druck):** entfällt; ein Spiel wird nicht gedruckt.
- **ADR-0010/0011 (Lösungs-Hürde, Selbst-Korrektur):** ersetzt durch die Rückmeldung nach jeder Antwort mit Tipp.
- **ADR-0013 (Quiz-Härtung):** nicht nötig; Spiele zeigen die richtige Antwort. Für Noten ist ein Spiel ungeeignet.

## Spezifische didaktische Entscheidungen

1. **Form nach Inhalt wählen, nicht nach Geschmack.** Die Auswahlhilfe in [`lernspiele/katalog.md`](../lernspiele/katalog.md) ordnet
   Inhalte Spielformen zu: Rechnen → Challenge oder Zielscheibe, Rechenweg → Escape-Room, steigende Schwierigkeit →
   Level, Begriffspaare → Memory.
2. **Immer aus einer Vorlage.** Spiele entstehen aus `templates/lernspiel/<typ>.html`, nur der Abschnitt `ANPASSEN`
   wird geändert. So bleiben Aussehen, Antwortprüfung und Regeln gleich.
3. **Falsche Optionen aus typischen Fehlern.** Distraktoren zeigen Fehlvorstellungen (Nenner addiert, Prozentwert statt
   neuer Preis), nicht Zufallszahlen.
4. **Tipp bei jeder schwereren Aufgabe.** Er erscheint nach einer falschen Antwort.
5. **Handy zuerst.** Antippen (`optionen`) ist schneller als Tippen; Eingabe nur für Zahlen und kurze Wörter.
6. **Mengen nach Steckbrief.** Memory 6–8 Paare, Challenge ab 15 Aufgaben, Level 4–5 Aufgaben je Level.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | nein (Untertitel im Kopf reicht) |
| Aufgaben-Karten | nein (eine Aufgabe zur Zeit auf der „Bühne“) |
| Inhalts-Boxen (Merke, Tipp, Warn) | nein |
| Selbst-Korrektur (`data-expected`) | nein, eigene Prüfung `richtig()` |
| Lösungs-Hürde (Tipp + Lösung) | nein, Tipp nach Fehler |
| Quiz mit gehashten Antworten | nein |
| Canvas-Stift-Eingabe | nein |
| Fortschrittsbalken | ja, im Spiel (Raum, Wurf, Level, Zeit) |
| Save-Status-Indikator | nein |
| Toast-Notifications | nein |
| JSON-Export/Import | nein |
| Reset-Dialog | nein |

## Aufgaben-Pattern (typisch)

```js
// ===== ANPASSEN =====
const TITEL = 'Escape-Room: Prozente';
const UNTERTITEL = 'Drei Räume, drei Ziffern. Dann öffnet sich das Schloss.';
const AUFGABEN = [
  { frage: 'Wie viel sind 25 % von 60 €?', antwort: 15, tipp: '25 % ist ein Viertel.' },
  { frage: 'Ein Preis steigt von 40 € auf 50 €. Um wie viel Prozent?', antwort: ['25 %', '25'],
    optionen: ['25 %', '10 %', '20 %', '50 %'], tipp: 'Die Erhöhung mit dem alten Preis vergleichen.' },
];
// ===== Ab hier nichts ändern =====
```

## Anti-Patterns

- **Rangliste oder Namenseingabe**: Vergleich unter SuS und Personendaten im Spiel – nach ADR-0033 verboten.
- **„Game over“, Leben, Punktabzug**: bestraft Fehler statt aus ihnen zu lernen.
- **Spiel als Test**: die Lösung steht im Quelltext; für Noten das QuizCenter oder einen Quiz-Onepager nehmen.
- **Welt aus einem kommerziellen Spiel**: Figuren, Marken und Welten aus Spielen (besonders für Erwachsene) weglassen.
- **Frei generiertes Spiel statt Vorlage**: sieht jedes Mal anders aus, ungetestet, oft mit Fehlern in der Prüfung.
- **Zu viele Aufgaben pro Runde**: nach 5–20 Minuten ist Schluss; lieber zwei kurze Spiele.

## Verwandte Profile

- [`profiles/vokabeln.md`](vokabeln.md) — Karteikarten zum Lernen; Memory ist die spielerische Wiederholung danach
- [`profiles/klausurvorbereitung.md`](klausurvorbereitung.md) — strukturiertes Üben vor der Arbeit; ein Spiel ergänzt, ersetzt nicht
- [`profiles/lerntheke.md`](lerntheke.md) — ein Spiel kann eine Wahl- oder „Für Schnelle“-Station sein (als eigene Datei verlinkt)
