# ADR-0013: Quiz-Hardening — Antworten nicht im Klartext

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Quiz, Anti-Spoiler, Source-Hygiene

## Kontext

Im Boilerplate v1 stand bei Multiple-Choice-Quizzes die richtige Antwort als Klartext-Attribut im DOM:

```html
<div class="quiz-frage" data-correct="b">…</div>
```

Wer „Quelltext anzeigen" auf Smartphone oder Desktop kennt (das ist in Klasse 6 oft schon der Fall), kann die Antwort einfach ablesen. Für **Lernmaterial** ist das hinnehmbar — aber wir wollen es zumindest nicht trivial machen.

Wichtig zur Erwartungssetzung: Der Onepager ist **keine Prüfungs- und keine Test-Umgebung**. Wer wirklich umgehen will, kann immer. Ziel ist „nicht im ersten Hingucker ablesbar" — kein Krypto-Schutz.

## Entscheidung

Statt der richtigen Antwort als Klartext speichern wir einen **Hash** der erwarteten Antwort. Beim „Auswerten" hasht JS die Schüler-Eingabe und vergleicht mit dem gespeicherten Hash.

### Hash-Funktion

Wir verwenden **djb2** — ein klassischer, sehr kleiner String-Hash. Keine Krypto, aber:
- Klein (~10 Zeilen JS)
- Deterministisch
- Output als Hex-String
- Reicht völlig, um die Antwort nicht im Source ablesbar zu machen

```js
function quizHash(str) {
  // djb2-Variante mit Normalisierung
  const s = String(str).toLowerCase().trim();
  let h = 5381;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) + h) + s.charCodeAt(i);  // h*33 + c
    h = h | 0;                              // 32-bit signed
  }
  return (h >>> 0).toString(16);            // unsigned hex
}
```

### HTML-Pattern

```html
<div class="quiz-frage" data-quiz-id="q1" data-answer-hash="f7d4e2a8">
  <p>Was ist ein Prisma?</p>
  <div class="quiz-option">
    <input type="radio" name="q1" id="q1-a" data-state="q1" value="a">
    <label for="q1-a">a) Ein Körper mit nur dreieckigen Flächen.</label>
  </div>
  <div class="quiz-option">
    <input type="radio" name="q1" id="q1-b" data-state="q1" value="b">
    <label for="q1-b">b) Ein Körper mit zwei parallelen, deckungsgleichen Grundflächen.</label>
  </div>
  <div class="quiz-option">
    <input type="radio" name="q1" id="q1-c" data-state="q1" value="c">
    <label for="q1-c">c) Ein Körper, bei dem alle Kanten gleich lang sind.</label>
  </div>
  <p class="quiz-feedback" hidden>…</p>
</div>
```

`data-answer-hash` ist der Hash der **richtigen Antwort-Value** (z. B. `quizHash("b")` → `"f7d4e2a8"`).

### Hash erzeugen

Beim Schreiben eines neuen Onepagers ruft die Lehrkraft in der Browser-Konsole auf:

```js
quizHash("b")  // "f7d4e2a8"
```

Und kopiert das Ergebnis ins HTML. Das Boilerplate stellt `window.quizHash` für genau diesen Zweck bereit (kein Build-Tool nötig).

### Auswertung

```js
function checkQuiz() {
  const fragen = document.querySelectorAll('.quiz-frage');
  let punkte = 0;
  fragen.forEach(q => {
    const expected = q.dataset.answerHash;
    const chosen = q.querySelector('input[type="radio"]:checked');
    const correct = chosen && quizHash(chosen.value) === expected;
    q.classList.toggle('quiz-correct', correct);
    q.classList.toggle('quiz-wrong', chosen && !correct);
    const fb = q.querySelector('.quiz-feedback');
    if (fb) {
      fb.hidden = false;
      fb.textContent = correct
        ? 'Richtig!'
        : (chosen ? 'Noch nicht — versuche es nochmal.' : 'Bitte eine Antwort wählen.');
    }
    if (correct) punkte++;
  });
  return { punkte, gesamt: fragen.length };
}
```

### Zwei Stufen wie bei der Lösungs-Hürde

Analog zu [ADR-0010](0010-loesungs-huerde.md):

1. **Erste Auswertung** zeigt nur, *welche* Fragen richtig/falsch sind. Die richtige Antwort wird **nicht** verraten.
2. **Erst nach explizitem „Lösungen anzeigen"-Klick** (oder zweitem Auswertungs-Klick) werden die korrekten Antworten farblich markiert.

So bleiben Schüler:innen länger im aktiven Modus.

### Erweiterung: Multiple-Choice mit mehreren richtigen

Wenn eine Frage mehrere richtige Antworten hat (Checkboxes statt Radios), wird die *sortierte Liste* der korrekten Values gehasht:

```js
quizHash(["a", "c"].sort().join("|"))
```

Die JS-Auswertung tut dasselbe mit den ausgewählten Checkboxes.

## Alternativen

- **Klartext beibehalten:** Verworfen — siehe Kontext.
- **AES-Verschlüsselung mit pre-shared key:** Verworfen — Krypto-Bibliothek wäre nötig (auch wenn inline möglich), der Mehrwert ist gering, der Schlüssel müsste irgendwo im JS stehen.
- **Antworten via `fetch` von Server holen:** Verworfen — verletzt ADR-0001 (kein Backend, kein Netzwerk zur Laufzeit).
- **SHA-256 statt djb2:** Erwogen, aber `crypto.subtle.digest()` ist async, erzwingt Promise-Ketten in JS, macht den Code für Lehrer-Lesbarkeit komplexer. djb2 reicht für den Zweck.
- **base64-reverse als Obfuskierung:** Erwogen, aber trivial rückrechenbar. djb2 ist nicht umkehrbar.

## Konsequenzen

**Positiv:**
- Quiz-Antworten sind im Source nicht ohne Aufwand ablesbar
- Hash-Funktion ist klein und transparent dokumentiert
- Kein externer Bibliotheks-Bedarf
- Beim Erstellen reicht ein Konsolen-Aufruf

**Negativ / Trade-offs:**
- Pseudosicherheit: Wer den Source liest und `quizHash`-Funktion findet, kann mit jeder möglichen Antwort vergleichen. Akzeptabel — kein Prüfungsschutz beabsichtigt.
- Lehrkraft muss beim Erstellen einen extra Schritt machen (Hash erzeugen)
- Hash-Werte sind als 8-Hex-String etwas wenig „menschlich" beim Code-Review

**Folgewirkungen für künftige Onepager:**
- Kein `data-correct="..."` mehr (alt aus Boilerplate v1)
- Stattdessen `data-quiz-id` + `data-answer-hash` auf `.quiz-frage`
- Boilerplate enthält `window.quizHash` für Lehrer-Workflow
- Bei Beispiel-Quiz im Boilerplate: in einem Kommentar zeigen, wie der Hash erzeugt wurde

## Verwandte ADRs

- [ADR-0001](0001-single-file-html-architektur.md) — Keine externen Libs für Hashing
- [ADR-0010](0010-loesungs-huerde.md) — Zwei-Stufen-Reveal wird hier wiederverwendet
- [ADR-0011](0011-selbst-korrektur.md) — Selbst-Korrektur ist `data-expected` (Klartext), Quiz ist `data-answer-hash` (gehasht) — bewusste Differenz
