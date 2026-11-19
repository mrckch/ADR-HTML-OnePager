#!/usr/bin/env python3
"""Fachwörter-Training bauen: Daten prüfen und in die Blaupause einsetzen.

    python3 tools/fachwoerter_bauen.py daten.json -o seite.html
    python3 tools/fachwoerter_bauen.py daten.json --nur-pruefen

Fehler brechen ab (Exit 1). Warnungen werden gezeigt und sind vor dem Veröffentlichen zu beheben oder
bewusst hinzunehmen; mit --streng brechen auch sie ab. Aufbau der Daten: profiles/fachwoerter.md.
Nur Standardbibliothek.
"""
import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

VORLAGE = Path(__file__).resolve().parent.parent / "templates" / "fachwoerter-boilerplate.html"
MARKE = re.compile(r"<!--FW-DATEN-->.*?<!--/FW-DATEN-->", re.S)
STAMM = 5  # so viele Anfangsbuchstaben eines Wortteils dürfen nicht in der Frage stehen


def norm(s):
    return re.sub(r"[\s\-–‐]+", "", unicodedata.normalize("NFC", str(s)).lower())


def wortteile(s):
    return [t for t in re.split(r"[^0-9A-Za-zÄÖÜäöüß]+", str(s)) if t]


def pruefe(d):
    """Gibt (fehler, warnungen) zurück, beides Listen von Sätzen."""
    f, w = [], []
    for feld in ("slug", "titel", "woerter"):
        if not d.get(feld):
            f.append(f"Feld „{feld}“ fehlt.")
    if f:
        return f, w
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d["slug"]):
        f.append("slug: nur Kleinbuchstaben, Ziffern und Bindestriche, ohne Umlaute.")
    for feld in ("label", "quelle"):
        if not d.get(feld):
            w.append(f"Feld „{feld}“ fehlt (Kopf der Seite bleibt dort leer).")
    woerter = d["woerter"]
    if len(woerter) < 4:
        f.append("Mindestens 4 Fachwörter (sonst gibt es keine drei falschen Antworten).")
    if len(woerter) > 30:
        w.append(f"{len(woerter)} Fachwörter sind viel für eine Sitzung: aufteilen oder „testlaenge“ setzen.")
    if "testlaenge" in d and not (isinstance(d["testlaenge"], int) and 4 <= d["testlaenge"] <= len(woerter)):
        f.append("testlaenge: ganze Zahl zwischen 4 und der Zahl der Fachwörter.")

    ids, namen = set(), set()
    laengste = kuerzeste = 0
    ungeprueft = []
    for i, e in enumerate(woerter, 1):
        wort = str(e.get("wort", "")).strip()
        wo = f"{i}. {wort or '(ohne Wort)'}"
        if not wort or not str(e.get("erklaerung", "")).strip():
            f.append(f"{wo}: „wort“ und „erklaerung“ sind Pflicht.")
            continue
        if "id" not in e:
            w.append(f"{wo}: keine „id“ – sie wird aus der Reihenfolge gebildet. Feste ids vergeben, "
                     "sonst passen gespeicherte Stände nach dem Umsortieren nicht mehr.")
        ident = e.get("id", f"v{i}")
        if ident in ids:
            f.append(f"{wo}: id „{ident}“ doppelt.")
        ids.add(ident)
        if norm(wort) in namen:
            f.append(f"{wo}: Fachwort doppelt.")
        namen.add(norm(wort))
        if e.get("geprueft") is False:
            ungeprueft.append(wort)

        falsch = e.get("falsch")
        if not (isinstance(falsch, list) and len(falsch) == 3 and all(str(x).strip() for x in falsch)):
            f.append(f"{wo}: genau drei falsche Antworten in „falsch“.")
            continue
        alle = [norm(wort)] + [norm(x) for x in falsch]
        if len(set(alle)) != 4:
            f.append(f"{wo}: die vier Antworten müssen verschieden sein.")
            continue

        frage = str(e.get("frage", "")).strip()
        if not frage:
            w.append(f"{wo}: keine „frage“ – der Test zeigt die Erklärung. Besser eine eigene Umschreibung.")
            frage = e["erklaerung"]
        elif norm(frage) == norm(e["erklaerung"]):
            w.append(f"{wo}: Frage ist wörtlich die Erklärung (Wiedererkennen statt Verstehen).")
        if not e.get("stamm_ok"):
            text = unicodedata.normalize("NFC", frage).lower()
            for teil in wortteile(wort):
                if len(teil) >= STAMM and teil[:STAMM].lower() in text:
                    f.append(f"{wo}: Die Frage verrät die Lösung – „{teil[:STAMM]}…“ steht im Fragetext. "
                             "Umformulieren (oder, wenn es nicht anders geht, \"stamm_ok\": true setzen).")
                    break

        # Länge: Die richtige Antwort darf nicht an der Länge zu erkennen sein.
        l, fl = len(wort), [len(str(x)) for x in falsch]
        if l > max(fl):
            laengste += 1
            if l > 1.6 * max(fl):
                w.append(f"{wo}: richtige Antwort ist deutlich länger als alle falschen ({l} gegen höchstens {max(fl)} Zeichen).")
        if l < min(fl):
            kuerzeste += 1
            if l < 0.6 * min(fl):
                w.append(f"{wo}: richtige Antwort ist deutlich kürzer als alle falschen ({l} gegen mindestens {min(fl)} Zeichen).")
        # Wortart grob: großgeschriebene und kleingeschriebene Antworten nicht mischen
        gross = [str(x).strip()[0].isupper() for x in [wort] + falsch]
        if gross.count(gross[0]) == 1:
            w.append(f"{wo}: richtige Antwort fällt durch Groß-/Kleinschreibung auf (andere Wortart als die falschen).")

    n = len(woerter)
    if n >= 8:
        if laengste > 0.4 * n:
            w.append(f"Bei {laengste} von {n} Fragen ist die richtige Antwort die längste (erwartet: etwa ein Viertel).")
        if kuerzeste > 0.4 * n:
            w.append(f"Bei {kuerzeste} von {n} Fragen ist die richtige Antwort die kürzeste (erwartet: etwa ein Viertel).")
    if ungeprueft:
        w.append(f"{len(ungeprueft)} Einträge sind im Glossar noch ungeprüft: " + ", ".join(ungeprueft)
                 + ". Vor dem Veröffentlichen ansehen lassen.")
    return f, w


def baue(d):
    vorlage = VORLAGE.read_text(encoding="utf-8")
    daten = json.dumps(d, ensure_ascii=False, indent=1).replace("</", "<\\/")
    block = f'<!--FW-DATEN--><script type="application/json" id="fw-daten">\n{daten}\n</script><!--/FW-DATEN-->'
    if len(MARKE.findall(vorlage)) != 1:
        sys.exit("Vorlage: Datenblock FW-DATEN nicht genau einmal gefunden.")
    seite = MARKE.sub(lambda _: block, vorlage)
    seite = seite.replace("<title>Fachwörter-Training</title>", f"<title>{html.escape(d['titel'])}</title>", 1)
    kopf = f"<!--\n  {d['titel']} · {d.get('label', '')}\n  Gebaut aus templates/fachwoerter-boilerplate.html"
    return seite.replace("<!--\n  Fachwörter-Training (Blaupause)", kopf + " (Blaupause Fachwörter-Training)", 1)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("daten", type=Path)
    p.add_argument("-o", "--ausgabe", type=Path)
    p.add_argument("--nur-pruefen", action="store_true")
    p.add_argument("--streng", action="store_true", help="Warnungen brechen ab")
    a = p.parse_args()
    d = json.loads(a.daten.read_text(encoding="utf-8"))
    fehler, warnungen = pruefe(d)
    for x in fehler:
        print("FEHLER   ", x)
    for x in warnungen:
        print("WARNUNG  ", x)
    if fehler or (a.streng and warnungen):
        sys.exit(1)
    if a.nur_pruefen:
        print(f"Geprüft: {len(d['woerter'])} Fachwörter, {len(warnungen)} Warnungen.")
        return
    if not a.ausgabe:
        sys.exit("Ausgabedatei fehlt (-o seite.html).")
    a.ausgabe.write_text(baue(d), encoding="utf-8")
    print(f"Gebaut: {a.ausgabe} ({len(d['woerter'])} Fachwörter, {len(warnungen)} Warnungen).")


if __name__ == "__main__":
    main()
