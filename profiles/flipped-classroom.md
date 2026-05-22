# Profil: Flipped Classroom (Video + Aufgaben)

- **Status:** Accepted
- **Datum:** 2026-05-22
- **Charakter:** Empfehlung / Style-Guide (siehe [ADR-0024](../adr/0024-schichten-modell-profile.md))

## Was ist das?

Ein Onepager für das **„Flipped Classroom"-Modell**: Schüler:innen sehen sich **zu Hause** (oder zur Stundenvorbereitung) ein **Erklärvideo** an, beantworten begleitende Fragen, und kommen vorbereitet in den Unterricht. Die eigentliche Vertiefung passiert dann gemeinsam in der Stunde.

Der Onepager bündelt das Video mit den Fragen — die Schüler:in muss nicht zwischen YouTube und Arbeitsblatt hin- und herwechseln.

## Typische Merkmale

- **Klassenstufe:** alle, besonders Sek I/II
- **Fachbereich:** alle
- **Zeitumfang:** 15–30 Min Video + 15–30 Min Aufgaben → ca. eine Hausaufgabe
- **Ziel-Typ:** Erarbeitung neuen Stoffes vor der Stunde, Vorbereitung
- **Gerät:** Laptop oder Tablet (Smartphone möglich, aber Video-Aufgabe-Wechsel auf kleinem Screen mühsam)

## Core-ADRs mit Schwerpunkt

| ADR | Besondere Relevanz |
|---|---|
| [ADR-0018](../adr/0018-aufgaben-karten.md) | Aufgaben-Karten für „während" und „nach" dem Video |
| [ADR-0002](../adr/0002-state-persistenz-localstorage.md) + [ADR-0003](../adr/0003-json-export-import.md) | Persistenz — der/die Schüler:in kann Video pausieren, später weitermachen |
| [ADR-0017](../adr/0017-save-status-toast.md) | Save-Status sichtbar, damit Eingaben während des Videos nicht verloren gehen |
| [ADR-0020](../adr/0020-html-export-eingebetteter-state.md) | HTML-Export für die Abgabe an die Lehrkraft |

## Core-ADRs abweichend oder weniger relevant

- **[ADR-0010](../adr/0010-loesungs-huerde.md):** Standard-Reveal — Schüler:in soll erst das Video gucken, dann antworten, dann Lösung sehen
- **Quiz:** möglich, aber meist nicht zentral (Diskussion folgt in der Stunde)
- **Canvas:** je nach Fach optional

## Spezifische didaktische Entscheidungen

### 1. Video prominent am Anfang

Direkt nach dem Lernziel kommt das Video — als großes, sichtbares Element. **Nicht** in einem Akkordeon versteckt, nicht klein gemacht.

```html
<div class="video-wrap">
  <iframe src="https://www.youtube-nocookie.com/embed/..." …></iframe>
</div>
<p class="video-meta">📺 Erklärvideo · 8:47 Min</p>
```

Snippet: [`templates/snippets/video-embed-snippet.html`](../templates/snippets/video-embed-snippet.html) — bietet Varianten für YouTube, Vimeo, lokales mp4 und externen Link.

### 2. Drei Aufgaben-Typen passend zum Flipped-Modell

Klare Sektionen-Aufteilung:

| Sektion | Inhalt |
|---|---|
| **Vor dem Video** | „Was vermutest du? Was weißt du schon zu …?" — Aktivierung von Vorwissen |
| **Während des Videos** | Aufgaben, die parallel zum Schauen bearbeitet werden — z. B. Lückentext zur Mitschrift, Fragen, die im Video beantwortet werden |
| **Nach dem Video** | Verständnisfragen, Anwendung, eigene Beispiele, was nicht klar ist → Liste an die Lehrkraft |

### 3. Notizfeld neben dem Video

Ein **„Was mir auffällt"-Feld** direkt neben/unter dem Video, das die ganze Bearbeitung über sichtbar bleibt:

```html
<div class="field">
  <label for="notizen">Was fällt dir auf? Was bleibt unklar? (Notizen während des Videos)</label>
  <textarea id="notizen" data-state="video-notizen" rows="4"></textarea>
</div>
```

### 4. „Was ich für die Stunde mitbringe"-Sektion am Ende

Eine spezielle Sektion, die explizit auf die kommende Stunde verweist:

```html
<div class="box info">
  <span class="box-title">📋 In die nächste Stunde mitbringen</span>
  <p>Diese drei Dinge bringst du mit (im Kopf oder im Heft notiert):</p>
  <ul>
    <li>Eine Frage, die im Video nicht beantwortet wurde</li>
    <li>Ein Beispiel, das du nicht aus dem Video kanntest</li>
    <li>Eine Verbindung zu etwas, das wir vorher gemacht haben</li>
  </ul>
</div>
```

Damit ist klar: das Onepager-Ergebnis dient als **Diskussionsgrundlage**, nicht als Selbstzweck.

### 5. Privatsphäre und Drittanbieter-Embed

YouTube/Vimeo setzen Cookies. Im Profil-Doku der Lehrkraft klar machen:
- **Bevorzugt**: `youtube-nocookie.com` oder Vimeo mit `?dnt=1` (Do Not Track)
- **Bei Minderjährigen / strengen DS-Vorgaben**: lokale mp4-Dateien hochladen
- **Schul-Firewall blockiert YouTube?** → Fallback-Link als externer Hinweis (Variante D im Snippet)

### 6. Druck-Tauglichkeit reduziert

Beim Drucken gibt es kein Video — der Onepager wird zu einem „nur Aufgaben"-Blatt. CSS im Snippet sorgt dafür, dass an der Video-Position ein Hinweis-Kasten steht: „📺 [Video — bitte online ansehen]". So ist der Druck nicht völlig sinnlos.

## Empfohlene Module

| Modul | Empfehlung |
|---|---|
| Lernziel-Box | ja |
| **Video-Embed-Snippet** | **ja, Hauptelement** |
| Aufgaben-Karten (Vor/Während/Nach) | **ja, in drei Sektionen** |
| Inhalts-Boxen (Tipp, Info) | ja, sparsam |
| Selbst-Korrektur | ja, bei eindeutigen Fragen |
| Lösungs-Hürde | Standard |
| Quiz | optional, eher selten |
| Canvas | optional |
| Fortschrittsbalken | ja |
| Save-Status | ja |
| Toast | ja |
| JSON-Export | ja |
| **HTML-Export** | ja (für Lehrer-Abgabe) |
| Reset-Dialog | ja |

## Aufgaben-Pattern (typisch)

```html
<article class="page">
  <header class="page-header">
    <span class="ue-label">Mathe · Klasse 7 · Vorbereitung Stunde 12</span>
    <h1>Bruchrechnung — Einführung</h1>
  </header>

  <div class="content">
    <div class="box lernziel">
      <span class="box-title">✦ Was du heute lernst</span>
      Du lernst, wie Brüche addiert werden und kommst vorbereitet
      in die nächste Stunde.
    </div>

    <h2>📺 Schau das Erklärvideo</h2>
    <div class="video-wrap">
      <iframe src="https://www.youtube-nocookie.com/embed/EXAMPLE_ID"
              title="Brüche addieren"
              allowfullscreen loading="lazy"
              sandbox="allow-scripts allow-same-origin allow-presentation"></iframe>
    </div>
    <p class="video-meta">📺 Erklärvideo · 8:47 Min · Schau es ein- bis zweimal an</p>

    <div class="field">
      <label for="notizen">Notizen (was fällt dir auf? Was bleibt unklar?)</label>
      <textarea id="notizen" data-state="notizen" rows="4"></textarea>
    </div>

    <hr class="page-break-hint">

    <h2>Vor dem Video — Was weißt du schon?</h2>
    <article class="aufgabe" data-task-id="vor-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Vor-Frage</span>
        <h3 class="aufgabe__titel">Wie würdest du 1/2 + 1/4 rechnen?</h3>
      </header>
      <div class="aufgabe__body">
        <textarea data-state="vor-1-antwort" rows="2"
          placeholder="Ich würde das so machen: …"></textarea>
      </div>
    </article>

    <h2>Nach dem Video — Was hast du gelernt?</h2>
    <article class="aufgabe" data-task-id="nach-1">
      <header class="aufgabe__header">
        <span class="aufgabe__nr">Aufgabe 1</span>
        <h3 class="aufgabe__titel">Berechne 1/3 + 1/4 wie im Video erklärt</h3>
      </header>
      <div class="aufgabe__body">
        <input data-state="nach-1-a" data-expected-keywords="7/12">
        <span class="feedback" data-feedback-for="nach-1-a"></span>
        <div class="reveal-actions">…</div>
      </div>
    </article>

    <h2>Für die Stunde</h2>
    <div class="box info">
      <span class="box-title">📋 In die nächste Stunde mitbringen</span>
      <ul>
        <li>Eine Frage, die im Video offen geblieben ist</li>
        <li>Eine Aufgabe, bei der du unsicher warst</li>
      </ul>
    </div>
    <div class="field">
      <label for="frage">Meine offene Frage:</label>
      <textarea id="frage" data-state="offene-frage" rows="2"></textarea>
    </div>
  </div>
</article>
```

## Anti-Patterns

- **Video nicht prominent** (klein, versteckt) → Schüler:innen überspringen es
- **Aufgaben ohne Bezug zum Video** → das Video wird sinnlos
- **Quiz mit Note nach dem Video** → erzeugt Druck statt Vorbereitung
- **YouTube ohne `nocookie`** → Datenschutz-schwach
- **Video > 20 Min** → Aufmerksamkeitsspanne überschritten, lieber in 2 Onepager teilen
- **Keine „Mit-in-die-Stunde"-Sektion** → der Flipped-Effekt verpufft

## Verwandte Profile

- [`profiles/erarbeitungsseite.md`](erarbeitungsseite.md) — Wenn die Erarbeitung KOMPLETT im Onepager passiert (statt mit Video)
- [`profiles/hausaufgaben.md`](hausaufgaben.md) — Flipped Classroom ist im Kern eine spezielle Hausaufgabe
- [`profiles/lesetext.md`](lesetext.md) — Analoge Variante mit Text statt Video
