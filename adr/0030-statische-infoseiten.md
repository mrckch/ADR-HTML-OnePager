# ADR-0030: Statische Info-Seiten-Variante (Persistenz optional)

- **Status:** Accepted
- **Datum:** 2026-05-28
- **Betrifft:** Architektur-Grundannahme, neue Einsatzklasse

## Kontext

Das gesamte System ist bisher um **Interaktion und Persistenz** herum gebaut: Schüler:innen geben etwas ein, ihre Eingaben werden im localStorage gespeichert ([ADR-0002](0002-state-persistenz-localstorage.md)), per JSON ([ADR-0003](0003-json-export-import.md)) oder HTML ([ADR-0020](0020-html-export-eingebetteter-state.md)) exportiert, der Save-Status wird angezeigt ([ADR-0017](0017-save-status-toast.md)), und ein Reset-Dialog ([ADR-0004](0004-reset-funktion-mit-bestaetigung.md)) räumt auf.

Es gibt jedoch einen häufigen schulischen Bedarf, der **gar keine Eingaben** kennt: die reine **Informationsseite**. Beispiele:

- **Elterninformation** zu einer Klassenfahrt, einem Elternabend, neuen Regeln
- **Schüler-Info** zu Bewertungskriterien, Ablauf einer Prüfung, Methodenübersicht
- **Lehrer-Info / Handreichung** zu einem Curriculum, einer Vertretungsregelung
- **Aushänge** wie Hausordnung, Förderangebote, Ansprechpartner-Listen

Solche Seiten **erklären**, sie sammeln nichts ein. Der Button „Ergebnisse sichern" ist hier sinnlos, ebenso Save-Status, Fortschrittsbalken, Reset, Import und die Aufgaben-/Quiz-/Canvas-Module.

Bisher hätte man dafür das volle Boilerplate genommen und ~1000 Zeilen Interaktions-Code gelöscht — fehleranfällig und für KI-Generierung unsauber.

## Entscheidung

Wir erklären die **Persistenz-Schicht für optional** und führen eine eigenständige **statische Variante** des Onepagers ein:

1. Ein eigenes, schlankes Template `templates/infoseite-boilerplate.html`.
2. Ein neues Profil [`profiles/infoseite.md`](../profiles/infoseite.md).

Damit zerfällt das Boilerplate konzeptionell in drei Lagen, von denen die Info-Seite nur die erste nutzt:

| Lage | Bestandteile | Info-Seite |
|---|---|---|
| **Präsentation** | Design-Tokens, Dark Mode, Inhalts-Boxen, Page-Header, Responsive, Barrierefreiheit, A4-Druck + Vorschau | ✅ vollständig |
| **Interaktion** | Aufgaben-Karten, Quiz, Selbst-Korrektur, Lösungs-Hürde, Cipher, Canvas | ❌ entfällt |
| **Persistenz** | localStorage, Save-Status, Fortschritt, JSON/HTML-Export/-Import, Reset, Toast, Meta-Felder | ❌ entfällt |

### Was die Info-Variante behält

- **[ADR-0001](0001-single-file-html-architektur.md)** — eine Datei, keine externen Abhängigkeiten
- **[ADR-0005](0005-sticky-menue-ios-safe-area.md)** — Sticky-Topbar, aber **schlank**: nur Titel + Druck/Vorschau
- **[ADR-0006](0006-responsives-layout.md)** — Mobile-First
- **[ADR-0007](0007-druck-pdf-optimierung.md)** + **[ADR-0023](0023-a4-druck-und-preview.md)** — A4-Druck + Bildschirm-Vorschau (Info-Seiten werden oft ausgedruckt / als PDF verschickt)
- **[ADR-0009](0009-barrierefreiheit-lesbarkeit.md)** — Tastatur, Kontrast, `prefers-reduced-motion`
- **[ADR-0015](0015-inhalts-boxen.md)** — Inhalts-Boxen (merke/info/tipp/warn) sind das **zentrale** Gestaltungsmittel
- **[ADR-0022](0022-design-system-v2.md)** — Design-Tokens, Dark Mode

### Was die Info-Variante streicht

- **[ADR-0002](0002-state-persistenz-localstorage.md)** — kein localStorage. Die Seite ist zustandslos.
- **[ADR-0003](0003-json-export-import.md)** — kein JSON-Export/-Import (nichts zu exportieren).
- **[ADR-0004](0004-reset-funktion-mit-bestaetigung.md)** — kein Reset (nichts zurückzusetzen).
- **[ADR-0017](0017-save-status-toast.md)** — kein Save-Status, kein Toast.
- **[ADR-0020](0020-html-export-eingebetteter-state.md)** — kein eingebetteter State. (Die Datei *ist* ohnehin schon selbsttragend — wer sie weitergeben will, verschickt einfach die `.html`.)
- **[ADR-0010](0010-loesungs-huerde.md)/[0011](0011-selbst-korrektur.md)/[0012](0012-gamification.md)/[0013](0013-quiz-hardening.md)/[0018](0018-aufgaben-karten.md)/[0019](0019-canvas-stift-modul.md)** — keine Aufgaben, Quiz, Selbst-Korrektur, Gamification, Canvas.

### Was die Info-Variante hinzufügt

Drei kleine, info-typische Bausteine, die im Aufgaben-Boilerplate fehlen:

1. **Inhaltsverzeichnis / Sprungmarken** (`.toc`) — Anker-Navigation zu den `<section id="…">`. Reines CSS (`scroll-behavior: smooth` mit `prefers-reduced-motion`-Ausnahme, `scroll-margin-top` gegen die Sticky-Topbar). Kein JS nötig.
2. **„Stand:"-Datum** (`.stand`) im Header — macht die Aktualität der Information sofort sichtbar. Wichtig, weil Info-Seiten oft länger leben und veralten können.
3. **Footer** (`.seiten-footer`) — Kontakt, Ansprechpartner, Quelle/Impressum.

Dazu eine optionale **Eckdaten-Tabelle** (`.fakten`) für „Termin / Ort / Kosten / Ansprechpartner"-Blöcke, die in Info-Seiten sehr häufig sind.

### JS-Minimalismus

Das gesamte Skript der Info-Variante besteht aus **zwei Funktionen**: A4-Vorschau-Toggle und `window.print()`. Kein Storage, keine Event-Bindings auf Eingabefelder, keine Module-Initialisierung. Das macht die Seite robust, schnell und trivial zu prüfen.

### Eigenes Template statt Strip-Anleitung

Wir liefern bewusst eine **separate Datei** statt einer Anleitung „lösche Block X bis Y aus dem großen Boilerplate". Gründe:

- KI generiert aus einer zweckgebauten Basis sauberer und ohne Geister-Referenzen.
- Lehrkräfte müssen nichts wegschneiden und können nichts versehentlich kaputt machen.
- Die Datei ist klein genug, um sie ganz zu lesen.

Der Preis ist eine **zweite Datei mit überlappendem CSS** (Tokens, Boxen, Print). Das ist bewusste, kontrollierte Duplikation — siehe Trade-offs.

## Alternativen

- **Großes Boilerplate mit Strip-Anleitung:** Eine Datei, aber fehleranfällig beim Entfernen, verwaiste Selektoren, schlecht für KI. Verworfen.
- **Feature-Flag im großen Boilerplate** (`data-mode="info"`, das per JS Interaktion abschaltet): Behält die ganze Komplexität und den toten Code in jeder Info-Seite. Widerspricht dem Single-File-Schlankheits-Gedanken. Verworfen.
- **Gemeinsames CSS in externe Datei auslagern:** Würde die Duplikation lösen, bricht aber [ADR-0001](0001-single-file-html-architektur.md) (Single-File). Verworfen.
- **Info-Seite ganz ohne Repo-Unterstützung** („nimm halt normales HTML"): Verschenkt Design-System, Druck-Layout, Barrierefreiheit und Konsistenz. Verworfen.

## Konsequenzen

**Positiv:**
- Neue, sehr häufige Einsatzklasse wird sauber abgedeckt — ohne den Aufgaben-Ballast.
- Info-Seiten erben das Design-System und das geprüfte A4-Druck-Layout 1:1 → einheitlicher Look mit den Arbeitsblättern.
- Maximale Robustheit: zustandslos, fast kein JS, nichts kann „verloren gehen".
- Klärt eine Architektur-Grundannahme: **Persistenz ist eine Schicht, kein Fundament.**

**Negativ / Trade-offs:**
- **CSS-Duplikation** zwischen `onepager-boilerplate.html` und `infoseite-boilerplate.html` (Tokens, Boxen, Print-Block). Bei Design-Änderungen müssen **beide** Templates gepflegt werden. Akzeptiert, weil Single-File-Prinzip Vorrang hat und die Überlappung überschaubar ist.
- Zwei Boilerplates erhöhen die Auswahl-Last minimal — das Profil und der AI_GUIDE lenken die Entscheidung.

**Folgewirkungen:**
- Der KI-Workflow ([AI_GUIDE.md](../AI_GUIDE.md)) muss bei „Info-Seite / Aushang / Elterninfo / kein Eingabebedarf" auf das **schlanke** Template verweisen, nicht auf das große.
- Wenn das Design-System sich ändert ([ADR-0022](0022-design-system-v2.md)), gilt die Änderung für **beide** Templates.
- Künftige rein-präsentative Einsätze (z. B. Glossar, Übersichtsplakat) lehnen sich an dieses Muster an.

## Verwandte ADRs / Profile

- [ADR-0001](0001-single-file-html-architektur.md) — Single-File-Prinzip (Grund für die kontrollierte Duplikation)
- [ADR-0015](0015-inhalts-boxen.md) — Inhalts-Boxen als zentrales Gestaltungsmittel der Info-Seite
- [ADR-0023](0023-a4-druck-und-preview.md) — A4-Druck + Vorschau, hier voll übernommen
- [ADR-0024](0024-schichten-modell-profile.md) — Schichten-Modell (Core + Profile)
- [profiles/infoseite.md](../profiles/infoseite.md) — Hauptkonsument dieser Entscheidung
