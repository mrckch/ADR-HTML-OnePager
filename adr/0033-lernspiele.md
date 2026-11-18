# ADR-0033: Lernspiele (Spiel-Variante mit begrenzten Spielmechaniken)

- **Status:** Proposed
- **Datum:** 2026-11-18
- **Betrifft:** Gamification (Ausnahme zu ADR-0012), neue Einsatzklasse, Design-System, Werkzeuge
- **Ändert nicht:** [ADR-0012](0012-gamification.md) — gilt in allen anderen Profilen unverändert

## Kontext

Auf einem Fachtag „Lernspiele mit KI“ (November 2026) bauten Lehrkräfte in zwei Runden 34 Mathe-Spiele: Escape-Rooms,
Zielscheiben, Level-Spiele, Memorys, 60-Sekunden-Challenges. Daraus sind fünf wiederverwendbare Vorlagen entstanden,
die die Lehrkraft und der KI-Assistent mit Aufgaben einer Lerngruppe füllen.

Diese Spiele passen in keines der bisherigen Profile:

| Aspekt | Onepager (Arbeitsblatt) | Lernspiel |
|---|---|---|
| Medium | Papier / A4 am Tablet | **Bildschirm**: Handy, iPad, Laptop |
| Ablauf | Aufgaben untereinander, beliebige Reihenfolge | **eine Aufgabe nach der anderen**, Spielzustand |
| Rückmeldung | Selbst-Korrektur, Lösungs-Hürde | sofort nach jeder Antwort, Tipp nach Fehler |
| Druck | Kernfunktion (ADR-0007, ADR-0023) | entfällt |
| Persistenz | alle Eingaben (ADR-0002) | höchstens Spielstand oder Bestwert |
| Motivation | sanft: Fortschritt, Abschnitt-Marker (ADR-0012) | **Spielmechanik**: Punkte, Level, Zeit |

Der Konflikt liegt in [ADR-0012](0012-gamification.md): Es schließt Punkte, Level, Sterne, Ranglisten, Streaks und Zeitdruck
(außer in ausdrücklichen Quiz-Aufgaben) aus und verlangt für jedes weitere Element eine neue ADR. Ein Zielscheiben-Spiel
ohne Punkte oder eine 60-Sekunden-Challenge ohne Zeit gibt es aber nicht. Die Gründe von ADR-0012 (kein Wettkampfdruck,
keine Angst vor dem Verlust einer Serie, kein Vergleich) bleiben richtig und sollen auch in Spielen gelten.

## Entscheidung

Eine eigene Variante **Lernspiel**: Profil [`profiles/lernspiel.md`](../profiles/lernspiel.md), Vorlagen unter
`templates/lernspiel/`, Werkzeuge und Sammlung unter `lernspiele/`. Spielmechaniken sind **nur in diesem Profil** und
nur in den Grenzen unten erlaubt.

### 1. Erlaubt (nur im Profil Lernspiel)

| Element | Grenze |
|---|---|
| **Punkte** | nur innerhalb einer Runde; nie über Runden aufaddiert, nie mit Namen |
| **Level** | als Gliederung von leicht nach schwer; ein Level wird durch Bestehen frei, Bestehen = Mindestanteil richtig, nie „fehlerfrei“ |
| **Zeitlimit** | nur im Spieltyp, der ausdrücklich eine Challenge ist (`zeit-challenge`) und so heißt; sonst nur „schnell“-Bonus ohne Strafe |
| **Combo** | höchstens ×2, setzt nach einem Fehler zurück, ohne Abzug |
| **Bestwert** | nur auf dem eigenen Gerät (`localStorage`), ohne Namen, nur der eigene |
| **Spielwelt** | eigene, neutrale Welt (Räume, Zielscheibe, Weg); keine Figuren, Marken oder Welten aus kommerziellen Spielen |

### 2. Weiter verboten (wie ADR-0012)

- Ranglisten, Vergleich mit anderen, Namenseingabe im Spiel
- Streaks über mehrere Tage, Verlust-Mechaniken („Leben“, die das Spiel beenden), Abzug für falsche Antworten
- Konfetti, Achievement-Popups, Belohnungs-Sounds
- Zeitdruck in Spielen, die keine Challenge sind

### 3. Pflicht

- **Tipp nach jeder falschen Antwort**, sofern die Aufgabe einen hat; nach einem Fehler geht es weiter, nichts ist verloren.
- **Ende ohne Abwertung**: „Fast! Nochmal?“ statt „Verloren“; das Ergebnis nennt, was geklappt hat.
- **Nochmal spielen** mit einem Knopf, Aufgaben neu gemischt.
- `prefers-reduced-motion` schaltet Animationen ab ([ADR-0009](0009-barrierefreiheit-lesbarkeit.md)).

### 4. Design-System v3 „Signal“

Spiele sind Bildschirmflächen. Nach der Medien-Regel aus [ADR-0031](0031-design-system-v3-signal.md) nutzen sie **v3**:
Signal-Blau, Orange nur als Akzent und Fokus, Display-Schrift, Radius 4 px. Dark Mode nach OS-Einstellung mit
`data-theme="light"` als Notausgang. Gut/Falsch-Farben ergänzen v3 nur für die Rückmeldung und stehen nie allein
(immer mit Text, ADR-0009). Kein Mischen mit v2.

### 5. Vorlagen, Aufgaben-Format, Werkzeuge

- Jede Vorlage ist eine einzige HTML-Datei ohne Nachladen ([ADR-0001](0001-single-file-html-architektur.md)).
  Oben im Skript steht der Abschnitt `ANPASSEN` mit Titel, Aufgaben und Spiel-Konstanten; nur dieser wird geändert.
- Aufgaben haben ein festes Format: `{ frage, antwort, optionen?, tipp? }`. `antwort` darf eine Liste richtiger
  Schreibweisen sein; die Prüfung ist tolerant (Groß/klein, Leerzeichen, Komma/Punkt, Zahlen als Zahl).
- `<meta name="lernspiel-typ" content="<typ>">` kennzeichnet den Spieltyp.
- Unter `lernspiele/basis/` liegen **optionale** Python-Werkzeuge: `bauen.py` baut die Vorlagen aus gemeinsamen Teilen,
  `fuellen.py` setzt Aufgaben aus einer JSON-Datei ein und prüft sie, `test.py` spielt mit Playwright durch.
  Sie sind kein Build-Schritt im Sinne von [CONTRIBUTING.md](../CONTRIBUTING.md): Wer ein Spiel baut, braucht sie
  nicht – die Vorlage lässt sich von Hand oder mit einer KI im Abschnitt `ANPASSEN` füllen. Die gebauten Vorlagen
  liegen fertig im Repo und werden nicht von Hand geändert.

## Alternativen

- **Spiele ohne Punkte und Zeit, ADR-0012 unverändert:** Escape-Room, Level und Memory gingen, Zielscheibe und
  60-Sekunden-Challenge nicht. Gerade die Formen zum Automatisieren fielen weg. Verworfen.
- **ADR-0012 allgemein lockern:** Würde Punkte und Zeit in Arbeitsblätter tragen, wo sie stören. Verworfen; die
  Ausnahme bleibt an das Profil gebunden.
- **Vorlagen auf `onepager-boilerplate.html` (v2):** Die Boilerplate ist ein A4-Arbeitsblatt mit Druck, Stift und
  Export; ein Spiel bräuchte davon fast nichts und widerspräche der Medien-Regel aus ADR-0031. Verworfen.
- **Eigenes Repo nur für Spiele:** Getrennte Regeln und Designs würden auseinanderlaufen. Verworfen; die Spiele
  leben als Variante hier.

## Konsequenzen

**Positiv:**
- Spielformen mit Punkten und Zeit sind möglich, ohne die Schutzgründe von ADR-0012 aufzugeben.
- Fünf geprüfte Vorlagen statt jedes Mal ein neu generiertes Spiel; gleiches Aussehen, gleiche Antwortprüfung.
- Automatischer Durchspiel-Test fängt kaputte Spiele ab, bevor SuS sie sehen.

**Negativ / Trade-offs:**
- Eine dritte Bauart neben Onepager und Foliensatz; v3-Tokens jetzt in drei Dateien-Gruppen (Drift-Risiko wie in ADR-0031).
- Python-Werkzeuge im Repo, auch wenn optional.
- Wer ein Spiel von Hand ändert, kann die Grenzen aus Abschnitt 1 verletzen; die Checkliste prüft das.

**Folgewirkungen:**
- `AI_GUIDE.md` nennt das Profil in Schritt 1 und die Vorlagen in Schritt 4.
- `CHECKLIST.md` prüft bei Spielen die Grenzen aus Abschnitt 1–3.
- Neue Spielformen kommen nach `lernspiele/README.md` („Neue Spielform“) dazu; neue Mechaniken außerhalb von
  Abschnitt 1 brauchen eine Änderung dieser ADR.

## Verwandte ADRs

- [ADR-0012](0012-gamification.md) — Gamification sanft; diese ADR ist die einzige Ausnahme
- [ADR-0031](0031-design-system-v3-signal.md) — Medien-Regel, v3 für Bildschirmflächen
- [ADR-0001](0001-single-file-html-architektur.md) — eine Datei, nichts nachladen
- [ADR-0002](0002-state-persistenz-localstorage.md) — Bestwert und Spielstand nur lokal
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — Rückmeldung nie nur über Farbe, reduzierte Bewegung
- [ADR-0013](0013-quiz-hardening.md) — Spiele zeigen die Lösung nach der Antwort; für Tests ist das QuizCenter oder ein Quiz-Onepager da
