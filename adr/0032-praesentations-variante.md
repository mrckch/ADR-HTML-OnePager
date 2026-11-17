# ADR-0032: Präsentations-Variante (Beamer-Foliensatz)

- **Status:** Accepted
- **Datum:** 2026-11-17
- **Betrifft:** Architektur-Grundannahme (Layout-Paradigma), neue Einsatzklasse, Navigation, Druck

## Kontext

Alle bisherigen Varianten des Baukastens sind **ein scrollendes Dokument**: oben ein Page-Header, darunter Abschnitte, Aufgaben oder Boxen, unten ein Footer — und darüber ein A4-Druck-Layout ([ADR-0023](0023-a4-druck-und-preview.md)). Das gilt für das große Boilerplate wie für die statische Info-Seite ([ADR-0030](0030-statische-infoseiten.md)).

Eine **lehrerzentrierte Präsentation am Beamer** passt in dieses Paradigma nicht:

| Aspekt | Scroll-Dokument | Beamer-Foliensatz |
|---|---|---|
| Leseabstand | 40 cm (Tisch, Tablet) | **4–10 m (letzte Reihe)** |
| Navigation | scrollen, Sprungmarken | **blättern** — Pfeiltasten, Presenter, Klick |
| Sichtbare Menge | so viel wie passt | **genau eine Folie** |
| Wer steuert | Schüler:in | **Lehrkraft** |
| Schriftgrad | 15 px | ≈ 30–60 px, abhängig von der Projektionsfläche |
| Zeitlicher Aufbau | alles sofort da | **schrittweise aufdeckbar** |
| Druck-Ziel | das Arbeitsblatt selbst | **Handout** (mehrere Folien pro Blatt) |
| Dark Mode | nach OS-Einstellung | hell, **unabhängig vom OS** |

Es ist also kein weiteres Profil auf dem bestehenden Template, sondern ein **anderes Layout-Paradigma**: n Flächen mit festem Seitenverhältnis statt eines Dokumentflusses. Zusätzlich weicht es bewusst von zwei Core-ADRs ab (Dark-Mode-Automatik aus [ADR-0022](0022-design-system-v2.md)/[ADR-0031](0031-design-system-v3-signal.md), Druck-Ziel aus [ADR-0007](0007-druck-pdf-optimierung.md)/[ADR-0023](0023-a4-druck-und-preview.md)). Profile dürfen Core-Entscheidungen laut [ADR-0024](0024-schichten-modell-profile.md) nur neu gewichten, nicht aufheben — deshalb braucht die Variante eine **Core-ADR**, nicht nur ein Profil.

Nach dem Schichtenbild aus [ADR-0030](0030-statische-infoseiten.md) nutzt der Foliensatz die **Präsentations-Lage** vollständig, die **Interaktions-Lage** stark reduziert (Aufdecken statt Eingabe) und die **Persistenz-Lage** gar nicht.

## Entscheidung

Eine dritte, eigenständige Variante: **`templates/praesentation-boilerplate.html`** plus Profil [`profiles/praesentation.md`](../profiles/praesentation.md). Sie folgt dem Präzedenzfall von [ADR-0030](0030-statische-infoseiten.md) (eigenes Template statt Strip-Anleitung) und nutzt Design-System **v3 „Signal"** ([ADR-0031](0031-design-system-v3-signal.md)), weil Projektion dort ausdrücklich zum Gültigkeitsbereich gehört.

### 1. Folien-Geometrie: logische Bühne per Container Queries

Jede Folie ist eine Fläche mit festem Seitenverhältnis, die in den Viewport eingepasst wird:

```css
.folie{
  width:  min(100vw, calc(100vh * var(--ar-w) / var(--ar-h)));
  height: min(100vh, calc(100vw * var(--ar-h) / var(--ar-w)));
  container-type: size;        /* macht die Folie zum Query-Container */
}
.folie__inhalt{ font-size: 2.4cqw; }   /* alle Größen relativ zur Folie */
```

Sämtliche Schriftgrade, Abstände und Linienstärken im Folieninhalt werden in **`cqw`/`cqh`** notiert — Prozent der **Folienbreite**, nicht des Viewports. Damit skaliert das Layout exakt und identisch auf 1024×768-Schulbeamer, Full-HD-Panel und 4K-Laptop, **ohne eine Zeile JS-Layout-Mathematik**.

> Wichtig für Umsetzende: `container-type: size` wirkt auf **Kinder**, nicht auf das Container-Element selbst. Schriftgrade gehören deshalb an `.folie__inhalt` und darunter, nie an `.folie`.

**Verworfen:** feste logische Bühne (z. B. 1280×720 px) plus `transform: scale()` per JS-Resize-Handler — der Weg etablierter Frameworks. Braucht JS für das Layout, erzeugt bei krummen Skalierungsfaktoren unscharfen Text und bricht, wenn das Script scheitert.

### 2. Seitenverhältnis umschaltbar: `data-format`

```html
<body data-format="16:9">   <!-- oder "4:3" -->
```

Setzt `--ar-w`/`--ar-h`. Schulrealität: ein erheblicher Teil der Beamer und fest montierten Leinwände ist weiterhin 4:3. Ein Foliensatz, der nur 16:9 kann, verschenkt in diesen Räumen ein Drittel der Fläche oder wird beschnitten.

### 3. Navigation: Index, Tastatur, Presenter

Genau eine Folie ist aktiv (`.folie.is-aktiv`), alle anderen tragen das `hidden`-Attribut — damit sind sie auch für Screenreader und die Tab-Reihenfolge weg.

| Eingabe | Wirkung |
|---|---|
| `→` `↓` `Leertaste` `Bild ab` `Enter` | vorwärts (nächster Schritt, sonst nächste Folie) |
| `←` `↑` `Bild auf` `Rücktaste` | zurück |
| `Pos1` / `Ende` | erste / letzte Folie |
| `f` | Vollbild |
| `b` | Blackout (schwarze Fläche — „jetzt zu mir") |
| `w` | Whiteout (weiße Fläche — Tafel/Projektionslicht) |
| `o` | Folien-Übersicht zum Springen |
| `n` | Notizen |
| `z` | Stift-Overlay |
| `t` | Kontrast-Thema umschalten |
| `?` | Tastenhilfe |
| Zahl + `Enter` | direkt zu Folie n |
| Klick / Tap rechte bzw. linke Bildhälfte, Wischen | vor / zurück |

**`Bild auf` / `Bild ab` ist der funktional entscheidende Teil:** praktisch jeder Presenter-Clicker sendet genau diese beiden Codes. Ohne sie ist der Foliensatz am Beamer nicht bedienbar, egal wie gut er aussieht.

**Verworfen:** `scroll-snap` als Primärmechanik. Elegant und ohne JS, aber Schritt-Aufdecken, Blackout, Übersicht und Direktsprung brauchen ohnehin einen Index — dann lieber ein Mechanismus statt zwei.

### 4. Position in der URL: `#/7` bzw. `#/7/2`

Die aktuelle Folie (und der Schritt darin) stehen im Hash. Gründe:

- **Robust im Unterricht:** HDMI-Kabel verrutscht, Laptop schläft ein, versehentlicher Reload — nach `F5` steht der Foliensatz wieder an derselben Stelle.
- **Verlinkbar:** „nach der Pause bei Folie 12 weiter" ist ein Link; aus einer Stundenplanung kann direkt auf eine Folie verwiesen werden.
- **Kein Storage nötig** — die Variante bleibt zustandslos wie die Info-Seite ([ADR-0002](0002-state-persistenz-localstorage.md) entfällt).

Einzige Ausnahme: das gewählte **Kontrast-Thema** liegt in `sessionStorage` (siehe Entscheidung 7), damit ein Reload im abgedunkelten Raum nicht wieder hell startet. Keine Lerndaten, kein `localStorage`.

### 5. Schrittweises Aufdecken: `.schritt`

```html
<section class="folie" data-schritte>
  <div class="folie__inhalt">
    <h2>Oberfläche eines Prismas</h2>
    <p class="schritt">Zwei Grundflächen …</p>
    <p class="schritt">… plus der Mantel.</p>
    <p class="schritt formel">O = 2 · G + M</p>
  </div>
</section>
```

`.schritt`-Elemente sind zunächst unsichtbar (`visibility: hidden`, **nicht** `display: none` — das Layout darf nicht springen) und erscheinen einzeln pro Navigationsschritt. Der bereits erschienene letzte Schritt wird mit einer orangen Marke hervorgehoben.

Das ist der **didaktische Kern** lehrerzentrierten Unterrichts: eine Herleitung aufbauen, eine Tabelle Zeile für Zeile besprechen, die Lösung erst zeigen, wenn die Klasse geantwortet hat. Es greift die Idee der Lösungs-Hürde ([ADR-0010](0010-loesungs-huerde.md)) auf, aber als **Präsentationsschritt der Lehrkraft**, nicht als Button der Schüler:innen.

### 6. Projektions- statt Lese-Typografie

[ADR-0009](0009-barrierefreiheit-lesbarkeit.md) wird neu gelesen: nicht Lesbarkeit auf Armlänge, sondern **aus der letzten Reihe**.

- Basis-Schriftgrad `2.4cqw` (≈ 31 px bei 1280 px Folienbreite), Überschriften `4.2cqw`, Titelfolie bis `7cqw`.
- **Keine Haarlinien:** Rahmen und Trennlinien mindestens `0.2cqw`, Akzentkanten `0.3cqw`.
- Volle Flächen statt zarter Washes, wo Kontrast gebraucht wird.
- Profil-Regel (nicht technisch erzwingbar): **ein Gedanke pro Folie, maximal etwa sechs Zeilen Text.**

### 7. Keine Dark-Mode-Automatik auf der Projektionsfläche

Der Foliensatz rendert **hell, unabhängig von `prefers-color-scheme`**. Begründung: der Lehrer-Laptop steht sehr häufig im Dark Mode, der Klassenraum ist aber hell — ein dunkles Thema wird an der Wand zu ausgewaschenem Grau mit unlesbarem Text. Die OS-Einstellung des präsentierenden Geräts sagt nichts über die Lichtverhältnisse im Raum aus.

Technisch gehört dazu ein ausdrückliches `color-scheme: light` (Meta-Tag **und** CSS): ohne diese Angabe kippt der Auto-Dark-Mode mancher Browser die weiße Folie eigenmächtig ins Graue — am Beamer der schlechteste denkbare Zustand, weil er weder hell noch wirklich dunkel ist.

Stattdessen schaltet `t` bewusst durch drei Themen: **hell** (Standard) → **dunkel** (abgedunkelter Raum, Film, Abendveranstaltung) → **hoher Kontrast** (schwacher oder alter Beamer, Sonne auf der Leinwand). Dokumentierte Abweichung von [ADR-0022](0022-design-system-v2.md) und [ADR-0031](0031-design-system-v3-signal.md).

### 8. Druck erzeugt ein Handout, keine Folien

[ADR-0007](0007-druck-pdf-optimierung.md) und [ADR-0023](0023-a4-druck-und-preview.md) bleiben in Kraft, ändern aber ihr Ziel: `@media print` setzt die Folien als **Kacheln im Seitenverhältnis des Foliensatzes** auf A4-Hochformat. Zwei Varianten über `data-handout` am `<body>`:

| Wert | Layout | pro A4-Seite |
|---|---|---|
| `notizen` (Standard) | Folie links, **Referenten-Notizen rechts** | ca. 3 |
| `kompakt` | zweispaltig, ohne Notizen | ca. 8 |

Die Zahlen ergeben sich aus dem Fluss (`break-inside: avoid` pro Folie), sie werden nicht erzwungen — eine feste Zahl „pro Seite" würde nur Leerraum produzieren. Im Handout sind **alle Schritte aufgedeckt**; die Bildschirmvorschau läuft über `?layout=handout` — derselbe Mechanismus wie das bestehende `?layout=a4`.

Eine Folie pro Blatt im Querformat auszudrucken wäre Papierverschwendung und didaktisch wertlos; ein Handout mit Notizenspalte ist genau das, was nach einer lehrerzentrierten Stunde gebraucht wird.

### 9. Notizen als Overlay, kein zweiter Bildschirm

`<aside class="notizen">` pro Folie: in der Projektion versteckt, per `n` als Overlay auf dem präsentierenden Schirm sichtbar, im Handout neben der Folie gedruckt.

Eine **echte Referentenansicht** (zweites Fenster mit Notizen und Vorschau, synchron zur Projektion) wird **nicht** umgesetzt: unter `file://` haben zwei Fenster eine Opaque Origin — `BroadcastChannel` und `storage`-Events funktionieren dort nicht zuverlässig, und ohne Server lässt sich der Foliensatz dann nicht mehr einfach per Datei weitergeben ([ADR-0001](0001-single-file-html-architektur.md)). Als mögliche späte Erweiterung für den `http`-Betrieb notiert, nicht als Zusage.

### 10. Lehrerzentriert heißt nicht passiv — vier Unterrichtsmodule

| Modul | Umsetzung |
|---|---|
| **Stift-Overlay** | [ADR-0019](0019-canvas-stift-modul.md) angepasst: transparenter Vollflächen-Canvas **über** der Folie statt Canvas-Block im Dokumentfluss. Vier Farben, Radierer, Löschen. Annotationen leben pro Folie im Speicher der Sitzung und verschwinden beim Reload — sie sind Tafelanschrift, kein Dokument. |
| **Timer-Folie** | `data-timer="5"` — großer Countdown für „Arbeitsphase 5 Minuten", Think-Pair-Share, Test-Zeit. Startet beim Aufrufen der Folie, `s` pausiert, `r` setzt zurück. |
| **Aufdeck-Lösung** | Kein eigenes Modul, sondern `.schritt` aus Entscheidung 5: fragen, Antworten sammeln, aufdecken. |
| **Impuls-Fläche** | Vollflächen-Bild oder -Zitat ohne Textrahmen (`.folie--impuls`) als Gesprächseinstieg. |

**Bewusst nicht enthalten:** Eingabefelder, `localStorage`, Gamification ([ADR-0012](0012-gamification.md)), gehashte Quiz-Antworten ([ADR-0013](0013-quiz-hardening.md)). Die Klasse antwortet mündlich; das Aufdecken *ist* die Kontrolle. Wer Schülereingaben braucht, baut zwei Dateien: Foliensatz für vorn, Arbeitsblatt für die Hände.

### 11. Was die Variante von der Core-Schicht übernimmt

- [ADR-0001](0001-single-file-html-architektur.md) — eine Datei, keine externen Abhängigkeiten, kein CDN
- [ADR-0006](0006-responsives-layout.md) — funktioniert auch auf dem Laptop-Bildschirm und am Tablet (zum Vorbereiten)
- [ADR-0009](0009-barrierefreiheit-lesbarkeit.md) — vollständige Tastatursteuerung, Fokus-Sichtbarkeit, `prefers-reduced-motion` (dann kein Crossfade), `hidden` auf inaktiven Folien
- [ADR-0015](0015-inhalts-boxen.md) — Inhalts-Boxen, in v3-Formensprache und Projektionsgröße
- [ADR-0031](0031-design-system-v3-signal.md) — Tokens, Display-Typografie, Orange-Budget

### 12. Was entfällt

[ADR-0002](0002-state-persistenz-localstorage.md) (localStorage), [ADR-0003](0003-json-export-import.md) (JSON-Export), [ADR-0004](0004-reset-funktion-mit-bestaetigung.md) (Reset), [ADR-0017](0017-save-status-toast.md) (Save-Status/Toast), [ADR-0020](0020-html-export-eingebetteter-state.md) (eingebetteter State), [ADR-0005](0005-sticky-menue-ios-safe-area.md) (Sticky-Topbar — ein Foliensatz hat eine ausblendende Steuerleiste, keine Topbar), [ADR-0010](0010-loesungs-huerde.md)/[0011](0011-selbst-korrektur.md)/[0012](0012-gamification.md)/[0013](0013-quiz-hardening.md)/[0018](0018-aufgaben-karten.md)/[0025](0025-lernportfolio-persistenz.md)/[0026](0026-tabellen-eingaben.md)/[0027](0027-datum-zeit-eingaben.md) (alle Aufgaben- und Eingabe-Mechaniken).

## Alternativen

- **Bestehendes Boilerplate mit `?layout=beamer`:** Ein Template weniger, aber die ganze Interaktions- und Persistenz-Maschinerie bleibt als toter Code in jedem Foliensatz, und das Layout-Paradigma lässt sich nicht per Media Query umdrehen. Verworfen (gleiche Begründung wie in [ADR-0030](0030-statische-infoseiten.md)).
- **Etabliertes Framework (reveal.js, Slidev) einbinden:** Mehr Funktionen für weniger Arbeit, bricht aber [ADR-0001](0001-single-file-html-architektur.md) (externe Abhängigkeit, CDN oder Build-Schritt) und bringt ein fremdes Design-System mit. Verworfen.
- **PowerPoint/Impress nutzen und das Repo außen vor lassen:** Für viele Lehrkräfte der Normalfall — verschenkt aber Versionierbarkeit, Verlinkbarkeit, das Design-System und die Weitergabe als eine Datei, die überall ohne Installation läuft. Verworfen für diesen Baukasten (steht natürlich jedem offen).
- **Nur ein Profil ohne Core-ADR:** Die Abweichungen bei Dark Mode und Druck sind Core-Abweichungen; [ADR-0024](0024-schichten-modell-profile.md) verbietet Profilen genau das. Verworfen.
- **Folien als `scroll-snap`-Strecke ohne JS:** Siehe Entscheidung 3. Verworfen.

## Konsequenzen

**Positiv:**
- Deckt die häufigste lehrerzentrierte Unterrichtsform ab, die dem Baukasten bisher komplett fehlte.
- Ein Foliensatz ist **eine Datei**: läuft auf jedem Schulrechner ohne Installation, ohne Konto, ohne Netz; per USB-Stick, Mail oder WebDAV weitergebbar.
- Versionierbar und verlinkbar — anders als eine `.pptx`.
- Schritt-Aufdecken und Stift-Overlay ersetzen zwei Werkzeuge (Folien + Tafel) durch eines.
- Robust gegen Unterrichtsunfälle: Position in der URL, nichts zu speichern, nichts zu verlieren.

**Negativ / Trade-offs:**
- **Drittes Template** mit erneut überlappendem CSS (Tokens, Boxen, Druck). Bewusste, kontrollierte Duplikation nach dem Muster von [ADR-0030](0030-statische-infoseiten.md) — der Preis des Single-File-Prinzips.
- **Zweites Design-System im Baukasten** sichtbar nebeneinander: Arbeitsblatt in v2, Foliensatz zur gleichen Stunde in v3 ([ADR-0031](0031-design-system-v3-signal.md) wiegt das ab).
- **Keine echte Referentenansicht** — für Lehrkräfte, die Notizen auf dem Laptop und Folien an der Wand getrennt brauchen, bleibt das ein Rückschritt gegenüber PowerPoint. Overlay und Handout mildern es.
- **Container Queries** werden gebraucht (alle aktuellen Browser können sie; sehr alte Schulrechner nicht). Fallback: ohne `cqw`-Unterstützung greift eine `vmin`-basierte Ersatzregel — etwas gröber, aber lesbar.
- `cqw`-Werte sind beim Schreiben ungewohnter als `px`.

**Folgewirkungen:**
- `AI_GUIDE.md` nimmt „Beamer-Präsentation" in die Einsatzfall-Liste auf und verweist auf das **dritte** Template.
- `CHECKLIST.md` bekommt Präsentations-Prüfpunkte (Clicker-Tasten, letzte Reihe, Handout-Druck, ein Gedanke pro Folie).
- Ändert sich v3 ([ADR-0031](0031-design-system-v3-signal.md)), müssen `UEBERSICHT.html` **und** dieses Template nachgezogen werden.
- Künftige projizierte Seitentypen (Lernvideo-Standbilder, Elternabend-Folien, Prüfungsablauf an der Wand) lehnen sich an dieses Muster an.

## Verwandte ADRs / Profile

- [ADR-0030](0030-statische-infoseiten.md) — Präzedenzfall: eigene Variante mit eigenem Template; Schichtenbild Präsentation/Interaktion/Persistenz
- [ADR-0031](0031-design-system-v3-signal.md) — Design-System v3 „Signal", hier erstmals in einem Template
- [ADR-0024](0024-schichten-modell-profile.md) — warum das eine Core-ADR und nicht nur ein Profil ist
- [ADR-0019](0019-canvas-stift-modul.md) — Stift-Modul, hier als Vollflächen-Overlay adaptiert
- [ADR-0023](0023-a4-druck-und-preview.md) — Druck-Vorschau-Mechanik, hier als Handout
- [profiles/praesentation.md](../profiles/praesentation.md) — Hauptkonsument dieser Entscheidung
