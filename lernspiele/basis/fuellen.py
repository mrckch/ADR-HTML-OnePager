"""Füllt eine Vorlage mit eigenem Inhalt.

Aufruf: python3 -I lernspiele/basis/fuellen.py <daten.json> <ziel.html>

daten.json:
  { "typ": "escape-room",                 # Datei templates/lernspiel/<typ>.html
    "werte": { "TITEL": "...", "UNTERTITEL": "...", "AUFGABEN": [...], "RAEUME": [...] } }

Ersetzt nur die Konstanten im Abschnitt ANPASSEN der Vorlage; was in "werte" fehlt, bleibt wie in der Vorlage.
Prüft die Daten (Pflichtfelder, Antwort unter den Optionen, Verweise) und gibt JSON aus: datei, typ, hinweise.
Bei Fehlern: Exit-Code 1 und "fehler" im JSON.
"""
import json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # ADR-HTML-OnePager


def norm(s):
    s = re.sub(r"\s+", " ", str(s).strip().lower()).replace("€", "").replace("euro", "").strip()
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return s


def js_wert(v):
    if isinstance(v, list):
        innen = ",\n  ".join(json.dumps(x, ensure_ascii=False) for x in v)
        s = "[\n  " + innen + ",\n]" if v else "[]"
    else:
        s = json.dumps(v, ensure_ascii=False)
    return s.replace("</", "<\\/")


def pruefe_aufgaben(aufgaben, wo, fehler, hinweise):
    for i, a in enumerate(aufgaben):
        if not isinstance(a, dict) or not a.get("frage") or a.get("antwort") in (None, "", []):
            fehler.append(f"{wo} {i}: frage und antwort nötig"); continue
        antworten = {norm(x) for x in (a["antwort"] if isinstance(a["antwort"], list) else [a["antwort"]])}
        if "optionen" in a:
            opt = [norm(o) for o in a["optionen"]]
            if not antworten & set(opt):
                fehler.append(f"{wo} {i} „{a['frage']}“: keine Option ist richtig")
            if sum(o in antworten for o in opt) > 1:
                hinweise.append(f"{wo} {i}: mehrere Optionen zählen als richtig")
            if len(set(opt)) != len(opt):
                fehler.append(f"{wo} {i}: doppelte Option")


def main():
    daten = json.loads(Path(sys.argv[1]).read_text(encoding="utf8"))
    ziel = Path(sys.argv[2])
    typ, werte = daten["typ"], daten["werte"]
    vorlage = REPO / "templates" / "lernspiel" / f"{typ}.html"
    if not vorlage.exists():
        raise SystemExit(json.dumps({"fehler": [f"Vorlage {typ} gibt es nicht"]}, ensure_ascii=False))
    html = vorlage.read_text(encoding="utf8")
    start, ende = html.index("// ===== ANPASSEN ====="), html.index("// ===== Ab hier nichts ändern =====")
    block = html[start:ende]
    erlaubt = re.findall(r"^const ([A-Z_]+) =", block, re.M)
    fehler, hinweise = [], []

    for k in werte:
        if k not in erlaubt:
            fehler.append(f"{k} gibt es in der Vorlage {typ} nicht (erlaubt: {', '.join(erlaubt)})")
    aufgaben = werte.get("AUFGABEN")
    if aufgaben is not None:
        pruefe_aufgaben(aufgaben, "Aufgabe", fehler, hinweise)
    n_auf = len(aufgaben) if aufgaben is not None else None
    for gruppe in ("RAEUME", "LEVELS"):
        for i, g in enumerate(werte.get(gruppe, [])):
            if not g.get("name") or not g.get("aufgaben"):
                fehler.append(f"{gruppe} {i}: name und aufgaben nötig"); continue
            if gruppe == "RAEUME" and not re.fullmatch(r"\d", str(g.get("ziffer", ""))):
                fehler.append(f"Raum {i}: ziffer muss eine Ziffer 0–9 sein")
            zahlen = [a for a in g["aufgaben"] if isinstance(a, int)]
            if zahlen and n_auf is None:
                fehler.append(f"{gruppe} {i}: verweist auf AUFGABEN, die fehlen")
            for a in zahlen:
                if n_auf is not None and not 0 <= a < n_auf:
                    fehler.append(f"{gruppe} {i}: Aufgabe {a} gibt es nicht")
            pruefe_aufgaben([a for a in g["aufgaben"] if isinstance(a, dict)], f"{gruppe} {i}", fehler, hinweise)
        if gruppe == "LEVELS" and werte.get("LEVELS") and "BESTANDEN" in werte:
            if any(len(l["aufgaben"]) < werte["BESTANDEN"] for l in werte["LEVELS"]):
                fehler.append("Ein Level hat weniger Aufgaben als BESTANDEN")
    paare = werte.get("PAARE")
    if paare is not None:
        if any(not isinstance(p, list) or len(p) != 2 for p in paare):
            fehler.append("PAARE: jedes Paar braucht genau zwei Texte")
        else:
            alle = [norm(x) for p in paare for x in p]
            if len(set(alle)) != len(alle):
                fehler.append("PAARE: ein Text kommt doppelt vor, dann ist das Paar nicht eindeutig")
            if not 4 <= len(paare) <= 10:
                hinweise.append(f"PAARE: {len(paare)} Paare; 6–8 passen am besten aufs Handy")
    if aufgaben is not None and len(aufgaben) < 10 and typ in ("zeit-challenge", "zielen-treffen"):
        hinweise.append("Wenige Aufgaben: Sie wiederholen sich schnell")
    if fehler:
        print(json.dumps({"fehler": fehler, "hinweise": hinweise}, ensure_ascii=False, indent=1)); sys.exit(1)

    for k, v in werte.items():
        if isinstance(v, list):
            muster = re.compile(rf"^const {k} = \[.*?^\];[^\n]*$", re.M | re.S)
        else:
            muster = re.compile(rf"^const {k} = [^\n]*$", re.M)
        block, n = muster.subn(lambda m: f"const {k} = {js_wert(v)};", block, count=1)
        if n != 1:
            fehler.append(f"{k}: in der Vorlage nicht als ersetzbare Konstante gefunden")
    if fehler:
        print(json.dumps({"fehler": fehler}, ensure_ascii=False, indent=1)); sys.exit(1)
    html = html[:start] + block + html[ende:]
    if "TITEL" in werte:
        html = re.sub(r"<title>.*?</title>", lambda m: "<title>" + werte["TITEL"].replace("<", "&lt;") + "</title>", html, count=1)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(html, encoding="utf8")
    print(json.dumps({"datei": str(ziel), "typ": typ, "hinweise": hinweise}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
