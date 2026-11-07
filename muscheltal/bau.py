#!/usr/bin/env python3
"""Muschel-Tal: Einwohnerliste -> Webseite (site/index.html) + Daten fürs Video (daten/video.json).

  python3 muscheltal/bau.py                     # Seite aus daten/ neu bauen
  python3 muscheltal/bau.py --import user_data_tiktok.json   # neue Follower aus TikTok-Export anhängen, dann bauen
  python3 muscheltal/bau.py --demo 3000 --out /tmp/demo       # Vorschau mit Testnamen (nie veröffentlichen)

Reihenfolge in daten/einwohner.csv = Einwohner-Nummer. Neue Namen werden nur hinten angehängt,
damit niemand seine Hütte verliert. Wer raus will: Zeile löschen.
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
        w = csv.DictWriter(f, fieldnames=["name", "datum", "markierung"])
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
    sauber, gesehen = [], set()
    for r in rows:
        name = norm(r.get("name", ""))
        if not name or name.lower() in gesehen:
            if r.get("name", "").strip():
                print("übersprungen:", r.get("name"), file=sys.stderr)
            continue
        gesehen.add(name.lower())
        sauber.append([name, (r.get("datum") or "").strip(), (r.get("markierung") or "").strip()])
    import copy
    pop = len(sauber)
    web = copy.deepcopy(insel)  # öffentliche Fassung: gesperrte/geheime Inseln ohne echten Namen
    for v in web["inseln"]:
        if pop < v["ab"]:
            v["name"], v["emoji"] = "???", "❔"
    g = web.get("geheim") or {}
    web["geheim"] = g if g.get("offen") else {"name": "???", "emoji": "❔", "offen": False}
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
    alt = os.path.join(out, "einwohner.json")
    if os.path.exists(alt):
        os.remove(alt)  # nicht mehr öffentlich (enthielt echte Inselnamen)

    # Daten fürs Video (HyperFrames) – NICHT im öffentlichen Ordner, enthält echte Inselnamen
    grenzen, s = [], 0
    for v in insel["inseln"]:
        s = s + v["plaetze"] if v["plaetze"] else float("inf")
        grenzen.append((s, v))
    def wo(nr):
        v = next(v for g, v in grenzen if nr <= g)
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
    ap.add_argument("--demo", type=int, help="Testnamen statt echter Liste")
    ap.add_argument("--out", default=os.path.join(HIER, "site"))
    a = ap.parse_args()
    if a.demo:
        if os.path.abspath(a.out) == os.path.join(HIER, "site"):
            sys.exit("Demo nie nach site/ bauen – bitte --out angeben.")
        return baue(demo_rows(a.demo), a.out)
    rows = lade_csv()
    if a.imp:
        importiere(a.imp, rows)
        speichere_csv(rows)
    baue(rows, a.out)


if __name__ == "__main__":
    main()
