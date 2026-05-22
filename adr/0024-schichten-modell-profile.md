# ADR-0024: Schichten-Modell — Core-ADRs + Einsatz-Profile

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Betrifft:** Repository-Struktur, KI-Workflow, Wartbarkeit
- **Typ:** Meta-ADR (Architektur des Repos selbst, nicht der Onepager)

## Kontext

Im bisherigen Aufbau lagen alle Entscheidungen — von „wie speichern wir State?" über „wie sieht Typografie aus?" bis „wie kommt die Lösung zum Vorschein?" — auf einer einzigen Ebene: dem `adr/`-Ordner. Das funktioniert, solange alle Onepager dieselben didaktischen Anforderungen haben.

In der Praxis tun sie das nicht. Ein Onepager als **Lösungszettel zum Schulbuch** trifft andere didaktische Entscheidungen als ein **digitales Arbeitsheft fürs iPad** oder eine **Erarbeitungsseite mit Lernpfad**:

| Aspekt | Lösungszettel | Arbeitsheft | Erarbeitungsseite |
|---|---|---|---|
| Aufgabentext im Onepager | nein (steht im Buch) | ja | ja |
| Lösungs-Hürde | sehr streng | irrelevant (keine Lösungen) | mittelstreng |
| Selbst-Korrektur | zentral | irrelevant (Handschrift) | wichtig |
| Stift-Eingabe (Canvas) | meist nicht | zentral | nur bei Bedarf |
| Quiz | meist nein | nein | am Ende |
| Lineares Gating | nein | nein | ja |

Wenn diese domänenspezifischen Entscheidungen in den Core-ADRs landen, werden die Core-ADRs unscharf — sie müssten Sonderfälle für jeden Einsatz auflisten. Werden sie nicht dokumentiert, geht das Wissen über die richtige Domänen-Anwendung verloren.

Außerdem soll der KI-Assistent, der dieses Repo nutzt, **vor jedem neuen Onepager** den Einsatzfall erfragen, damit er die richtigen Patterns anwendet.

## Entscheidung

Das Repository wird in **drei Schichten** organisiert:

```
Core-ADRs (adr/)           ← universelle Entscheidungen, gelten immer
       ↓ erweitert/präzisiert durch
Einsatz-Profile (profiles/) ← style-guide-artige Empfehlungen pro Anwendungsfall
       ↓ konkretisiert in
Konkreter Onepager          ← die fertige HTML-Datei für die Klasse
```

### 1. Core-ADRs (`adr/`)

Bleiben wie bisher. Inhalt: universelle Entscheidungen, die in **jedem** Onepager gelten — Architektur, Persistenz, A11y, Druck, Design-Tokens, Aufgaben-Karten, Save-Status, …

ADRs in `adr/` ändern sich **nicht** durch die Einführung von Profilen. Sie sind die Grundlage.

### 2. Einsatz-Profile (`profiles/`)

Neuer Ordner. Pro Einsatzgebiet eine Markdown-Datei (z. B. `profiles/loesungszettel.md`).

**Charakter — bewusst empfehlend, nicht zwingend:**

| Sprache | Bedeutung |
|---|---|
| „Empfohlen" | Standard, aber begründet abweichbar |
| „Vorsicht bei …" | Anti-Pattern, meistens vermeiden |
| „Typischer Pattern" | Vorlage, kein Schema F |

Profile dürfen Core-ADRs **neu gewichten** („für dieses Profil ist ADR-0011 besonders zentral", „ADR-0013 spielt hier keine Rolle"), aber **nicht ersetzen**. Wenn ein Profil eine Core-Entscheidung tatsächlich aufheben wollte, gehört das in eine neue oder geänderte Core-ADR.

### 3. KI-Workflow (`AI_GUIDE.md`)

Auf Repository-Wurzelebene. Beschreibt:
- Reihenfolge der Schritte für einen KI-Assistenten („Frage zuerst den Einsatzfall …")
- Wie das Profil und die Core-ADRs zusammen interpretiert werden
- Wie das Boilerplate als Basis genommen und an das Profil angepasst wird

Beim Forken oder Wiederverwenden des Repos ist `AI_GUIDE.md` die maschinen-lesbare Brücke zwischen Repo-Inhalt und KI-Tooling.

### 4. Boilerplate bleibt generisch

Es gibt weiterhin **ein** `templates/onepager-boilerplate.html`. Es ist profil-neutral. Die KI passt es beim Generieren an das gewählte Profil an (Sektionen hinzufügen/entfernen, Module aktivieren/deaktivieren, Konstanten setzen).

Profile dürfen **kleine Helper-Snippets** als Code-Beispiele enthalten (z. B. ein `loesungs-cipher.js`-Snippet im Lösungszettel-Profil), aber **kein eigenes Boilerplate** mit redundantem Code.

## Profil-Template (Struktur)

Jedes Profil folgt dieser Sektion-Reihenfolge (Detail in `profiles/_template.md`):

1. **Was ist das?** (Kurzbeschreibung)
2. **Typische Merkmale** (Klassenstufe, Fach, Zeitumfang, Ziel-Typ)
3. **Core-ADRs mit Schwerpunkt** (Tabelle: ADR → Begründung der besonderen Relevanz)
4. **Core-ADRs abweichend oder weniger relevant** (Liste mit Begründung)
5. **Spezifische didaktische Entscheidungen** (was *hier* anders ist)
6. **Empfohlene Module** (Lernziel-Box, Quiz, Canvas, …: ja/nein/optional)
7. **Aufgaben-Pattern** (HTML-Skizze typischer Aufgaben)
8. **Anti-Patterns** (was hier vermeiden)
9. **Verwandte Profile**

## Alternativen

- **Alles in `adr/` belassen, mit Fußnoten je nach Einsatz:** Verworfen — Core-ADRs würden zu Sonderfall-Sammlungen, schwer lesbar.
- **Profile als ADRs selbst** (in `adr/` mit eigener Nummerngruppe `P1xx`, `P2xx`): Verworfen — würde die Nummerierungslogik der ADRs aufweichen und die Trennung verwischen.
- **Eigenes Sub-Repo pro Profil:** Verworfen — zu viel Overhead, Profile sind keine eigenständigen Projekte.
- **Profile bindend mit MUSS/DARF NICHT:** Verworfen, weil Lehrkräfte und Domänen verschieden sind. „Style-Guide-Charakter" ist genug Disziplin.

## Konsequenzen

**Positiv:**
- Saubere Trennung „Was gilt immer?" vs. „Was gilt hier?"
- Skalierbar: Neues Einsatzgebiet = neues Profil, ohne Core zu berühren
- KI-freundlich: maschinell durchsuchbar, deterministisch interpretierbar
- Dokumentiert pädagogische Entscheidungen pro Domäne — wertvoll für Kollegen, die forken

**Negativ / Trade-offs:**
- Mehr Wartungsaufwand: Profile altern, müssen aktualisiert werden
- Risiko der Duplizierung — Profile dürfen Core-Inhalt nicht wiederholen, sondern nur referenzieren
- Profile sind weicher als ADRs („empfohlen" statt „entschieden") → erfordert Disziplin beim Schreiben

**Folgewirkungen für künftige Onepager:**
- Vor Erstellung: Einsatzgebiet bestimmen, passendes Profil lesen
- KI-Erstellung: `AI_GUIDE.md` führt durch den Workflow
- CHECKLIST.md bekommt einen Punkt „Profil-Konformität geprüft?"
- Neue ADR-Vorschläge fragen: gehört das in Core (universell) oder in ein Profil (domänenspezifisch)?

## Verwandte ADRs

Diese ADR ist meta — sie betrifft die Struktur des Repos selbst. Alle bisherigen ADRs (0001–0023) bleiben unverändert die „Core-Schicht". Die ersten drei Profile sind:

- [profiles/loesungszettel.md](../profiles/loesungszettel.md)
- [profiles/digitales-arbeitsheft.md](../profiles/digitales-arbeitsheft.md)
- [profiles/erarbeitungsseite.md](../profiles/erarbeitungsseite.md)
