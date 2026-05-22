# Profil: <Einsatzgebiet>

- **Status:** Draft | Accepted
- **Datum:** YYYY-MM-DD
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein bis drei Sätze: Was ist der typische Einsatz dieses Onepager-Typs? Was unterscheidet ihn von anderen?

## Typische Merkmale

- **Klassenstufe:** z. B. Sek I / Sek II / Grundschule / alle
- **Fachbereich:** z. B. Mathematik / Sprachen / Naturwissenschaften / fächerübergreifend
- **Zeitumfang:** z. B. Einzelstunde, Doppelstunde, Hausaufgabe, mehrwöchiges Projekt
- **Ziel-Typ:** Übung / Erarbeitung / Diagnose / Reflexion / Anwendung / Kontrolle
- **Gerät:** Laptop / Tablet (iPad mit Stift) / Smartphone / Druck

## Core-ADRs mit Schwerpunkt

Welche Core-ADRs sind in diesem Profil besonders wichtig — und warum?

| ADR | Besondere Relevanz |
|---|---|
| [ADR-XXXX](../adr/XXXX-...md) | Warum es hier besonders zählt |

## Core-ADRs abweichend oder weniger relevant

Welche Core-ADRs sind hier zweitrangig oder bekommen eine andere Auslegung?

- **ADR-XXXX**: Knappe Begründung, warum hier nicht/anders.

## Spezifische didaktische Entscheidungen

Was ist *speziell für dieses Profil* anders oder strenger als die Core-Schicht vorgibt? Hier dürfen domänenspezifische Patterns dokumentiert werden, die in den Core-ADRs nicht stehen.

1. **Punkt 1**: …
2. **Punkt 2**: …

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja / nein / optional |
| Aufgaben-Karten | ja / nein / optional |
| Inhalts-Boxen (Merke, Tipp, Warn) | ja / nein / optional |
| Selbst-Korrektur (`data-expected`) | ja / nein / optional |
| Lösungs-Hürde (Tipp + Lösung) | ja / nein / optional |
| Quiz mit gehashten Antworten | ja / nein / optional |
| Canvas-Stift-Eingabe | ja / nein / optional |
| Fortschrittsbalken | ja / nein / optional |
| Save-Status-Indikator | ja / nein / optional |
| Toast-Notifications | ja / nein / optional |
| JSON-Export/Import | ja / nein / optional |
| Reset-Dialog | ja / nein / optional |

## Aufgaben-Pattern (typisch)

Eine HTML-Skizze einer typischen Aufgabe in diesem Profil. Kein vollständiges Boilerplate, sondern das *Domänen-charakteristische* Muster.

```html
<article class="aufgabe" data-task-id="...">
  <header class="aufgabe__header">
    <span class="aufgabe__nr">…</span>
    <h3 class="aufgabe__titel">…</h3>
  </header>
  <div class="aufgabe__body">
    …
  </div>
</article>
```

## Anti-Patterns

Was vermeidet man in diesem Profil — und warum?

- **Anti-Pattern 1**: Begründung
- **Anti-Pattern 2**: Begründung

## Verwandte Profile

- `profiles/<anderes-profil>.md` — Wo das passt / sich überschneidet
