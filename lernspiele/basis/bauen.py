"""Baut alle Spiel-Vorlagen nach templates/lernspiel/<typ>.html (ADR-0033).
Aufruf: python3 -I lernspiele/basis/bauen.py [<zielordner>]   (ohne Angabe: templates/lernspiel/ im Repo)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from basis import CSS, JS, KOPF

ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'templates' / 'lernspiel'

# Beispielinhalt Brüche (Kl. 6), in allen Vorlagen gleich, damit man den Vergleich hat.
AUFGABEN = """const AUFGABEN = [
  // frage: was angezeigt wird · antwort: richtige Antwort (Liste = mehrere sind richtig)
  // optionen: Auswahl zum Antippen (weglassen = Eingabefeld) · tipp: erscheint nach falscher Antwort
  { frage: '1/2 + 1/4 = ?', antwort: '3/4', optionen: ['3/4', '2/6', '1/6', '2/4'], tipp: 'Erst gleichnamig machen: 1/2 = 2/4.' },
  { frage: 'Wie viel sind 3/4 von 20?', antwort: 15, tipp: '20 : 4 = 5, dann mal 3.' },
  { frage: 'Schreibe 0,25 als gekürzten Bruch.', antwort: '1/4', optionen: ['1/4', '2/5', '1/25', '25/10'] },
  { frage: 'Schreibe 2/5 als Dezimalzahl.', antwort: '0,4', tipp: '2/5 = 4/10.' },
  { frage: 'Kürze 6/8 so weit wie möglich.', antwort: '3/4', optionen: ['3/4', '2/3', '6/4', '1/2'] },
  { frage: '1/3 · 3/5 = ?', antwort: ['1/5', '3/15'], optionen: ['1/5', '4/8', '3/8', '1/15'], tipp: 'Zähler mal Zähler, Nenner mal Nenner.' },
  { frage: '5/6 − 1/3 = ?', antwort: ['1/2', '3/6'], optionen: ['1/2', '4/3', '4/6', '1/3'], tipp: '1/3 = 2/6.' },
  { frage: '1/2 : 1/4 = ?', antwort: 2, tipp: 'Mit dem Kehrwert malnehmen: 1/2 · 4/1.' },
  { frage: 'Was ist größer: 3/5 oder 2/3?', antwort: '2/3', optionen: ['3/5', '2/3', 'beide gleich'], tipp: 'Auf Fünfzehntel bringen: 9/15 und 10/15.' },
  { frage: 'Wie viel Prozent sind 7/10?', antwort: ['70 %', '70%', '70'], optionen: ['70 %', '7 %', '0,7 %', '17 %'] },
  { frage: 'Schreibe 1 1/2 als unechten Bruch.', antwort: '3/2', optionen: ['3/2', '2/2', '1/2', '11/2'] },
  { frage: '3/8 + 1/8 = ?', antwort: ['1/2', '4/8'], optionen: ['1/2', '4/16', '3/64', '2/8'] },
];"""

SPIELE = {}

# ---------- 1 Escape-Room ----------
SPIELE["escape-room"] = dict(typ="Escape-Room", titel="Escape-Room: Brüche", extra_css="""
.raum{font-size:1.1rem;font-weight:700}
.ziffern{display:flex;gap:10px;justify-content:center;margin:10px 0}
.ziffern b{display:grid;place-items:center;width:52px;height:64px;border-radius:var(--radius);border:2px dashed var(--border-2);font:700 2rem/1 var(--font-display)}
.ziffern b.da{border-style:solid;border-color:var(--gut);color:var(--gut);animation:auf .4s}
@keyframes auf{from{transform:scale(.4)}to{transform:scale(1)}}
.schloss{font-size:3rem}
""", body="""
<div class="karte">
  <div class="leiste"><span id="raumName"></span><span id="raumNr"></span></div>
  <div class="ziffern" id="ziffern" aria-label="Gefundene Ziffern"></div>
</div>
<div class="karte" id="buehne"></div>
<p class="rm" id="rm" aria-live="polite"></p>
""", anpassen="""// ===== ANPASSEN =====
const TITEL = 'Escape-Room: Brüche';
const UNTERTITEL = 'Löse die Aufgaben in jedem Raum. Jeder Raum verrät dir eine Ziffer für das Zahlenschloss.';
// Jeder Raum: Name, Ziffer (wird nach dem Raum aufgedeckt) und Aufgaben.
const RAEUME = [
  { name: 'Raum 1: Die Bibliothek', ziffer: '4', aufgaben: [0, 1, 2] },
  { name: 'Raum 2: Das Labor', ziffer: '7', aufgaben: [3, 4, 5] },
  { name: 'Raum 3: Der Tresorraum', ziffer: '2', aufgaben: [6, 7, 8] },
];  // Zahlen = Position in AUFGABEN (0 = erste). Statt Zahl geht auch eine ganze Aufgabe { frage, antwort }.
""" + AUFGABEN, spiel=r"""
$('#titel').textContent = TITEL; $('#untertitel').textContent = UNTERTITEL; document.title = TITEL;
const raeume = RAEUME.map(r => ({ ...r, aufgaben: r.aufgaben.map(a => typeof a === 'number' ? AUFGABEN[a] : a) }));
// ADR-0033: keine Uhr im Escape-Room – Zeitdruck nur in der Challenge
let r = 0, a = 0;
function ziffern() { $('#ziffern').innerHTML = raeume.map((x, i) => `<b class="${i < r ? 'da' : ''}">${i < r ? x.ziffer : '?'}</b>`).join(''); }
function rm(t, k) { $('#rm').textContent = t; $('#rm').className = 'rm ' + (k || ''); }
function weiter() {
  ziffern();
  if (r >= raeume.length) return schloss();
  const raum = raeume[r]; $('#raumName').textContent = raum.name; $('#raumNr').textContent = `Aufgabe ${a + 1}/${raum.aufgaben.length}`;
  zeigeAufgabe($('#buehne'), raum.aufgaben[a], ok => {
    if (ok) { rm('Richtig!', 'gut'); a++;
      if (a >= raum.aufgaben.length) { a = 0; r++; ziffern(); rm(`Raum geschafft! Deine Ziffer: ${raum.ziffer}`, 'gut'); setTimeout(weiter, 1400); }
      else setTimeout(weiter, 700);
    } else { rm('Noch nicht. ' + (raum.aufgaben[a].tipp || 'Versuch es noch einmal.'), 'schlecht'); setTimeout(weiter, 1800); }
  });
}
function schloss() {
  $('#raumName').textContent = 'Das Zahlenschloss'; $('#raumNr').textContent = '';
  $('#buehne').innerHTML = `<div class="mitte"><div class="schloss" aria-hidden="true">🔒</div><p class="frage">Gib den Code aus allen Räumen ein.</p>
    <form class="eingabe"><input inputmode="numeric" aria-label="Code" autocomplete="off"><button class="haupt">Öffnen</button></form></div>`;
  const f = $('#buehne form'), i = f.querySelector('input'); i.focus();
  f.addEventListener('submit', e => { e.preventDefault();
    if (i.value.trim() === raeume.map(x => x.ziffer).join('')) {
      $('#buehne').innerHTML = `<div class="mitte"><div class="schloss" aria-hidden="true">🔓</div><p class="gross">Entkommen!</p><p>Alle ${raeume.length} Räume geschafft.</p><button class="haupt" onclick="location.reload()">Noch einmal</button></div>`; rm('');
    } else rm('Der Code stimmt nicht. Schau auf deine Ziffern.', 'schlecht'); });
}
weiter();
""")

# ---------- 2 Zielen und Treffen ----------
SPIELE["zielen-treffen"] = dict(typ="Zielen und Treffen", titel="Zielscheibe: Brüche", extra_css="""
canvas{display:block;width:100%;max-width:min(420px,42vh);height:auto;margin:0 auto;aspect-ratio:1}
""", body="""
<div class="karte"><div class="leiste"><span id="wurf"></span><span id="punkte">0 Punkte</span></div></div>
<div class="karte"><canvas id="scheibe" width="420" height="420" role="img" aria-label="Zielscheibe"></canvas></div>
<div class="karte" id="buehne"></div>
<p class="rm" id="rm" aria-live="polite"></p>
""", anpassen="""// ===== ANPASSEN =====
const TITEL = 'Zielscheibe: Brüche';
const UNTERTITEL = 'Jede richtige Antwort ist ein Treffer. Je schneller du antwortest, desto näher an der Mitte.';
const WUERFE = 10;           // Aufgaben pro Runde
const SCHNELL_SEKUNDEN = 8;  // so schnell gibt es die Mitte
""" + AUFGABEN, spiel=r"""
$('#titel').textContent = TITEL; $('#untertitel').textContent = UNTERTITEL; document.title = TITEL;
const cv = $('#scheibe'), g = cv.getContext('2d'), M = 210, R = 190, RINGE = 10;
const farben = ['#f2f2f2', '#f2f2f2', '#222', '#222', '#2f6fd6', '#2f6fd6', '#d63a2f', '#d63a2f', '#f2c94c', '#f2c94c'];
const treffer = []; let n = 0, punkte = 0, t0;
const liste = mischen(AUFGABEN).slice(0, WUERFE);
const leise = matchMedia('(prefers-reduced-motion: reduce)').matches;
function malen(pfeil) {
  g.clearRect(0, 0, 420, 420);
  for (let i = 0; i < RINGE; i++) { g.beginPath(); g.arc(M, M, R * (1 - i / RINGE), 0, 7); g.fillStyle = farben[i]; g.fill(); g.strokeStyle = '#888'; g.lineWidth = 1; g.stroke(); }
  treffer.concat(pfeil ? [pfeil] : []).forEach(p => { g.beginPath(); g.arc(p.x, p.y, 7, 0, 7); g.fillStyle = '#17243d'; g.fill(); g.strokeStyle = '#fff'; g.lineWidth = 2; g.stroke(); });
}
function wurf(ok) {
  const sek = (Date.now() - t0) / 1000;
  // Treffer: Ring nach Antwortzeit (10 = Mitte); daneben: außerhalb der Scheibe
  const ring = ok ? Math.max(1, Math.round(10 - Math.max(0, sek - SCHNELL_SEKUNDEN) / 2)) : 0;
  const ab = ok ? R * ((10 - ring) + Math.random() * .9) / RINGE : R + 12 + Math.random() * 10, w = Math.random() * 6.283;
  const ziel = { x: M + ab * Math.cos(w), y: M + ab * Math.sin(w) }, von = { x: M, y: 440 };
  return new Promise(fertig => {
    if (leise) { treffer.push(ziel); malen(); return fertig(ring); }
    const t1 = performance.now();
    (function schritt(t) { const k = Math.min(1, (t - t1) / 450);
      malen({ x: von.x + (ziel.x - von.x) * k, y: von.y + (ziel.y - von.y) * k - Math.sin(k * 3.14) * 60 });
      if (k < 1) requestAnimationFrame(schritt); else { treffer.push(ziel); malen(); fertig(ring); } })(t1);
  });
}
function rm(t, k) { $('#rm').textContent = t; $('#rm').className = 'rm ' + (k || ''); }
function naechste() {
  if (n >= liste.length) {
    $('#buehne').innerHTML = `<div class="mitte"><p class="gross">${punkte} von ${WUERFE * 10}</p><p>Punkte in dieser Runde</p><button class="haupt" onclick="location.reload()">Neue Runde</button></div>`;
    return rm('');
  }
  $('#wurf').textContent = `Wurf ${n + 1} von ${liste.length}`; t0 = Date.now();
  zeigeAufgabe($('#buehne'), liste[n], async ok => {
    const ring = await wurf(ok); punkte += ring; $('#punkte').textContent = punkte + ' Punkte';
    rm(ok ? `Treffer! ${ring} Punkte.` : 'Daneben – kein Abzug. Richtig wäre: ' + [].concat(liste[n].antwort)[0] + (liste[n].tipp ? ' – ' + liste[n].tipp : ''), ok ? 'gut' : 'schlecht');
    n++; setTimeout(naechste, ok ? 900 : 2200);
  });
}
malen(); naechste();
""")

# ---------- 3 Level-Abenteuer ----------
SPIELE["level-abenteuer"] = dict(typ="Level-Abenteuer", titel="Level-Abenteuer: Brüche", extra_css="""
.weg{position:relative;height:64px;margin:6px 0 2px}
.weg::before{content:"";position:absolute;left:4%;right:4%;top:50%;border-top:3px dashed var(--border-2)}
.weg .stein{position:absolute;top:50%;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--border-2)}
.weg .stein.ok{background:var(--gut)}
.weg .figur{position:absolute;top:50%;font-size:2.2rem;transform:translate(-50%,-60%);transition:left .5s}
.weg .ziel{position:absolute;right:0;top:50%;transform:translateY(-55%);font-size:1.8rem}
.levels{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
""", body="""
<div class="karte" id="uebersicht"><p class="frage">Wähle ein Level</p><div class="levels" id="levels"></div></div>
<div id="spiel" hidden>
  <div class="karte"><div class="leiste"><span id="levelName"></span><span id="stand"></span></div>
    <div class="weg" id="weg" aria-hidden="true"></div></div>
  <div class="karte" id="buehne"></div>
  <p class="rm" id="rm" aria-live="polite"></p>
  <button type="button" id="zurueck">Zur Übersicht</button>
</div>
""", anpassen="""// ===== ANPASSEN =====
const TITEL = 'Level-Abenteuer: Brüche';
const UNTERTITEL = 'Bring die Figur ans Ziel. Mit genug richtigen Antworten schaltest du das nächste Level frei.';
const FIGUR = '🦊';
const ZIEL = '🏁';
const SPEICHER_NAME = 'level-brueche';  // für jedes Spiel anders wählen
const BESTANDEN = 3;                     // so viele richtige Antworten pro Level
// Jedes Level: Name und Aufgaben (Zahl = Position in AUFGABEN oder eine ganze Aufgabe { frage, antwort }).
const LEVELS = [
  { name: 'Level 1: Kürzen und Umwandeln', aufgaben: [2, 3, 4, 9] },
  { name: 'Level 2: Plus und Minus', aufgaben: [0, 6, 11, 8] },
  { name: 'Level 3: Mal und Geteilt', aufgaben: [5, 7, 1, 10] },
];
""" + AUFGABEN, spiel=r"""
$('#titel').textContent = TITEL; $('#untertitel').textContent = UNTERTITEL; document.title = TITEL;
const levels = LEVELS.map(l => ({ ...l, aufgaben: l.aufgaben.map(a => typeof a === 'number' ? AUFGABEN[a] : a) }));
let frei = speicher.lies(SPEICHER_NAME, 0), L, i, ok;
function uebersicht() {
  $('#spiel').hidden = true; $('#uebersicht').hidden = false;
  $('#levels').innerHTML = levels.map((l, k) => `<button type="button" data-l="${k}" ${k > frei ? 'disabled' : ''}>${k > frei ? '🔒 ' : k < frei ? '✓ ' : ''}${l.name}</button>`).join('');
  $('#levels').querySelectorAll('[data-l]').forEach(b => b.addEventListener('click', () => starte(+b.dataset.l)));
}
function weg() {
  const n = levels[L].aufgaben.length, pos = k => 6 + k * (82 / n);
  $('#weg').innerHTML = levels[L].aufgaben.map((_, k) => `<span class="stein ${k < i ? 'ok' : ''}" style="left:${pos(k + 1)}%"></span>`).join('')
    + `<span class="figur" style="left:${pos(ok)}%">${FIGUR}</span><span class="ziel">${ZIEL}</span>`;
}
function rm(t, k) { $('#rm').textContent = t; $('#rm').className = 'rm ' + (k || ''); }
function starte(k) { L = k; i = 0; ok = 0; $('#uebersicht').hidden = true; $('#spiel').hidden = false; rm(''); runde(); }
function runde() {
  const auf = levels[L].aufgaben; $('#levelName').textContent = levels[L].name; $('#stand').textContent = `${ok} richtig · ${BESTANDEN} nötig`; weg();
  if (i >= auf.length) {
    const geschafft = ok >= BESTANDEN;
    if (geschafft && L === frei) { frei = L + 1; speicher.schreib(SPEICHER_NAME, frei); }
    $('#buehne').innerHTML = `<div class="mitte"><p class="gross">${geschafft ? 'Geschafft!' : 'Fast!'}</p><p>${ok} von ${auf.length} richtig.</p>
      <button class="haupt" id="nochmal">${geschafft && L < levels.length - 1 ? 'Nächstes Level' : 'Noch einmal'}</button></div>`;
    $('#nochmal').addEventListener('click', () => starte(geschafft && L < levels.length - 1 ? L + 1 : L)); return;
  }
  zeigeAufgabe($('#buehne'), auf[i], r => {
    if (r) { ok++; rm('Richtig! Die Figur läuft weiter.', 'gut'); }
    else rm('Leider falsch. Richtig: ' + [].concat(auf[i].antwort)[0] + (auf[i].tipp ? ' – ' + auf[i].tipp : ''), 'schlecht');
    i++; setTimeout(runde, r ? 900 : 2400);
  });
}
$('#zurueck').addEventListener('click', uebersicht);
uebersicht();
""")

# ---------- 4 Zuordnen (Memory) ----------
SPIELE["memory-zuordnen"] = dict(typ="Zuordnen (Memory)", titel="Memory: Brüche und Dezimalzahlen", extra_css="""
.feld{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.feld button{aspect-ratio:1/1;min-height:0;padding:4px;font-size:clamp(.9rem,3.6vw,1.3rem);font-weight:700;background:var(--blue);color:transparent;border-color:var(--blue);transition:transform .25s}
.feld button.offen,.feld button.weg{background:var(--bg-card);color:var(--ink)}
.feld button.weg{border-color:var(--gut);opacity:.6}
""", body="""
<div class="karte"><div class="leiste"><span id="paare"></span><span id="zuege">0 Züge</span></div></div>
<div class="karte"><div class="feld" id="feld"></div></div>
<p class="rm" id="rm" aria-live="polite"></p>
""", anpassen="""// ===== ANPASSEN =====
const TITEL = 'Memory: Brüche und Dezimalzahlen';
const UNTERTITEL = 'Decke zwei Karten auf. Finde die Paare, die den gleichen Wert haben.';
// Jedes Paar: zwei Texte, die zusammengehören. 8 Paare ergeben 16 Karten.
const PAARE = [
  ['1/2', '0,5'], ['1/4', '0,25'], ['3/4', '0,75'], ['1/5', '0,2'],
  ['2/5', '0,4'], ['1/10', '0,1'], ['3/10', '30 %'], ['1/8', '0,125'],
];
""", spiel=r"""
$('#titel').textContent = TITEL; $('#untertitel').textContent = UNTERTITEL; document.title = TITEL;
const karten = mischen(PAARE.flatMap((p, k) => p.map(t => ({ t, k }))));
let offen = [], zuege = 0, gefunden = 0, sperre = false;
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
$('#feld').innerHTML = karten.map((c, i) => `<button type="button" data-i="${i}" aria-label="Verdeckte Karte ${i + 1}">${esc(c.t)}</button>`).join('');
const stand = () => { $('#paare').textContent = `${gefunden} von ${PAARE.length} Paaren`; $('#zuege').textContent = zuege + ' Züge'; };
$('#feld').addEventListener('click', e => {
  const b = e.target.closest('[data-i]'); if (!b || sperre || b.classList.contains('offen') || b.classList.contains('weg')) return;
  b.classList.add('offen'); b.setAttribute('aria-label', karten[b.dataset.i].t); offen.push(b);
  if (offen.length < 2) return;
  zuege++; const [x, y] = offen; offen = [];
  if (karten[x.dataset.i].k === karten[y.dataset.i].k) {
    [x, y].forEach(z => { z.classList.replace('offen', 'weg'); z.disabled = true; }); gefunden++;
    $('#rm').textContent = 'Passt!'; $('#rm').className = 'rm gut';
    if (gefunden === PAARE.length) { $('#rm').innerHTML = `Alle Paare gefunden in ${zuege} Zügen! <button class="haupt" onclick="location.reload()">Neues Spiel</button>`; }
  } else {
    sperre = true; $('#rm').textContent = 'Kein Paar.'; $('#rm').className = 'rm schlecht';
    setTimeout(() => { [x, y].forEach(z => { z.classList.remove('offen'); z.setAttribute('aria-label', 'Verdeckte Karte'); }); sperre = false; }, 1100);
  }
  stand();
});
stand();
""")

# ---------- 5 Zeit-Challenge ----------
SPIELE["zeit-challenge"] = dict(typ="60-Sekunden-Challenge", titel="60 Sekunden: Brüche", extra_css="""
.uhr{font-size:2rem;font-weight:800;font-variant-numeric:tabular-nums}
.uhr.knapp{color:var(--schlecht)}
.combo{color:var(--blue)}
""", body="""
<div class="karte"><div class="leiste"><span class="uhr" id="uhr"></span><span class="combo" id="combo"></span><span id="punkte">0 Punkte</span></div>
  <div class="balken" style="margin-top:10px"><i id="balken" style="width:100%"></i></div></div>
<div class="karte" id="buehne"></div>
<p class="rm" id="rm" aria-live="polite"></p>
""", anpassen="""// ===== ANPASSEN =====
const TITEL = '60 Sekunden: Brüche';
const UNTERTITEL = 'So viele Aufgaben wie möglich. Drei richtige hintereinander verdoppeln deine Punkte.';
const SEKUNDEN = 60;
const SPEICHER_NAME = 'challenge-brueche';  // Bestwert bleibt nur auf diesem Gerät
// Tipp: Für dieses Spiel am besten Aufgaben mit „optionen“ (Antippen geht schneller als Tippen).
""" + AUFGABEN, spiel=r"""
$('#titel').textContent = TITEL; $('#untertitel').textContent = UNTERTITEL; document.title = TITEL;
let punkte = 0, serie = 0, rest = SEKUNDEN, stapel = [], tick, laeuft = false;
const best = () => speicher.lies(SPEICHER_NAME, 0);
function rm(t, k) { $('#rm').textContent = t; $('#rm').className = 'rm ' + (k || ''); }
function anzeige() {
  $('#uhr').textContent = rest + ' s'; $('#uhr').classList.toggle('knapp', rest <= 10);
  $('#balken').style.width = (100 * rest / SEKUNDEN) + '%';
  $('#punkte').textContent = punkte + ' Punkte'; $('#combo').textContent = serie >= 3 ? `Combo ×2 (${serie})` : '';
}
function startbild() {
  anzeige();
  $('#buehne').innerHTML = `<div class="mitte"><p class="frage">Bereit?</p><p>Bestwert auf diesem Gerät: ${best()}</p><button class="haupt" id="los">Los geht's</button></div>`;
  $('#los').addEventListener('click', start); $('#los').focus();
}
function start() {
  punkte = 0; serie = 0; rest = SEKUNDEN; laeuft = true; rm(''); anzeige();
  tick = setInterval(() => { rest--; anzeige(); if (rest <= 0) ende(); }, 1000); frage();
}
function frage() {
  if (!laeuft) return;
  if (!stapel.length) stapel = mischen(AUFGABEN);
  const a = stapel.pop();
  zeigeAufgabe($('#buehne'), a, ok => {
    if (!laeuft) return;
    if (ok) { serie++; punkte += serie >= 3 ? 2 : 1; rm('Richtig!', 'gut'); }
    else { serie = 0; rm('Richtig ist ' + [].concat(a.antwort)[0] + (a.tipp ? ' – ' + a.tipp : ''), 'schlecht'); }  // ADR-0033: Tipp, kein Abzug
    anzeige(); setTimeout(frage, ok ? 300 : 1200);
  });
}
function ende() {
  clearInterval(tick); laeuft = false; rest = 0; anzeige();
  const neu = punkte > best(); if (neu) speicher.schreib(SPEICHER_NAME, punkte);
  $('#buehne').innerHTML = `<div class="mitte"><p class="gross">${punkte} Punkte</p><p>${neu ? 'Neuer Bestwert!' : 'Bestwert: ' + best()}</p><button class="haupt" id="los">Noch einmal</button></div>`;
  $('#los').addEventListener('click', start); rm('');
}
startbild();
""")

for name, s in SPIELE.items():
    html = KOPF.format(name=name, typ=s["typ"], titel=s["titel"], css=CSS, extra_css=s["extra_css"], body=s["body"],
                       anpassen=s["anpassen"], js=JS, spiel=s["spiel"])
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / f"{name}.html").write_text(html, encoding="utf8")
    print(name, len(html))
