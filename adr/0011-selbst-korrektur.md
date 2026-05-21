# ADR-0011: Selbst-Korrektur statt nur Lösungsvergleich

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Didaktik, Feedback, Motivation

## Kontext

Auch mit der Lösungs-Hürde aus [ADR-0010](0010-loesungs-huerde.md) bleibt das Standard-Lernmuster:

1. Aufgabe lesen
2. Eingabe machen
3. Lösung aufdecken
4. Vergleichen — passt oder passt nicht

Schritt 4 erfordert Selbstdisziplin: passt der Wert nur „grob" zur Lösung, neigen viele Schüler:innen dazu, sich selbst als richtig zu deklarieren — oder umgekehrt, bei richtiger Antwort an sich zu zweifeln.

**Besser:** Direkt nach der Eingabe einen sanften Hinweis, ob es passt — ohne die Lösung zu spoilern.

## Entscheidung

Eingabefelder können **eine erwartete Antwort** als Attribut tragen. Beim Verlassen des Feldes (`blur`-Event, nicht `input` — vermeidet Stress beim Tippen) zeigt ein dezenter Hinweis, ob die Eingabe passt.

### HTML-Pattern

```html
<!-- Numerisch mit Toleranz -->
<input type="number" id="v-1-1" data-state="v-1-1"
       data-expected="60" data-tolerance="0.01"
       inputmode="decimal" step="0.01">
<span class="feedback" data-feedback-for="v-1-1"></span>

<!-- Text mit Keywords (mind. eines muss vorkommen) -->
<input type="text" id="def-prisma" data-state="def-prisma"
       data-expected-keywords="parallel,deckungsgleich,Grundfläche">
<span class="feedback" data-feedback-for="def-prisma"></span>
```

### Anzeige-Regeln

| Eingabe | Anzeige |
|---|---|
| Leer | nichts |
| Korrekt (im Toleranzbereich / Keyword vorhanden) | grünes ✓ + „Stimmt!" |
| Falsch | gelbes Symbol + „Noch nicht — schau nochmal." |
| Nach 2× falsch in Folge | zusätzlich Hinweis „💡 Möchtest du dir einen Tipp ansehen?" (verlinkt zum Tipp-Button aus ADR-0010) |

Wichtig: **Bei falscher Eingabe wird NICHT die richtige Antwort verraten.** Der Hinweis verschwindet beim nächsten Tippen — das Feld ist wieder offen.

### Toleranz für Zahlen

- `data-tolerance="0.01"` → absolute Toleranz (`|user - expected| ≤ 0.01`)
- `data-tolerance="0.01rel"` → relative Toleranz (1 % vom erwarteten Wert)
- Default ohne `data-tolerance`: `0` (exakter Vergleich), aber mit `data-tolerance="auto"` werden 2 signifikante Stellen toleriert

### Text-Vergleich (Keywords)

- `data-expected-keywords="a,b,c"` → mindestens eines der Keywords muss in der Eingabe vorkommen (case-insensitive, Wortgrenzen egal)
- `data-expected-keywords-all="a,b,c"` → alle müssen vorkommen
- Diakritische Zeichen werden ignoriert („Grundfläche" matcht „grundflache")
- Bewusst tolerant: Schüler-Antworten sind oft anders formuliert als gedacht

### JS-Hash-frei

Da `data-expected="60"` direkt im DOM steht, ist das **nicht** für „Test-Modus" geeignet. Für Quizze siehe [ADR-0013](0013-quiz-hardening.md). Selbst-Korrektur ist explizit eine **Lernhilfe**, kein Prüfungsfilter — die Sichtbarkeit der Erwartung ist akzeptabel.

### Counter für Fehlversuche

JS zählt pro Feld die Fehlversuche in Folge:

```js
const failCount = new Map();  // feldKey → number
// bei jedem 'blur' mit falscher Eingabe: increment
// bei korrekter Eingabe oder leerem Feld: reset auf 0
```

Bei `failCount >= 2`: zusätzlich Hint-Hinweis einblenden.

## Alternativen

- **Live-Validierung bei jedem Tastendruck:** Verworfen — erzeugt Stress, blinkt rot/grün während Tippen.
- **Validierung nur bei explizitem „Prüfen"-Klick:** Erwogen — kommt der Lehrkraft entgegen, aber Schüler:innen klicken den Knopf oft nicht. Default ist deshalb `blur`; einen optionalen „Prüfen"-Knopf können einzelne Onepager ergänzen.
- **Lösung direkt verraten** bei falsch: Verworfen — widerspricht ADR-0010.
- **Punktabzug für Fehlversuche** (Gamification): Verworfen — würde Lerndruck erhöhen statt senken.

## Konsequenzen

**Positiv:**
- Schnelles, präzises Feedback ohne Lösungsspoiler
- Mehrere Anläufe sind ausdrücklich erwünscht und problemlos möglich
- Schüler:innen erfahren früh, ob sie auf dem richtigen Weg sind
- Sanfte Brücke zur Lösungs-Hürde (ADR-0010) bei wiederholten Fehlversuchen

**Negativ / Trade-offs:**
- `data-expected` ist im Source sichtbar — bewusste Akzeptanz für Lernmaterial
- Keyword-Matching ist heuristisch; falsch-positive/negative Treffer sind möglich
- Mehr Aufmerksamkeit beim Schreiben neuer Onepager (Antwort + sinnvolle Keywords)

**Folgewirkungen für künftige Onepager:**
- Für jede numerische Aufgabe: `data-expected` setzen (sofern es eine klare Lösung gibt)
- Für Definitions-/Erklärfragen: `data-expected-keywords` mit 2–4 Kernbegriffen
- Offen formulierte Antworten (Reflexion, eigene Begründung) bleiben **ohne** Validation — kein erzwungenes Korrektheits-Schema
- Feedback-Span (`<span class="feedback">`) immer direkt nach dem Eingabefeld
- Bei `failCount >= 2`: dezenter Verweis auf Tipp, kein Pop-up

## Verwandte ADRs

- [ADR-0010](0010-loesungs-huerde.md) — Tipp-Verweis bei wiederholten Fehlversuchen
- [ADR-0013](0013-quiz-hardening.md) — Wenn Antworten *nicht* im Source stehen sollen
- [ADR-0017](0017-save-status-toast.md) — Visueller Feedback-Stil (Farben aus Tokens)
