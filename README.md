# ADR — HTML-Onepager für den Unterricht

> Bauplan und Werkzeugkasten für **interaktive HTML-Arbeitsblätter**, die per Link an Schüler:innen verteilt werden. Mit oder ohne KI nutzbar, von Lehrer:in für Lehrer:in.

[![Lizenz: CC BY 4.0](https://img.shields.io/badge/Lizenz-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/deed.de)

---

## Was ist das?

Eine **Sammlung dokumentierter Entscheidungen + ein einsatzbereites HTML-Template**, mit dem du ohne Programmierkenntnisse hochwertige digitale Arbeitsblätter bauen kannst. Schüler:innen öffnen sie als Link im Browser, ihre Eingaben werden automatisch gespeichert, alles funktioniert offline und auf jedem Gerät.

Im Repo findest du:

- 🧭 **Einsatz-Profile** für 9 typische schulische Szenarien (Lösungszettel, Arbeitsheft, Erarbeitungsseite, Lesetext, Vokabeln, …) — sie sagen dir, *welcher Aufbau zu welchem Lernziel passt*
- 📋 **Architecture Decision Records (ADRs)** — Entscheidungen über Persistenz, Druck, Barrierefreiheit, iPad-Tauglichkeit … die universell für jeden Onepager gelten
- 🎨 **Ein Boilerplate-Template** (`templates/onepager-boilerplate.html`), das alle Entscheidungen direkt umsetzt — kopieren, Inhalte einfügen, fertig
- 🤖 **KI-Workflow** (`AI_GUIDE.md`) — wenn du mit Claude, GPT oder einer anderen KI arbeitest, führt sie dich automatisch durch die richtigen Fragen

## Für wen ist das?

- **Lehrer:innen**, die digitale Arbeitsblätter bauen wollen, ohne sich in Frameworks oder Build-Pipelines zu vertiefen
- **KI-Nutzer:innen**, die einer KI ein klares Korsett geben wollen, damit das Ergebnis nicht jedes Mal anders aussieht
- **Tüftler:innen**, die die ADRs als Diskussionsgrundlage für eigene Standards nehmen wollen

---

## 5-Minuten-Schnellstart

### Mit KI (Claude, GPT, …)

1. Forke das Repo oder klone es lokal
2. Sag der KI: **„Bau mir einen HTML-Onepager nach diesem Repo."** (Falls du Claude Code/Cursor benutzt: einfach im Repo-Verzeichnis starten.)
3. Die KI fragt dich nach dem **Einsatzgebiet** und stellt Rückfragen zu Inhalt und Lernzielen
4. Du bekommst eine fertige `.html`-Datei → auf einen beliebigen Webhoster legen → Link an Schüler:innen verteilen

Hinter den Kulissen folgt die KI [`AI_GUIDE.md`](AI_GUIDE.md): erst Profil wählen, dann Boilerplate anpassen, dann Inhalte einfüllen.

### Ohne KI (manuell)

1. **Profil wählen** aus [`profiles/`](profiles/) — z. B. „Lösungszettel" wenn du Schulbuch-Aufgaben begleitest, „Arbeitsheft" wenn die Schüler:innen am iPad mit Stift schreiben
2. **Boilerplate kopieren**: [`templates/onepager-boilerplate.html`](templates/onepager-boilerplate.html) in eine neue Datei
3. **Drei Stellen anpassen**:
   - `ONEPAGER_SLUG = 'bruchrechnen-kl6-01'` (eindeutiger Name, keine Leerzeichen)
   - `<title>` und `<h1>` mit deinem Onepager-Titel
   - UE-Label („Mathe · Klasse 6 · Einheit 3 von 9")
4. **Aufgaben einfügen** nach dem Pattern aus deinem Profil (Beispiele direkt im Profil-Dokument)
5. **Veröffentlichen**: [`CHECKLIST.md`](CHECKLIST.md) durchgehen, Datei auf Webhoster legen, Link verteilen

---

## Was die Onepager können

| Feature | Default | Profil-abhängig |
|---|---|---|
| 💾 **Auto-Save** in localStorage | ✅ | |
| 📂 **JSON-Export/Import** für Geräte-Wechsel | ✅ | |
| 📎 **HTML-Export** (selbsttragend, mit allen Antworten eingebettet) | ✅ | |
| 🔄 **Reset** mit Bestätigungsdialog | ✅ | |
| 📱 **iOS-Safe-Area** (kein abgeschnittenes Menü unter Notch) | ✅ | |
| 🌓 **Dark Mode** (folgt System) | ✅ | |
| ♿ **Barrierearm** (Tastatur, Screenreader, prefers-reduced-motion) | ✅ | |
| 🖨 **A4-Druck-Vorschau** + sauberer Druck mit Seitenumbrüchen | ✅ | |
| 🔍 **Gestufter Lösungs-Reveal** (Tipp → Lösung mit Bestätigung) | ✅ | Lösungszettel: schärfer (Cipher) |
| ✓ **Selbst-Korrektur** numerischer Antworten und mit Keywords | ✅ | |
| 📊 **Fortschrittsbalken** für lange Onepager | ✅ | |
| 🎯 **Quiz** mit gehashten Antworten (kein Spoiler im Source) | ✅ | |
| ✏️ **Canvas-Stift-Eingabe** (Apple Pencil + Maus + Touch) | ✅ | Arbeitsheft: zentral |
| 📄 **PDF-Export** (für GoodNotes, mit korrekten A4-Umbrüchen) | Snippet | |

---

## Die 21 Einsatz-Profile

| Profil | Wofür |
|---|---|
| [Lösungszettel](profiles/loesungszettel.md) | Schüler arbeiten am Buch, Onepager liefert Hilfen und prüft Lösung. Anti-Spoiler via XOR-Cipher: Lösungserklärung erscheint nur bei richtiger Eingabe. |
| [Digitales Arbeitsheft](profiles/digitales-arbeitsheft.md) | iPad mit Apple Pencil, großzügige Canvas-Schreibflächen pro Aufgabe. Lineatur, Karo oder leer. Save besonders prominent. |
| [Erarbeitungsseite](profiles/erarbeitungsseite.md) | Strukturierter Lernpfad: Vorwissen → Erarbeitung → Übung → Vertiefung → Quiz. Sektionen werden nacheinander freigeschaltet. |
| [Reflexionstagebuch](profiles/reflexionstagebuch.md) | Metakognition: offene Reflexionen, Smiley-Skalen, keine Korrektur. Privatsphäre-Hinweis. |
| [Stationenlernen-Station](profiles/stationenlernen.md) | Eine kompakte Station eines Lernzirkels. Passt auf eine A4-Seite, max. 15 Min Bearbeitungszeit. |
| [Lese-/Verständnistext](profiles/lesetext.md) | Sachtext oder Quelle als Hauptelement, mit Zeilennummern und gemischten Antwortformaten (Zitat, Analyse, Stellungnahme). |
| [Differenzierungs-Onepager](profiles/differenzierung.md) | Drei Niveaus (★/★★/★★★) als Tabs. Gleicher Inhalt, drei Anforderungsgrade. Schüler:in wählt selbst. |
| [Kompetenzraster](profiles/kompetenzraster.md) | „Ich kann …"-Aussagen mit 4er-Skala (Smileys). Pre/Post-Vergleich über eine Einheit hinweg. |
| [Vokabel-/Wortschatz](profiles/vokabeln.md) | Karteikarten mit Flip-Mechanik, „kann ich"-Marker, Filter, Shuffle. Smartphone-tauglich. |
| [Hausaufgaben-Auftrag](profiles/hausaufgaben.md) | Strukturierte HA mit Datum-Feldern und Abgabe-Hinweis. HTML-Export für Lehrer-Übergabe. |
| [Klausurvorbereitung](profiles/klausurvorbereitung.md) | Repetitorium mit Themen-Tags und Schwierigkeitsgrad-Markern. Fortschritt pro Thema, nicht global. |
| [Recherche-Auftrag](profiles/recherche.md) | 5-Schritt-Recherche: Forschungsfrage → Quellen → Notizen → Synthese → Fazit. Quellenkritik-Hilfen. |
| [Lektüre-/Buchtagebuch](profiles/lektuere.md) | Begleiter zu einem ganzen Buch über Wochen. Kapitelweise Einträge mit Zitaten und Reflexionen. |
| [Methoden-/Strategien](profiles/methoden.md) | Lernmethode erklären + anwenden + reflektieren (z. B. SQ3R, Mindmap, Pomodoro). Inkl. Methoden-Karte zum Drucken. |
| [Concept Map / Mindmap](profiles/concept-map.md) | Vorgegebene Begriffe per drag-and-drop platzieren, mit dem Stift verbinden. Wissens-Vernetzung. |
| [Flipped Classroom](profiles/flipped-classroom.md) | Video + Aufgaben dazu. Vorbereitung zu Hause, Diskussion in der Stunde. YouTube-nocookie oder lokales mp4. |
| [Lerntheke](profiles/lerntheke.md) | Aufgaben-Pool mit Pflicht/Wahl/Vertiefung-Markern. Schüler:in wählt Reihenfolge selbst, Filter-Toolbar. |
| [Code-Übungen (Informatik)](profiles/code-uebung.md) | Code-Lesen mit Syntax-Highlighting, Code-Eingabe, Live-Preview für HTML/CSS, externe Sandboxen für Python/JS. |
| [Statistik / Datenanalyse](profiles/statistik.md) | Eingebettete Datentabelle, Inline-SVG-Säulendiagramm, numerische Selbst-Korrektur mit Toleranz. |
| [Lernportfolio (Advanced)](profiles/lernportfolio.md) | Langzeit-Sammelmappe über Wochen/Monate. ⚠️ Listen-Persistenz noch nicht implementiert. |
| [Worked Examples](profiles/worked-examples.md) | Lösungsbeispiel-Methode (Sweller): Beispiel → faded Aufgabe → analoge Aufgabe. Forschungsbasiert (Cognitive Load Theory). Besonders für Anfänger:innen wirksam. |

Jedes Profil ist eine eigene Markdown-Datei mit konkreten Beispielen, empfohlenen Modulen und Anti-Patterns.

> 📊 **Detaillierter Vergleich aller Profile**: [`profiles/UEBERSICHT.md`](profiles/UEBERSICHT.md) — mit Tabellen für Kontext (Klassenstufe/Fach/Zeit/Gerät), Mechaniken (welche Module), Entscheidungshilfe („Welches Profil nehme ich?"), Anti-Kombinationen und sinnvollen Profil-Mischungen.

---

## Was du im Repo findest

```
adr/                  Architecture Decision Records (universell)
profiles/             Einsatz-Profile (style-guide-artig)
templates/
  onepager-boilerplate.html    fertiges Template
  snippets/                    optionale Erweiterungs-Snippets
examples/             Echte Beispiel-Onepager pro Profil
tools/
  lehrer-aggregator.html       JSON-Exporte mehrerer Schüler zusammenführen
AI_GUIDE.md           Workflow für KI-Assistenten
CHECKLIST.md          Vor-Veröffentlichung-Checkliste
CONTRIBUTING.md       Wenn du beitragen willst
LICENSE               CC BY 4.0
```

## Beispiel-Onepager und Tools

Voll funktionsfähige Demos zum Anschauen und Kopieren:

| Demo | Profil | Was es zeigt |
|---|---|---|
| [loesungszettel-bruchrechnen-kl7](examples/loesungszettel-bruchrechnen-kl7.html) | Lösungszettel | XOR-Cipher: Lösung erscheint nur bei richtiger Antwort |
| [erarbeitungsseite-photosynthese-kl8](examples/erarbeitungsseite-photosynthese-kl8.html) | Erarbeitungsseite | 5-Phasen-Lernpfad mit Gating und Quiz |
| [arbeitsheft-geometrie-kl7](examples/arbeitsheft-geometrie-kl7.html) | Digitales Arbeitsheft | Canvas-Stift-Eingabe für Konstruktionen |
| [worked-example-flaechenberechnung-kl6](examples/worked-example-flaechenberechnung-kl6.html) | Worked Examples | Drei-Stufen-Sequenz nach Sweller (Beispiel → Faded → Analog) |
| [vokabeln-englisch-unit3](examples/vokabeln-englisch-unit3.html) | Vokabeln | Karteikarten-Flip, Marker, Filter, Shuffle |
| [differenzierung-prozentrechnung-kl7](examples/differenzierung-prozentrechnung-kl7.html) | Differenzierung | Drei Niveaus (★/★★/★★★) als Tabs |
| [lerntheke-bruchrechnen-kl7](examples/lerntheke-bruchrechnen-kl7.html) | Lerntheke | Aufgaben-Pool mit Pflicht/Wahl/Vertiefung + Filter |
| [reflexionstagebuch-woche](examples/reflexionstagebuch-woche.html) | Reflexionstagebuch | Textareas + Smiley-Skalen, keine Korrektur |
| [statistik-noten-kl7](examples/statistik-noten-kl7.html) | Statistik | Datentabelle mit Inline-SVG-Säulendiagramm |
| [kompetenzraster-prismen-kl8](examples/kompetenzraster-prismen-kl8.html) | Kompetenzraster | „Ich kann…"-Tabelle mit Pre/Post-Vergleich |
| [code-uebung-python-kl9](examples/code-uebung-python-kl9.html) | Code-Übungen | Python: Code lesen, vorhersagen, schreiben |
| [lesetext-bienen-kl7](examples/lesetext-bienen-kl7.html) | Lese-/Verständnistext | Sachtext mit Zeilennummern + gemischte Antwortformate |
| [hausaufgaben-mathe-kl6](examples/hausaufgaben-mathe-kl6.html) | Hausaufgaben-Auftrag | Multiplikation mit Zehnerzahlen, mit Datum-Abgabe |
| [klausurvorbereitung-mathe-kl8](examples/klausurvorbereitung-mathe-kl8.html) | Klausurvorbereitung | Themen-Filter + Schwierigkeitsgrad-Marker |
| [recherche-klimawandel-kl9](examples/recherche-klimawandel-kl9.html) | Recherche-Auftrag | 5-Phasen-Recherche mit Quellen-Karten und URL-Preview |
| [methoden-sq3r-kl8](examples/methoden-sq3r-kl8.html) | Methoden-Onepager | SQ3R-Lesemethode mit druckbarer Methoden-Karte |
| [stationenlernen-bruchrechnen-station3](examples/stationenlernen-bruchrechnen-station3.html) | Stationenlernen | Kompakte Station eines Bruchrechnungs-Zirkels |
| [lektuere-besuch-alte-dame](examples/lektuere-besuch-alte-dame.html) | Lektüre-Tagebuch | Dürrenmatt — Kapitel-Sektionen mit Figurenanalyse |
| [concept-map-photosynthese-kl8](examples/concept-map-photosynthese-kl8.html) | Concept Map | Drag-and-drop-Knoten mit Stift-Verbindungen |
| [flipped-classroom-bruchrechnen-kl6](examples/flipped-classroom-bruchrechnen-kl6.html) | Flipped Classroom | Video-basierte Stunden-Vorbereitung |
| [lernportfolio-halbjahr](examples/lernportfolio-halbjahr.html) | Lernportfolio (Skizze) | Halbjahres-Sammelmappe mit festen Slots |

Plus das **Lehrer-Auswertungs-Tool**:

- [tools/lehrer-aggregator.html](tools/lehrer-aggregator.html) — Standalone-HTML, mehrere JSON/HTML-Exporte einsammeln und aggregiert auswerten (Häufigkeiten, freie Antworten, Canvas-Galerie). Privacy: alles client-side, kein Server.

Drei Schichten Trennen Verantwortung:

```
Core-ADRs        ← gelten immer, für jeden Onepager
   ↓
Einsatz-Profile  ← gewichten die ADRs für eine konkrete Domäne
   ↓
Konkreter Onepager ← deine fertige .html-Datei
```

Details: [ADR-0024 Schichten-Modell](adr/0024-schichten-modell-profile.md).

---

## Mitwirken

Vorschläge, Korrekturen, neue Profile, neue Patterns — alles willkommen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

Du musst kein:e Softwareentwickler:in sein. Lehrer:innen, die ihre eigenen didaktischen Patterns beisteuern wollen, sind besonders willkommen.

---

## Tiefere Doku

### Alle Architecture Decision Records

| Nr. | Titel | Status |
|---|---|---|
| [0001](adr/0001-single-file-html-architektur.md) | Single-File-HTML-Architektur | Accepted |
| [0002](adr/0002-state-persistenz-localstorage.md) | State-Persistenz im localStorage | Accepted |
| [0003](adr/0003-json-export-import.md) | JSON-Export und -Import für Schülerergebnisse | Accepted |
| [0004](adr/0004-reset-funktion-mit-bestaetigung.md) | Reset-Funktion mit Bestätigungsdialog | Accepted |
| [0005](adr/0005-sticky-menue-ios-safe-area.md) | Sticky Top-Menü mit iOS Safe-Area-Beachtung | Accepted |
| [0006](adr/0006-responsives-layout.md) | Responsives Mobile-First-Layout | Accepted |
| [0007](adr/0007-druck-pdf-optimierung.md) | Druck- und PDF-Optimierung (A4) | Accepted |
| [0008](adr/0008-design-system.md) | Konsistentes Design-System | Superseded by [0022](adr/0022-design-system-v2.md) |
| [0009](adr/0009-barrierefreiheit-lesbarkeit.md) | Barrierefreiheit und Lesbarkeit | Accepted |
| [0010](adr/0010-loesungs-huerde.md) | Lösungs-Hürde (gestufter Reveal: Tipp + Lösung) | Accepted |
| [0011](adr/0011-selbst-korrektur.md) | Selbst-Korrektur statt nur Lösungsvergleich | Accepted |
| [0012](adr/0012-gamification.md) | Gamification (sanft, nicht-kompetitiv) | Accepted |
| [0013](adr/0013-quiz-hardening.md) | Quiz-Hardening (Antworten nicht im Klartext) | Accepted |
| [0015](adr/0015-inhalts-boxen.md) | Inhalts-Boxen (Merke, Tipp, Achtung …) | Accepted |
| [0017](adr/0017-save-status-toast.md) | Save-Status-Indikator und Toast-Feedback | Accepted |
| [0018](adr/0018-aufgaben-karten.md) | Aufgaben-Karten — visuelle Struktur | Accepted |
| [0019](adr/0019-canvas-stift-modul.md) | Canvas-Stift-Modul (Pointer-Events, Apple Pencil) | Accepted |
| [0020](adr/0020-html-export-eingebetteter-state.md) | HTML-Export mit eingebettetem State | Accepted |
| [0021](adr/0021-pdf-export-inline.md) | PDF-Export mit inline html2canvas + jsPDF | Accepted |
| [0022](adr/0022-design-system-v2.md) | Aktualisiertes Design-System (Editorial) | Accepted |
| [0023](adr/0023-a4-druck-und-preview.md) | A4-Druck-Layout und A4-Preview-Modus | Accepted |
| [0024](adr/0024-schichten-modell-profile.md) | Schichten-Modell: Core-ADRs + Einsatz-Profile (Meta) | Accepted |
| [0026](adr/0026-tabellen-eingaben.md) | Tabellen-Eingaben (editierbare Tabellen) | Accepted |
| [0027](adr/0027-datum-zeit-eingaben.md) | Datum/Zeit-Eingaben | Accepted |
| [0028](adr/0028-worked-examples.md) | Worked-Examples-Pattern (Lösungsbeispiele nach Sweller) | Accepted |

| Status | Bedeutung |
|---|---|
| **Accepted** | Aktiv gültig, wird angewendet |
| **Proposed** | Vorgeschlagen, noch nicht endgültig |
| **Superseded by ADR-XXXX** | Durch neuere Entscheidung ersetzt |

### URL-Parameter, die jeder Onepager versteht

| Parameter | Wirkung |
|---|---|
| `?layout=a4` | A4-Druck-Vorschau auf dem Bildschirm (was du siehst, ist was aus dem Drucker kommt) |
| `?solutions=1` | Lehrer-Modus: alle Tipps und Lösungen sofort sichtbar (für Lehrer-Lösungsblatt-Druck) |

Lassen sich kombinieren: `?layout=a4&solutions=1` → druckfertiges Lehrer-Lösungsblatt.

### Neue ADR oder neues Profil anlegen

- **ADR**: [`adr/template.md`](adr/template.md) kopieren → nächste freie Nummer → in die Übersicht oben ergänzen
- **Profil**: [`profiles/_template.md`](profiles/_template.md) kopieren → Slug vergeben → in `AI_GUIDE.md` und README-Tabelle ergänzen

---

## Lizenz

Creative Commons Namensnennung 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de)).

Du darfst die Inhalte teilen, anpassen und auch kommerziell nutzen — solange du die ursprüngliche Quelle nennst. Siehe [LICENSE](LICENSE) für den vollständigen Text.
