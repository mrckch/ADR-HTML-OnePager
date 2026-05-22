# AI_GUIDE — KI-Workflow für dieses Repository

Dieses Dokument richtet sich an **KI-Assistenten** (z. B. Claude, GPT, lokale LLMs), die einen Onepager mit diesem Repository erstellen sollen. Es beschreibt den festen Ablauf, damit jeder generierte Onepager zur Kombination aus Core-Entscheidungen und domänenspezifischen Patterns passt.

Der Workflow basiert auf [ADR-0024](adr/0024-schichten-modell-profile.md) (Schichten-Modell).

---

## Workflow für KI-Assistenten

### Schritt 1 — Einsatzgebiet erfragen

**Bevor irgendetwas anderes passiert**, frage die Lehrkraft nach dem Einsatzgebiet. Beispiel-Formulierung:

> Bevor wir den Onepager bauen — welchen Einsatzfall hast du im Kopf?
>
> - **Lösungszettel zum Schulbuch** — Schüler arbeiten mit Buch, Onepager liefert Hilfen und Selbst-Kontrolle
> - **Digitales Arbeitsheft** — Aufgaben mit großzügigen Schreibflächen, Bearbeitung am iPad mit Stift
> - **Erarbeitungsseite** — Lernpfad: Vorwissen → Erarbeitung → Übung → Vertiefung → Quiz
> - … (weitere aus `profiles/`)
> - **Etwas anderes** — beschreib's mir, wir prüfen gemeinsam

Die Liste der verfügbaren Profile kannst du dem Verzeichnis `profiles/` entnehmen (alle `.md`-Dateien außer `_template.md`).

### Schritt 2 — Profil lesen

Sobald das Einsatzgebiet feststeht, lies das passende Profil aus `profiles/<slug>.md` vollständig. Achte besonders auf:

- **Core-ADRs mit Schwerpunkt** — Patterns, die hier besonders zentral sind
- **Core-ADRs abweichend oder weniger relevant** — was hier nicht oder anders gilt
- **Spezifische didaktische Entscheidungen** — Punkte, die nur in diesem Profil dokumentiert sind
- **Empfohlene Module** — was aktiviert/deaktiviert sein sollte
- **Aufgaben-Pattern** — das domänen-typische HTML-Muster
- **Anti-Patterns** — was vermeiden

### Schritt 3 — Core-ADRs verfolgen

Lies die im Profil referenzierten Core-ADRs (`adr/00XX-…md`). Die Profile verweisen, statt zu duplizieren — der Detailgehalt steht in den ADRs.

Default-Annahme, wenn ein Profil schweigt: **die Core-ADRs gelten unverändert.**

### Schritt 4 — Boilerplate als Basis

Starte mit `templates/onepager-boilerplate.html`. Es ist profil-neutral und enthält die universellen Module (localStorage, Save-Status, Toast, Reset-Dialog, A4-Druck, Print-Layout, …).

Passe es an das Profil an:

- **Sektionen ergänzen oder entfernen** (z. B. Lernziel-Box weglassen, wenn das Profil sie nicht braucht)
- **Module aktivieren/deaktivieren** (z. B. Quiz-Block raus, wenn Profil kein Quiz vorsieht)
- **Konstanten setzen**: `ONEPAGER_SLUG`, Titel, UE-Label, Datum
- **Aufgaben einbauen** nach dem Profil-Pattern
- **Profil-spezifische Helper-Snippets** einbinden, falls das Profil welche definiert (z. B. Lösungs-Cipher im Lösungszettel-Profil)

### Schritt 5 — Profilspezifische Patterns anwenden

Wenn das Profil zusätzliche Patterns vorsieht, die nicht im Boilerplate enthalten sind (z. B. Gating-Modul für Erarbeitungsseite, Lösungs-Cipher für Lösungszettel), füge die entsprechenden Snippets ein. Diese sind im jeweiligen Profil als Code-Block dokumentiert.

### Schritt 6 — Inhalte einfüllen

Erst jetzt geht es um die fachlichen Inhalte (Aufgaben, Tipps, Lösungen, Lernziele). Halte dich an die Aufgaben-Pattern des Profils.

### Schritt 7 — Selbst-Check gegen CHECKLIST.md

Bevor du das Ergebnis abgibst, lies `CHECKLIST.md` und prüfe Punkte automatisch durch, soweit möglich:

- Profil-Konformität (Abschnitt 0)
- Standard-Quality-Gates (Abschnitte 1–8)

Wenn ein Punkt nicht eindeutig erfüllt ist, flagge ihn explizit der Lehrkraft.

---

## Regeln für KI-Assistenten

### Was du tun solltest

- **Immer** Schritt 1 (Einsatzgebiet erfragen) durchführen — auch wenn die Lehrkraft direkt mit dem Inhalt loslegt
- Bei Unklarheit zwischen zwei Profilen: **fragen**, nicht raten
- Profile sind **empfehlend**, nicht zwingend (siehe [ADR-0024](adr/0024-schichten-modell-profile.md)). Wenn ein Abweichen sinnvoll erscheint: das **explizit ansprechen**, nicht heimlich abweichen
- ADR-Verweise im generierten Code als Kommentare beibehalten (z. B. `<!-- ADR-0018: Aufgaben-Karte -->`) — das hilft beim späteren Lesen
- Eindeutiger `ONEPAGER_SLUG` für jeden neuen Onepager (z. B. `bruchrechnen-kl6-01`)

### Was du nicht tun solltest

- **Nicht** einfach das Boilerplate ungefiltert ausliefern und „füll die Aufgaben ein" sagen
- **Nicht** Core-ADRs durch Profile außer Kraft setzen — Profile dürfen nur neu gewichten
- **Nicht** Lösungen im Klartext im DOM ablegen, wenn das gewählte Profil Anti-Spoiler vorsieht (Lösungszettel-Profil)
- **Nicht** externe CDN-Links einfügen (ADR-0001)
- **Nicht** auf eigene Faust neue Patterns erfinden — wenn etwas fehlt: das **als ADR/Profil-Vorschlag** an die Lehrkraft melden

---

## Wenn das passende Profil fehlt

Wenn die Lehrkraft einen Einsatz beschreibt, der zu keinem bestehenden Profil passt:

1. **Vorschlagen, ein neues Profil zu schreiben** (`profiles/<neuer-slug>.md` nach `profiles/_template.md`)
2. Für den aktuellen Onepager: das **am nächsten passende Profil** als Basis nehmen und die Abweichungen direkt mit der Lehrkraft besprechen
3. Die Abweichungen anschließend in einen Profil-Entwurf gießen — Material für die nächste Iteration

---

## Liste der aktuellen Profile

Diese Liste wird automatisch aus `profiles/` gepflegt — beim Lesen prüfe immer dort, ob neue dazugekommen sind.

- [`profiles/loesungszettel.md`](profiles/loesungszettel.md) — Lösungs-Begleiter zu einem gedruckten Schulbuch
- [`profiles/digitales-arbeitsheft.md`](profiles/digitales-arbeitsheft.md) — iPad-Arbeitsblatt mit Stift-Eingabe
- [`profiles/erarbeitungsseite.md`](profiles/erarbeitungsseite.md) — Lernpfad mit Gating: Vorwissen → Erarbeitung → Übung → Quiz

---

## Quick-Reference für menschliche Lehrkräfte

Falls du selbst (ohne KI) einen Onepager baust:

1. Lies das passende Profil aus `profiles/`
2. Kopiere `templates/onepager-boilerplate.html`
3. Setze `ONEPAGER_SLUG`, Titel, UE-Label
4. Füge Lernziele, Aufgaben, Hilfen, Lösungen nach dem Profil-Pattern ein
5. Vor Veröffentlichung: `CHECKLIST.md` durchgehen
6. Mit `?layout=a4` Druck prüfen, mit `?solutions=1` Lehrer-Lösungsblatt
