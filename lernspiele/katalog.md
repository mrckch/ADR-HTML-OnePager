# Katalog der Spielformen

Welche Spielform passt zu welchem Inhalt? Der Skill `/lernspiel` des Schulassistenten wählt hier aus. Gebaut = es gibt
eine Vorlage `templates/lernspiel/<typ>.html` und einen Steckbrief `steckbriefe/<typ>.md`. Regeln: [ADR-0033](../adr/0033-lernspiele.md),
Profil [Lernspiel](../profiles/lernspiel.md).

## Auswahlhilfe: Was für ein Inhalt ist es?

| Inhalt | Beispiel | Erste Wahl | Zweite Wahl |
|---|---|---|---|
| Rechenaufgaben, schnell zu lösen | Kopfrechnen, Bruchrechnen, Einheiten | `zeit-challenge` | `zielen-treffen` |
| Aufgaben mit Rechenweg, mehrere Schritte | Prozentrechnung, Gleichungen, Pythagoras | `escape-room` | `level-abenteuer` |
| Stoff mit steigender Schwierigkeit | Terme vom Einfachen zum Schweren | `level-abenteuer` | `escape-room` |
| Begriff und Erklärung, zwei Darstellungen | Zellbestandteile, Bruch und Dezimalzahl, Vokabeln, Funktion und Graph (als Text) | `memory-zuordnen` | `zeit-challenge` |
| Fakten abfragen, Auswahlantworten | Fachbegriffe, Merkmale | `zeit-challenge` | `zielen-treffen` |
| Abläufe, Reihenfolgen | Mitose, Verdauung, Algorithmus | `reihenfolge` (geplant) | `level-abenteuer` |
| In Gruppen einordnen | Wirbeltierklassen, Wortarten, Datentypen | `sortieren` (geplant) | `memory-zuordnen` |
| Fehlvorstellungen aufdecken | typische Rechenfehler, falsche Aussagen | `fehler-finden` (geplant) | `escape-room` mit Auswahl |
| Größen und Werte einschätzen | Längen, Winkel, Wahrscheinlichkeit | `schaetzen` (geplant) | `zielen-treffen` |
| Parameter ausprobieren | Funktionen, Parabeln, Steigung | `simulation` (geplant) | – |

Faustregeln:
- Wiederholen und Automatisieren → kurz und schnell (60 Sekunden, Zielscheibe).
- Anwenden und Verstehen → mit Tipp nach falscher Antwort (Escape-Room, Level).
- Handy: Antippen (`optionen`) ist schneller als Tippen; Eingabe nur, wo das Ergebnis eine Zahl oder ein kurzes Wort ist.

## Spielformen

| Typ | Name | Stand | Kurz |
|---|---|---|---|
| `escape-room` | Escape-Room | gebaut | Räume mit Aufgaben, jeder Raum gibt eine Ziffer, am Ende das Zahlenschloss |
| `zielen-treffen` | Zielen und Treffen | gebaut | Zielscheibe, richtige und schnelle Antworten treffen die Mitte |
| `level-abenteuer` | Level-Abenteuer | gebaut | Figur läuft zum Ziel, Level werden freigeschaltet, Stand bleibt auf dem Gerät |
| `memory-zuordnen` | Memory | gebaut | Paare aufdecken, die zusammengehören |
| `zeit-challenge` | 60-Sekunden-Challenge | gebaut | so viele Aufgaben wie möglich, Combo, Bestwert auf dem Gerät |
| `reihenfolge` | Reihenfolge ordnen | geplant | Schritte per Tippen in die richtige Reihenfolge bringen |
| `sortieren` | Sortieren in Gruppen | geplant | Kärtchen in zwei bis vier Körbe einordnen |
| `fehler-finden` | Fehler finden | geplant | Lösung oder Aussage prüfen: stimmt das? Wo steckt der Fehler? |
| `schaetzen` | Schätzen | geplant | erst schätzen, dann auflösen, Punkte nach Abweichung |
| `luecken` | Lückentext | geplant | Wörter in Lücken tippen oder ziehen |
| `quiz-duell` | Quiz-Duell zu zweit | geplant | zwei Spieler an einem Gerät, abwechselnd |
| `shop` | Einkaufen und Rollenspiel | als Spiel (`spiele/mathe/prozent-shop-7.html`) | Rechnen in einer kleinen Welt; noch keine Vorlage |
| `simulation` | Ausprobieren | geplant | Regler verändern, Ziel treffen (wie Parabel-Golf) |

Neue Formen kommen zuerst als Zeile „geplant“ hierher (mit Herkunft in `ideen/`), gebaut werden sie auf Zuruf.
