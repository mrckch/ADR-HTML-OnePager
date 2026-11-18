"""Spielt Lernspiele automatisch durch (PC- und Handy-Größe) und meldet Fehler.

Aufruf: python3 -I lernspiele/basis/test.py <datei.html|ordner> … [--bilder <ordner>]
Ohne Angabe: alle Vorlagen in templates/lernspiel/. Braucht playwright (chromium).
Erkennt den Typ an <meta name="lernspiel-typ">; Spiele ohne bekannten Typ werden nur geladen.
Ausgabe je Datei: ok | FEHLER mit Grund. Exit-Code 1, wenn eine Datei scheitert.
"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]  # ADR-HTML-OnePager
ANTWORTE = """() => { const f = document.querySelector('#buehne .frage'); if (!f) return 'keine-frage';
  const pool = (typeof AUFGABEN !== 'undefined' ? AUFGABEN : []).concat(
    typeof raeume !== 'undefined' ? raeume.flatMap(r => r.aufgaben) : [], typeof levels !== 'undefined' ? levels.flatMap(l => l.aufgaben) : []);
  const a = pool.find(x => x.frage === f.textContent); if (!a) return 'unbekannt';
  const b = [...document.querySelectorAll('#buehne [data-o]')].find(b => richtig(b.dataset.o, a.antwort));
  if (b && !b.disabled) { b.click(); return 'ok'; }
  const i = document.querySelector('#buehne input');
  if (i && !i.disabled) { i.value = String([].concat(a.antwort)[0]); document.querySelector('#buehne form button').click(); return 'ok'; }
  return 'gesperrt'; }"""


def spiele(pg, typ):
    if typ == "escape-room":
        for _ in range(200):
            if pg.inner_text("#raumName") == "Das Zahlenschloss": break
            pg.evaluate(ANTWORTE); pg.wait_for_timeout(1500)
        code = pg.evaluate("raeume.map(r => r.ziffer).join('')")
        pg.fill("#buehne input", code); pg.click("#buehne form button"); pg.wait_for_timeout(300)
        return pg.locator("text=Entkommen!").count() == 1
    if typ == "zielen-treffen":
        for _ in range(pg.evaluate("liste.length")):
            pg.evaluate(ANTWORTE); pg.wait_for_timeout(1500)
        return pg.locator("text=Punkte in dieser Runde").count() == 1
    if typ == "level-abenteuer":
        n = pg.evaluate("levels.length")
        pg.click('[data-l="0"]')
        for L in range(n):
            for _ in range(pg.evaluate(f"levels[{L}].aufgaben.length")):
                pg.evaluate(ANTWORTE); pg.wait_for_timeout(1000)
            if L < n - 1: pg.click("#nochmal")
        pg.click("#zurueck")
        return pg.locator("#levels button:not([disabled])").count() == n
    if typ == "memory-zuordnen":
        pg.evaluate("""() => { const k = {}; karten.forEach((c, i) => (k[c.k] = k[c.k] || []).push(i));
          for (const x in k) for (const i of k[x]) document.querySelector(`[data-i="${i}"]`).click(); }""")
        return pg.locator("text=Alle Paare gefunden").count() == 1
    if typ == "zeit-challenge":
        pg.click("#los")
        for _ in range(6):
            pg.evaluate(ANTWORTE); pg.wait_for_timeout(400)
        return pg.evaluate("punkte") >= 6
    return True


def main():
    args = sys.argv[1:]
    bilder = None
    if "--bilder" in args:
        i = args.index("--bilder"); bilder = Path(args[i + 1]); del args[i:i + 2]; bilder.mkdir(parents=True, exist_ok=True)
    dateien = []
    for a in args or [str(REPO / "templates" / "lernspiel")]:
        p = Path(a).resolve()
        dateien += sorted(p.rglob("*.html")) if p.is_dir() else [p]
    schlecht = 0
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for d in dateien:
            m = re.search(r'name="lernspiel-typ" content="([^"]+)"', d.read_text(encoding="utf8"))
            typ = m.group(1) if m else "?"
            gruende = []
            for w, h, name in [(390, 844, "handy"), (1200, 900, "pc")]:
                pg = b.new_page(viewport={"width": w, "height": h}); fehler = []
                pg.on("pageerror", lambda e: fehler.append(str(e)))
                pg.goto(d.as_uri()); pg.wait_for_timeout(300)
                if pg.evaluate("document.documentElement.scrollWidth") > w + 1: gruende.append(f"{name}: zu breit")
                if bilder: pg.screenshot(path=str(bilder / f"{d.stem}-{name}.png"))
                if name == "pc":
                    try:
                        if not spiele(pg, typ): gruende.append("Durchspielen nicht bis zum Ende gekommen")
                    except Exception as e:
                        gruende.append("Durchspielen: " + str(e).splitlines()[0])
                gruende += [f"{name}: {f}" for f in fehler]
                pg.close()
            print(f"{d.name} ({typ}):", "ok" if not gruende else "FEHLER " + "; ".join(gruende))
            schlecht += bool(gruende)
        b.close()
    sys.exit(1 if schlecht else 0)


if __name__ == "__main__":
    main()
