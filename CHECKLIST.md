# Pre-Publish-Checkliste für HTML-Onepager

Vor dem Hochladen jeden Onepager einmal durchgehen. Abgeleitet aus den
„Folgewirkungen"-Abschnitten der [ADRs](adr/) und den [profiles/](profiles/).

## 0. Profil-Konformität (ADR-0024)

- [ ] Einsatzgebiet ist klar — passendes Profil aus [profiles/](profiles/) gewählt
- [ ] Profil-spezifische didaktische Entscheidungen umgesetzt (z. B. Lösungs-Cipher beim Lösungszettel, Canvas beim Arbeitsheft, Gating bei der Erarbeitungsseite)
- [ ] Empfohlene Module aus dem Profil aktiviert, nicht empfohlene deaktiviert/weggelassen
- [ ] Aufgaben-Pattern folgt dem Profil-Beispiel
- [ ] Keine Anti-Patterns aus dem Profil verwendet

## 1. Grundgerüst (ADR-0001, ADR-0008)

- [ ] Datei ist eine einzige, eigenständige `.html`-Datei (keine externen JS/CSS/Schriftarten)
- [ ] Bilder sind als SVG inline oder als optimiertes Base64-Image eingebettet
- [ ] Design-Tokens (`--bg`, `--fg`, `--space-*` etc.) sind vorhanden und werden konsistent verwendet
- [ ] Keine willkürlichen Farb-/Abstandswerte im CSS — alles über Tokens

## 2. State-Persistenz (ADR-0002, ADR-0003, ADR-0004)

- [ ] `ONEPAGER_SLUG` ist auf einen **eindeutigen** Wert für diesen Onepager gesetzt
- [ ] `SCHEMA_VERSION` ist definiert; bei Änderung der Datenstruktur erhöht
- [ ] Auto-Save funktioniert bei jeder Eingabe (kurzer Test mit Reload)
- [ ] Export erzeugt eine valide JSON-Datei mit korrektem Dateinamen
- [ ] Import lädt die Daten und füllt die UI; abweichender Slug/Version werden abgelehnt
- [ ] Reset-Dialog erscheint mit Bestätigungsfrage, **nicht** `window.confirm`
- [ ] Nach Reset ist `localStorage` leer und UI auf Default-Werten

## 3. Top-Menü und iOS (ADR-0005)

- [ ] `<meta name="viewport" … viewport-fit=cover>` ist gesetzt
- [ ] `env(safe-area-inset-*)` als Body-Padding vorhanden
- [ ] Topbar bleibt beim Scrollen oben sichtbar (`position: sticky`)
- [ ] Auf iPhone getestet: Menü nicht unter Notch/Statusleiste verdeckt
- [ ] Buttons sind mindestens 44×44 px groß
- [ ] Auf schmalen Screens: Button-Labels brechen nicht unschön um

## 4. Responsives Layout (ADR-0006)

- [ ] Test auf Smartphone-Breite (≤ 400 px): kein horizontaler Scrollbalken
- [ ] Test auf Tablet (~ 768 px): Layout wirkt aufgeräumt, nicht zu schmal
- [ ] Test auf Desktop (≥ 1024 px): Inhalt zentriert, max. ~ 800 px breit
- [ ] Browser-Zoom auf 200 % bricht das Layout nicht
- [ ] Tabellen sind in `overflow-x: auto`-Wrapper, scrollen statt auszubrechen

## 5. Druck / A4 (ADR-0007, ADR-0023)

- [ ] **A4-Vorschau auf Bildschirm** geprüft: URL um `?layout=a4` ergänzen oder Topbar-Button „A4-Vorschau" klicken
- [ ] Seitenumbrüche durch `.page-break-hint` bewusst gesetzt — keine wichtigen Inhalte zerschnitten
- [ ] Aufgaben-Karten passen jeweils auf eine Seite (sonst aufteilen)
- [ ] Tabellen, Boxen, Quiz-Fragen werden nicht zwischen zwei Seiten getrennt
- [ ] Keine Überschriften am Seitenende getrennt vom Folgeabschnitt
- [ ] Druckvorschau (`Strg/Cmd + P`) sieht aus wie die A4-Vorschau
- [ ] Topbar, Modals, Toast werden **nicht** gedruckt
- [ ] Schülerantworten in Inputs/Textareas sind im Druck sichtbar
- [ ] Lehrer-Lösungsblatt getestet: URL mit `?solutions=1` → alle Tipps und Lösungen sichtbar im Druck

## 6. Barrierefreiheit (ADR-0009)

- [ ] `<html lang="de">` (oder passende Sprache)
- [ ] Sinnvolle Überschriftenhierarchie: genau **ein** `<h1>`, danach `<h2>`/`<h3>`
- [ ] Alle Formularfelder haben ein `<label>` (verknüpft via `for=`)
- [ ] Alle `<img>` haben `alt`-Attribut (dekorativ → `alt=""`)
- [ ] Tab-Reihenfolge durchgehen: alle interaktiven Elemente erreichbar, logisch sortiert
- [ ] `Esc` schließt Modal-Dialoge
- [ ] Fokus-Outline (`*:focus-visible`) ist sichtbar — nicht entfernt
- [ ] Farbkontraste prüfen (z. B. WebAIM Contrast Checker): Text ≥ 4.5:1
- [ ] Im System-Dark-Mode testen: lesbar, Kontraste passen
- [ ] `prefers-reduced-motion`-Block vorhanden
- [ ] Texte: kurze Absätze, klare Sprache, keine Blocksatz-Lücken (linksbündig)

## 7. Letzter Cross-Browser-Smoke-Test

- [ ] Chrome / Edge (Desktop)
- [ ] Safari (iOS — echtes Gerät oder iOS-Simulator)
- [ ] Firefox (Desktop)
- [ ] Sticky-Menü, Modal, Export/Import in jedem Browser kurz angetippt

## 8. Veröffentlichung

- [ ] Datei-Name aussagekräftig und URL-freundlich (`thema-stichwort-vYY-MM.html`)
- [ ] Hoster: Datei ist über den Link erreichbar
- [ ] Link einmal selbst auf dem Handy geöffnet (nicht nur Desktop)
- [ ] Eigener Stichprobentest: Eingabe → Reload → Eingabe noch da?

---

Wenn alle Punkte abgehakt sind: 🎉 Der Onepager ist bereit für den Klassensatz.
