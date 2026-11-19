#!/usr/bin/env python3
"""Spielt ein Fachwörter-Training in Handy-Größe durch und meldet Fehler.

    python3 tools/fachwoerter_test.py seite.html [--bilder ordner]

Geprüft wird: Karten, Markierungen, beide Tests (Auswählen, Schreiben), abgebrochener Versuch nach
Neuladen, Fehler landen bei „Übe ich“, Verlauf, Stand vom Server auf einem zweiten Gerät, alter Stand
ohne „art“, Lehrkraft-Ansicht, Druckansicht. HTML-Share wird nachgestellt. Braucht playwright (chromium).
Exit-Code 1 bei Fehlern.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Nachgestelltes HTML-Share: merkt sich save() in window.__hs, load() liefert den mitgegebenen Stand.
HS = """window.__hs={saves:0,submits:[],stand:%s};
window.HTMLShare={readOnly:%s,load:()=>Promise.resolve(window.__hs.stand),
  save:o=>{window.__hs.saves++;window.__hs.stand=JSON.parse(JSON.stringify(o));},submit:o=>{window.__hs.submits.push(o);}};"""

fehler = []


def pruef(ok, text):
    print(("ok      " if ok else "FEHLER  ") + text)
    if not ok:
        fehler.append(text)


def antworte(pg, richtig=True, eingabe=None):
    """Beantwortet die aktuelle Frage und geht weiter. Gibt das Fachwort zurück."""
    wort = pg.evaluate("WID[lauf.order[lauf.pos]].wort")
    if pg.locator("#eingabe").count():
        pg.fill("#eingabe", eingabe if eingabe is not None else (wort if richtig else "xxxxxxxx"))
        pg.click("#pruefen")
    else:
        knopf = pg.locator(".test-optionen button")
        for i in range(knopf.count()):
            if (knopf.nth(i).inner_text() == wort) == richtig:
                knopf.nth(i).click()
                break
    pg.click("#test-weiter")
    return wort


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    datei = Path(args[0]).resolve()
    bilder = Path(sys.argv[sys.argv.index("--bilder") + 1]) if "--bilder" in sys.argv else None
    if bilder:
        bilder.mkdir(parents=True, exist_ok=True)
    url = datei.as_uri()
    with sync_playwright() as p:
        br = p.chromium.launch()
        js = []

        def geraet(stand=None, ro=False, ohne_hs=False):
            ctx = br.new_context(viewport={"width": 390, "height": 800})
            if not ohne_hs:
                ctx.add_init_script(HS % (json.dumps(stand), "true" if ro else "false"))
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: js.append(str(e)))
            pg.on("dialog", lambda d: d.accept())
            pg.goto(url)
            return ctx, pg

        # Gerät 1: Karten
        ctx, pg = geraet()
        n = pg.evaluate("W.length")
        pruef(pg.locator(".vokabel-eintrag").count() == n and n >= 4, f"{n} Karten aus dem Datenblock")
        pruef(pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth"), "kein waagerechtes Scrollen bei 390 px")
        pg.locator(".vokabel-flip").first.click()
        pruef(pg.locator(".vokabel-flip[aria-expanded=true] .vokabel-rueckseite").first.is_visible(), "Karte deckt die Lösung auf")
        pg.locator('.vokabel-feedback button[data-value="kannt"]').first.click()
        pruef("1 kann ich" in pg.inner_text("#stats"), "Markierung „Wusste ich“ zählt")
        if bilder:
            pg.screenshot(path=str(bilder / "karten.png"))

        # Test Auswählen: drei Antworten (die zweite falsch), dann neu laden und weitermachen
        pg.click("#modus-test")
        pg.click("#test-start")
        m = pg.evaluate("lauf.order.length")
        antworte(pg)
        falsches = antworte(pg, richtig=False)
        antworte(pg)
        pg.wait_for_timeout(100)
        pg.reload()
        pg.click("#modus-test")
        knopf = pg.locator("#test-fortsetzen")
        pruef(knopf.count() == 1 and f"Frage 4 von {m}" in knopf.inner_text(), "abgebrochener Versuch lässt sich fortsetzen")
        knopf.click()
        for _ in range(m - 3):
            antworte(pg)
        pruef(f"{m - 1} von {m}" in pg.inner_text(".test-ergebnis h2"), f"Ergebnis Auswählen: {m - 1} von {m}")
        marker = pg.evaluate("w=>{const x=W.find(e=>e.wort===w);return document.querySelector('[data-vokabel-id=\"'+x.id+'\"]').dataset.marker}", falsches)
        pruef(marker == "uebe", "falsch beantwortetes Wort steht bei „Übe ich“")
        if bilder:
            pg.screenshot(path=str(bilder / "ergebnis.png"), full_page=True)
        pg.click("#fehler-ueben")
        sichtbar = pg.locator(".vokabel-eintrag:visible").count()
        pruef(pg.evaluate("document.body.dataset.modus") == "karten" and sichtbar == 1, "„Nur meine Fehler üben“ zeigt genau die Fehler-Karte")

        # Test Schreiben: abweichende Groß-/Kleinschreibung zählt, Tippfehler nicht
        pg.click("#modus-schreiben")
        pg.click("#test-start")
        w1 = pg.evaluate("WID[lauf.order[lauf.pos]].wort")
        pg.fill("#eingabe", w1.swapcase().replace("-", " "))
        pg.click("#pruefen")
        pruef(pg.inner_text(".test-rueck strong").startswith("Richtig"), "Schreiben: andere Groß-/Kleinschreibung zählt als richtig")
        pg.click("#test-weiter")
        w2 = pg.evaluate("WID[lauf.order[lauf.pos]].wort")
        pg.fill("#eingabe", w2[:-1] + ("x" if w2[-1] != "x" else "y"))
        pg.click("#pruefen")
        pruef(pg.inner_text(".test-rueck strong").startswith("Fast") or len(w2) <= 4, "Schreiben: Tippfehler gibt „Fast“ und zählt nicht")
        pg.click("#test-weiter")
        for _ in range(m - 2):
            antworte(pg)
        pruef(f"{m - 1} von {m}" in pg.inner_text(".test-ergebnis h2"), f"Ergebnis Schreiben: {m - 1} von {m}")

        # Zweiter Versuch Auswählen, alles richtig: Verlauf zeigt Fortschritt
        pg.click("#modus-test")
        pg.click("#test-start")
        for _ in range(m):
            antworte(pg)
        text = pg.inner_text("#test")
        pruef("2. Versuch" in text and "Du wirst besser: 1 mehr" in text and f"Bester Versuch: {m} von {m}" in text, "Verlauf mit zwei Versuchen und „Du wirst besser“")
        hs = pg.evaluate("window.__hs")
        pruef(len(hs["submits"]) == 3 and len(hs["stand"]["versuche"]) == 3 and not hs["stand"]["laufend"], "drei Versuche an HTML-Share gemeldet und gespeichert")
        stand = hs["stand"]
        if bilder:
            pg.screenshot(path=str(bilder / "verlauf.png"), full_page=True)
        pg.emulate_media(media="print")
        pruef(pg.locator(".vokabel-eintrag:visible").count() == n and not pg.locator(".modus").is_visible(), "Druckansicht zeigt die ganze Wörterliste")
        ctx.close()

        # Gerät 2: leerer Browser, Stand kommt vom Server; ein dort offener Versuch auch
        stand2 = json.loads(json.dumps(stand))
        ids = [w["id"] for w in json.loads(datei.read_text(encoding="utf-8").split('id="fw-daten">')[1].split("</script>")[0])["woerter"]]
        stand2["laufend"] = {"schreiben": {"order": ids[:4], "pos": 2, "score": 1, "falsch": ["x"]}}
        ctx, pg = geraet(stand2)
        pg.wait_for_timeout(200)
        uebe = sum(1 for k, v in stand["karten"].items() if k.endswith("-marker") and v == "uebe")
        pruef(uebe >= 1 and f"{uebe} übe ich" in pg.inner_text("#stats"), "zweites Gerät: Karten-Markierungen vom Server")
        pg.click("#modus-test")
        pruef(pg.locator("#test .verlauf-liste li").count() == 2, "zweites Gerät: Verlauf vom Server")
        pg.click("#modus-schreiben")
        pruef("Frage 3 von 4" in pg.inner_text("#test-fortsetzen"), "zweites Gerät: offener Versuch vom Server")
        ctx.close()

        # Alter Stand (Versuche ohne „art“, kein „laufend“) und Lehrkraft-Ansicht
        alt = {"v": 1, "karten": {"richtung": "wort"}, "versuche": [{"t": "2026-01-01T08:00:00.000Z", "score": 2, "max": 4, "falsch": ["a", "b"]}]}
        ctx, pg = geraet(alt, ro=True)
        pg.wait_for_timeout(200)
        ro = pg.inner_text("#verlauf-ro")
        pruef("Auswählen" in ro and "2 von 4" in ro and "Noch zu üben: a, b" in ro, "Lehrkraft-Ansicht zeigt alten Stand mit Details")
        pruef(pg.evaluate("window.__hs.saves") == 0, "Lehrkraft-Ansicht speichert nichts")
        ctx.close()

        # Ohne HTML-Share (Datei lokal geöffnet)
        ctx, pg = geraet(ohne_hs=True)
        pg.click("#modus-test")
        pg.click("#test-start")
        antworte(pg)
        pruef(pg.locator(".test-frage").count() == 1, "läuft auch ohne HTML-Share")
        ctx.close()
        br.close()
    pruef(not js, "keine JavaScript-Fehler" + (": " + "; ".join(js[:3]) if js else ""))
    print(f"\n{'FEHLER: ' + str(len(fehler)) if fehler else 'Alles in Ordnung.'}")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
