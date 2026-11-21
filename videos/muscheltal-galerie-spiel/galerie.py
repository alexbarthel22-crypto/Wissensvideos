# TikTok-Foto-Galerie „Spiel ab 1.000“ – Look wie Cover Tag 1 (dunkelblau, Strahlen, gelbe Schrift, Karten)
S = [
 dict(first=True),
 dict(img="huetten", eyebrow="DAS IST MEIN SPIEL", head="DU SPIELST", big="DICH SELBST", sub="Deine eigene Figur, deine Hütte mit <b>deinem TikTok-Namen</b> – mitten zwischen allen anderen Followern.", chips=[("ye","🏠 deine Hütte"),("bl","🛴 E-Scooter & Skateboard")]),
 dict(grid=[("w_doener","🥙 Dönerbude"),("w_baeckerei","🥐 Bäckerei"),("w_strandbar","🍹 Strandbar"),("w_tierheim","🐾 Tierheim")], eyebrow="IHR HABT ABGESTIMMT", head="IHR HABT SIE GEWÜNSCHT –", big="SIE SPIELEN EINE<br>GROSSE ROLLE", sub="Diese Gebäude gibt es, <b>weil ihr abgestimmt habt</b>. Im Spiel lauft ihr hin: <b>Aufgaben</b>, <b>Jobs</b>, <b>Döner für 2 €</b> …", chips=[("pk","🗳️ eure Abstimmungen")]),
 dict(grid3=["hund","katze","hase","schildi","schwein","robbe"], eyebrow="🐾 TIERHEIM PFOTENKUSS", head="ADOPTIER DEIN", big="EIGENES<br>HAUSTIER", sub="Hund, Katze, Hase, Schildkröte … dein Tier <b>läuft dir beim Erkunden überall hinterher</b> 💗", chips=[("pk","🐶 süß"),("ye","🐱 süßer"),("tq","🐰 am süßesten")]),
 dict(img="karte", eyebrow="ENTDECKEN", head="DAS KANNST DU", big="ERKUNDEN", sub="Haupt-Insel, Kokos-Küste, Strand, Angelsteg, Lagerfeuer, Freiluftkino, Golden Pearl – und <b>geheime Inseln</b> ???", chips=[("tq","🏝️ 2 Inseln"),("vi","🔒 geheime Inseln")]),
 dict(img="sand", eyebrow="ACTION", head="DAS KANNST DU", big="ERLEBEN", sub="<b>Sandburg</b> mitbauen, <b>angeln</b>, Film im <b>Freiluftkino</b>, <b>Wal</b> & <b>Babyschildkröten</b> sehen, <b>Flaschenpost</b>-Quiz lösen …", chips=[("ye","🏰 Sandburg"),("bl","🎣 Angeln"),("gr","🐢 Events")]),
 dict(img="angel", eyebrow="SAMMELN", head="DAS KANNST DU", big="SAMMELN", sub="<b>Muscheln</b>, <b>Sticker</b>, <b>Fische</b>, <b>Erfolge</b>, Titel, Profilrahmen, Namensschilder, Haustiere, Fahrzeuge …", chips=[("ye","🐚 Muscheln"),("pk","🧩 Sticker"),("tq","🐟 Fische")]),
 dict(img="insel", eyebrow="NUR VON EUCH GESTALTET", head="IHR ENTSCHEIDET,", big="WAS HIER<br>PASSIERT", sub="Muschel-Tal wird <b>weiter nur von euch</b> gestaltet: Wünsche in die Kommentare, ihr <b>stimmt ab</b>, was gebaut wird.", chips=[("vi","💬 eure Wünsche"),("gr","🗳️ eure Abstimmung")]),
 dict(pod=True, eyebrow="DAS ZIEL", head="WER HAT DIE", big="MEISTEN<br>MUSCHELN? 🐚", sub="… und die <b>meisten Erfolge</b>? Login-Serie, Aufgaben, Geheimcodes – kletter in der <b>Rangliste</b> nach oben.", chips=[("ye","🏆 Rangliste"),("bl","🏅 Erfolge")]),
 dict(grid=[("spiele/taucher","🫧 Perlentaucher"),("spiele/turm","🥥 Kokos-Turm"),("spiele/memory","🐚 Memory"),("spiele/krebs","🦀 Krebs-Sprint")], eyebrow="GOLDEN PEARL 💎", head="SCHAU REIN:", big="MINISPIELE", sub="Vier Spiele, <b>kostenlos</b>, nur Geschick zählt. <b>Fordere Freunde heraus</b> – die Top 3 der Woche gewinnen Muscheln.", chips=[("vi","🎮 4 Minispiele"),("pk","⚔️ Duelle")]),
 dict(img="insel", eyebrow="NUR FÜR DIE ERSTEN", head="DIE ERSTEN 1.000", big="BEKOMMEN<br>VORTEILE", sub="Wer jetzt einzieht, ist <b>von Anfang an</b> dabei.", chips=[], bar=True),
 dict(img="huetten", eyebrow="SO BIST DU DABEI", head="FOLG", big="@MUSCHELTAL", sub="Dann bekommst du <b>deine eigene Hütte</b>. <b>Markier deine Freunde</b>, damit sie unter den ersten 1.000 sind!", chips=[("pk","1️⃣ Folgen"),("ye","2️⃣ Freunde markieren"),("gr","3️⃣ mitbestimmen")], last=True),
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
#bar .fi{height:100%;width:80%;border-radius:45px;background:linear-gradient(90deg,#ffe500,#ff2e7e)}
#bar .lb{display:flex;justify-content:space-between;margin-top:18px;font-family:L;font-size:60px;-webkit-text-stroke:8px #1a0f08;paint-order:stroke fill}
#bar .lb span:last-child{color:#ffe500}
#free{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1130px;padding:12px 36px 16px;border-radius:40px;background:#00b86b;font-weight:900;font-size:54px;box-shadow:0 0 0 6px #1a0f08;transform:rotate(-2deg)}
#gridc{position:absolute;left:110px;width:860px;top:610px;height:690px;display:grid;grid-template-columns:1fr 1fr;gap:22px;transform:rotate(1.2deg)}
.gi{position:relative;border-radius:30px;overflow:hidden;border:8px solid #fff;box-shadow:0 0 0 5px #1a0f08,0 12px 0 rgba(0,0,0,.4);background:center/cover}
.gi span{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);white-space:nowrap;padding:3px 16px 7px;border-radius:18px;background:#1a0f08;color:#ffe500;font-weight:900;font-size:30px}
.pod{position:absolute;left:170px;right:170px;top:700px;height:560px;display:flex;align-items:flex-end;gap:20px}
.pd{flex:1;border-radius:24px 24px 0 0;text-align:center;box-shadow:0 0 0 6px #1a0f08;padding-top:14px}.pd i{font-style:normal;font-size:96px;display:block}.pd b{font-family:L;font-size:84px;font-weight:400;color:#1a0f08}
.p1{height:520px;background:#ffe500}.p2{height:400px;background:#b9c9d9}.p3{height:320px;background:#e09a5a}
.stampx{position:absolute;padding:6px 26px 10px;border:9px solid #ff2e7e;border-radius:36px;background:rgba(255,255,255,.96);color:#ff2e7e;font-family:L;font-size:64px;white-space:nowrap;box-shadow:0 10px 0 rgba(0,0,0,.35)}
#mega{position:absolute;left:0;right:0;top:300px;text-align:center;font-family:L;font-size:96px;line-height:1;color:#fff;-webkit-text-stroke:12px #1a0f08;paint-order:stroke fill;transform:rotate(-3deg)}
#mega2{position:absolute;left:0;right:0;top:395px;text-align:center;font-family:L;font-size:250px;line-height:.9;color:#ffe500;-webkit-text-stroke:16px #1a0f08;paint-order:stroke fill;text-shadow:0 14px 0 #ff2e7e;transform:rotate(-3deg)}
#cardb{position:absolute;left:130px;width:820px;top:740px;height:580px;border-radius:50%;background:center/cover;-webkit-mask:radial-gradient(ellipse 50% 50% at 50% 50%,#000 72%,transparent 100%);filter:drop-shadow(0 0 60px rgba(40,220,255,.8))}
#ring{position:absolute;left:110px;width:860px;top:720px;height:620px;border-radius:50%;box-shadow:0 0 90px 30px rgba(255,229,0,.35)}
"""
STAR = '<svg class="sp" style="left:{}px;top:{}px;width:{}px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="{}"/></svg>'
import html
for i, s in enumerate(S, 1):
    body = f'<div id="spot"></div><div id="rays"></div><div id="nr">{i}/{len(S)}</div>'
    if not s.get("last") and not s.get("first"): body += '<div id="swipe">wisch ➜</div>'
    if s.get("first"):
        body += '<div id="ep" class="pill" style="top:180px;font-size:40px;padding:10px 30px 13px;background:#ff2e7e;box-shadow:0 0 0 5px #fff">🔴 EINZIGARTIG AUF TIKTOK</div>'
        body += '<div id="mega2" style="top:330px;font-size:176px;line-height:.95">WILLST DU<br>DABEI SEIN?</div>'
        body += '<div id="ring" style="top:800px"></div><div id="cardb" style="top:820px;background-image:url(bilder/insel.jpg)"></div>'
        body += '<div class="stampx" style="left:0;right:0;margin:0 auto;width:fit-content;top:1300px;transform:rotate(-4deg);font-size:62px">800 FOLLOWER WOHNEN HIER</div>'
        body += '<div id="chips" style="top:1520px"><div class="c ye" style="font-size:54px">WISCH ➜</div></div>'
    else:
        two = "<br>" in s["big"]
        body += f'<div id="ep" class="pill">{s["eyebrow"]}</div><div id="hd" class="pill">{s["head"]}</div><div id="big"' + (' style="font-size:100px"' if two else '') + f'>{s["big"]}</div>'
        if two: body += '<style>#card,#gridc{top:680px!important;height:620px!important}.pod{top:740px!important;height:520px!important}</style>'
        if s.get("bar"):
            body += '<div id="bar"><div class="tr"><div class="fi"></div></div><div class="lb"><span>800</span><span>1.000 🎮</span></div></div><div id="free">NOCH 200 PLÄTZE FREI</div>'
        elif s.get("grid"):
            body += '<div id="gridc">' + "".join(f'<div class="gi" style="background-image:url(bilder/{f}.jpg)"><span>{n}</span></div>' for f, n in s["grid"]) + '</div>'
        elif s.get("grid3"):
            body += '<div id="gridc" style="grid-template-columns:1fr 1fr 1fr">' + "".join(f'<div class="gi" style="background-image:url(bilder/tiere/{f}.jpg)"></div>' for f in s["grid3"]) + '</div>'
        elif s.get("pod"):
            body += '<div class="pod"><div class="pd p2"><i>🥈</i><b>2.</b></div><div class="pd p1"><i>🥇</i><b>1.</b></div><div class="pd p3"><i>🥉</i><b>3.</b></div></div>'
        else:
            body += f'<div id="card" style="background-image:url(bilder/{s["img"]}.jpg)"></div>'
        body += f'<div id="sub">{s["sub"]}</div><div id="chips">' + "".join(f'<div class="c {c}">{html.escape(t)}</div>' for c, t in s["chips"]) + '</div>'
    body += STAR.format(120, 560, 64, "#ffe500") + STAR.format(880, 540, 50, "#fff") + STAR.format(70, 1250, 44, "#fff") + STAR.format(930, 1240, 56, "#ffe500")
    open(f"seite_{i:02d}.html", "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
print(len(S))
