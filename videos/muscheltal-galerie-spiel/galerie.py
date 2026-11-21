# TikTok-Foto-Galerie „Spiel ab 1.000“ – Look wie Cover Tag 1 (dunkelblau, Strahlen, gelbe Schrift, Karten)
S = [
 dict(first=True),
 dict(what=True, eyebrow="KURZ ERKLÄRT", big="WAS IST<br>MUSCHEL-TAL?"),
 dict(duo=[("erkunden1c","🚶 zu Fuß"),("erkunden2c","🛵 mit dem Moped")], eyebrow="SO MACHT'S SPASS 🤩", head="DU STEUERST DEINE FIGUR:", big="LAUF ÜBER<br>DIE INSEL", stamp2="🎮 DEIN EIGENES ABENTEUER"),
 dict(grid=[("sand","🏰 Sandburg bauen"),("angel","🎣 Angeln"),("kino","🎬 Kino"),("pearl","💎 Golden Pearl")], eyebrow="LANGWEILIG WIRD'S NIE", head="SO VIEL ZU TUN:", big="DEINE INSEL"),
 dict(liste=[("ye","💼 JOBS"),("pk","🏗️ GEBÄUDE"),("tq","🏝️ NEUE INSELN"),("vi","🎉 EVENTS"),("gr","🐾 TIERE")], eyebrow="SO FUNKTIONIERT'S", head="IN DIESEM SPIEL GILT:", big="IHR<br>ENTSCHEIDET"),
 dict(pair=("kommentare/marie_comment.jpg","w_yacht"), eyebrow="DEIN WUNSCH WIRD WAHR", big="DU WILLST<br>EINE YACHT?", stamp="✅ MARIE HAT JETZT IHRE YACHT"),
 dict(pair=("kommentare/cmt_club.jpg","w_clubnacht"), eyebrow="DEIN WUNSCH WIRD WAHR", big="DU WILLST<br>EINEN CLUB?", stamp="✅ GEBAUT – BESITZER VERLOST"),
 dict(pair2=[("kommentare/cmt_drog.jpg","w_drog","✅ CocoCare"),("kommentare/sophia_amtshandlung.jpg","w_doener","✅ Döner 2 €")], eyebrow="UND NOCH MEHR", big="IHR WÜNSCHT –<br>ES PASSIERT"),
 dict(grid=[("w_doener","🥙 Dönerbude"),("w_strandbar","🍹 Strandbar"),("w_drog","🧴 CocoCare"),("w_clubnacht","🕶️ Kokos-Club")], gh=700, eyebrow="WIE IM ECHTEN LEBEN", head="JEDER FOLLOWER KANN", big="EINEN JOB<br>BEKOMMEN 💼", stamp2="🗳️ IHR VERGEBT DIE JOBS", chips2=[("ye","🐚 Muscheln verdienen"),("pk","📝 bewerben"),("vi","🗳️ abstimmen")]),
 dict(grid3=["hund","katze","hase","schildi","schwein","robbe"], eyebrow="🗳️ EURE ABSTIMMUNG", head="TIERHEIM STATT HOTEL –", big="ADOPTIER<br>DEIN TIER 🐾", stamp2="✅ EURE ENTSCHEIDUNG"),
 dict(grid=[("spiele/taucher","🫧 Perlentaucher"),("spiele/turm","🥥 Kokos-Turm"),("spiele/memory","🐚 Memory"),("spiele/krebs","🦀 Krebs-Sprint")], eyebrow="GOLDEN PEARL 💎", head="FORDER FREUNDE HERAUS:", big="MINISPIELE"),
 dict(duo=[("wal","🐋 Wal-Sprung"),("schild","🐢 Schildkröten")], eyebrow="SELTENE EVENTS", head="IHR BESTIMMT AUCH,", big="WAS<br>PASSIERT", stamp2="💬 WÜNSCH DIR DAS NÄCHSTE EVENT"),
 dict(pod=True, eyebrow="DAS ZIEL", head="MEISTE MUSCHELN & ERFOLGE:", big="WER WIRD<br>NR. 1? 🐚"),
 dict(img="insel", eyebrow="NUR FÜR DIE ERSTEN", head="DIE ERSTEN 1.000", big="BEKOMMEN<br>VORTEILE", bar=True),
 dict(img="huetten", eyebrow="DEIN WUNSCH IST DER NÄCHSTE", head="KOMMENTIER ES –", big="FOLG<br>@MUSCHELTAL", last=True),
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

.cm{position:absolute;left:80px;right:80px;border-radius:26px;overflow:hidden;border:6px solid #fff;box-shadow:0 0 0 5px #1a0f08,0 12px 0 rgba(0,0,0,.4);transform:rotate(-2deg)}.cm img{display:block;width:100%}
.bld{position:absolute;left:150px;width:780px;height:780px;border-radius:40px;background:center/cover;border:10px solid #fff;box-shadow:0 0 0 6px #1a0f08,0 18px 0 rgba(0,0,0,.4),0 0 100px rgba(40,200,230,.45);transform:rotate(1.5deg)}
.ok{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;padding:8px 30px 12px;border-radius:36px;background:#00b86b;color:#fff;font-family:L;font-size:62px;box-shadow:0 0 0 6px #1a0f08,0 10px 0 rgba(0,0,0,.35);transform:rotate(-3deg);white-space:nowrap}
.col{position:absolute;width:440px}.col .cm{position:relative;left:0;right:0;margin-bottom:20px}.col .bld{position:relative;left:0;width:440px;height:520px}.col .ok{position:relative;font-size:44px;margin-top:-30px}
#ring{position:absolute;left:110px;width:860px;top:720px;height:620px;border-radius:50%;box-shadow:0 0 90px 30px rgba(255,229,0,.35)}
"""
STAR = '<svg class="sp" style="left:{}px;top:{}px;width:{}px" viewBox="-10 -10 20 20"><path d="M0 -10 L2 -2 L10 0 L2 2 L0 10 L-2 2 L-10 0 L-2 -2Z" fill="{}"/></svg>'
import html
for i, s in enumerate(S, 1):
    body = f'<div id="spot"></div><div id="rays"></div><div id="nr">{i}/{len(S)}</div>'
    if not s.get("last") and not s.get("first"): body += '<div id="swipe">wisch ➜</div>'
    if s.get("first"):
        body += '<div id="ep" class="pill" style="top:180px;font-size:40px;padding:10px 30px 13px;background:#ff2e7e;box-shadow:0 0 0 5px #fff">🔴 SENSATION</div><div class="pill" style="top:660px;padding:10px 32px 14px;font-size:44px;background:#7b4fe0;box-shadow:0 0 0 5px #1a0f08;transform:rotate(2deg)">🎮 EIN SPIEL – UND JEDER KANN MITSPIELEN</div>'
        body += '<div id="mega2" style="top:310px;font-size:156px;line-height:.95">EINZIGARTIG<br>AUF TIKTOK</div>'
        body += '<div id="ring" style="top:790px"></div><div id="cardb" style="top:810px;background-image:url(bilder/insel.jpg)"></div>'
        body += '<div class="stampx" style="left:0;right:0;margin:0 auto;width:fit-content;top:1250px;transform:rotate(-3deg);font-size:64px;text-align:center;line-height:1.05;white-space:normal">WILLST DU TEIL VON<br>ETWAS GROSSEM SEIN?</div>'
        body += '<div id="chips" style="top:1530px"><div class="c ye" style="font-size:48px">NEUGIERIG GEWORDEN? SWIPE ➜</div></div>'
    else:
        two = "<br>" in s["big"]
        body += f'<div id="ep" class="pill" style="top:250px">{s["eyebrow"]}</div>'
        if s.get("head"): body += f'<div id="hd" class="pill" style="top:335px">{s["head"]}</div>'
        top = 425 if s.get("head") else 345
        body += f'<div id="big" style="top:{top}px' + (';font-size:104px' if two else ';font-size:128px') + f'">{s["big"]}</div>'
        y0 = top + (230 if two else 150)
        if s.get("pair"):
            c, im = s["pair"]
            body += f'<div class="cm" style="top:{y0}px"><img src="bilder/{c}"></div>'
            body += f'<div class="bld" style="top:{y0+230}px;left:120px;width:840px;height:{1500-y0-230}px;background-image:url(bilder/{im}.jpg)"></div>'
            body += f'<div class="ok" style="top:1460px">{s["stamp"]}</div>'
        elif s.get("liste"):
            body += f'<div id="ring" style="top:{y0+10}px;height:480px"></div><div id="cardb" style="top:{y0+30}px;height:440px;background-image:url(bilder/karte.jpg)"></div>'
            body += f'<div id="chips" style="top:{y0+520}px;gap:22px">' + "".join(f'<div class="c {c}" style="font-family:L;font-weight:400;font-size:60px;transform:rotate({(-3,2,-2,3,-1)[k]}deg)">{t}</div>' for k, (c, t) in enumerate(s["liste"])) + '</div>'
            body += '<div class="ok" style="top:1560px;font-size:50px">👇 SO SIEHT DAS AUS</div>'
        elif s.get("what"):
            body += f'<div id="gridc" style="top:{y0+20}px;height:400px;grid-template-columns:1fr 1fr 1fr;left:70px;width:940px">' + "".join(f'<div class="gi" style="background-image:url(bilder/{f}.jpg)"><span>{n}</span></div>' for f, n in [("haupt","🏰 Haupt-Insel"),("kokos","🥥 Kokos-Küste"),("karte","🔒 neue Inseln")]) + '</div>'
            body += f'<div id="chips" style="top:{y0+470}px;flex-direction:column;align-items:center;gap:18px">' + "".join(f'<div class="c {c}" style="font-size:40px;white-space:nowrap">{t}</div>' for c, t in [("tq","🏝️ Eine Insel-Region in der Südsee"),("ye","🌴 Jede Insel mit eigenem Thema"),("bl","🗺️ Strände, Läden, Club, Kino …"),("pk","🏠 Jede Hütte = ein echter Follower"),("vi","🎮 Ein Spiel, in dem jeder mitspielt")]) + '</div>'
        elif s.get("pair2"):
            for k, (c, im, t) in enumerate(s["pair2"]):
                body += f'<div class="col" style="left:{70+k*480}px;top:{y0+20}px;transform:rotate({(-1.5,1.5)[k]}deg)"><div class="cm"><img src="bilder/{c}"></div><div class="bld" style="background-image:url(bilder/{im}.jpg)"></div><div class="ok">{t}</div></div>'
        elif s.get("bar"):
            body += '<div id="bar"><div class="tr"><div class="fi"></div></div><div class="lb"><span>800</span><span>1.000 🎮</span></div></div><div id="free">NOCH 200 PLÄTZE FREI</div>'
        elif s.get("grid3"):
            body += f'<div id="gridc" style="grid-template-columns:1fr 1fr 1fr;top:{y0+40}px;height:620px">' + "".join(f'<div class="gi" style="background-image:url(bilder/tiere/{f}.jpg)"></div>' for f in s["grid3"]) + '</div>'
        elif s.get("grid"):
            body += f'<div id="gridc" style="top:{y0+30}px;height:{s.get("gh",820)}px">' + "".join(f'<div class="gi" style="background-image:url(bilder/{f}.jpg)"><span>{n}</span></div>' for f, n in s["grid"]) + '</div>'
        elif s.get("duo"):
            body += f'<div id="gridc" style="top:{y0+40}px;height:740px;grid-template-columns:1fr 1fr">' + "".join(f'<div class="gi" style="background-image:url(bilder/{f}.jpg)"><span>{n}</span></div>' for f, n in s["duo"]) + '</div>'
        elif s.get("pod"):
            body += f'<div class="pod" style="top:{y0+80}px;height:600px"><div class="pd p2"><i>🥈</i><b>2.</b></div><div class="pd p1"><i>🥇</i><b>1.</b></div><div class="pd p3"><i>🥉</i><b>3.</b></div></div>'
        else:
            body += f'<div id="card" style="top:{y0+40}px;height:740px;background-image:url(bilder/{s["img"]}.jpg)"></div>'
        if s.get("stamp2"): body += f'<div class="ok" style="top:1470px;font-size:54px">{s["stamp2"]}</div>'
        if s.get("chips2"): body += '<div id="chips" style="top:1590px">' + "".join(f'<div class="c {c}" style="font-size:42px">{t}</div>' for c, t in s["chips2"]) + '</div>'
        if s.get("last"): body += '<div class="ok" style="top:1500px;background:#ff2e7e">💬 WAS SOLL ICH BAUEN?</div>'
    body += STAR.format(120, 560, 64, "#ffe500") + STAR.format(880, 540, 50, "#fff") + STAR.format(70, 1250, 44, "#fff") + STAR.format(930, 1240, 56, "#ffe500")
    open(f"seite_{i:02d}.html", "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
print(len(S))