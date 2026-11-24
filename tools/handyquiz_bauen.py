#!/usr/bin/env python3
"""Handyquiz bauen: Daten prüfen und in die Blaupause einsetzen.

    python3 tools/handyquiz_bauen.py daten.json -o seite.html
    python3 tools/handyquiz_bauen.py daten.json --nur-pruefen

Fehler brechen ab (Exit 1). Warnungen werden gezeigt und sind vor dem Veröffentlichen zu beheben oder bewusst
hinzunehmen; mit --streng brechen auch sie ab. Aufbau der Daten: profiles/handyquiz.md, Regeln: ADR-0035.
Nur Standardbibliothek.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

VORLAGE = Path(__file__).resolve().parent.parent / "templates" / "handyquiz-boilerplate.html"
MARKE = re.compile(r"<!--HQ-DATEN-->.*?<!--/HQ-DATEN-->", re.S)
TYPEN = ("eins", "mehr", "wf")


def pruefe(d):
    """Gibt (fehler, warnungen) zurück, beides Listen von Sätzen."""
    f, w = [], []
    for feld in ("slug", "titel", "fragen", "fehlvorstellungen"):
        if not d.get(feld):
            f.append(f"Feld „{feld}“ fehlt.")
    if f:
        return f, w
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d["slug"]):
        f.append("slug: nur Kleinbuchstaben, Ziffern und Bindestriche, ohne Umlaute.")
    if not d.get("label"):
        w.append("Feld „label“ fehlt (Startseite ohne Fach/Gruppe/Thema).")

    fv = d["fehlvorstellungen"]
    for fid, e in fv.items():
        if not str(e.get("titel", "")).strip() or not str(e.get("richtig", "")).strip():
            f.append(f"Fehlvorstellung {fid}: „titel“ (der Denkfehler) und „richtig“ (so ist es richtig) sind Pflicht.")

    fragen = d["fragen"]
    if not 5 <= len(fragen) <= 15:
        w.append(f"{len(fragen)} Fragen: für 10 Minuten am Handy sind 8–12 gut.")
    ids, texte, benutzt = set(), set(), {}
    zaehl = {t: 0 for t in TYPEN}

    def nutze(fid, wo):
        if fid not in fv:
            f.append(f"{wo}: Fehlvorstellung „{fid}“ gibt es nicht.")
        else:
            benutzt.setdefault(fid, set()).add(wo.split(":")[0])

    for i, q in enumerate(fragen, 1):
        qid = q.get("id") or ""
        wo = f"Frage {i} ({qid or 'ohne id'})"
        if not qid:
            f.append(f"{wo}: „id“ fehlt.")
        elif qid in ids:
            f.append(f"{wo}: id doppelt.")
        ids.add(qid)
        typ = q.get("typ")
        if typ not in TYPEN:
            f.append(f"{wo}: typ muss eins, mehr oder wf sein.")
            continue
        zaehl[typ] += 1
        frage = str(q.get("frage", "")).strip()
        if not frage:
            f.append(f"{wo}: „frage“ fehlt.")
        if frage.lower() in texte:
            w.append(f"{wo}: gleiche Frage kommt zweimal vor.")
        texte.add(frage.lower())
        if typ == "wf":
            if not isinstance(q.get("wahr"), bool):
                f.append(f"{wo}: wf braucht „wahr“: true oder false.")
            if not q.get("fv"):
                f.append(f"{wo}: wf braucht „fv“ – welche Fehlvorstellung steckt hinter der falschen Antwort?")
            else:
                nutze(q["fv"], wo)
            if "optionen" in q:
                w.append(f"{wo}: wf hat keine „optionen“ (Wahr/Falsch setzt die Seite selbst).")
            continue
        opts = q.get("optionen") or []
        richtig = [o for o in opts if o.get("richtig")]
        falsch = [o for o in opts if not o.get("richtig")]
        if not 3 <= len(opts) <= 5:
            f.append(f"{wo}: 3 bis 5 Antworten.")
        if typ == "eins" and len(richtig) != 1:
            f.append(f"{wo}: bei „eins“ genau eine richtige Antwort ({len(richtig)} markiert).")
        if typ == "mehr" and (len(richtig) < 2 or not falsch):
            f.append(f"{wo}: bei „mehr“ mindestens zwei richtige und eine falsche Antwort.")
        gesehen = set()
        for o in opts:
            t = str(o.get("text", "")).strip()
            if not t:
                f.append(f"{wo}: Antwort ohne „text“.")
            if t.lower() in gesehen:
                f.append(f"{wo}: Antwort „{t}“ doppelt.")
            gesehen.add(t.lower())
            if o.get("richtig"):
                if o.get("fv"):
                    f.append(f"{wo}: richtige Antwort „{t}“ hat „fv“ – nur Distraktoren zeigen auf Fehlvorstellungen.")
                if o.get("fv_wenn_fehlt"):
                    if typ != "mehr":
                        w.append(f"{wo}: „fv_wenn_fehlt“ wirkt nur bei „mehr“.")
                    nutze(o["fv_wenn_fehlt"], wo)
            else:
                if not o.get("fv"):
                    f.append(f"{wo}: Distraktor „{t}“ ohne „fv“ – jede falsche Antwort braucht eine Fehlvorstellung (ADR-0035).")
                else:
                    nutze(o["fv"], wo)
        if typ == "eins":
            ls = [len(str(o.get("text", ""))) for o in opts]
            r = len(str(richtig[0].get("text", ""))) if len(richtig) == 1 else 0
            if r and r == max(ls) and r > 1.5 * sorted(ls)[-2]:
                w.append(f"{wo}: richtige Antwort ist deutlich die längste – verrät sich.")

    for t in TYPEN:
        if zaehl[t] == 0:
            w.append(f"Kein Fragetyp „{t}“ dabei (Mischung aus eins, mehr und wf ist gewollt).")
    for fid in fv:
        if fid not in benutzt:
            w.append(f"Fehlvorstellung {fid} wird von keiner Frage angesteuert.")
        elif len(benutzt[fid]) < 2:
            w.append(f"Fehlvorstellung {fid} hängt nur an einer Frage – am Ende ist sie nur ein „vielleicht“ (besser zwei Fragen).")
    return f, w


def baue(d):
    vorlage = VORLAGE.read_text(encoding="utf-8")
    daten = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    block = f'<!--HQ-DATEN--><script type="application/json" id="hq-daten">\n{daten}\n</script><!--/HQ-DATEN-->'
    if not MARKE.search(vorlage):
        sys.exit("Blaupause ohne HQ-DATEN-Marke.")
    seite = MARKE.sub(lambda m: block, vorlage, count=1)
    return re.sub(r"<title>.*?</title>", f"<title>{html.escape(d['titel'])}</title>", seite, count=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("daten")
    ap.add_argument("-o", "--ausgabe")
    ap.add_argument("--nur-pruefen", action="store_true")
    ap.add_argument("--streng", action="store_true")
    a = ap.parse_args()
    d = json.loads(Path(a.daten).read_text(encoding="utf-8"))
    fehler, warn = pruefe(d)
    for s in fehler:
        print("FEHLER   " + s)
    for s in warn:
        print("WARNUNG  " + s)
    if fehler or (a.streng and warn):
        sys.exit(1)
    if a.nur_pruefen:
        print("Daten in Ordnung.")
        return
    ziel = Path(a.ausgabe or Path(a.daten).with_suffix(".html"))
    ziel.write_text(baue(d), encoding="utf-8")
    print(f"Gebaut: {ziel} ({len(d['fragen'])} Fragen, {len(d['fehlvorstellungen'])} Fehlvorstellungen)")


if __name__ == "__main__":
    main()
