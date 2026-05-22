# Profil: Code-Übungen (Informatik)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager für **Informatik-Aufgaben**, bei denen Schüler:innen Code lesen, analysieren oder selbst schreiben. Der Onepager bietet:
- **Code-Boxen** mit Syntax-Highlighting zum Lesen vorgegebenen Codes
- **Code-Eingabefelder** zum Schreiben eigenen Codes
- **Live-Preview** für HTML/CSS direkt im Browser
- **Externe Sandbox-Links** für ausführbaren Code (Python, JavaScript)

## Typische Merkmale

- **Klassenstufe:** Sek I (Wahlpflicht) bis Sek II (Informatik-Kurse)
- **Fachbereich:** Informatik (Hauptfall), MINT-Wahlpflicht
- **Zeitumfang:** Doppelstunde
- **Ziel-Typ:** Erarbeitung, Übung, Anwendung von Programmier-Konzepten
- **Gerät:** Laptop (idealerweise mit Tastatur); Tablet möglich, aber Tippen mühsam

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten mit Code-Boxen und Code-Eingabefeldern |
| [ADR-0022](../adr/0022-design-system-v2.md) | **JetBrains-Mono / `ui-monospace`** für Code-Bereiche, GitHub-Dark-Theme |
| [ADR-0001](../adr/0001-single-file-html-architektur.md) | Wir nutzen **keine** externen Syntax-Highlighter-Libs — einfacher eigener Highlighter im Snippet |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0011](../adr/0011-selbst-korrektur.md):** Code-Selbstkorrektur ist schwierig (verschiedene Lösungswege). Eher Keyword-Check oder „Code muss ein bestimmtes Wort enthalten"
- **Canvas:** nicht typisch
- **Lösungs-Hürde:** Standard, oft mit „Beispiel-Lösung"-Charakter

## Spezifische didaktische Entscheidungen

### 1. Drei Code-Bereich-Typen

| Typ | Wofür | Element |
|---|---|---|
| **Lesen** | Code zum Verstehen / Analysieren | `<pre class="code-box">` mit Syntax-Highlighting |
| **Schreiben** | Schüler:in tippt Code ein | `<textarea class="code-answer">` mit Monospace |
| **Live-Preview** | HTML/CSS interaktiv testen | Tab-Navigation mit `<iframe sandbox>` für Vorschau |

Snippet: [`templates/snippets/code-box-snippet.html`](../templates/snippets/code-box-snippet.html).

### 2. Externer Sandbox-Link statt eingebetteter Code-Ausführung

Eigentliche **Ausführung** von Python/JavaScript überlassen wir externen Diensten — z. B. [pythonsandbox.com](https://pythonsandbox.com), [trinket.io](https://trinket.io), [codepen.io](https://codepen.io). Der Onepager bietet einen Link mit „↗ Im Sandbox testen". Vorteile:

- Kein 5 MB Python-Interpreter inline (Pyodide wäre möglich, aber zu schwer)
- Trennung von Lerninhalt (im Onepager) und Ausführung (im Sandbox)
- Die Schüler:in lernt: Code wird woanders ausgeführt

**Ausnahme HTML/CSS**: Browser kann das von Natur aus, daher Live-Preview eingebaut (siehe oben).

### 3. Syntax-Highlighting per Span-Klassen (manuell)

Bei Lese-Code-Boxen wird das Highlighting **manuell** per Span-Klassen gemacht (`<span class="kw">`, `<span class="fn">` etc.). Das ist:
- mühsam zu schreiben (für die Lehrkraft)
- aber 100 % kontrolliert und ohne externe Libs

KI-Hilfe: einer KI sagen „färbe diesen Python-Code mit unseren Klassen" geht schnell.

Eigener mini-Highlighter (~30 Zeilen pro Sprache) ist möglich, aber das Profil bleibt explizit bewusst beim manuellen Pattern für Lernkontext.

### 4. Code-Eingabe-Optimierungen

`<textarea class="code-answer">` bekommt diese Attribute:

```html
<textarea class="code-answer"
          spellcheck="false"
          autocapitalize="off"
          autocorrect="off"
          tab-size="2"
          data-state="…"></textarea>
```

Zusätzliches JS (optional): Tab-Taste fügt Tab ein statt zum nächsten Element zu springen.

### 5. Aufgaben-Typen-Mix

Typische Mischung in einem Onepager:

| Aufgabe | Beispiel |
|---|---|
| **Code-Vorhersage** | „Was gibt dieser Code aus, bevor du ihn ausprobierst?" |
| **Code-Vervollständigung** | Lückencode, Schüler:in füllt fehlende Zeile aus |
| **Code-Korrektur** | „In diesem Code ist ein Fehler. Finde ihn und korrigiere." |
| **Code-Eigenschreibung** | „Schreibe ein Programm, das …" |
| **Code-Erklärung** | „Erkläre in eigenen Worten, was dieser Code macht" |

### 6. Privatsphäre bei externen Sandboxes

Externe Sandboxes haben eigene Datenschutz-Bestimmungen. In Schule:
- Empfehlung: Schul-eigene Code-Plattform, wenn vorhanden
- Sonst: Hinweis im Onepager, dass die Sandbox extern ist und Schüler:innen keine personenbezogenen Daten dort eingeben sollten

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja |
| Aufgaben-Karten | ja |
| **Code-Box (lesen)** | **ja, Hauptelement** |
| **Code-Answer (schreiben)** | **ja, Hauptelement** |
| **Live-Preview (HTML/CSS)** | optional, je nach Aufgabe |
| **Sandbox-Link** (extern) | ja, für Python/JS |
| Selbst-Korrektur (Keyword) | optional |
| Lösungs-Hürde | ja, mit „Beispiel-Lösung"-Charakter |
| Quiz | optional, für Code-Verständnis |
| Canvas | nein |
| Fortschrittsbalken | ja |
| Save-Status | ja, kritisch — getippter Code soll nicht verloren gehen |
| Toast | ja |
| JSON/HTML-Export | ja |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Informatik · Klasse 9 · Python — Funktionen</span>
    <h1>Funktionen verstehen und schreiben</h1>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Was du heute lernst</span>
      Du verstehst, wie Funktionen aufgebaut sind, und kannst eigene
      Python-Funktionen schreiben.
    </div>

    <h2>Lesen — wie funktioniert das?</h2>
    <article class="aufgabe" data-task-id="lesen-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">1</span>
        <h3 class="aufgabe__titel">Was gibt dieser Code aus?</h3>
      </header>
      <div class="aufgabe__body">
        <pre class="code-box"><span class="kw">def</span> <span class="fn">begruessung</span>(name):
    <span class="kw">return</span> <span class="st">"Hallo, "</span> + name + <span class="st">"!"</span>

<span class="kw">print</span>(<span class="fn">begruessung</span>(<span class="st">"Schüler:in"</span>))</pre>
        <input data-state="lesen-1-vorhersage"
               placeholder="Vorhersage: …"
               data-expected-keywords="Hallo,Schüler">
        <span class="feedback" data-feedback-for="lesen-1-vorhersage"></span>
        <a class="sandbox-link" href="https://pythonsandbox.com" target="_blank" rel="noopener">
          ↗ Im Python-Sandbox prüfen
        </a>
      </div>
    </article>

    <h2>Schreiben — jetzt du</h2>
    <article class="aufgabe" data-task-id="schreiben-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">2</span>
        <h3 class="aufgabe__titel">Schreibe eine Funktion, die das Quadrat einer Zahl zurückgibt</h3>
      </header>
      <div class="aufgabe__body">
        <p>Die Funktion soll <code>quadrat(5)</code> = 25 ergeben.</p>
        <textarea class="code-answer" data-state="schreiben-1-code"
                  spellcheck="false" autocapitalize="off"
                  placeholder="def quadrat(zahl):&#10;    …"></textarea>
        <a class="sandbox-link" href="https://pythonsandbox.com" target="_blank" rel="noopener">
          ↗ Im Python-Sandbox testen
        </a>
        <div class="reveal-actions">
          <button class="reveal-btn reveal-btn--solution" data-task-id="schreiben-1">🔍 Beispiel-Lösung</button>
        </div>
        <div class="solution-content" data-task-id="schreiben-1" hidden>
          <p><strong>Eine mögliche Lösung:</strong></p>
          <pre class="code-box"><span class="kw">def</span> <span class="fn">quadrat</span>(zahl):
    <span class="kw">return</span> zahl * zahl</pre>
          <p class="hint">Andere Wege sind möglich — z. B. <code>zahl ** 2</code>.</p>
        </div>
      </div>
    </article>
  </div>
</article>
```

## Anti-Patterns

- **Eigene Code-Ausführungs-Engine inline** (Pyodide, BrythonJS) → zu groß, verletzt Single-File-Geist
- **Externe Highlighter-Libs ohne Fallback** → bei Netzwerk-Problemen kein Highlighting
- **`spellcheck="true"` auf Code-Eingaben** → unterstreicht „Variablen" als Tippfehler
- **Selbst-Korrektur mit exaktem String-Match** → Code-Lösungen variieren zu sehr
- **Quiz statt offene Code-Aufgaben** → reduziert Programmieren auf Multiple Choice

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn ein Konzept neu erarbeitet wird (Lernpfad)
- [`profiles/lerntheke.md`](lerntheke.md) — Wenn Code-Übungen frei wählbar sind
- [`profiles/lesetext.md`](lesetext.md) — Wenn ein Code-Beispiel als „Text" analysiert wird, aber nicht selbst geschrieben
