# ADR-0034: Ein Tor öffnet nur an geprüften, richtigen Antworten

- **Status:** Accepted (Entscheidung der Lehrkraft, 24.11.2026)
- **Datum:** 2026-11-24
- **Betrifft:** Gating (Profil Erarbeitungsseite und jedes Profil, das Sektionen sperrt), Selbst-Korrektur, Quiz
- **Ergänzt:** [ADR-0011](0011-selbst-korrektur.md), [ADR-0013](0013-quiz-hardening.md); die Fortschrittsanzeige nach
  [ADR-0012](0012-gamification.md) bleibt unverändert

## Kontext

Das Gating-Snippet galt eine Sektion als „bearbeitet“, sobald in jeder Pflichtaufgabe **irgendein** Feld einen Wert
hatte. Eine Durchsicht von 34 Seiten eines Schuljahres (24.11.2026) zeigte die Folge: In acht Blättern öffnete sich die
nächste Etappe bei beliebigem Text, bei einer falschen Zahl und bei einer falsch angekreuzten Quiz-Antwort. Die
Rückmeldung „Stimmt / Noch nicht“ gab es, sie hing aber nicht am Tor. Schülerinnen und Schüler gingen so mit einer
Fehlvorstellung in die nächste Etappe.

Randbedingung: Die Seiten laufen ohne Server und ohne KI im Hintergrund ([ADR-0001](0001-single-file-html-architektur.md)).
Ob ein frei geschriebener Text inhaltlich stimmt, kann die Seite nicht beurteilen. Auswerten lässt sich nur, was
deterministisch prüfbar ist.

## Entscheidung

1. **Ein Tor hängt nur an Tor-Fragen.** Tor-Fragen sind Felder, die die Seite sicher prüfen kann:
   - Zahl oder Wort mit `data-expected` (und `data-tolerance`),
   - Quiz-Frage `.quiz-frage` mit `data-answer-hash` (ADR-0013),
   - Stichwort-Felder mit `data-expected-keywords` / `data-expected-keywords-all` – nur für kurze Fachbegriffe,
     nicht für ganze Sätze (Stichwörter belegen nicht, dass die Aussage stimmt).
2. **Das Tor öffnet erst, wenn alle Tor-Fragen der Sektion richtig sind.** „Ausgefüllt“ reicht nicht.
3. **Freie Texte zählen nie für das Tor** – weder öffnen sie es, noch sperren sie es. Sie bleiben wertvoll
   (erklären, begründen, reflektieren), ihre Rückmeldung kommt aber von außerhalb der Seite: Musterlösung mit
   Selbstabgleich an Kriterien, Lehrkraft (eingesammelte Eingaben) oder ein Dialogpartner.
4. **Jede gesperrte Etappe braucht mindestens eine Tor-Frage zum Kern der Sektion davor.** Besteht eine Sektion nur
   aus freien Texten, steht an ihrem Ende eine prüfbare Frage zum selben Inhalt (Auswahl, Zuordnung, Zahl, Lücke).
   Eine Sektion ohne Tor-Frage fällt auf „alle Pflichtaufgaben ausgefüllt“ zurück und meldet das in der Konsole
   (`ADR-0034`); bewusst gewollt ist das nur bei `data-gate="frei"` (z. B. Vorwissen aktivieren).
5. **Die Sektion zeigt ihren Tor-Stand** („Noch 2 Tor-Fragen offen“ / „Geschafft – weiter“), damit niemand vor
   einem Schloss steht, ohne zu wissen, was fehlt. `?gate=off` und `?solutions=1` öffnen wie bisher alles.

Umgesetzt in [`templates/snippets/gating-snippet.html`](../templates/snippets/gating-snippet.html).

## Alternativen

- **„Ausgefüllt“ als Tor behalten** – verworfen: genau die beobachtete Falle.
- **Mindestlänge oder Stichwörter für freie Texte** – verworfen als Tor: prüft Form, nicht Inhalt; belohnt Textsalat
  mit den richtigen Wörtern.
- **KI in der Seite bewertet den Text** – verworfen: verletzt ADR-0001, nicht deterministisch, Datenschutz.
- **Kein Gating mehr** – verworfen: Der Lernpfad der Erarbeitungsseite braucht die Reihenfolge.

## Konsequenzen

**Positiv:**
- Wer weiterkommt, hat den Kern der Etappe nachweislich richtig.
- Die Rückmeldung der Seite ist ehrlich: sicher, wo geprüft werden kann, sonst ausdrücklich keine Wertung.

**Negativ / Trade-offs:**
- Mehr Arbeit beim Bauen: Zu jeder Etappe gehört eine gute prüfbare Frage mit durchdachten Falschantworten.
- Wer an einer Tor-Frage hängt, kommt nicht weiter: Tipps (ADR-0010) müssen zu den Tor-Fragen passen; die Lehrkraft
  kann mit `?gate=off` öffnen.

**Folgewirkungen für künftige Onepager:**
- Beim Bauen je gesperrter Sektion fragen: „Woran erkennt die Seite sicher, dass der Kern verstanden ist?“
- Nie ein Tor an ein Freitextfeld hängen. Freitext ohne `data-expected*` bekommt keinen „✓“.
- Bestehende Seiten mit dem alten Snippet beim nächsten Anfassen umstellen.

## Verwandte ADRs

- ADR-0010 (Lösungs-Hürde), ADR-0011 (Selbst-Korrektur), ADR-0013 (Quiz), ADR-0024 (Profile)
