"""Erzeugt scenes/_world.html: 3D-Kokos-Küste (three.js), deterministisch über die Timeline-Zeit.
python3 werkzeug/welt.py   (liest werkzeug/namen.json)"""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent
NAMES = json.loads((D / "werkzeug" / "namen.json").read_text())

JS = r"""
      const NAMES = __NAMES__;
      const W = 1080, H = 1920, TAU = Math.PI * 2;
      const hash = (i, s) => { let x = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return x - Math.floor(x); };
      const cv = document.getElementById("w-cv");
      const R = new THREE.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, preserveDrawingBuffer: true });
      R.setPixelRatio(1); R.setSize(W, H, false);
      const S = new THREE.Scene(); S.fog = new THREE.Fog(0xcdeefa, 45, 150);
      const cam = new THREE.PerspectiveCamera(50, W / H, 0.1, 400);
      S.add(new THREE.HemisphereLight(0xfff4dc, 0x8a7a5a, 1.15));
      const sun = new THREE.DirectionalLight(0xffffff, 1.35); sun.position.set(-18, 30, 22); S.add(sun);
      const L = (c, o = {}) => new THREE.MeshLambertMaterial(Object.assign({ color: c }, o));
      const B = (c, o = {}) => new THREE.MeshBasicMaterial(Object.assign({ color: c }, o));
      const mesh = (g, m, x = 0, y = 0, z = 0) => { const k = new THREE.Mesh(g, m); k.position.set(x, y, z); return k; };

      // ---------- Boden, Meer, Stege ----------
      const sea = mesh(new THREE.PlaneGeometry(900, 900), L(0x2cb6cf)); sea.rotation.x = -Math.PI / 2; sea.position.y = -0.06; S.add(sea);
      const sand = mesh(new THREE.CircleGeometry(95, 72), L(0xf1d79e)); sand.rotation.x = -Math.PI / 2; sand.position.set(0, 0, -25); S.add(sand);
      const foam = mesh(new THREE.RingGeometry(95, 97.5, 72), B(0xffffff, { transparent: true, opacity: .75 })); foam.rotation.x = -Math.PI / 2; foam.position.set(0, .01, -25); S.add(foam);
      const shallow = mesh(new THREE.RingGeometry(97.5, 112, 72), B(0x7fe3e6, { transparent: true, opacity: .6 })); shallow.rotation.x = -Math.PI / 2; shallow.position.set(0, -.03, -25); S.add(shallow);
      for (let i = 0; i < 40; i++) { const r = 1 + hash(i, 1) * 2.2, g = mesh(new THREE.CircleGeometry(r, 18), L(0xa9d77c)); g.rotation.x = -Math.PI / 2;
        g.position.set((hash(i, 2) - .5) * 120, .012, -25 + (hash(i, 3) - .5) * 120); if (Math.hypot(g.position.x, g.position.z + 25) < 88) S.add(g); }
      const plankTex = (() => { const c = document.createElement("canvas"); c.width = 512; c.height = 64; const x = c.getContext("2d"); x.fillStyle = "#b07a48"; x.fillRect(0, 0, 512, 64);
        x.fillStyle = "#8a5a32"; for (let i = 0; i < 512; i += 32) x.fillRect(i, 0, 3, 64); const t = new THREE.CanvasTexture(c); t.wrapS = THREE.RepeatWrapping; t.repeat.set(12, 1); return t; })();
      const ROWS = [0, -10, -20, -30];
      for (const z of ROWS) { const w = mesh(new THREE.BoxGeometry(70, .12, 2.2), L(0xffffff, { map: plankTex })); w.position.set(0, .06, z + 3.9); S.add(w); }
      const cross = mesh(new THREE.BoxGeometry(2.2, .12, 52), L(0xb07a48)); cross.position.set(-12.5, .055, -24); S.add(cross);

      // ---------- Kokosnuss-Haus ----------
      const signTex = (txt, bg = "#fff6e0", fg = "#2a1b12") => { const c = document.createElement("canvas"); c.width = 512; c.height = 128; const x = c.getContext("2d");
        x.fillStyle = bg; x.fillRect(0, 0, 512, 128); x.strokeStyle = "#5a3418"; x.lineWidth = 12; x.strokeRect(6, 6, 500, 116);
        let fs = 64; x.font = `900 ${fs}px Inter, Arial, sans-serif`; while (x.measureText(txt).width > 460 && fs > 26) { fs -= 2; x.font = `900 ${fs}px Inter, Arial, sans-serif`; }
        x.fillStyle = fg; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(txt, 256, 68); const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t; };
      const sphereG = new THREE.SphereGeometry(1.7, 28, 20), leafG = new THREE.SphereGeometry(1, 14, 8), doorG = new THREE.BoxGeometry(1.0, 1.45, .8), archG = new THREE.CylinderGeometry(.5, .5, .8, 20);
      const shadowG = new THREE.CircleGeometry(2.3, 28), shadowM = B(0x000000, { transparent: true, opacity: .16, depthWrite: false });
      function makeSign(txt, special) { const g = new THREE.Group(); const post = mesh(new THREE.BoxGeometry(.14, 1.25, .14), L(0x6b4426), 0, .62, 0); g.add(post);
        const wood = L(0x8a5a32), face = new THREE.MeshBasicMaterial({ map: signTex(txt, special ? "#ffe066" : "#fff6e0") });
        const board = new THREE.Mesh(new THREE.BoxGeometry(2.1, .52, .08), [wood, wood, wood, wood, face, wood]); board.position.set(0, 1.42, 0); g.add(board); return g; }
      function makeHouse(x, z, i, name, special) {
        const g = new THREE.Group(); g.position.set(x, 0, z);
        const col = new THREE.Color().setHSL(.07 + hash(i, 4) * .02, .45, .24 + hash(i, 5) * .06);
        const body = mesh(sphereG, L(col), 0, 1.2, 0); body.scale.set(1, .95, 1); g.add(body);
        const band = mesh(new THREE.TorusGeometry(1.62, .07, 8, 40), L(col.clone().multiplyScalar(.7)), 0, 1.25, 0); band.rotation.x = Math.PI / 2; g.add(band);
        const dm = L(0x4a2a14); g.add(mesh(doorG, dm, 0, .72, 1.25)); const arch = mesh(archG, dm, 0, 1.45, 1.25); arch.rotation.x = Math.PI / 2; g.add(arch);
        g.add(mesh(new THREE.PlaneGeometry(.66, 1.15), B(0x1e1009), 0, .6, 1.66)); g.add(mesh(new THREE.CircleGeometry(.33, 18), B(0x1e1009), 0, 1.18, 1.66));
        const lit = hash(i, 6) > .35, n = new THREE.Vector3(.6, .45, .66).normalize(), wp = new THREE.Vector3(0, 1.2, 0).addScaledVector(n, 1.72);
        const win = mesh(new THREE.CircleGeometry(.3, 20), B(lit ? 0xffd27a : 0x2a1a0e), wp.x, wp.y, wp.z); win.lookAt(wp.clone().add(n)); g.add(win);
        const lg = L(0x3f9a45); for (let k = 0; k < 3; k++) { const lf = mesh(leafG, lg, 0, 2.78, 0); lf.scale.set(1.15, .17, .42); lf.rotation.set(0, k * 1.05 + hash(i, 7), (k % 2 ? .45 : -.45)); g.add(lf); }
        const sh = mesh(shadowG, shadowM, .3, .015, .3); sh.rotation.x = -Math.PI / 2; g.add(sh);
        if (name) { const sg = makeSign("@" + name, special); sg.position.set(1.95, 0, 1.55); sg.rotation.y = -.25; g.add(sg); g.userData.sign = sg; }
        S.add(g); return g; }
      const HOUSES = []; let ni = 0;
      for (const z of ROWS) for (let x = -25; x <= 25; x += 5) { if (z === 0 && (x === 0 || x === 5)) continue; HOUSES.push(makeHouse(x, z, HOUSES.length, NAMES[ni++ % NAMES.length])); }
      const MY = makeHouse(0, 0, 99, "dein.name", true), BF = makeHouse(5, 0, 98, "dein.bestie?", true);

      // ---------- Palmen ----------
      const PALMS = [];
      function makePalm(x, z, h, lean, i) { const g = new THREE.Group(); g.position.set(x, 0, z);
        const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0, 0), new THREE.Vector3(lean * .3, h * .4, 0), new THREE.Vector3(lean * .7, h * .75, 0), new THREE.Vector3(lean, h, 0)]);
        g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 16, .2, 8, false), L(0x8a6440)));
        const crown = new THREE.Group(); crown.position.set(lean, h, 0); g.add(crown); const lm = L(0x34a04a);
        for (let k = 0; k < 7; k++) { const p = new THREE.Group(); p.rotation.y = k / 7 * TAU + hash(i, 8); const lf = mesh(leafG, lm, 1.35, -.35, 0); lf.scale.set(1.6, .07, .38); lf.rotation.z = -.38; p.add(lf); crown.add(p); }
        crown.add(mesh(new THREE.SphereGeometry(.28, 10, 8), L(0x5a3a1a), 0, -.2, 0));
        g.userData = { crown, i }; S.add(g); PALMS.push(g); }
      [[-8, 6, 7, 1], [9.5, 7, 6.5, -1.1], [-17, -5, 8, .9], [17, -5, 7.5, -.8], [-6, -44, 7, 1], [7, -52, 7.5, -1], [-30, 5, 8, 1.2], [30, 4, 7, -1], [23, -40, 8, -1], [-24, -38, 7, 1]].forEach((p, i) => makePalm(p[0], p[1], p[2], p[3], i));

      // ---------- Lagerfeuer-Platz ----------
      const PZ = new THREE.Vector3(0, 0, -46);
      const plaza = mesh(new THREE.CircleGeometry(9, 40), L(0xf6e2b0), PZ.x, .02, PZ.z); plaza.rotation.x = -Math.PI / 2; S.add(plaza);
      for (let k = 0; k < 9; k++) { const a = k / 9 * TAU; S.add(mesh(new THREE.SphereGeometry(.28, 10, 8), L(0x8d8a84), PZ.x + Math.cos(a) * .95, .15, PZ.z + Math.sin(a) * .95)); }
      for (const a of [.5, -.5]) { const lg = mesh(new THREE.CylinderGeometry(.13, .13, 1.6, 10), L(0x5a3418), PZ.x, .2, PZ.z); lg.rotation.set(Math.PI / 2, 0, a); S.add(lg); }
      const FL = []; [[0xff5a1a, .55, 1.5], [0xff9a2a, .4, 1.1], [0xffe08a, .22, .7]].forEach(([c, r, h], k) => { const f = mesh(new THREE.ConeGeometry(r, h, 10), B(c), PZ.x, .3 + h / 2, PZ.z); S.add(f); FL.push(f); });
      const fireL = new THREE.PointLight(0xffa04a, 3, 14, 1.5); fireL.position.set(PZ.x, 1.4, PZ.z); S.add(fireL);
      const BENCH = []; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + .26; const lg = mesh(new THREE.CylinderGeometry(.22, .22, 1.9, 10), L(0x6b4426), PZ.x + Math.cos(a) * 3.3, .22, PZ.z + Math.sin(a) * 3.3); lg.rotation.set(0, -a, Math.PI / 2); S.add(lg); BENCH.push(a); }
      for (let k = 0; k < 8; k++) { const a = k / 8 * TAU, x = PZ.x + Math.cos(a) * 8.2, z = PZ.z + Math.sin(a) * 8.2; S.add(mesh(new THREE.CylinderGeometry(.06, .06, 2.2, 6), L(0x8a6440), x, 1.1, z)); S.add(mesh(new THREE.SphereGeometry(.2, 10, 8), B(0xffd27a), x, 2.3, z)); }

      // ---------- Bewohner ----------
      const SHIRTS = [0xe8467c, 0xff6a1a, 0x18b8c0, 0x7b3fe0, 0xffd23f, 0x2e9e5b, 0x3fa0e8, 0xffffff], SKIN = [0xf1c7a0, 0xd9a07a, 0xa86a45, 0x7a4a2a], HAIR = [0x2a1b12, 0x5a3418, 0xe0b050, 0x111111];
      const legG = new THREE.CylinderGeometry(.11, .1, .8, 8), armG = new THREE.CylinderGeometry(.075, .07, .65, 8), bodyG = new THREE.CylinderGeometry(.27, .31, .78, 12), headG = new THREE.SphereGeometry(.26, 14, 12);
      const nameSprite = (txt) => { const c = document.createElement("canvas"); c.width = 512; c.height = 96; const x = c.getContext("2d"); let fs = 54; x.font = `800 ${fs}px Inter, Arial, sans-serif`;
        while (x.measureText(txt).width > 470 && fs > 24) { fs -= 2; x.font = `800 ${fs}px Inter, Arial, sans-serif`; } const w = x.measureText(txt).width + 40;
        x.fillStyle = "rgba(42,27,18,.85)"; x.beginPath(); x.roundRect(256 - w / 2, 8, w, 80, 40); x.fill(); x.fillStyle = "#fff"; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(txt, 256, 50);
        const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false })); s.scale.set(2.2, .41, 1); return s; };
      const bubble = (em) => { const c = document.createElement("canvas"); c.width = 160; c.height = 160; const x = c.getContext("2d"); x.fillStyle = "#fff"; x.beginPath(); x.arc(80, 72, 62, 0, TAU); x.fill();
        x.beginPath(); x.moveTo(60, 120); x.lineTo(50, 156); x.lineTo(92, 126); x.fill(); x.font = "72px 'Noto Color Emoji', sans-serif"; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(em, 80, 76);
        const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false })); s.scale.set(.8, .8, 1); return s; };
      function makePerson(i, name, em) { const g = new THREE.Group(); const sh = SHIRTS[i % SHIRTS.length], sk = SKIN[Math.floor(hash(i, 9) * 4)], hr = HAIR[Math.floor(hash(i, 10) * 4)];
        const legs = [-.13, .13].map((x) => { const p = new THREE.Group(); p.position.set(x, .8, 0); p.add(mesh(legG, L(0x2a2f4a), 0, -.4, 0)); g.add(p); return p; });
        const bod = mesh(bodyG, L(sh), 0, 1.18, 0); g.add(bod); const head = mesh(headG, L(sk), 0, 1.83, 0); g.add(head);
        const hair = mesh(headG, L(hr), 0, 1.9, -.03); hair.scale.set(1.05, .62, 1.05); g.add(hair);
        const arms = [-.37, .37].map((x) => { const p = new THREE.Group(); p.position.set(x, 1.5, 0); p.add(mesh(armG, L(sh), 0, -.31, 0)); g.add(p); return p; });
        const sh2 = mesh(new THREE.CircleGeometry(.45, 16), shadowM, 0, .016, 0); sh2.rotation.x = -Math.PI / 2; g.add(sh2);
        let tag = null; if (name) { tag = nameSprite("@" + name); tag.position.set(0, 2.45, 0); g.add(tag); }
        let bub = null; if (em) { bub = bubble(em); bub.position.set(.55, 2.95, 0); g.add(bub); }
        g.userData = { legs, arms, bod, head, hair, tag, bub, i }; S.add(g); return g; }
      function pose(p, t, mode, k = 1) { const u = p.userData, s = Math.sin(t * 8 + u.i);
        u.legs.forEach((l, j) => { l.rotation.x = mode === "walk" ? (j ? -s : s) * .55 : mode === "sit" ? -1.45 : 0; });
        u.arms.forEach((a, j) => { a.rotation.x = mode === "walk" ? (j ? s : -s) * .5 : 0; a.rotation.z = 0; });
        const dy = mode === "sit" ? -.42 : mode === "walk" ? Math.abs(s) * .05 : 0; [u.bod, u.head, u.hair].forEach((m, j) => m.position.y = [1.18, 1.83, 1.9][j] + dy); u.arms.forEach((a) => a.position.y = 1.5 + dy);
        if (u.tag) u.tag.position.y = 2.45 + dy; if (u.bub) { u.bub.position.y = 2.95 + dy + Math.sin(t * 3 + u.i) * .06; }
        if (mode === "wave") { u.arms[1].rotation.z = 2.5 + Math.sin(t * 10 + u.i) * .35; }
        if (mode === "talk") { u.head.rotation.y = Math.sin(t * 2 + u.i) * .25; u.arms[0].rotation.x = -.4 + Math.sin(t * 4 + u.i) * .25; } }
      let pi = 0; const nm = () => NAMES[(40 + pi) % NAMES.length];
      // Spaziergänger auf den Stegen
      const WALK = []; for (let k = 0; k < 14; k++) { const row = ROWS[k % 4], p = makePerson(pi++, k < 9 ? nm() : null, null); p.userData.row = row; p.userData.x0 = (hash(k, 11) - .5) * 60; p.userData.v = (hash(k, 12) > .5 ? 1 : -1) * (1.1 + hash(k, 13) * .5); WALK.push(p); }
      // Lagerfeuer: sitzend + plaudernd
      const EM = ["🥥", "😂", "🔥", "🎉", "💬", "🏝️"];
      const SIT = BENCH.map((a, k) => { const p = makePerson(pi++, nm(), k % 2 ? EM[k] : null); p.position.set(PZ.x + Math.cos(a) * 3.3, 0, PZ.z + Math.sin(a) * 3.3); p.userData.face = PZ; return p; });
      const PW = []; for (let k = 0; k < 4; k++) { const p = makePerson(pi++, nm(), k === 1 ? "👋" : null); p.userData.ang = k / 4 * TAU; PW.push(p); }
      // Nachbarn-Szene: zwei Bewohner vor den Häusern
      const N1 = makePerson(2, null, null), N2 = makePerson(5, null, null);

      // ---------- Zeit / Kamera ----------
      const s02 = C.s02[0], s03 = C.s03[0], s04 = C.s04[0], s05 = C.s05[0], END = C.__dur;
      const T_HOUSE = at("L2", "das") - .1, T_SIGN = at("L2", "dein") - .05, T_BF = s04 + .3, T_HI = at("L5", "markier") - .25;
      const ease = (k) => k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, cl = (v) => Math.max(0, Math.min(1, v));
      const lerp = (a, b, k) => a + (b - a) * k, V = (x, y, z) => new THREE.Vector3(x, y, z);
      function camShot(t) {
        if (t < s02) { const k = ease(cl(t / s02)), a = lerp(0, .32, ease(cl((t - T_HOUSE) / (s02 - T_HOUSE))));
          return [V(Math.sin(a) * 12.5, lerp(2.7, 2.4, k), Math.cos(a) * 12.5 + lerp(0, -1, k)), V(0, 1.35, 0)]; }
        if (t < s03) { const k = ease(cl((t - s02) / (s03 - s02))), x = lerp(-26, 1, k); return [V(x, 2.5, 11), V(x + 3, 1.3, 0)]; }
        if (t < s04) { const k = cl((t - s03) / (s04 - s03)), a = lerp(-.55, .7, ease(k)), r = lerp(13.5, 11.5, k); return [V(PZ.x + Math.sin(a) * r, lerp(5.2, 4.2, k), PZ.z + Math.cos(a) * r), V(PZ.x, .9, PZ.z)]; }
        if (t < s05) { const k = ease(cl((t - s04) / (s05 - s04))); return [V(3.5, lerp(2.9, 2.6, k), lerp(15, 13.5, k)), V(3.5, 1.4, 0)]; }
        const k = ease(cl((t - s05) / (END - s05))); return [V(2.5, lerp(3, 46, k), lerp(11, 42, k)), V(lerp(2.5, 0, k), 0, lerp(0, -20, k))]; }
      function draw(t) {
        // Häuser
        const hk = cl((t - T_HOUSE) / .45), hs = hk <= 0 ? 0.0001 : (hk >= 1 ? 1 : 1 - Math.pow(1 - hk, 3) * Math.cos(hk * 9) * 1.0);
        MY.scale.setScalar(Math.max(.0001, hs)); MY.visible = hk > 0; MY.userData.sign.visible = t >= T_SIGN; MY.userData.sign.scale.setScalar(t >= T_SIGN ? Math.min(1, .3 + (t - T_SIGN) * 4) : 1);
        BF.visible = t >= s04; const bk = cl((t - T_BF) / .45); BF.scale.setScalar(Math.max(.0001, bk >= 1 ? 1 : 1 - Math.pow(1 - bk, 3) * Math.cos(bk * 9)));
        // Palmen
        PALMS.forEach((p) => { p.userData.crown.rotation.z = Math.sin(t * 1.3 + p.userData.i) * .06; p.userData.crown.rotation.x = Math.cos(t * 1.1 + p.userData.i) * .04; });
        // Feuer
        FL.forEach((f, k) => { f.scale.set(1 + Math.sin(t * 11 + k) * .12, 1 + Math.sin(t * 9 + k * 2) * .22, 1 + Math.cos(t * 12 + k) * .12); }); fireL.intensity = 2.6 + Math.sin(t * 13) * .5;
        // Spaziergänger
        WALK.forEach((p) => { const u = p.userData; let x = u.x0 + u.v * t; x = ((x + 32) % 64 + 64) % 64 - 32; p.position.set(x, .12, u.row + 3.9 + (u.v > 0 ? .45 : -.45)); p.rotation.y = u.v > 0 ? Math.PI / 2 : -Math.PI / 2; pose(p, t, "walk"); });
        SIT.forEach((p, k) => { p.lookAt(PZ.x, 0, PZ.z); pose(p, t, k % 2 ? "talk" : "sit"); if (k % 2) pose(p, t, "sit"), p.userData.head.rotation.y = Math.sin(t * 2 + k) * .3; });
        PW.forEach((p, k) => { const a = p.userData.ang + t * .22, r = 5.2; p.position.set(PZ.x + Math.cos(a) * r, 0, PZ.z + Math.sin(a) * r); p.rotation.y = -a; pose(p, t, k === 1 ? "wave" : "walk"); if (k === 1) { const u = p.userData; u.legs.forEach((l, j) => l.rotation.x = (j ? -1 : 1) * Math.sin(t * 8) * .5); } });
        // Nachbarn: laufen aufeinander zu und klatschen ab
        const vis = t >= s04 && t < s05; N1.visible = N2.visible = vis;
        if (vis) { const k = ease(cl((t - (s04 + .4)) / (T_HI - s04 - .4))); N1.position.set(lerp(-.3, 4.0, k), .12, 3.4); N2.position.set(lerp(9.3, 4.9, k), .12, 3.4);
          N1.rotation.y = Math.PI / 2; N2.rotation.y = -Math.PI / 2; pose(N1, t, k < 1 ? "walk" : "stand"); pose(N2, t, k < 1 ? "walk" : "stand");
          if (t >= T_HI) { const h = Math.min(1, (t - T_HI) / .15); N1.userData.arms[1].rotation.z = 0; N1.userData.arms[1].rotation.x = -2.6 * h; N2.userData.arms[0].rotation.x = -2.6 * h; } }
        foam.scale.setScalar(1 + Math.sin(t * 1.4) * .004);
        const [p, l] = camShot(t); cam.position.copy(p); cam.lookAt(l); R.render(S, cam); }
      const tl = gsap.timeline({ paused: true }), o = { t: 0 };
      tl.to(o, { t: C.__dur, duration: C.__dur, ease: "none", onUpdate: () => draw(o.t) }, 0);
      draw(0);
      window.__timelines["world"] = tl;
"""

TPL = """<template>
  <style>
    #root { position: absolute; inset: 0; background: linear-gradient(180deg, #5fc4ee 0%, #9fdcf5 38%, #e8f7fb 52%, #bfe8f5 60%); }
    #w-cv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
  </style>
  <div id="root" data-composition-id="world" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
    <canvas id="w-cv" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0" width="1080" height="1920"></canvas>
  </div>
  <script src="assets/vendor/three.min.js"></script>
  <script>
    (() => {
      /*__CUE_HELPERS__*/
""" + JS.replace("__NAMES__", json.dumps(NAMES)) + """
    })();
  </script>
</template>
"""
(D / "scenes" / "_world.html").write_text(TPL)
print("ok", len(NAMES))
