# Profil: Beamer-Präsentation

- **Status:** Accepted
- **Datum:** 2026-11-17
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

> 📽️ **Dritte Variante** — nutzt [`templates/praesentation-boilerplate.html`](../templates/praesentation-boilerplate.html), **nicht** `onepager-boilerplate.html` und **nicht** `infoseite-boilerplate.html`. Grundlage: [ADR-0032](../adr/0032-praesentations-variante.md). Design: **v3 „Signal"** ([ADR-0031](../adr/0031-design-system-v3-signal.md)), nicht v2.

## Was ist das?

Ein **Foliensatz für die Projektion an die Wand** — lehrerzentriert. Die Lehrkraft steuert, die Klasse schaut und spricht. Genau eine Folie ist sichtbar, geblättert wird mit Pfeiltasten, Presenter-Clicker oder Klick; Inhalte lassen sich **schrittweise aufdecken**.

Im Unterschied zu allen anderen Profilen ist das Medium nicht Papier und nicht das Tablet in Schülerhand, sondern eine **4 bis 10 Meter entfernte Leinwand**. Das verändert fast alles: Schriftgrad, Kontrast, Informationsdichte, Navigation und Druck-Ziel.

Typische Einsätze:
- **Einführung eines neuen Themas** — Impuls, Begriffsklärung, Herleitung schrittweise entwickeln
- **Erklär- und Mustersequenz** — Rechenweg oder Verfahren Schritt für Schritt vorne vorführen
- **Besprechung** — Hausaufgaben, Klassenarbeit, Lösungen gemeinsam durchgehen
- **Stundenregie** — Agenda, Arbeitsaufträge, Timer für Arbeitsphasen, Ergebnissicherung
- **Vortrag außerhalb des Unterrichts** — Elternabend, Fachkonferenz, Fortbildung

## Typische Merkmale

- **Klassenstufe:** alle; ebenso für Erwachsenen-Publikum (Elternabend, Kollegium)
- **Fachbereich:** fächerübergreifend; besonders stark, wo etwas **entwickelt** wird (Mathematik, Naturwissenschaften, Grammatik)
- **Zeitumfang:** eine Phase bis zur Doppelstunde; typisch 8–25 Folien
- **Ziel-Typ:** Erarbeitung im Plenum / Erklärung / Besprechung / Stundenregie
- **Gerät:** **Beamer oder Panel** (16:9 oder 4:3), gesteuert von Laptop oder Tablet; Druck als **Handout**

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0032](../adr/0032-praesentations-variante.md) | **Definiert dieses Profil** — Folien-Geometrie, Navigation, Schritt-Aufdecken, Handout-Druck |
| [ADR-0031](../adr/0031-design-system-v3-signal.md) | Design-System **v3 „Signal"** — kräftige Flächen und harte Kontraste überleben einen Beamer im hellen Raum |
| [ADR-0009](../adr/0009-barrierefreiheit-lesbarkeit.md) | Neu gelesen als **Lesbarkeit aus der letzten Reihe**; außerdem vollständige Tastatursteuerung — am Beamer ist die Tastatur das Hauptbedienmittel |
| [ADR-0019](../adr/0019-canvas-stift-modul.md) | Stift als **transparentes Overlay über der Folie** — Tafelanschrift auf der Projektion |
| [ADR-0015](../adr/0015-inhalts-boxen.md) | Boxen (Merke/Info/Tipp/Warn) in Projektionsgröße — das zentrale Strukturmittel innerhalb einer Folie |
| [ADR-0001](../adr/0001-single-file-html-architektur.md) | Eine Datei läuft auf **jedem** Schulrechner — kein Konto, kein Netz, keine Installation, keine PowerPoint-Version |

## Core-ADRs abweichend oder weniger relevant

- **ADR-0022 (Design-System v2):** gilt hier **nicht** — Projektion läuft auf v3 „Signal" ([ADR-0031](../adr/0031-design-system-v3-signal.md)). Kein Mischen: keine Navy/Gold-Elemente im Foliensatz.
- **ADR-0022/0031 (Dark-Mode-Automatik):** bewusst abgeschaltet. Der Foliensatz startet **hell**, unabhängig vom OS; `t` schaltet auf dunkel oder hohen Kontrast ([ADR-0032](../adr/0032-praesentations-variante.md), Entscheidung 7).
- **ADR-0007/0023 (A4-Druck):** bleiben in Kraft, aber das Druck-Ziel ist ein **Handout** — `data-handout="notizen"` (Folie plus Notizenspalte, ca. 3 pro Seite) oder `"kompakt"` (zweispaltig, ca. 8 pro Seite) —, nicht die Folie selbst.
- **ADR-0005 (Sticky-Topbar):** entfällt — eine Steuerleiste blendet sich nach wenigen Sekunden aus, statt dauerhaft Projektionsfläche zu kosten.
- **ADR-0002/0003/0004/0017/0020 (Persistenz-Lage):** entfallen komplett. Position steht im URL-Hash, sonst wird nichts gespeichert (Ausnahme: gewähltes Thema in `sessionStorage`).
- **ADR-0010/0011/0012/0013/0018/0025/0026/0027 (Aufgaben- und Eingabe-Mechaniken):** entfallen. Keine Eingabefelder, keine Punkte, keine gehashten Quizantworten — die Klasse antwortet mündlich.

## Spezifische didaktische Entscheidungen

1. **Ein Gedanke pro Folie, maximal ~6 Zeilen.** Die Folie ist Projektionsfläche, nicht Skript. Was mehr Text braucht, gehört in die Notizen oder ins Handout.
2. **Nie vorlesen, was dasteht.** Mayers Redundanzprinzip: gleichzeitig identischen Text lesen und hören kostet Verstehensleistung. Die Folie zeigt den **Anker** (Begriff, Formel, Bild, Zahl), gesprochen wird die Erklärung.
3. **Schrittweise aufdecken statt fertige Folie.** Herleitungen, Tabellenzeilen und Lösungen erscheinen einzeln — das hält das Tempo beim Denken der Klasse, nicht beim Lesen.
4. **Frage vor Antwort.** Die Lösung ist immer ein eigener `.schritt`: fragen, Antworten sammeln, dann aufdecken. Das ist die Plenums-Variante der Lösungs-Hürde.
5. **Agenda-Folie als Stundentransparenz.** Nach der Titelfolie der Stundenverlauf; Kapitel-Trennfolien markieren später, wo man ist.
6. **Folien-Nummer sichtbar lassen.** „Schaut noch mal auf Folie 7" ist im Unterricht ständig nötig — und verlinkbar als `#/7`.
7. **Timer-Folie für Arbeitsphasen.** Ein großer Countdown vorne an der Wand strukturiert Gruppen- und Partnerarbeit besser als jede Ansage.
8. **Stift-Overlay statt Tafelwechsel.** In die projizierte Zeichnung hineinschreiben: Hilfslinien an die Skizze, Ergebnis an die Formel, Fehler markieren. Verschwindet beim Reload — es ist Tafelanschrift, kein Dokument.
9. **Handout mit Notizenspalte** erzeugen, wenn die Klasse mitschreiben soll. Dann darf die Folie knapp bleiben, weil das Papier den Platz hat.
10. **Blackout (`b`) kennen und nutzen.** Schwarze Fläche, wenn die Aufmerksamkeit nach vorn zu dir soll — wirksamer als jede Aufforderung.
11. **Vor der Stunde einmal aus der letzten Reihe anschauen.** Der einzige verlässliche Lesbarkeitstest.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Titelfolie (Thema, Fach/Klasse, Datum) | **ja** |
| Agenda-/Stundenverlaufs-Folie | ja |
| Kapitel-Trennfolien | ja (ab ~12 Folien) |
| Schrittweises Aufdecken (`.schritt`) | **ja, zentral** |
| Inhalts-Boxen (Merke/Info/Tipp/Warn) | **ja** |
| Folien-Nummer + Fortschrittsbalken | ja (dezent) |
| Referenten-Notizen (`.notizen`) | ja |
| Folien-Übersicht zum Springen (`o`) | ja |
| Blackout / Whiteout (`b` / `w`) | ja |
| Themen-Umschalter hell/dunkel/Kontrast (`t`) | **ja** |
| Stift-Overlay (`z`) | ja — unverzichtbar in Mathematik/NW |
| Timer-Folie (`data-timer`) | optional, oft nützlich |
| Impuls-/Vollflächen-Folie | optional |
| Handout-Druck (`data-handout`) | **ja** |
| Tastenhilfe (`?`) | ja |
| Lernziel-Box | optional (als Agenda-Variante) |
| Aufgaben-Karten | **nein** (keine Schülereingaben) |
| Selbst-Korrektur (`data-expected`) | **nein** |
| Lösungs-Hürde als Schüler-Button | **nein** — stattdessen `.schritt` |
| Quiz mit gehashten Antworten | **nein** — mündlich im Plenum |
| Fortschritts-/Punkte-Gamification | **nein** |
| Save-Status, Toast, Reset, JSON-/HTML-Export | **nein** |
| localStorage | **nein** |

## Folien-Pattern (typisch)

Kein `.aufgabe`-Block, sondern Folien mit Inhaltsschritten und Notizen:

```html
<!-- Titelfolie: Marken-Fläche, ADR-0031 -->
<section class="folie folie--titel">
  <div class="folie__inhalt">
    <span class="eyebrow">Mathematik · Klasse 8</span>
    <h1>Oberfläche von Prismen</h1>
    <p class="folie__lead">Warum zwei Grundflächen und ein Mantel reichen</p>
  </div>
</section>

<!-- Erarbeitungsfolie mit Schritt-Aufdecken (ADR-0032, Entscheidung 5) -->
<section class="folie" data-schritte>
  <div class="folie__inhalt">
    <span class="kicker">Herleitung</span>
    <h2>Woraus besteht die Oberfläche?</h2>
    <ul class="liste">
      <li class="schritt">zwei <b>Grundflächen</b> — oben und unten, deckungsgleich</li>
      <li class="schritt">ein <b>Mantel</b> — alle Seitenflächen zusammen</li>
    </ul>
    <p class="formel schritt">O = 2 · G + M</p>
    <div class="box box--merke schritt">
      <span class="box__titel">Merke</span>
      <p>Der Mantel ist ein Rechteck: Umfang der Grundfläche × Höhe.</p>
    </div>
  </div>
  <aside class="notizen">
    Erst fragen lassen: „Was sehen wir, wenn wir das Prisma aufschneiden?" —
    Netz an der Tafel skizzieren, dann Schritt 3 aufdecken.
  </aside>
</section>

<!-- Timer-Folie für die Arbeitsphase -->
<section class="folie folie--timer" data-timer="5">
  <div class="folie__inhalt">
    <span class="kicker">Partnerarbeit</span>
    <h2>Berechnet die Oberfläche von Prisma B</h2>
    <p class="timer__anzeige" aria-live="off">05:00</p>
  </div>
</section>
```

## Anti-Patterns

- **Stichpunkt-Tapete** — zehn Zeilen Text pro Folie: aus der letzten Reihe unlesbar, und niemand hört dir zu, solange gelesen wird.
- **Folien vorlesen** — Redundanzprinzip; die Folie zeigt den Anker, du lieferst die Erklärung.
- **Scrollen statt Blättern** — wenn der Inhalt einer Folie scrollen muss, ist es zu viel: aufteilen.
- **Dark Mode als Default** — im hellen Klassenraum wird die Projektion grau und der Text verschwindet.
- **Haarlinien, Pastelltöne, 1-px-Rahmen** — vom Beamer verschluckt. Mindestens `0.2cqw`, volle Flächen.
- **Animationen und Übergänge** über ein kurzes Crossfade hinaus — kosten Zeit, erzeugen Unruhe, und `prefers-reduced-motion` muss ohnehin greifen.
- **Eingabefelder für Schüler:innen** — dann ist es kein Foliensatz: zwei Dateien bauen (Folien für vorn, Arbeitsblatt für die Hände).
- **Reiner Info-Inhalt ohne Vortrag** (Elterninfo, Aushang) → [`profiles/infoseite.md`](infoseite.md).
- **Das Arbeitsblatt einfach projizieren** — A4-Layout in 15 px ist an der Wand unlesbar. Entweder Foliensatz bauen oder ein Dokument am Platz bearbeiten lassen.
- **Fehlende Notizen** bei komplexen Herleitungen — in drei Wochen weiß niemand mehr, welche Frage vor Schritt 3 gehörte.

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — dieselbe Didaktik (Lernpfad, aufbauende Schritte), aber **in Schülerhand** mit Eingaben; häufiges Gespann: Foliensatz vorn, Erarbeitungsseite am Platz
- [`profiles/worked-examples.md`](worked-examples.md) — Lösungsbeispiele schrittweise; am Beamer vorgeführt wird daraus eine Erklärsequenz
- [`profiles/infoseite.md`](infoseite.md) — statisch und ohne Vortrag; wenn niemand dazu spricht, ist es eine Info-Seite
- [`profiles/lerntheke.md`](lerntheke.md) / [`profiles/stationenlernen.md`](stationenlernen.md) — die Gegenbewegung: Foliensatz für Auftrag und Ergebnissicherung, Lerntheke für die Arbeitsphase
- [`profiles/methoden.md`](methoden.md) — eine Methode erklären; vorne am Beamer eingeführt, am Platz angewendet
