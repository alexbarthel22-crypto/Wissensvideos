#!/usr/bin/env python3
"""Muschel-Tal: Einwohnerliste -> Webseite (site/index.html) + Daten fürs Video (daten/video.json).

  python3 muscheltal/bau.py                     # Seite aus daten/ neu bauen
  python3 muscheltal/bau.py --import user_data_tiktok.json   # neue Follower aus TikTok-Export anhängen, dann bauen
  python3 muscheltal/bau.py --liste Follower.txt              # komplette Followerliste (Datum/Anmeldename): neue anhängen, Entfolgte ziehen aus
  python3 muscheltal/bau.py --demo 3000 --out /tmp/demo       # Vorschau mit Testnamen (nie veröffentlichen)

Reihenfolge in daten/einwohner.csv = Folge-Reihenfolge = Einwohner-Nr. Wer entfolgt, zieht aus und wird komplett
aus der Liste gelöscht (Name taucht nirgends mehr auf); alle danach rücken eine Nummer auf – wer dadurch unter die Grenze einer Insel rutscht, zieht auf die vorige Insel um (in ein frei
gewordenes Haus). Spalte „platz“ (Insel:Platz) merkt sich das Haus, damit sonst niemand umziehen muss.
Spalte „gruender“ = 1: hat den Erfolg Gründer (die ersten 500 Follower + Ausnahmen).
"""
import argparse, csv, datetime as dt, json, os, random, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HIER, "daten", "einwohner.csv")
INSEL = os.path.join(HIER, "daten", "insel.json")
VORLAGE = os.path.join(HIER, "vorlage.html")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]


def norm(name):
    name = name.strip().lstrip("@").strip()
    return "@" + name if re.fullmatch(r"[A-Za-z0-9._]{1,40}", name) else None


def lade_csv():
    if not os.path.exists(CSV):
        return []
    with open(CSV, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def speichere_csv(rows):
    with open(CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["name", "datum", "markierung", "platz", "gruender"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def finde_follower(obj, drin=False):
    """Sucht im TikTok-Datenexport die Follower-Liste (Einträge mit UserName + Date).
    Nur unterhalb von Schlüsseln mit 'Follower'/'Fans' – nicht 'Following' (denen DU folgst) oder 'Block'."""
    if isinstance(obj, dict):
        keys = {k.lower(): k for k in obj}
        if drin and "username" in keys and "date" in keys:
            yield obj[keys["username"]], str(obj[keys["date"]])
            return
        for k, v in obj.items():
            kl = k.lower()
            if "following" in kl or "block" in kl:
                continue
            yield from finde_follower(v, drin or "follower" in kl or "fans" in kl)
    elif isinstance(obj, list):
        for v in obj:
            yield from finde_follower(v, drin)


def importiere(pfad, rows):
    with open(pfad, encoding="utf-8") as f:
        data = json.load(f)
    neu = sorted(finde_follower(data), key=lambda x: x[1])
    da = {r["name"].lower() for r in rows}
    n = 0
    for user, datum in neu:
        name = norm(user)
        if not name or name.lower() in da:
            continue
        d = re.match(r"(\d{4})-(\d{2})-(\d{2})", datum)
        rows.append({"name": name, "datum": f"{int(d[3])}.{int(d[2])}.{d[1]}" if d else "", "markierung": ""})
        da.add(name.lower())
        n += 1
    print(f"Import: {n} neue Einwohner")
    return n


def importiere_liste(pfad, rows):
    """Komplette Followerliste im Format 'Datum: 2026-11-07 22:54:52 UTC / Anmeldename: name'.
    Neue werden (älteste zuerst) hinten angehängt, wer fehlt, zieht aus, wer wieder folgt, zieht hinten neu ein."""
    txt = open(pfad, encoding="utf-8").read()
    paare = re.findall(r"Datum:\s*(\d{4})-(\d\d)-(\d\d)[ T]([\d:]+)[^\n]*\n\s*Anmeldename:\s*(\S+)", txt)
    if len(paare) < 10:
        sys.exit("Liste nicht erkannt (zu wenige Einträge) – nichts geändert.")
    paare.sort(key=lambda p: p[:4])
    drin = {p[4].lower().lstrip("@") for p in paare}
    heute = dt.date.today()
    weg = 0
    for r in list(rows):  # Entfolgte ziehen aus und verschwinden komplett aus der Liste
        if r["name"].lower().lstrip("@") not in drin:
            rows.remove(r)
            weg += 1
    aktiv = {r["name"].lower().lstrip("@") for r in rows}
    neu = 0
    for y, m, d, _, n in paare:
        if n.lower().lstrip("@") in aktiv:
            continue
        rows.append({"name": n, "datum": f"{int(d)}.{int(m)}.{y}", "markierung": "", "platz": "", "gruender": ""})
        aktiv.add(n.lower().lstrip("@"))
        neu += 1
    print(f"Liste: {neu} neu eingezogen, {weg} ausgezogen (komplett gelöscht)")


def _gebaeude_bewohner(insel):
    """Wer in einem Gebäude wohnt und deshalb keine Hütte braucht. Ausnahme Muschelpalast
    (Palast-Leitung, befristet): behält seine Hütte mit Namen."""
    return {k.lower().lstrip("@") for k, o in (insel.get("wohnorte") or {}).items()
            if (o[0] if isinstance(o, list) else o) != "Muschelpalast"}


def inselgrenzen(sauber, insel):
    """Letzte Einwohner-Nr. je Insel. Wer in einem Gebäude wohnt (wohnorte), braucht keine Hütte –
    seine Hütte wird frei und der Nächste rückt nach (Insel fasst dann entsprechend mehr Einwohner)."""
    wo = _gebaeude_bewohner(insel)
    sonder = [r[0].lower().lstrip("@") in wo for r in sauber]
    grenzen, s = [], 0
    for v in insel["inseln"]:
        if not v["plaetze"]:
            grenzen.append(float("inf")); continue
        start, g = s, s + v["plaetze"]
        while True:
            extra = sum(1 for j in range(start, min(g, len(sauber))) if sonder[j])
            if start + v["plaetze"] + extra == g:
                break
            g = start + v["plaetze"] + extra
        s = g
        grenzen.append(g)
    return grenzen


def insel_je(sauber, insel):
    """Insel-Index je Einwohner (nach Einwohner-Nr. und Inselgrenzen) – plus Nachbarn-Wünsche (insel.json → nachbarn):
    Ist von einem Paar nur einer auf der Haupt-Insel, zieht der andere dazu; dafür zieht der zuletzt auf die
    Haupt-Insel Gekommene (höchste Nr. dort, ohne Gebäude-Bewohner) auf die Insel des Nachziehenden."""
    grenzen = inselgrenzen(sauber, insel)
    isl = [next(i for i, g in enumerate(grenzen) if nr <= g) for nr in range(1, len(sauber) + 1)]
    wo = _gebaeude_bewohner(insel)
    idx = {r[0].lower().lstrip("@"): j for j, r in enumerate(sauber)}
    paare = [[idx.get(n.lower().lstrip("@")) for n in paar] for paar in (insel.get("nachbarn") or [])]
    geschuetzt = {j for pa in paare for j in pa if j is not None}
    for a, b in paare:
        if a is None or b is None or isl[a] == isl[b] or 0 not in (isl[a], isl[b]):
            continue
        k = b if isl[a] == 0 else a
        kand = [j for j in range(len(sauber)) if isl[j] == 0 and j not in geschuetzt and sauber[j][0].lower().lstrip("@") not in wo]
        if not kand:
            continue
        letzter = max(kand)
        isl[letzter], isl[k] = isl[k], 0
        print(f"Nachbarn: @{sauber[k][0].lstrip('@')} zieht auf die Haupt-Insel, @{sauber[letzter][0].lstrip('@')} zieht dafür um")
    return isl


def verteile(sauber, insel):
    """Insel je Einwohner-Nr.; jeder behält sein Haus (platz), Frei gewordene werden mit den Nachrückern
    (nach Einwohner-Nr.) besetzt. Gibt Liste 'i:k' zurück."""
    isl = insel_je(sauber, insel)
    wo = _gebaeude_bewohner(insel)
    sonder = [r[0].lower().lstrip("@") in wo for r in sauber]  # wohnen in einem Gebäude, kein Hütten-Platz
    plaetze, belegt = [None] * len(sauber), {}
    for j, r in enumerate(sauber):
        if sonder[j]:
            plaetze[j] = "H"
    for j, r in enumerate(sauber):  # 1. Durchgang: wer auf seiner Insel bleibt, behält sein Haus
        if sonder[j]:
            continue
        m = re.fullmatch(r"(\d+):(\d+)", r[3] or "")
        if m and int(m[1]) == isl[j]:
            k, cap = int(m[2]), insel["inseln"][isl[j]]["plaetze"] or 10 ** 9
            if k < cap and k not in belegt.setdefault(isl[j], set()):
                belegt[isl[j]].add(k)
                plaetze[j] = k
    for j in range(len(sauber)):  # 2. Durchgang: Neue und Umzügler bekommen das nächste freie Haus (nah an der Mitte)
        if plaetze[j] is None and not sonder[j]:
            b, k = belegt.setdefault(isl[j], set()), 0
            while k in b:
                k += 1
            b.add(k)
            plaetze[j] = k
    return [f"{isl[j]}:{plaetze[j]}" for j in range(len(sauber))]


def uebersicht(sauber, insel, out):
    """einwohner.html: alle Einwohner von Muschel-Tal nach Insel, Gründer mit kleiner Münze."""
    import html as H
    erf = open(os.path.join(HIER, "erfolge.html"), encoding="utf-8").read()
    head = erf[:erf.index("<style>") + len("<style>")]
    head = head.replace("<title>Erfolge – Muschel-Tal</title>", "<title>Einwohner – Muschel-Tal</title>").replace(
        "Alle Erfolge und Abzeichen der Bewohner von Muschel-Tal.", "Alle Einwohner von Muschel-Tal auf einen Blick.")
    css = erf[erf.index("<style>") + len("<style>"):erf.index("</style>")]
    keep = "\n".join(l for l in css.split("\n") if l.startswith((":root", " --f", "*{", "body{", ".top", "main{", ".cta{", ".count")))
    m = re.search(r'<svg class="coin".*?</svg>', erf, re.S)
    coin = re.sub(r'class="coin" ', "", m[0]) if m else ""
    coin_uri = "data:image/svg+xml;charset=utf-8," + coin.replace("#", "%23").replace('"', "'").replace("\n", "")
    isl = insel_je(sauber, insel)
    teile = []
    for i, v in enumerate(insel["inseln"]):
        leute = [(j + 1, r) for j, r in enumerate(sauber) if isl[j] == i]
        if not leute or len(sauber) < v["ab"]:
            continue
        li = "".join(f'<li><a href="./?n={H.escape(r[0])}"><span class="nr">{nr}</span><b>{H.escape(r[0])}</b>{"<i class=g title=Gründer></i>" if r[4] else ""}</a></li>' for nr, r in leute)
        teile.append(f'<section><h2>{H.escape(v["emoji"])} {H.escape(v["name"])} <small>{len(leute):,} Einwohner</small></h2><ul>{li}</ul></section>'.replace(",", "."))
    gr = sum(1 for r in sauber if r[4])
    seite = head + "\n" + keep + f"""
.count{{margin-bottom:14px}}
.such{{display:block;width:100%;border:3px solid var(--ink);border-radius:14px;padding:12px 14px;font:800 17px var(--f);margin:0 0 16px;box-shadow:3px 3px 0 var(--ink)}}
section h2{{font-size:22px;margin:22px 0 10px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}}
section h2 small{{font-size:14px;color:var(--soft)}}
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px}}
li a{{display:flex;align-items:center;gap:6px;background:#fff;border:2px solid #f0e2c8;border-radius:10px;padding:5px 8px;color:var(--ink);text-decoration:none;min-width:0}}
li a:active{{background:#fff3cf}}
li .nr{{font-size:11px;font-weight:900;color:var(--soft);min-width:26px}}
li b{{font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}}
li .g{{flex:none;width:16px;height:16px;background:url("{coin_uri}") center/contain no-repeat}}
.leg{{display:flex;align-items:center;justify-content:center;gap:6px;color:var(--soft);font-weight:800;font-size:14px;margin:-6px 0 14px}}
.leg i{{width:18px;height:18px;background:url("{coin_uri}") center/contain no-repeat}}
.nix{{text-align:center;color:var(--soft);font-weight:800}}
</style>
</head>
<body>
<header class="top"><a href="./">← Zur Karte</a><small>MUSCHEL-TAL</small><h1>👥 Einwohner</h1><p>Alle Bewohner von Muschel-Tal – tipp einen Namen an, um zu seiner Hütte zu fliegen.</p>
<svg viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M0 14 Q25 2 50 14 T100 14 T150 14 T200 14 T250 14 T300 14 T350 14 T400 14 V24 H0Z" fill="#fff4e0"/></svg></header>
<main>
 <div class="count"><span>{len(sauber):,} Einwohner</span><span>{len(teile)} Inseln</span></div>
 <p class="leg"><i></i> = Gründer ({gr:,})</p>
 <input class="such" id="such" type="search" placeholder="Namen suchen …" autocomplete="off" autocapitalize="off" spellcheck="false">
 {"".join(teile)}
 <p class="nix" id="nix" hidden>Niemand gefunden – folgst du schon @muscheltal?</p>
 <a class="cta" href="https://www.tiktok.com/@muscheltal" target="_blank" rel="noopener">➕ @muscheltal folgen und einziehen</a>
</main>
<script>
const f=document.getElementById('such');f.addEventListener('input',()=>{{const t=f.value.trim().toLowerCase().replace(/^@/,'');let n=0;
document.querySelectorAll('li').forEach(li=>{{const ok=!t||li.textContent.toLowerCase().includes(t);li.hidden=!ok;if(ok)n++;}});
document.querySelectorAll('section').forEach(s=>s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden));document.getElementById('nix').hidden=n>0;}});
</script>
</body>
</html>
""".replace("{len(sauber):,}", "")
    seite = seite.replace(f"{len(sauber):,} Einwohner</span>", f"{len(sauber):,}".replace(",", ".") + " Einwohner</span>").replace(f"Gründer ({gr:,})", "Gründer (" + f"{gr:,}".replace(",", ".") + ")")
    open(os.path.join(out, "einwohner.html"), "w", encoding="utf-8").write(seite)


def nachrichten(insel, out):
    """news.html: alles, was in Muschel-Tal passiert ist – neueste zuerst, nach Datum."""
    import html as H
    erf = open(os.path.join(HIER, "erfolge.html"), encoding="utf-8").read()
    head = erf[:erf.index("<style>") + len("<style>")].replace("<title>Erfolge – Muschel-Tal</title>", "<title>News – Muschel-Tal</title>").replace(
        "Alle Erfolge und Abzeichen der Bewohner von Muschel-Tal.", "Alles, was in Muschel-Tal passiert ist: neue Inseln, Gebäude, Events, Jobs, Bürgermeister.")
    css = erf[erf.index("<style>") + len("<style>"):erf.index("</style>")]
    keep = "\n".join(l for l in css.split("\n") if l.startswith((":root", " --f", "*{", "body{", ".top", "main{", ".cta{")))
    start = dt.date.fromisoformat(insel["start"]) if insel.get("start") else None
    gruppen = {}
    for e in insel.get("ereignisse", []):
        gruppen.setdefault(e[0], []).append(e)
    teile = []
    for datum, liste in gruppen.items():
        t, m, j = (int(x) for x in datum.split("."))
        tag = (dt.date(j, m, t) - start).days + 1 if start else 0
        kopf = f"{t}. {MONATE[m - 1]} {j}" + (f" <span>Tag {tag}</span>" if tag >= 1 else "")
        karten = "".join(f'<div class="n"><div class="em">{H.escape(e[1])}</div><div><h3>{H.escape(e[2])}</h3><p>{H.escape(e[3])}</p></div></div>' for e in liste)
        teile.append(f"<section><h2>{kopf}</h2>{karten}</section>")
    seite = head + "\n" + keep + """
section h2{font-size:18px;margin:22px 0 10px;display:flex;align-items:center;gap:8px}
section h2 span{background:var(--sun);border:2px solid var(--ink);border-radius:999px;padding:0 10px;font-size:14px}
.n{display:grid;grid-template-columns:46px 1fr;gap:12px;align-items:start;background:#fff;border:3px solid var(--ink);border-radius:18px;padding:12px;margin-bottom:10px;box-shadow:3px 3px 0 var(--ink)}
.n .em{width:46px;height:46px;border-radius:50%;background:var(--sand);border:2px solid var(--ink);display:grid;place-items:center;font-size:24px}
.n h3{margin:2px 0 2px;font-size:18px;line-height:1.25}
.n p{margin:0;color:var(--soft);font-weight:700;font-size:15px}
</style>
</head>
<body>
<header class="top"><a href="./">← Zur Karte</a><small>MUSCHEL-TAL</small><h1>📰 News</h1><p>Alles, was auf den Inseln passiert ist – neue Inseln, Gebäude, Events, Jobs und Bürgermeister.</p>
<svg viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M0 14 Q25 2 50 14 T100 14 T150 14 T200 14 T250 14 T300 14 T350 14 T400 14 V24 H0Z" fill="#fff4e0"/></svg></header>
<main>
""" + "\n".join(teile) + """
 <a class="cta" href="https://www.tiktok.com/@muscheltal" target="_blank" rel="noopener">➕ @muscheltal folgen und einziehen</a>
</main>
</body>
</html>
"""
    open(os.path.join(out, "news.html"), "w", encoding="utf-8").write(seite)



def bauprojekte(sauber, insel, out):
    """bau.html: alle aktuellen Baustellen mit Ziel zur Fertigstellung; Ort verlinkt auf die Karte."""
    import html as H
    from urllib.parse import quote
    erf = open(os.path.join(HIER, "erfolge.html"), encoding="utf-8").read()
    head = erf[:erf.index("<style>") + len("<style>")].replace("<title>Erfolge – Muschel-Tal</title>", "<title>Bauprojekte – Muschel-Tal</title>").replace(
        "Alle Erfolge und Abzeichen der Bewohner von Muschel-Tal.", "Aktuelle Bauprojekte in Muschel-Tal und wann sie fertig werden.")
    css = erf[erf.index("<style>") + len("<style>"):erf.index("</style>")]
    keep = "\n".join(l for l in css.split("\n") if l.startswith((":root", " --f", "*{", "body{", ".top", "main{", ".cta{")))
    n = len(sauber)
    tz = lambda x: f"{x:,}".replace(",", ".")
    teile = []
    for b in sorted([b for b in insel.get("baustellen", []) if n < b["ziel"]], key=lambda b: b["ziel"]):
        pr = min(100, round(n * 100 / b["ziel"]))
        ort = "am Steg der Haupt-Insel" if b.get("ort") == "steg" else "auf der " + (insel["inseln"][int(b["key"].split(":")[0])]["name"] if b.get("key") else "Haupt-Insel")
        teile.append(f'''<a class="bp" href="./?ort={quote(b["name"])}"><div class="kopf"><span class="em">{H.escape(b.get("emoji", "🏗️"))}</span><div><b>{H.escape(b["name"])}</b><small>{H.escape(ort)}</small></div></div>
<div class="bar"><i style="width:{pr}%"></i></div><div class="zl"><span>{tz(n)} von {tz(b["ziel"])} Bewohnern</span><span>noch {tz(b["ziel"] - n)}</span></div><u>📍 Auf der Karte ansehen →</u></a>''')
    leer = '<p class="hint">Gerade wird nichts gebaut. Neue Projekte kommen bald!</p>' if not teile else ""
    seite = head + "\n" + keep + """
.hint{background:#fff;border:3px dashed var(--ink);border-radius:18px;padding:14px;margin:4px 0 18px;font-weight:800;text-align:center}
.bp{display:block;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:14px;margin-bottom:14px;box-shadow:4px 4px 0 var(--ink);color:var(--ink);text-decoration:none}
.kopf{display:flex;align-items:center;gap:12px}
.em{font-size:34px;line-height:1}
.kopf{min-width:0}.kopf>div{min-width:0}
.kopf b{display:block;font-size:min(22px,5.6vw);font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kopf small{display:block;font-size:14px;font-weight:800;color:#7a5a2b}
.bar{height:14px;background:#f0e2c8;border:2px solid var(--ink);border-radius:999px;overflow:hidden;margin:12px 0 6px}
.bar i{display:block;height:100%;background:#2e9e5b}
.zl{display:flex;justify-content:space-between;gap:10px;font-size:14px;font-weight:900}
.bp u{display:block;margin-top:8px;font-size:14px;font-weight:900;color:#0a8fd0;text-decoration:none}
</style>
</head>
<body>
<header class="top"><a href="./">← Zur Karte</a><small>MUSCHEL-TAL</small><h1>🏗️ Aktuelle Bauprojekte</h1><p>Was gerade gebaut wird – fertig, sobald genug Bewohner da sind. Tipp auf ein Projekt, um auf der Karte hinzukommen.</p>
<svg viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M0 14 Q25 2 50 14 T100 14 T150 14 T200 14 T250 14 T300 14 T350 14 T400 14 V24 H0Z" fill="#fff4e0"/></svg></header>
<main>
""" + leer + "\n".join(teile) + """
 <a class="cta" href="https://www.tiktok.com/@muscheltal" target="_blank" rel="noopener">🐚 Folgen &amp; mitbauen</a>
</main>
</body>
</html>
"""
    open(os.path.join(out, "bau.html"), "w", encoding="utf-8").write(seite)


def schnell(out):
    """Seitenwechsel ohne spürbare Ladezeit: weiche Übergänge (View Transitions), Unterseiten werden beim
    Antippen/Überfahren vorgeladen (bzw. in Chrome vorgerendert), „← Zur Karte“ springt per Zurück sofort
    auf die noch geladene Karte (Back-Forward-Cache) statt sie neu zu laden."""
    css = "<style>@view-transition{navigation:auto}</style>"
    unter = ["bau.html", "berufe.html", "einwohner.html", "news.html", "regeln.html", "erfolge.html"]
    spec = '<script type="speculationrules">{"prerender":[{"where":{"href_matches":"/*.html"},"eagerness":"moderate"}],"prefetch":[{"where":{"href_matches":"/*"},"eagerness":"moderate"}]}</script>'
    vor = """<script>(()=>{const done=new Set(),pre=u=>{if(done.has(u))return;done.add(u);try{const l=document.createElement('link');l.rel='prefetch';l.href=u;document.head.appendChild(l);fetch(u,{credentials:'same-origin'}).catch(()=>{});}catch(e){}};
const h=e=>{const a=e.target.closest&&e.target.closest('a[href]');if(!a)return;const u=new URL(a.href,location.href);if(u.origin===location.origin&&u.pathname!==location.pathname)pre(u.pathname);};
addEventListener('pointerdown',h,{passive:true});addEventListener('mouseover',h,{passive:true});addEventListener('touchstart',h,{passive:true});
const z=document.querySelector('header.top a[href="./"]');if(z)z.addEventListener('click',e=>{try{const r=document.referrer&&new URL(document.referrer);if(r&&r.origin===location.origin&&(r.pathname==='/'||r.pathname.endsWith('/index.html'))&&history.length>1){e.preventDefault();history.back();}}catch(x){}});})();</script>"""
    for name in ["index.html"] + unter:
        f = os.path.join(out, name)
        if not os.path.exists(f):
            continue
        t = open(f, encoding="utf-8").read()
        if "@view-transition" in t:
            continue
        t = t.replace("</head>", css + (spec if name == "index.html" else "") + "</head>", 1)
        t = t.replace("</body>", vor + "</body>", 1) if "</body>" in t else t + vor
        open(f, "w", encoding="utf-8").write(t)

def berufe(sauber, insel, out):
    """berufe.html: alle Einwohner mit Job, nach Arbeitsort; Ort und Name verlinkt auf die Karte."""
    import html as H
    from urllib.parse import quote
    erf = open(os.path.join(HIER, "erfolge.html"), encoding="utf-8").read()
    head = erf[:erf.index("<style>") + len("<style>")].replace("<title>Erfolge – Muschel-Tal</title>", "<title>Berufe – Muschel-Tal</title>").replace(
        "Alle Erfolge und Abzeichen der Bewohner von Muschel-Tal.", "Alle Berufe in Muschel-Tal: wer wo arbeitet.")
    css = erf[erf.index("<style>") + len("<style>"):erf.index("</style>")]
    keep = "\n".join(l for l in css.split("\n") if l.startswith((":root", " --f", "*{", "body{", ".top", "main{", ".cta{")))
    nr = {r[0].lower().lstrip("@"): i + 1 for i, r in enumerate(sauber)}
    orte, emo = {}, {g["name"]: g.get("emoji", "📍") for g in insel.get("gebaeude", [])}
    emo.setdefault("Muschelpalast", "🏰")
    import datetime as _dt
    try:
        from zoneinfo import ZoneInfo
        jetzt = _dt.datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%dT%H:%M")
    except Exception:
        jetzt = _dt.datetime.now().strftime("%Y-%m-%dT%H:%M")
    bis_ok = lambda b: not b or jetzt < (b if len(b) > 10 else b + "T24:00")
    for n, job in (insel.get("jobs") or {}).items():
        beruf, ort, bis = (list(job) + [None])[:3]
        if n.lower() in nr and bis_ok(bis):
            orte.setdefault(ort, []).append((beruf, n, bis))
    rang = {"Bürgermeisterin": 0, "Bürgermeister": 0, "Leitung": 1, "Palast-Leitung": 1}
    teile = []
    for ort in sorted(orte, key=lambda o: (o != "Muschelpalast", o)):
        leute = sorted(orte[ort], key=lambda x: (rang.get(x[0], 5), nr[x[1].lower()]))
        li = "".join(f'<a class="p{" chef" if x[0] in rang else ""}" href="./?n={quote("@" + x[1])}"{f' data-bis="{x[2]}"' if x[2] else ""}><b>{H.escape("👑 " if x[0] == "Palast-Leitung" else "⭐ " if rang.get(x[0]) == 1 else "🎖️ " if rang.get(x[0]) == 0 else "")}@{H.escape(x[1])}</b><span>{H.escape(x[0])}{H.escape(" · bis Mo " + ".".join(str(int(t)) for t in reversed(x[2][:10].split("-")[1:])) + "." + (", " + str(int(x[2][11:13])) + " Uhr" if len(x[2]) > 10 else "")) if x[2] else ""}</span></a>' for x in leute)
        teile.append(f'<section><a class="ort" href="./?ort={quote(ort)}">{emo.get(ort, "📍")} {H.escape(ort)} <small>auf der Karte ansehen →</small></a><div class="pl">{li}</div></section>')
    seite = head + "\n" + keep + """
.hint{background:#fff;border:3px dashed var(--ink);border-radius:18px;padding:14px;margin:4px 0 18px;font-weight:800;text-align:center}
.hint a{color:var(--hib)}
section{background:#fff;border:3px solid var(--ink);border-radius:20px;padding:14px;margin-bottom:14px;box-shadow:4px 4px 0 var(--ink)}
.ort{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;font-size:22px;font-weight:900;color:var(--ink);text-decoration:none;margin-bottom:10px}
.ort small{font-size:14px;color:#0a8fd0}
.pl{display:grid;gap:8px}
.p{display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--sand);border:2px solid #f0e2c8;border-radius:12px;padding:8px 12px;color:var(--ink);text-decoration:none}
.p b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.p span{flex:none;font-size:14px;font-weight:900;color:#fff;background:var(--ink);border-radius:999px;padding:2px 10px}
.p.chef span{background:var(--hib)}
</style>
</head>
<body>
<header class="top"><a href="./">← Zur Karte</a><small>MUSCHEL-TAL</small><h1>💼 Berufe</h1><p>Wer in Muschel-Tal wo arbeitet – tipp auf einen Ort oder Namen, um auf der Karte hinzukommen.</p>
<svg viewBox="0 0 400 24" preserveAspectRatio="none"><path d="M0 14 Q25 2 50 14 T100 14 T150 14 T200 14 T250 14 T300 14 T350 14 T400 14 V24 H0Z" fill="#fff4e0"/></svg></header>
<main>
 <p class="hint">💬 Du willst auch einen Job auf Muschel-Tal? Schreib es in die Kommentare unter dem neuesten Video von <a href="https://www.tiktok.com/@muscheltal" target="_blank" rel="noopener">@muscheltal</a> auf TikTok!</p>
""" + "\n".join(teile) + """
 <a class="cta" href="https://www.tiktok.com/@muscheltal" target="_blank" rel="noopener">💬 Auf TikTok kommentieren</a>
</main>
<script>/* Jobs mit Ablaufdatum: nach dem letzten Tag automatisch ausblenden */
(()=>{let h;try{const p=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Berlin',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date()).map(x=>[x.type,x.value]));h=p.year+'-'+p.month+'-'+p.day+'T'+p.hour+':'+p.minute;}catch(e){h=new Date().toISOString().slice(0,16);}
document.querySelectorAll('[data-bis]').forEach(a=>{const b=a.dataset.bis;if(h>=(b.length>10?b:b+'T24:00'))a.remove();});document.querySelectorAll('section').forEach(s=>{if(!s.querySelector('.p'))s.remove();});})();</script>
</body>
</html>
"""
    open(os.path.join(out, "berufe.html"), "w", encoding="utf-8").write(seite)


def demo_rows(n):
    rnd = random.Random(7)
    heute = dt.date.today()
    rows = []
    for i in range(n):
        tag = heute - dt.timedelta(days=3 - min(3, int(4 * (i / n) ** 1.6)))
        rows.append({"name": f"@demo_{i + 1:04d}", "datum": f"{tag.day}.{tag.month}.",
                     "markierung": "Video" if rnd.random() < 0.02 else ""})
    return rows


def baue(rows, out):
    insel = json.load(open(INSEL, encoding="utf-8"))
    try:
        from zoneinfo import ZoneInfo
        jetzt = dt.datetime.now(ZoneInfo("Europe/Berlin"))
    except Exception:
        jetzt = dt.datetime.now()
    insel["stand"] = f"{jetzt.day}. {MONATE[jetzt.month - 1]} {jetzt.year}, {jetzt:%H:%M} Uhr"
    if insel.get("start"):  # Tag 1 = Startdatum, danach zählt der Tag automatisch hoch
        insel["tag"] = max(0, (jetzt.date() - dt.date.fromisoformat(insel["start"])).days + 1)
    if insel.get("ereignisse"):  # „Neu:“-Kasten auf der Startseite = neuestes Ereignis
        e = insel["ereignisse"][0]
        insel["news"] = [f"{e[1]} {e[2]} – {e[3]}"]
    sauber, gesehen, quelle = [], set(), []
    for pos, r in enumerate(rows):
        name = norm(r.get("name", ""))
        if not name or name.lower() in gesehen:
            if r.get("name", "").strip():
                print("übersprungen:", r.get("name"), file=sys.stderr)
            continue
        gesehen.add(name.lower())
        gr = r.get("gruender")
        sauber.append([name, (r.get("datum") or "").strip(), (r.get("markierung") or "").strip(),
                       (r.get("platz") or "").strip(), (1 if gr.strip() == "1" else 0) if gr is not None else (1 if pos < 500 else 0)])
        quelle.append(r)
    plaetze = verteile(sauber, insel)
    isl_l = insel_je(sauber, insel)
    for j, r in enumerate(sauber):
        r[3] = int(plaetze[j].split(":")[1]) if plaetze[j][-1] != "H" else None
        quelle[j]["platz"] = plaetze[j]
    for j, r in enumerate(sauber):
        r.append(isl_l[j])
    import copy
    pop = len(sauber)
    web = copy.deepcopy(insel)  # öffentliche Fassung: gesperrte/geheime Inseln ohne echten Namen
    for v in web["inseln"]:
        if pop < v["ab"]:
            v["name"], v["emoji"] = "???", "❔"
    g = web.get("geheim") or {}
    web["geheim"] = g if g.get("offen") else {"name": "???", "emoji": "❔", "offen": False}
    web["grenzen"] = [g if g != float("inf") else None for g in inselgrenzen(sauber, insel)]
    data = {"r": sauber, "insel": web}
    html = open(VORLAGE, encoding="utf-8").read()
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = html.replace("/*__DATEN__*/null", js)
    os.makedirs(out, exist_ok=True)
    for datei in ("CNAME",):
        quelle = os.path.join(HIER, "site", datei)
        if os.path.exists(quelle) and os.path.abspath(out) != os.path.join(HIER, "site"):
            open(os.path.join(out, datei), "w", encoding="utf-8").write(open(quelle, encoding="utf-8").read())
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    # Zusatzseiten (statisch) mitkopieren
    for datei in ("erfolge.html", "regeln.html"):
        quelle = os.path.join(HIER, datei)
        if os.path.exists(quelle):
            open(os.path.join(out, datei), "w", encoding="utf-8").write(open(quelle, encoding="utf-8").read())
    uebersicht(sauber, insel, out)
    nachrichten(insel, out)
    berufe(sauber, insel, out)
    bauprojekte(sauber, insel, out)
    schnell(out)
    # Hinweis: Nachbarn-Wünsche, sobald beide eingezogen sind (Karte setzt sie automatisch nebeneinander)
    namen = {r[0].lower().lstrip("@") for r in sauber}
    for paar in insel.get("nachbarn") or []:
        da = [n for n in paar if n.lower().lstrip("@") in namen]
        print(f"Nachbarn-Wunsch {' + '.join('@' + n for n in paar)}: " + ("beide da → wohnen nebeneinander" if len(da) == 2 else f"noch nicht beide Follower ({len(da)}/2)"))
    alt = os.path.join(out, "einwohner.json")
    if os.path.exists(alt):
        os.remove(alt)  # nicht mehr öffentlich (enthielt echte Inselnamen)

    # Daten fürs Video (HyperFrames) – NICHT im öffentlichen Ordner, enthält echte Inselnamen
    isl_v = insel_je(sauber, insel)
    def wo(nr):
        v = insel["inseln"][isl_v[nr - 1]]
        return v["name"] if pop >= v["ab"] else "wartet am Steg"
    video = {"stand": insel["stand"], "tag": insel["tag"], "einwohner": pop,
             "muscheln": pop * insel["muscheln_pro_einwohner"], "aemter": insel["aemter"], "projekt": insel.get("projekt"),
             "inseln": [{"name": v["name"], "ab": v["ab"], "offen": pop >= v["ab"]} for v in insel["inseln"]],
             "liste": [{"nr": i + 1, "name": r[0], "insel": wo(i + 1), "seit": r[1], "markierung": r[2]}
                       for i, r in enumerate(sauber)]}
    ziel = os.path.join(HIER, "daten", "video.json") if os.path.abspath(out) == os.path.join(HIER, "site") else os.path.join(out, "video.json")
    json.dump(video, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Fertig: {len(sauber)} Einwohner -> {os.path.join(out, 'index.html')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--import", dest="imp", help="TikTok-Datenexport (JSON)")
    ap.add_argument("--liste", help="komplette Followerliste als Text (Datum + Anmeldename)")
    ap.add_argument("--demo", type=int, help="Testnamen statt echter Liste")
    ap.add_argument("--out", default=os.path.join(HIER, "site"))
    a = ap.parse_args()
    if a.demo:
        if os.path.abspath(a.out) == os.path.join(HIER, "site"):
            sys.exit("Demo nie nach site/ bauen – bitte --out angeben.")
        return baue(demo_rows(a.demo), a.out)
    rows = lade_csv()
    if a.liste:
        importiere_liste(a.liste, rows)
    if a.imp:
        importiere(a.imp, rows)
        speichere_csv(rows)
    baue(rows, a.out)
    if os.path.abspath(a.out) == os.path.join(HIER, "site"):
        speichere_csv(rows)  # Häuser (platz) und Auszüge merken


if __name__ == "__main__":
    main()
