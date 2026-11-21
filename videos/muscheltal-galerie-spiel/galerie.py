# TikTok-Foto-Galerie „Was dich im Spiel ab 1.000 erwartet“ – Look wie Video Tag 1 (Untertitel-Balken, .bt-Boxen, Stempel)
import re, html
BAR = ["#e8467c", "#0a9fa6", "#7b4fe0", "#2f7fe0"]
def bars(lines, size=116, top=470):
    out = []
    for i, l in enumerate(lines):
        t = re.sub(r"\*(.+?)\*", r'<span class="k">\1</span>', html.escape(l).replace("&lt;br&gt;", "<br>"))
        out.append(f'<div class="bar" style="background:{BAR[i % 4]};transform:rotate({(-2, 1.5, -1, 2)[i % 4]}deg)">{t}</div>')
    return f'<div class="bars" style="top:{top}px;font-size:{size}px">' + "".join(out) + "</div>"
def bt(items, top):  # Video-1-Boxen
    return f'<div class="bts" style="top:{top}px">' + "".join(f'<div class="bt {c}"><span class="bx">{t}</span></div>' for c, t in items) + "</div>"
def grid(imgs, top, lab=True):
    return f'<div class="grid" style="top:{top}px">' + "".join(f'<div class="gi"><div class="im" style="background-image:url({src})"></div>' + (f'<div class="gl">{n}</div>' if lab else "") + "</div>" for src, n in imgs) + "</div>"
S = [
 dict(bg="insel", label=("dk", "MUSCHEL-TAL · DAS SPIEL"), body=bars(["Hier passiert", "gerade etwas,", "das es auf *TikTok*", "*noch nie* gab"], 96, 400)
   + '<div class="stamp" style="left:500px;top:1120px;font-size:56px;white-space:nowrap;color:#e8467c;border-color:#e8467c;transform:rotate(-8deg)">790 FOLLOWER 🏝️</div>'
   + bt([("pk", "Eine Insel. Jede Hütte = ein echter Follower."), ("vi", "Bei 1.000 wird daraus ein Spiel 🎮")], 1300)),
 dict(bg="huetten", label=("ye", "BEI 1.000 FOLLOWERN"), body=bars(["Du spielst", "*dich selbst*"], 130, 430)
   + bt([("tq", "🚶 deine eigene Figur"), ("pk", "🏠 deine Hütte mit deinem Namen"), ("bl", "🗺️ lauf über alle Inseln")], 900)),
 dict(bg="insel", dim=.55, label=("pk", "IHR HABT ABGESTIMMT"), body=bars(["Ihr habt sie *gewünscht* –", "jetzt könnt ihr sie *erkunden*"], 66, 290)
   + grid([("bilder/w_doener.jpg", "🥙 Dönerbude"), ("bilder/w_baeckerei.jpg", "🥐 Bäckerei"), ("bilder/w_strandbar.jpg", "🍹 Strandbar"), ("bilder/w_tierheim.jpg", "🐾 Tierheim")], 640)),
 dict(bg="huetten3", label=("vi", "EURE GEBÄUDE"), body=bars(["Sie spielen eine", "*große Rolle*"], 116, 400)
   + bt([("pk", "🐾 Tiere adoptieren im Tierheim"), ("ye", "🥙 Döner für 2 € holen"), ("tq", "🍹 Dirty Muschel an der Strandbar"), ("bl", "💼 Jobs in euren Läden")], 930)),
 dict(bg="karte", label=("dk", "NUR VON EUCH GESTALTET"), body=bars(["*Ihr* entscheidet,", "was in Muschel-Tal", "*passiert*"], 112, 420)
   + bt([("pk", "💬 Wünsche in die Kommentare"), ("vi", "🗳️ ihr stimmt ab, was gebaut wird"), ("tq", "🌍 die Welt wächst mit euch weiter")], 1140)),
 dict(bg="huetten2", label=("ye", "DAS ZIEL"), body=bars(["Wer hat die", "*meisten Muscheln* 🐚?"], 90, 380)
   + '<div class="pod"><div class="pd p2"><i>🥈</i><b>2.</b></div><div class="pd p1"><i>🥇</i><b>1.</b></div><div class="pd p3"><i>🥉</i><b>3.</b></div></div>'
   + bt([("tq", "📅 tägliche Login-Serie · ✅ Aufgaben · 🔑 Geheimcodes")], 1330)),
 dict(bg="wal", label=("bl", "UND"), body=bars(["Wer hat die", "*meisten Erfolge* 🏅?"], 104, 400)
   + bt([("bl", "🐋 Wal-Watcher"), ("ye", "🏆 Aufgaben-Legende"), ("pk", "🥇 Wochensieger"), ("tq", "🧩 Sticker- & 🎣 Fisch-Album")], 860)),
 dict(bg="pearl", dim=.5, label=("ye", "GOLDEN PEARL 💎"), body=bars(["*Minispiele*", "warten auf dich"], 88, 290)
   + grid([("bilder/spiele/taucher.jpg", "🫧 Perlentaucher"), ("bilder/spiele/turm.jpg", "🥥 Kokos-Turm"), ("bilder/spiele/memory.jpg", "🐚 Muschel-Memory"), ("bilder/spiele/krebs.jpg", "🦀 Krebs-Sprint")], 650)),
 dict(bg="pearl", dim=.35, label=("vi", "⚔️ DUELLE"), body=bars(["Fordere deine", "*Freunde* heraus"], 116, 420)
   + bt([("pk", "Link schicken – wer schafft mehr?"), ("ye", "🏆 Wochen-Rangliste je Spiel"), ("tq", "Top 3 gewinnen Muscheln 🐚")], 900)),
 dict(bg="schild", label=("gr", "SELTENE EVENTS"), body=bars(["Sei zur", "*richtigen Zeit* da"], 116, 420)
   + bt([("bl", "🐋 ein Wal springt aus dem Meer"), ("gr", "🐢 Babyschildkröten wandern"), ("tq", "🍾 Flaschenpost mit Quiz")], 900)),
 dict(bg="insel", label=("pk", "NUR FÜR DIE ERSTEN"), body=bars(["Die ersten *1.000*", "bekommen *Vorteile*"], 104, 420)
   + '<div id="bar"><div class="tr"><div class="fi"></div></div><div class="lb"><span>790</span><span>1.000 🎮</span></div></div>'
   + '<div class="stamp" style="left:0;right:0;margin:0 auto;width:fit-content;top:1190px;color:#2fbf6a;border-color:#2fbf6a;transform:rotate(-3deg)">NOCH 210 PLÄTZE</div>'),
 dict(bg="huetten", label=("dk", "SO BIST DU DABEI"), body=bars(["Folg", "*@muscheltal*"], 130, 420), last=True,
   extra=bt([("pk", "1️⃣ Folgen = eigene Hütte mit deinem Namen"), ("ye", "2️⃣ Freunde markieren"), ("tq", "3️⃣ ihr entscheidet, was als Nächstes kommt")], 900)),
]
CSS = """@font-face{font-family:L;src:url(LilitaOne-Regular.woff2)}*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;overflow:hidden;position:relative;background:#0b7fae;font-family:Inter,system-ui,sans-serif;color:#fff}
#bg{position:absolute;inset:0;background:center/cover}#dim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,20,40,.55),rgba(0,20,40,.15) 35%,rgba(0,20,40,.15) 65%,rgba(0,20,40,.55))}
.bars{position:absolute;left:50px;right:150px;display:flex;flex-direction:column;align-items:center;gap:14px;font-family:L;line-height:1.05;text-align:center}
.bar{padding:.04em .36em .1em;border-radius:.55em;box-shadow:0 8px 0 rgba(0,0,0,.25);text-transform:uppercase}
.k{color:#ffe45c}
.bts{position:absolute;left:60px;right:150px;display:flex;flex-direction:column;align-items:center;gap:22px}
.bt{text-align:center;font-weight:900;font-size:46px;line-height:1.25;color:#fff;max-width:860px}
.bt .bx{padding:.06em .4em .14em;border-radius:.6em;-webkit-box-decoration-break:clone;box-decoration-break:clone;box-shadow:0 9px 0 rgba(0,0,0,.28)}
.bt.pk .bx{background:#e8467c}.bt.tq .bx{background:#0a9fa6}.bt.vi .bx{background:#7b4fe0}.bt.bl .bx{background:#2f7fe0}
.bt.ye .bx{background:#ffd23f}.bt.ye{color:#2a1b12}.bt.gr .bx{background:#2fbf6a}.bt.dk .bx{background:#2a1b12}.bt.dk{color:#ffd23f}
#lab{position:absolute;top:200px;left:0;right:90px}#lab .bt{margin:0 auto;font-size:40px}
#nr{position:absolute;right:70px;top:120px;font-weight:900;font-size:30px;color:#fff;text-shadow:0 3px 0 rgba(0,0,0,.5)}
.stamp{position:absolute;padding:6px 30px 10px;border:10px solid;border-radius:40px;background:rgba(255,255,255,.95);font-weight:900;font-size:66px;box-shadow:0 10px 0 rgba(0,0,0,.3)}
.grid{position:absolute;left:130px;right:210px;display:grid;grid-template-columns:1fr 1fr;gap:26px}
.gi{position:relative}.im{width:100%;aspect-ratio:1/1.1;border-radius:30px;border:8px solid #fff;background:center/cover;box-shadow:0 10px 0 rgba(0,0,0,.3)}
.gl{position:absolute;left:50%;bottom:-18px;transform:translateX(-50%);white-space:nowrap;padding:4px 18px 8px;border-radius:20px;background:#2a1b12;color:#ffd23f;font-weight:900;font-size:32px}
.pod{position:absolute;left:150px;right:230px;top:860px;height:420px;display:flex;align-items:flex-end;gap:20px}
.pd{flex:1;border-radius:24px 24px 0 0;text-align:center;box-shadow:0 0 0 7px #fff;padding-top:14px}.pd i{font-style:normal;font-size:90px;display:block}.pd b{font-family:L;font-size:80px;font-weight:400}
.p1{height:440px;background:#ffd23f;color:#2a1b12}.p2{height:340px;background:#9fb3c8}.p3{height:270px;background:#d98a4a}
#bar{position:absolute;left:130px;right:190px;top:960px}#bar .tr{height:90px;border-radius:45px;background:rgba(0,0,0,.55);box-shadow:0 0 0 7px #fff;overflow:hidden}
#bar .fi{height:100%;width:79%;border-radius:45px;background:linear-gradient(90deg,#ffd23f,#e8467c)}
#bar .lb{display:flex;justify-content:space-between;margin-top:16px;font-family:L;font-size:62px;text-shadow:0 5px 0 rgba(0,0,0,.45)}
#sw{position:absolute;right:70px;top:162px;font-family:L;font-size:36px;text-shadow:0 3px 0 rgba(0,0,0,.5)}"""
for i, s in enumerate(S, 1):
    b = f'<div id="bg" style="background-image:url(bilder/{s["bg"]}.jpg)"></div><div id="dim" style="opacity:{1 if not s.get("dim") else 1}"></div>'
    if s.get("dim"): b += f'<div style="position:absolute;inset:0;background:rgba(0,20,40,{s["dim"]})"></div>'
    b += f'<div id="nr">{i}/{len(S)}</div>' + ('' if s.get("last") else '<div id="sw">wisch ➜</div>')
    c, t = s["label"]; b += f'<div id="lab"><div class="bt {c}"><span class="bx">{t}</span></div></div>' + s["body"] + s.get("extra", "")
    open(f"seite_{i:02d}.html", "w").write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{b}</body></html>')
print(len(S))
