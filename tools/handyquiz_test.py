#!/usr/bin/env python3
"""Spielt ein Handyquiz in Handy-Größe durch und meldet Fehler.

    python3 tools/handyquiz_test.py seite.html [--bilder ordner]

Geprüft wird: Start, alle Fragen richtig (volle Punktzahl, keine Denkfehler), alle Fragen mit Distraktoren falsch
(jede gewählte Fehlvorstellung erscheint am Ende), neues Mischen beim neuen Versuch, kein waagerechtes Scrollen bei
390 px, nichts in localStorage/sessionStorage, keine JS-Fehler. Braucht playwright (chromium). Exit-Code 1 bei Fehlern.
"""
import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

fehler = []


def pruef(ok, text):
    print(("ok      " if ok else "FEHLER  ") + text)
    if not ok:
        fehler.append(text)


def runde(pg, modus, bilder=None, name=""):
    """modus: richtig | falsch. Gibt (fragen-ids in Reihenfolge, erwartete fv) zurück."""
    reihenfolge, erwartet = [], set()
    n = pg.evaluate("__hq.fragen.length")
    for i in range(n):
        f = pg.evaluate("__hq.fragen[__hq.pos]")
        reihenfolge.append(f["id"])
        opts = f["optionen"]
        if modus == "richtig":
            wahl = [k for k, o in enumerate(opts) if o["richtig"]]
        else:
            falsche = [k for k, o in enumerate(opts) if not o["richtig"]]
            wahl = [falsche[0]]
            if opts[falsche[0]].get("fv"):
                erwartet.add(opts[falsche[0]]["fv"])
            if f["typ"] == "mehr":
                for k, o in enumerate(opts):
                    if o["richtig"] and o.get("fvFehlt"):
                        erwartet.add(o["fvFehlt"])
        for k in wahl:
            pg.click(f'.opt[data-k="{k}"]')
        if bilder and i == 0:
            pg.screenshot(path=str(Path(bilder) / f"{name}-{modus}-frage.png"))
        pg.click("#weiter")
        if modus == "falsch":
            pruef(pg.locator(".rueck.nein").count() == 1, f"Frage {f['id']}: falsche Antwort als falsch gemeldet")
            if opts[wahl[0]].get("fv"):
                pruef(pg.locator(".denkfehler").count() >= 1, f"Frage {f['id']}: Denkfehler direkt genannt")
        pg.click("#weiter")
    return reihenfolge, erwartet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seite")
    ap.add_argument("--bilder")
    a = ap.parse_args()
    url = Path(a.seite).resolve().as_uri()
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        js = []
        pg.on("pageerror", lambda e: js.append(str(e)))
        pg.goto(url)
        pruef(pg.locator("#los").count() == 1, "Startseite mit „Quiz starten“")
        pg.click("#los")
        n = pg.evaluate("__hq.fragen.length")
        r1, _ = runde(pg, "richtig", a.bilder, Path(a.seite).stem)
        pruef(pg.inner_text(".zahl").replace(" ", "") == f"{n}/{n}", f"alles richtig → {n}/{n}")
        pruef(pg.locator(".fv-liste li").count() == 0, "alles richtig → keine Denkfehler")
        pg.click("#nochmal")
        r2, erwartet = runde(pg, "falsch", a.bilder, Path(a.seite).stem)
        pruef(pg.inner_text(".zahl").replace(" ", "") == f"0/{n}", f"alles falsch → 0/{n}")
        gezeigt = pg.locator(".fv-liste li").count()
        pruef(gezeigt == len(erwartet), f"Ergebnis nennt {gezeigt} Denkfehler, erwartet {len(erwartet)}")
        if a.bilder:
            pg.screenshot(path=str(Path(a.bilder) / f"{Path(a.seite).stem}-ergebnis.png"), full_page=True)
        pruef(r1 != r2, "neuer Versuch mischt die Fragen neu")
        breit = pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
        pruef(breit, "kein waagerechtes Scrollen bei 390 px")
        pruef(pg.evaluate("localStorage.length + sessionStorage.length") == 0, "nichts gespeichert")
        pruef(not js, "keine JS-Fehler" + (f": {js}" if js else ""))
        br.close()
    print("Alles in Ordnung." if not fehler else f"{len(fehler)} Fehler.")
    sys.exit(1 if fehler else 0)


if __name__ == "__main__":
    main()
