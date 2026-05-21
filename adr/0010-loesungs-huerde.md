# ADR-0010: Lösungs-Hürde — gestufter Reveal

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Didaktik, UX, Motivation

## Kontext

In früheren Onepagern lagen Lösungen in einem schlichten `<details><summary>Lösung anzeigen</summary>…</details>`. Ein einziger Klick reicht — und genau das ist das Problem:

- Die Hürde ist so niedrig, dass viele Schüler:innen **klicken, bevor sie rechnen**.
- Selbst kurzes Stutzen vor der Aufgabe wird übersprungen.
- Das eigentliche Lernziel — selbst überlegen, Fehler machen, korrigieren — geht verloren.

Wir brauchen eine **bewusste, kleine Hürde**, die zum Innehalten zwingt, ohne die Schüler:innen zu gängeln.

## Entscheidung

Lösungen werden **zweistufig** mit einer **Kontextprüfung** freigegeben.

### Stufe 1 — Tipp (niedrige Hürde)

Vor der eigentlichen Lösung gibt es einen **Tipp**, der einen Denkanstoß gibt, aber nicht die Lösung verrät:

```html
<button type="button" class="btn-hint" data-task-id="1.1">💡 Tipp anzeigen</button>
<div class="hint-content" data-task-id="1.1" hidden>
  Tipp: Erinnere dich an die Formel V = G · h.
</div>
```

Ein Klick zeigt den Tipp. Kein Bestätigungsdialog — das Hürdchen liegt darin, dass der/die Schüler:in den Tipp aktiv anfordert.

### Stufe 2 — Lösung (höhere Hürde mit Kontextprüfung)

Erst danach (optional) erscheint der Button für die **vollständige Lösung**:

```html
<button type="button" class="btn-solution" data-task-id="1.1">🔍 Lösung anzeigen</button>
<div class="solution-content" data-task-id="1.1" hidden>
  G = 5·3 = 15 cm² &nbsp; V = 15·4 = 60 cm³
</div>
```

Beim Klick prüft JS, ob die Eingabefelder **innerhalb der zugehörigen `.aufgabe`-Karte** (gleiches `data-task-id`) gefüllt sind:

- **Mindestens ein Feld nicht leer** → Lösung wird direkt angezeigt.
- **Alle Felder leer** → Bestätigungs-Modal:
  > „Du hast noch keine eigene Antwort eingetragen. Möchtest du die Lösung wirklich schon ansehen?"
  > [Erst probieren] [Trotzdem anzeigen]

Default-Fokus auf **„Erst probieren"** — der freundliche Stopp.

### Persistenz

Lösungs-Sichtbarkeit wird **mitgespeichert** in `localStorage` (Schema aus [ADR-0002](0002-state-persistenz-localstorage.md)):

```json
{
  "...": "...",
  "_revealed": {
    "1.1": "solution",
    "1.2": "hint"
  }
}
```

Beim Reload sind alle bereits sichtbaren Tipps/Lösungen wieder offen — Schüler:in muss nicht wieder von vorn anfangen.

### Kein `<details>` mehr

Wir verzichten ab sofort komplett auf `<details>/<summary>` für Lösungen. Begründung: zu nieder, zu nahe am „versehentlich aufgeklappt", schlecht steuerbar via JS, schlechtes Druckverhalten (siehe [ADR-0007](0007-druck-pdf-optimierung.md)).

### Druck

Im Druckbild (Lehrer-Lösungsblatt) gibt es einen URL-Parameter `?solutions=1`, der **alle** Lösungen sofort sichtbar macht. Schüler-Druck (ohne Parameter) zeigt nur was bereits aufgedeckt wurde.

## Alternativen

- **`<details>` beibehalten:** Verworfen — siehe Kontext.
- **Zeit-Gate** (Lösung erst nach z. B. 60 Sekunden): Verworfen — frustriert ohne pädagogischen Mehrwert; manche Schüler:innen brauchen länger, andere kürzer.
- **Eingabe-Pflicht** (Lösung nur freigeschaltet wenn alle Felder gefüllt): Verworfen — zu rigide, blockiert „ich weiß nicht weiter"-Fall.
- **Drei Stufen** (Tipp → Mini-Lösungsweg → vollständige Lösung): Verworfen — zu viel Klick-Choreografie für einen Onepager.
- **Reflexionsfrage als Pflicht** vor Lösung: Erwogen, aber zu viel Reibung. Stattdessen sanfter via Bestätigungsmodal.

## Konsequenzen

**Positiv:**
- Schüler:innen halten bewusst kurz inne, bevor sie die Lösung sehen
- Die Hürde ist klein genug, um nicht zu nerven, aber sichtbar genug, um Reflexion auszulösen
- Persistenz: Lösung bleibt nach Reload offen — keine doppelte Hürde
- Lehrer-Lösungsblatt-Druck via `?solutions=1` möglich

**Negativ / Trade-offs:**
- Mehr DOM und JS pro Aufgabe
- Etwas mehr Aufwand beim Schreiben neuer Aufgaben (Tipp + Lösung statt nur Lösung)

**Folgewirkungen für künftige Onepager:**
- Jede Aufgabe mit Lösung hat **Tipp + Lösung** als Doppel-Struktur
- `data-task-id` auf `.aufgabe`-Karte, `.btn-hint`, `.btn-solution`, `.hint-content`, `.solution-content` — alle gleich
- Kein `<details>` mehr für Lösungen
- Bestätigungsmodal default auf „Erst probieren"
- Im URL: `?solutions=1` deckt alle Lösungen auf (Lehrer-Druck)

## Verwandte ADRs

- [ADR-0002](0002-state-persistenz-localstorage.md) — `_revealed`-Feld im State-Schema
- [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) — Reset löscht auch `_revealed`
- [ADR-0011](0011-selbst-korrektur.md) — Nach 2 falschen Eingaben verweist Selbst-Korrektur auf „Lösung ansehen?"
- [ADR-0018](0018-aufgaben-karten.md) — `data-task-id` ist auf der Karte verortet
