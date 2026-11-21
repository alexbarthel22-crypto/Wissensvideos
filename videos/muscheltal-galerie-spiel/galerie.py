# TikTok-Foto-Galerie „Was dich im Spiel ab 1.000 Bewohnern erwartet“ (21.11.) – Stil wie Video 1 / Cover Tag 1
import json, html
S = [
 dict(img="insel", eyebrow="MUSCHEL-TAL · 790 FOLLOWER", head="HIER PASSIERT GERADE ETWAS,", big="DAS ES AUF TIKTOK<br>NOCH NIE GAB", sub="790 Follower wohnen auf <b>einer Insel</b> – jede Hütte trägt einen echten Namen. Bei <b>1.000</b> wird daraus ein <b>Spiel</b>.", chips=[("pk","Und du kannst dabei sein 👀")], first=True),
 dict(img="huetten", eyebrow="ALLES, WAS DICH ERWARTET", head="DU SPIELST", big="DICH SELBST", sub="Deine eigene Figur, deine Hütte mit <b>deinem TikTok-Namen</b> – mitten zwischen allen anderen Followern.", chips=[("ye","🏠 Hütte mit deinem Namen"),("bl","🚶 eigene Spielfigur")]),
 dict(img="karte", eyebrow="ERKUNDEN", head="LAUF ÜBER", big="DIE INSELN", sub="Haupt-Insel, Kokos-Küste – und <b>geheime Inseln</b>, die erst später aufgehen. ???", chips=[("tq","🗺️ ganze Welt erkunden"),("vi","🔒 geheime Inseln")]),
 dict(img="huetten2", eyebrow="MUSCHELN", head="SAMMLE", big="MUSCHELN 🐚", sub="Jeden Tag reinschauen, <b>Aufgaben</b> erledigen, <b>Geheimcodes</b> aus meinen Videos einlösen – deine Muscheln wachsen.", chips=[("ye","📅 tägliche Login-Serie"),("gr","✅ 3 Aufgaben pro Tag")]),
 dict(img="huetten3", eyebrow="SHOP & STYLE", head="STYLE DICH", big="& DEINE HÜTTE", sub="Namensschilder, Titel, Profilrahmen, Hintergründe – und bald kannst du <b>deine Hütte einrichten</b>.", chips=[("pk","👑 seltene Items"),("bl","🛋️ Hütte einrichten (bald)")]),
 dict(img="pearl", eyebrow="GOLDEN PEARL", head="MINISPIELE", big="& DUELLE 💎", sub="Fordere deine <b>Freunde</b> heraus, kämpf um den <b>Wochensieg</b> – und nachts wird gefeiert.", chips=[("vi","⚔️ Freunde herausfordern"),("ye","🥇 Wochensieger")]),
 dict(img="wal", eyebrow="SELTENE EVENTS", head="SEI ZUR", big="RICHTIGEN ZEIT DA", sub="Ein <b>Wal</b> springt aus dem Meer, <b>Babyschildkröten</b> wandern ins Wasser, <b>Flaschenpost</b> treibt an den Strand …", chips=[("bl","🐋 Wal"),("gr","🐢 Schildkröten"),("tq","🍾 Flaschenpost")]),
 dict(img="schild", eyebrow="SAMMELN", head="FÜLL DEINE", big="ALBEN", sub="<b>Erfolge</b> freischalten, <b>Sticker</b> sammeln, am Steg <b>angeln</b> und jeden Fisch ins Album packen.", chips=[("ye","🏅 Erfolge"),("pk","🧩 Sticker-Album"),("tq","🎣 Fisch-Album")]),
 dict(img="club", eyebrow="JOBS & VERLOSUNGEN", head="BEKOMM", big="EINEN JOB", sub="Club-Besitzer, Leitung, Team … ich verlose regelmäßig. <b>Wer einen Job hat, startet mit Vorteil.</b>", chips=[("go","🎁 Live-Verlosungen"),("vi","⭐ Vorteil im Spiel")]),
 dict(img="kino", eyebrow="ZUSAMMEN", head="SPIEL MIT", big="DEINEN FREUNDEN", sub="Werdet <b>Nachbarn</b>, trefft euch im <b>Freiluftkino</b>, auf dem Markt oder am Lagerfeuer.", chips=[("pk","👯 Nachbarn werden"),("tq","🎬 Kino Fr & Sa")]),
 dict(img="insel", eyebrow="NUR FÜR DIE ERSTEN", head="DIE ERSTEN 1.000", big="BEKOMMEN VORTEILE", sub="Wer jetzt einzieht, ist von Anfang an dabei. Später kommt man nicht mehr so leicht rein.", chips=[], bar=True),
 dict(img="huetten", eyebrow="SO BIST DU DABEI", head="FOLG", big="@MUSCHELTAL", sub="Dann bekommst du <b>deine eigene Hütte</b> mit deinem Namen. <b>Markier deine Freunde</b>, damit sie unter den ersten 1.000 sind!", chips=[("pk","1️⃣ Folgen"),("ye","2️⃣ Freunde markieren"),("gr","3️⃣ Hütte finden")], last=True),
]
CSS = """@font-face{font-family:L;src:url(LilitaOne-Regular.woff2)}*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;overflow:hidden;position:relative;background:#04203a;font-family:Inter,system-ui,sans-serif;color:#fff}
#rays{position:absolute;left:-260px;top:260px;width:1600px;height:1600px;border-radius:50%;background:repeating-conic-gradient(from 4deg,rgba(255,229,0,.13) 0deg 7deg,rgba(255,229,0,0) 7deg 18deg);-webkit-mask:radial-gradient(circle,#000 0%,#000 25%,transparent 62%)}
#spot{position:absolute;inset:0;background:radial-gradient(ellipse 60% 32% at 50% 56%,rgba(20,170,200,.45),rgba(4,32,58,0) 70%)}
.pill{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;border-radius:40px;font-weight:900}
#ep{top:150px;padding:6px 22px 9px;font-size:28px;letter-spacing:.14em;background:#1a0f08;box-shadow:0 0 0 4px #ffe500}
#nr{position:absolute;right:70px;top:150px;font-weight:900;font-size:28px;color:#ffe500}
#hd{top:235px;padding:8px 30px 12px;font-size:46px;letter-spacing:.06em;background:#ffe500;color:#1a0f08;box-shadow:0 0 0 5px #1a0f08;transform:rotate(-2deg);text-align:center;line-height:1.1}
#big{position:absolute;left:40px;right:40px;top:330px;text-align:center;font-family:L;font-size:112px;line-height:1;color:#ffe500;-webkit-text-stroke:13px #1a0f08;paint-order:stroke fill;text-shadow:0 11px 0 #ff2e7e;transform:rotate(-3deg)}
#card{position:absolute;left:110px;width:860px;top:620px;height:660px;border-radius:44px;overflow:hidden;border:10px solid #fff;box-shadow:0 0 0 6px #1a0f08,0 20px 0 rgba(0,0,0,.4),0 0 120px rgba(40,200,230,.45);transform:rotate(1.5deg);background:#0b7fae center/cover}
#sub{position:absolute;left:90px;right:150px;top:1325px;padding:18px 28px 22px;border-radius:30px;background:#1a0f08;box-shadow:0 0 0 5px #ffe500;font-size:40px;line-height:1.25;font-weight:700;text-align:center}
#sub b{color:#ffe500}
#chips{position:absolute;left:80px;right:140px;top:1555px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center}
.c{padding:10px 26px 14px;border-radius:30px;font-weight:900;font-size:38px;box-shadow:0 0 0 5px #1a0f08,0 9px 0 rgba(0,0,0,.35)}
.pk{background:#ff2e7e}.ye{background:#ffe500;color:#1a0f08}.bl{background:#0098ff}.tq{background:#0a9fa6}.vi{background:#7b4fe0}.gr{background:#00b86b}.go{background:#ffb800;color:#1a0f08}
#swipe{position:absolute;right:70px;top:196px;font-family:L;font-size:38px;color:#fff;opacity:.9}
.sp{position:absolute}
#bar{position:absolute;left:150px;right:150px;top:900px;}
#bar .tr{height:90px;border-radius:45px;background:rgba(0,0,0,.55);box-shadow:0 0 0 7px #fff,0 0 0 13px #1a0f08;overflow:hidden}
#bar .fi{height:100%;width:79%;border-radius:45px;background:linear-gradient(90deg,#ffe500,#ff2e7e)}
#bar .lb{display:flex;justify-content:space-between;margin-top:18px;font-family:L;font-size:60px;-webkit-text-stroke:8px #1a0f08;paint-order:stroke fill}
#bar .lb span:last-child{color:#ffe500}
#free{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1130px;padding:12px 36px 16px;border-radius:40px;background:#00b86b;font-weight:900;font-size:54px;box-shadow:0 0 0 6px #1a0f08;transform:rotate(-2deg)}
"""
STAR = '<svg class="sp" style="left:{}px;top:{}px;width:{}px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="{}"/></svg>'
for i, s in enumerate(S, 1):
    body = f'<div id="spot"></div><div id="rays"></div><div id="ep" class="pill">{s["eyebrow"]}</div><div id="nr">{i}/{len(S)}</div>'
    body += f'<div id="hd" class="pill">{s["head"]}</div><div id="big">{s["big"]}</div>'
    if s.get("bar"):
        body += '<div id="bar"><div class="tr"><div class="fi"></div></div><div class="lb"><span>790</span><span>1.000 🎮</span></div></div><div id="free">NOCH 210 PLÄTZE FREI</div>'
    else:
        body += f'<div id="card" style="background-image:url(bilder/{s["img"]}.jpg)"></div>'
    body += f'<div id="sub">{s["sub"]}</div><div id="chips">' + "".join(f'<div class="c {c}">{html.escape(t)}</div>' for c, t in s["chips"]) + '</div>'
    if not s.get("last"): body += '<div id="swipe">wisch ➜</div>'
    body += STAR.format(120, 560, 64, "#ffe500") + STAR.format(880, 540, 50, "#fff") + STAR.format(70, 1250, 44, "#fff") + STAR.format(930, 1240, 56, "#ffe500")
    open(f"seite_{i:02d}.html", "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
print(len(S))
