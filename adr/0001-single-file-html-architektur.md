# ADR-0001: Single-File-HTML-Architektur

- **Status:** Accepted
- **Datum:** 2026-05-21
- **Betrifft:** Architektur, Verteilung, Hosting

## Kontext

Die Onepager werden auf einem Webhoster abgelegt und per Link an die Schüler:innen verteilt. Die Schüler:innen öffnen den Link auf unterschiedlichen Geräten (iOS, Android, Windows, macOS) und in unterschiedlichen Browsern. Es gibt keine Build-Pipeline und keinen Server-Backend-Code.

Wichtige Randbedingungen:
- Schnelles Laden, auch über mobile Datenverbindungen
- Keine externen Abhängigkeiten, die später wegbrechen könnten (CDN-Ausfall, Versionswechsel)
- Einfaches Verteilen, ggf. auch offline weitergeben (Datei per Mail oder Messenger)
- Kein Build-Schritt nötig

## Entscheidung

Jeder Onepager ist eine **einzelne, in sich geschlossene `.html`-Datei**:

- HTML, CSS und JavaScript liegen inline in derselben Datei
- Bilder werden bevorzugt als Inline-SVG oder als `data:`-URI (Base64) eingebettet, wenn klein genug
- Keine externen CSS- oder JS-Dateien
- Keine externen Schriftarten (Google Fonts o. ä.) — System-Font-Stack verwenden ([siehe ADR-0008](0008-design-system.md))
- Keine externen JS-Frameworks (kein React, Vue, jQuery o. ä.). Vanilla JS reicht.

## Alternativen

- **Multi-File-Setup mit Assets-Ordner:** Verworfen, weil das Verteilen per Link komplizierter wird (Pfade, Hosting-Struktur) und die Datei nicht mehr eigenständig weitergegeben werden kann.
- **Externe CDN-Bibliotheken (z. B. Tailwind, Alpine.js via CDN):** Verworfen, weil Offline-Nutzung leidet und CDNs in der Schule blockiert sein können.
- **Static Site Generator (z. B. Astro, 11ty):** Overkill für Einzelseiten; erzeugt zusätzlichen Wartungsaufwand.

## Konsequenzen

**Positiv:**
- Maximale Portabilität: Datei läuft überall, auch lokal per Doppelklick
- Keine Abhängigkeit von externen Diensten
- Sehr schnelle Erstanzeige (nur ein HTTP-Request)
- Einfach in Versionskontrolle und Backup

**Negativ / Trade-offs:**
- Dateigröße wird größer, wenn Bilder eingebettet werden → bewusst klein halten
- Kein Code-Sharing zwischen Onepagern; gemeinsame Snippets müssen kopiert werden
- Kein Tree-Shaking, kein Minifying durch Build

**Folgewirkungen für künftige Onepager:**
- Jeder Onepager ist genau **eine** `.html`-Datei
- Bilder vor dem Einbetten optimieren (SVG bevorzugt, sonst komprimiertes JPEG/WebP als Base64)
- Wiederverwendbare Snippets (z. B. Sticky-Menü, Storage-Modul) als kopierbare Blöcke im Repository vorhalten

## Verwandte ADRs

- [ADR-0008](0008-design-system.md) — Konsistentes Design-System (System-Fonts)
