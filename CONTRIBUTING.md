# Mitwirken am ADR-HTML-Onepager-Repo

Schön, dass du beitragen möchtest. Dieses Repo lebt vom Austausch zwischen Lehrer:innen, die digitale Arbeitsblätter bauen. Du musst **kein:e Softwareentwickler:in sein**, um beizutragen — gute Idee zählt mehr als perfekter Code.

## Was du beitragen kannst

### 🆕 Neues Einsatz-Profil

Du hast ein Szenario, das von den bestehenden Profilen (`profiles/`) nicht abgedeckt ist? Dann brauchen wir ein neues Profil!

Typische Beispiele, die noch fehlen könnten:
- Klausurvorbereitung / Repetitorium
- Experimentier-Protokoll (NaWi)
- Concept Map / Wissensvernetzung
- Hausaufgaben-Auftrag
- Recherche-Auftrag
- Lernportfolio über eine Einheit
- … und vieles, was du im Unterricht einsetzt

**So gehst du vor:**

1. **Issue eröffnen** mit dem Tag „Profil-Vorschlag" — beschreibe das Szenario in 5–10 Sätzen:
   - Was ist die didaktische Funktion?
   - Welche Klassenstufen/Fächer?
   - Was unterscheidet es klar von bestehenden Profilen?
2. Wir diskutieren im Issue, ob es ein eigenes Profil verdient oder eher Variante eines bestehenden ist
3. Wenn ja: kopiere [`profiles/_template.md`](profiles/_template.md), fülle es aus und sende einen Pull Request

### 🐛 Bug / Fehler / Verbesserung im Boilerplate

Hast du einen Fehler im Template gefunden? Funktioniert was nicht auf deinem Gerät? Anregung, wie das Boilerplate sauberer/besser sein könnte?

**Issue mit dem Tag „Bug"** oder „Verbesserung" eröffnen — gerne mit:
- Welcher Browser / welches Gerät?
- Schritte zum Reproduzieren
- Screenshot, wenn visuell

Bei kleinen Fixes (Typos, kleine CSS-Korrekturen) direkt einen Pull Request.

### 📋 Neue ADR vorschlagen

Du findest eine Entscheidung, die im Repo fehlt oder anders sein sollte?

**So gehst du vor:**

1. Issue mit Tag „ADR-Vorschlag" eröffnen
2. Skizziere:
   - Kontext: welches Problem soll gelöst werden?
   - Vorgeschlagene Entscheidung
   - Alternativen, die du erwogen hast
   - Konsequenzen für künftige Onepager
3. Bei Konsens: ADR nach [`adr/template.md`](adr/template.md) anlegen, nächste freie Nummer, PR

**Wichtig:** Eine ADR ist eine **bewusste, begründete Entscheidung**, kein „TODO". Wenn etwas „nett wäre", aber noch nicht durchdacht, ist es noch keine ADR.

### 💡 Andere Beiträge

- **Korrekturen in Profilen** (didaktisch oder sachlich): per PR
- **Übersetzung** in andere Sprachen: erst Issue, weil es einen größeren Scope-Wechsel bedeutet
- **Demo-Onepager** als echte Beispiele für die Profile: per PR willkommen (in einem `examples/`-Ordner)
- **Verbesserungen am `AI_GUIDE.md`** wenn du gemerkt hast, dass eine KI Probleme bei einem Schritt hat

## Wie schicke ich einen Pull Request?

Wenn dir GitHub-Workflows neu sind, ist das die Kurzversion:

1. **Forke** das Repository (Button oben rechts auf GitHub)
2. **Klone** deinen Fork lokal oder bearbeite direkt im GitHub-Web-Editor
3. **Ändere** die Dateien, die du anpassen willst
4. **Commit + Push** zurück zu deinem Fork
5. **Pull Request** vom Fork zum Hauptrepo öffnen — beschreibe kurz, was und warum

Klingt aufwändig, ist es beim ersten Mal auch — aber danach geht's schnell.

**Alternativ ohne PR:** Schreib mir per Issue, was du ändern würdest. Ich übernehme es dann gerne ins Repo.

## Stilrichtlinien

Damit das Repo konsistent bleibt:

### Sprache

- **Deutsch** in allen Dokumenten — das ist die Zielgruppe (deutschsprachige Lehrer:innen)
- Du-Form bei Anweisungen
- Geschlechtergerechte Sprache (Doppelpunkt, generisches Femininum, oder umschreibend)

### Markdown-Konventionen

- **Tabellen** dort, wo Vergleiche oder Übersichten passen
- **Code-Snippets** in ` ``` ` mit Sprachen-Tag (`html`, `css`, `js`)
- **Überschriften** sparsam, dafür ordentliche Struktur (h2 für Hauptabschnitte, h3 für Unterabschnitte)
- **Links** als Markdown-Links, relativ wenn im Repo

### ADR-Struktur

Eine ADR folgt der Vorlage in [`adr/template.md`](adr/template.md):

- Status, Datum, Betrifft
- Kontext
- Entscheidung
- Alternativen
- Konsequenzen (positiv, negativ, Folgewirkungen)
- Verwandte ADRs

### Profil-Struktur

Ein Profil folgt der Vorlage in [`profiles/_template.md`](profiles/_template.md):

- Was ist das?
- Typische Merkmale (Klassenstufe, Fach, Zeitumfang, Ziel-Typ)
- Core-ADRs mit Schwerpunkt
- Core-ADRs abweichend
- Spezifische didaktische Entscheidungen
- Empfohlene Module (Tabelle)
- Aufgaben-Pattern (HTML-Beispiel)
- Anti-Patterns
- Verwandte Profile

### Code-Stil (im Boilerplate)

- **Kein** Build-Schritt, kein TypeScript, kein Framework — Vanilla HTML/CSS/JS
- Tokens (CSS-Custom-Properties) statt Hard-Coded-Werten
- ADR-Verweise als HTML-/CSS-/JS-Kommentare nahe an den jeweiligen Code-Blöcken
- Kommentar-Fences (`/* ===== ADR-XXXX ===== */`) für optional entfernbare Module

## Was wir nicht annehmen

- **Externe CDN-Links** (verletzen [ADR-0001](adr/0001-single-file-html-architektur.md))
- **Build-Tools / npm-Abhängigkeiten** (verletzen das Single-File-Prinzip)
- **Tracking / Analytics** — Schülerdaten bleiben auf dem Gerät
- **PRs ohne Begründung** — gerne mit ein paar Sätzen, warum diese Änderung sinnvoll ist
- **Massenänderungen über das ganze Repo** ohne vorhergehenden Issue-Konsens

## Lizenz deiner Beiträge

Alle Beiträge werden unter [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de) lizenziert — der Repository-Lizenz. Mit dem Einreichen eines Pull Requests akzeptierst du das.

## Fragen?

Eröffne ein Issue mit dem Tag „Frage". Lieber einmal zu viel gefragt als am Ziel vorbei gearbeitet.

Danke fürs Beitragen 🙏
