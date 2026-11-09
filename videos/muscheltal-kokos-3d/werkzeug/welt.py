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
      R.setPixelRatio(1); R.setSize(W, H, false); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
      const S = new THREE.Scene(); S.fog = new THREE.Fog(0xcdeefa, 45, 150);
      const cam = new THREE.PerspectiveCamera(50, W / H, 0.1, 400);
      S.add(new THREE.HemisphereLight(0xfff4dc, 0x8a7a5a, 1.15));
      const sun = new THREE.DirectionalLight(0xfff2dd, 1.5); sun.position.set(-14, 26, 20); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); const sc = sun.shadow.camera; sc.left = -34; sc.right = 34; sc.top = 34; sc.bottom = -34; sc.near = 1; sc.far = 90; sun.shadow.bias = -.0008; sun.shadow.radius = 3; S.add(sun); S.add(sun.target); sun.target.position.set(0, 0, -10);
      const L = (c, o = {}) => new THREE.MeshLambertMaterial(Object.assign({ color: c }, o));
      const B = (c, o = {}) => new THREE.MeshBasicMaterial(Object.assign({ color: c }, o));
      const mesh = (g, m, x = 0, y = 0, z = 0) => { const k = new THREE.Mesh(g, m); k.position.set(x, y, z); return k; };

      // ---------- Boden, Meer, Stege ----------
      const sea = mesh(new THREE.PlaneGeometry(900, 900), L(0x2cb6cf)); sea.rotation.x = -Math.PI / 2; sea.position.y = -0.06; S.add(sea);
      const sand = mesh(new THREE.CircleGeometry(95, 72), L(0xf1d79e)); sand.rotation.x = -Math.PI / 2; sand.position.set(0, 0, -25); sand.receiveShadow = true; S.add(sand);
      const foam = mesh(new THREE.RingGeometry(95, 97.5, 72), B(0xffffff, { transparent: true, opacity: .75 })); foam.rotation.x = -Math.PI / 2; foam.position.set(0, .01, -25); S.add(foam);
      const shallow = mesh(new THREE.RingGeometry(97.5, 112, 72), B(0x7fe3e6, { transparent: true, opacity: .6 })); shallow.rotation.x = -Math.PI / 2; shallow.position.set(0, -.03, -25); S.add(shallow);
      for (let i = 0; i < 40; i++) { const r = 1 + hash(i, 1) * 2.2, g = mesh(new THREE.CircleGeometry(r, 18), L(0xa9d77c)); g.rotation.x = -Math.PI / 2;
        g.position.set((hash(i, 2) - .5) * 120, .012, -25 + (hash(i, 3) - .5) * 120); if (Math.hypot(g.position.x, g.position.z + 25) < 88) S.add(g); }
      const plankTex = (() => { const c = document.createElement("canvas"); c.width = 512; c.height = 64; const x = c.getContext("2d"); x.fillStyle = "#b07a48"; x.fillRect(0, 0, 512, 64);
        x.fillStyle = "#8a5a32"; for (let i = 0; i < 512; i += 32) x.fillRect(i, 0, 3, 64); const t = new THREE.CanvasTexture(c); t.wrapS = THREE.RepeatWrapping; t.repeat.set(12, 1); return t; })();
      const ROWS = [0, -10, -20, -30];
      for (const z of ROWS) { const w = mesh(new THREE.BoxGeometry(70, .12, 2.2), L(0xffffff, { map: plankTex })); w.position.set(0, .06, z + 3.9); w.receiveShadow = true; S.add(w); }
      const cross = mesh(new THREE.BoxGeometry(2.2, .12, 52), L(0xb07a48)); cross.position.set(-12.5, .055, -24); S.add(cross);

      // ---------- Kokosnuss-Haus ----------
      const signTex = (txt, bg = "#fff6e0", fg = "#2a1b12") => { const c = document.createElement("canvas"); c.width = 512; c.height = 128; const x = c.getContext("2d");
        x.fillStyle = bg; x.fillRect(0, 0, 512, 128); x.strokeStyle = "#5a3418"; x.lineWidth = 12; x.strokeRect(6, 6, 500, 116);
        let fs = 64; x.font = `900 ${fs}px Inter, Arial, sans-serif`; while (x.measureText(txt).width > 460 && fs > 26) { fs -= 2; x.font = `900 ${fs}px Inter, Arial, sans-serif`; }
        x.fillStyle = fg; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(txt, 256, 68); const t = new THREE.CanvasTexture(c); t.anisotropy = 4; return t; };
      const leafG = new THREE.SphereGeometry(1, 14, 8);
      const shadowM = B(0x000000, { transparent: true, opacity: .14, depthWrite: false });
      function makeSign(txt, special) { const g = new THREE.Group(); const post = mesh(new THREE.BoxGeometry(.14, 1.25, .14), L(0x6b4426), 0, .62, 0); post.castShadow = true; g.add(post);
        const wood = L(0x8a5a32), face = new THREE.MeshBasicMaterial({ map: signTex(txt, special ? "#ffe066" : "#fff6e0") });
        const board = new THREE.Mesh(new THREE.BoxGeometry(2.1, .52, .08), [wood, wood, wood, wood, face, wood]); board.position.set(0, 1.42, 0); board.castShadow = true; g.add(board); return g; }
      const fiberTex = (base, light, seed, n) => { const c = document.createElement("canvas"); c.width = 1024; c.height = 512; const x = c.getContext("2d");
        const g = x.createLinearGradient(0, 0, 0, 512); g.addColorStop(0, light); g.addColorStop(1, base); x.fillStyle = g; x.fillRect(0, 0, 1024, 512);
        for (let k = 0; k < n; k++) { const px = hash(k, seed) * 1024, py = hash(k, seed + 1) * 512, a = (hash(k, seed + 2) - .5) * 1.6, l = 18 + hash(k, seed + 3) * 34;
          x.strokeStyle = `rgba(${200 + hash(k, 9) * 40},${150 + hash(k, 8) * 40},${110 + hash(k, 7) * 30},${.18 + hash(k, 6) * .22})`; x.lineWidth = 3 + hash(k, 5) * 3; x.lineCap = "round";
          x.beginPath(); x.moveTo(px, py); x.lineTo(px + Math.cos(a) * l, py + Math.sin(a) * l); x.stroke(); }
        const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; };
      const SHELL = [0, 1, 2].map((k) => fiberTex("#2c1f26", "#4a3640", 20 + k * 7, 260)), DOME = [0, 1, 2].map((k) => fiberTex("#5a3e34", "#7a5646", 50 + k * 7, 220));
      const shellG = new THREE.SphereGeometry(1.75, 48, 32), domeG = new THREE.SphereGeometry(1.4, 48, 32), poreG = new THREE.SphereGeometry(1, 20, 14), fibG = new THREE.CapsuleGeometry(.018, .26, 3, 6);
      const archShape = (w, h) => { const sh = new THREE.Shape(); sh.moveTo(-w / 2, 0); sh.lineTo(-w / 2, h - w / 2); sh.absarc(0, h - w / 2, w / 2, Math.PI, 0, true); sh.lineTo(w / 2, 0); sh.lineTo(-w / 2, 0); return sh; };
      const frameShape = archShape(1.02, 1.42); frameShape.holes.push(archShape(.74, 1.24));
      const frameG = new THREE.ExtrudeGeometry(frameShape, { depth: .14, bevelEnabled: true, bevelSize: .025, bevelThickness: .025, bevelSegments: 3, curveSegments: 24 });
      const lightG = new THREE.ShapeGeometry(archShape(.74, 1.24), 24), tunnelG = new THREE.BoxGeometry(1.02, 1.3, .8);
      const leafShape = new THREE.Shape(); leafShape.moveTo(0, 0); leafShape.bezierCurveTo(.5, .3, .62, 1.25, 0, 1.9); leafShape.bezierCurveTo(-.62, 1.25, -.5, .3, 0, 0);
      const leafG2 = new THREE.ExtrudeGeometry(leafShape, { depth: .05, bevelEnabled: true, bevelSize: .03, bevelThickness: .03, bevelSegments: 2, curveSegments: 20 });
      const ribG = new THREE.BoxGeometry(.035, 1.6, .02), GREY = 0x9d9599, LIGHT = 0xfff0a0;
      const onEll = (c, rx, ry, rz, x, y) => { const k = 1 - (x / rx) ** 2 - ((y - c.y) / ry) ** 2; const z = c.z + rz * Math.sqrt(Math.max(.02, k)), p = V3(x, y, z); const n = V3(x / rx / rx, (y - c.y) / ry / ry, (z - c.z) / rz / rz).normalize(); return [p, n]; };
      const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
      function makeHouse(x, z, i, name, special, rich) {
        const g = new THREE.Group(); g.position.set(x, 0, z); const sm = new THREE.MeshLambertMaterial({ map: SHELL[i % 3] }), dmM = new THREE.MeshLambertMaterial({ map: DOME[i % 3] });
        const C0 = V3(0, 1.62, 0), shell = mesh(shellG, sm, C0.x, C0.y, C0.z); shell.castShadow = shell.receiveShadow = true; g.add(shell);
        for (const [px, py, r] of [[-.4, 2.68, .2], [.4, 2.68, .2], [0, 2.25, .16]]) { const n = V3(px, py - C0.y, Math.sqrt(1.75 ** 2 - px * px - (py - C0.y) ** 2)).normalize(), p = C0.clone().addScaledVector(n, 1.7);
          const po = mesh(poreG, L(0x15111a), p.x, p.y, p.z); po.scale.set(r, r, r * .45); po.lookAt(p.clone().add(n)); g.add(po); }
        const DC = V3(0, 1.0, .74), RX = 1.4, RY = 1.4 * .92, RZ = 1.4 * .72; const dome = mesh(domeG, dmM, DC.x, DC.y, DC.z); dome.scale.set(1, .92, .72); dome.castShadow = dome.receiveShadow = true; g.add(dome);
        const tun = mesh(tunnelG, dmM, 0, .65, 1.38); g.add(tun);
        const fr = mesh(frameG, L(GREY), 0, 0, 1.66); fr.castShadow = true; g.add(fr); g.add(mesh(lightG, B(LIGHT), 0, 0, 1.79));
        const wn = V3(.95, 1.55 - C0.y, Math.sqrt(1.75 ** 2 - .95 ** 2 - (1.55 - C0.y) ** 2)).normalize(), wp = C0.clone().addScaledVector(wn, 1.76), wr = mesh(new THREE.TorusGeometry(.29, .07, 12, 32), L(GREY), wp.x, wp.y, wp.z); wr.lookAt(wp.clone().add(wn)); g.add(wr);
        const wl = mesh(new THREE.CircleGeometry(.25, 28), B(LIGHT), wp.x, wp.y, wp.z); wl.position.addScaledVector(wn, .01); wl.lookAt(wl.position.clone().add(wn)); g.add(wl);
        const fm = L(0x9a7462), nf = rich ? 70 : 22;
        for (let k = 0; k < nf; k++) { const u = hash(i * 31 + k, 1) * 2 - 1, v = hash(i * 31 + k, 2), th = u * 1.3, ph = .15 + v * 1.2; const onDome = hash(i * 31 + k, 3) > .55;
          let p, n; if (onDome) { [p, n] = onEll(DC, RX, RY, RZ, Math.sin(th) * 1.1, .35 + v * 1.1); } else { n = V3(Math.sin(th) * Math.cos(ph - .6), Math.sin(ph - .2) * .9 + .2, Math.cos(th) * Math.cos(ph - .6)).normalize(); p = C0.clone().addScaledVector(n, 1.755); }
          if (p.z < .2) continue; const f = mesh(fibG, fm, p.x, p.y, p.z); f.lookAt(p.clone().add(n)); f.rotateX(Math.PI / 2); f.rotateY(hash(k, 4) * 3); g.add(f); }
        const lm = L(0x2f6a4c), rm = L(0x4a8f66);
        for (const [rz, ry] of [[.95, .25], [-.85, -.2]]) { const pv = new THREE.Group(); pv.position.set(0, 3.25, -.1); pv.rotation.set(-.35, ry, rz); const lf = mesh(leafG2, lm, 0, 0, -.03); lf.castShadow = true; pv.add(lf); pv.add(mesh(ribG, rm, 0, .9, .06)); g.add(pv); }
        if (rich) { for (const sx of [-1, 1]) { const pot = mesh(new THREE.CylinderGeometry(.2, .15, .3, 16), L(0xc0603a), sx * .9, .15, 1.95); pot.castShadow = true; g.add(pot);
            for (let k = 0; k < 5; k++) { const fl = mesh(new THREE.SphereGeometry(.09, 10, 8), L([0xff5a8a, 0xffd23f, 0xffffff, 0xff8a3a, 0xe8467c][k]), sx * .9 + (hash(k, sx + 3) - .5) * .3, .4 + hash(k, 5) * .12, 1.95 + (hash(k, 7) - .5) * .25); g.add(fl); } }
          for (let k = 0; k < 4; k++) { const st = mesh(new THREE.CylinderGeometry(.28, .3, .06, 14), L(0xbdb6a6), (hash(k, 9) - .5) * .25, .03, 2.3 + k * .6); st.receiveShadow = true; g.add(st); }
          const mat = mesh(new THREE.BoxGeometry(.9, .03, .5), L(0xc65b4b), 0, .02, 1.95); g.add(mat);
          const lp = mesh(new THREE.CylinderGeometry(.05, .05, 1.6, 8), L(0x6b4426), -1.75, .8, 1.7); lp.castShadow = true; g.add(lp); g.add(mesh(new THREE.SphereGeometry(.17, 14, 10), B(0xffe08a), -1.75, 1.72, 1.7)); }
        const sh = mesh(new THREE.CircleGeometry(2.4, 28), shadowM, .2, .015, .3); sh.rotation.x = -Math.PI / 2; g.add(sh);
        if (name) { const sg = makeSign("@" + name, special); sg.position.set(2.05, 0, 1.75); sg.rotation.y = -.25; g.add(sg); g.userData.sign = sg; }
        S.add(g); return g; }
      const HOUSES = []; let ni = 0;
      for (const z of ROWS) for (let x = -25; x <= 25; x += 5) { if (z === 0 && (x === 0 || x === 5)) continue; HOUSES.push(makeHouse(x, z, HOUSES.length, NAMES[ni++ % NAMES.length])); }
      const MY = makeHouse(0, 0, 99, "dein.name", true, true), BF = makeHouse(5, 0, 98, "dein.bestie?", true, false);

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
      const ftex = (stops) => { const c = document.createElement("canvas"); c.width = 128; c.height = 256; const x = c.getContext("2d"); const g = x.createRadialGradient(64, 190, 4, 64, 150, 120);
        stops.forEach(([o, col]) => g.addColorStop(o, col)); x.fillStyle = g; x.beginPath(); x.moveTo(64, 4); x.bezierCurveTo(120, 90, 124, 200, 64, 252); x.bezierCurveTo(4, 200, 8, 90, 64, 4); x.fill(); return new THREE.CanvasTexture(c); };
      const FT = [ftex([[0, "rgba(255,240,180,1)"], [.35, "rgba(255,150,40,.95)"], [1, "rgba(220,40,10,0)"]]), ftex([[0, "rgba(255,255,230,1)"], [.5, "rgba(255,200,80,.9)"], [1, "rgba(255,120,20,0)"]])];
      const glowT = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"); const g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, "rgba(255,170,70,.9)"); g.addColorStop(1, "rgba(255,120,40,0)"); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); })();
      const addSp = (tex, sx, sy, x, y, z, op = 1) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, blending: THREE.NormalBlending, depthWrite: false, transparent: true, opacity: op })); sp.scale.set(sx, sy, 1); sp.position.set(x, y, z); S.add(sp); return sp; };
      const FL = []; for (let k = 0; k < 9; k++) { const big = k < 5, sp = addSp(FT[big ? 0 : 1], big ? 1.1 : .6, big ? 1.9 : 1.1, PZ.x + (hash(k, 30) - .5) * .7, big ? 1.0 : .75, PZ.z + (hash(k, 31) - .5) * .7); sp.userData = { k, big, bx: sp.position.x, bz: sp.position.z }; FL.push(sp); }
      const GLOW = addSp(glowT, 4.5, 4.5, PZ.x, .9, PZ.z, .3);
      const EMB = []; for (let k = 0; k < 26; k++) { const e = addSp(glowT, .12, .12, PZ.x, 1, PZ.z, 1); EMB.push(e); }
      for (const [a, tz] of [[.55, 0], [-.55, 0], [0, .55], [0, -.55]]) { const lg = mesh(new THREE.CylinderGeometry(.11, .14, 1.5, 10), L(0x4a2c18), PZ.x, .55, PZ.z); lg.rotation.set(tz, 0, a); lg.castShadow = true; S.add(lg); }
      { const ash = mesh(new THREE.CircleGeometry(.8, 20), B(0x1a1210), PZ.x, .025, PZ.z); ash.rotation.x = -Math.PI / 2; S.add(ash); }
      const fireL = new THREE.PointLight(0xffa04a, 3, 14, 1.5); fireL.position.set(PZ.x, 1.4, PZ.z); S.add(fireL);
      const BENCH = []; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + .26; const lg = mesh(new THREE.CylinderGeometry(.22, .22, 1.9, 10), L(0x6b4426), PZ.x + Math.cos(a) * 3.3, .22, PZ.z + Math.sin(a) * 3.3); lg.rotation.set(0, -a, Math.PI / 2); S.add(lg); BENCH.push(a); }
      for (let k = 0; k < 8; k++) { const a = k / 8 * TAU, x = PZ.x + Math.cos(a) * 8.2, z = PZ.z + Math.sin(a) * 8.2; S.add(mesh(new THREE.CylinderGeometry(.06, .06, 2.2, 6), L(0x8a6440), x, 1.1, z)); S.add(mesh(new THREE.SphereGeometry(.2, 10, 8), B(0xffd27a), x, 2.3, z)); }

      // ---------- Bewohner ----------
      const SHIRTS = [0xe8467c, 0xff6a1a, 0x18b8c0, 0x7b3fe0, 0xffd23f, 0x2e9e5b, 0x3fa0e8, 0xffffff], SKIN = [0xf1c7a0, 0xd9a07a, 0xa86a45, 0x7a4a2a], HAIR = [0x2a1b12, 0x5a3418, 0xe0b050, 0x111111];
      const PANTS = [0x2a2f4a, 0x3b5b8a, 0x6b4a2a, 0xe8e0d0, 0x2e9e5b, 0x1d1d24];
      const legG = new THREE.CapsuleGeometry(.085, .5, 4, 10), shoeG = new THREE.SphereGeometry(1, 12, 8), torsoG = new THREE.CapsuleGeometry(.2, .34, 6, 14), headG2 = new THREE.SphereGeometry(.19, 24, 18);
      const armG2 = new THREE.CapsuleGeometry(.055, .4, 4, 10), sleeveG = new THREE.CapsuleGeometry(.075, .16, 4, 10), handG = new THREE.SphereGeometry(.06, 12, 10), eyeG = new THREE.SphereGeometry(.022, 8, 6), hipG = new THREE.CylinderGeometry(.21, .2, .2, 16);
      const nameSprite = (txt) => { const c = document.createElement("canvas"); c.width = 512; c.height = 96; const x = c.getContext("2d"); let fs = 54; x.font = `800 ${fs}px Inter, Arial, sans-serif`;
        while (x.measureText(txt).width > 470 && fs > 24) { fs -= 2; x.font = `800 ${fs}px Inter, Arial, sans-serif`; } const w = x.measureText(txt).width + 40;
        x.fillStyle = "rgba(42,27,18,.85)"; x.beginPath(); x.roundRect(256 - w / 2, 8, w, 80, 40); x.fill(); x.fillStyle = "#fff"; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(txt, 256, 50);
        const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false })); s.scale.set(2.0, .375, 1); return s; };
      const bubble = (em) => { const c = document.createElement("canvas"); c.width = 160; c.height = 160; const x = c.getContext("2d"); x.fillStyle = "#fff"; x.beginPath(); x.arc(80, 72, 62, 0, TAU); x.fill();
        x.beginPath(); x.moveTo(60, 120); x.lineTo(50, 156); x.lineTo(92, 126); x.fill(); x.font = "72px 'Noto Color Emoji', sans-serif"; x.textAlign = "center"; x.textBaseline = "middle"; x.fillText(em, 80, 76);
        const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthWrite: false })); s.scale.set(.7, .7, 1); return s; };
      function makePerson(i, name, em) { const g = new THREE.Group(); const sh = SHIRTS[i % SHIRTS.length], sk = SKIN[Math.floor(hash(i, 9) * 4)], hr = HAIR[Math.floor(hash(i, 10) * 4)], pa = PANTS[Math.floor(hash(i, 14) * 6)];
        const skM = new THREE.MeshLambertMaterial({ color: sk }), shM = L(sh), paM = L(pa), cast = (m) => { m.castShadow = true; return m; };
        const legs = [-.11, .11].map((x) => { const p = new THREE.Group(); p.position.set(x, .9, 0); p.add(cast(mesh(legG, paM, 0, -.4, 0))); const sho = mesh(shoeG, L(0x222222), 0, -.84, .05); sho.scale.set(.09, .06, .14); p.add(sho); g.add(p); return p; });
        const up = new THREE.Group(); g.add(up); up.add(cast(mesh(hipG, paM, 0, .95, 0))); const tor = cast(mesh(torsoG, shM, 0, 1.3, 0)); tor.scale.set(1.12, 1, .78); up.add(tor);
        up.add(mesh(new THREE.CylinderGeometry(.06, .07, .1, 10), skM, 0, 1.62, 0)); const head = cast(mesh(headG2, skM, 0, 1.79, 0)); head.scale.set(1, 1.08, 1); up.add(head);
        for (const ex of [-.065, .065]) head.add(mesh(eyeG, B(0x1a1a1a), ex, .02, .175));
        const hs = Math.floor(hash(i, 15) * 3), hair = mesh(headG2, L(hr), 0, 1.86, -.025); hair.scale.set(1.06, .66, 1.06); up.add(hair);
        if (hs === 1) up.add(mesh(new THREE.SphereGeometry(.1, 12, 10), L(hr), 0, 1.9, -.2)); if (hs === 2) { const lh = mesh(new THREE.CapsuleGeometry(.17, .25, 4, 12), L(hr), 0, 1.68, -.08); lh.scale.set(1.15, 1, .7); up.add(lh); }
        const arms = [-.29, .29].map((x) => { const p = new THREE.Group(); p.position.set(x, 1.52, 0); p.add(mesh(sleeveG, shM, 0, -.08, 0)); p.add(cast(mesh(armG2, skM, 0, -.28, 0))); p.add(mesh(handG, skM, 0, -.53, 0)); up.add(p); return p; });
        let tag = null; if (name) { tag = nameSprite("@" + name); tag.position.set(0, 2.32, 0); up.add(tag); }
        let bub = null; if (em) { bub = bubble(em); bub.position.set(.5, 2.8, 0); up.add(bub); }
        g.userData = { legs, arms, up, head, tag, bub, i }; S.add(g); return g; }
      function pose(p, t, mode) { const u = p.userData, s = Math.sin(t * 7 + u.i);
        u.legs.forEach((l, j) => { l.rotation.x = mode === "walk" ? (j ? -s : s) * .5 : mode === "sit" ? -1.45 : 0; l.position.y = mode === "sit" ? .48 : .9; });
        u.arms.forEach((a, j) => { a.rotation.x = mode === "walk" ? (j ? s : -s) * .45 : mode === "sit" ? -.5 : 0; a.rotation.z = (j ? -1 : 1) * .06; });
        u.up.position.y = mode === "sit" ? -.42 : mode === "walk" ? Math.abs(s) * .04 : 0; u.head.rotation.y = 0;
        if (u.bub) u.bub.position.y = 2.8 + Math.sin(t * 3 + u.i) * .06;
        if (mode === "wave") { u.arms[1].rotation.z = -2.5 - Math.sin(t * 10 + u.i) * .35; u.arms[1].rotation.x = 0; }
        if (mode === "talk") { u.head.rotation.y = Math.sin(t * 2 + u.i) * .3; u.arms[0].rotation.x = -.8 + Math.sin(t * 4 + u.i) * .3; } }
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
      const T_HOUSE = line("L1")[1] + .35, T_SIGN = T_HOUSE + .45, T_BF = s04 + .3, T_HI = at("L5", "markier") - .25;
      const ease = (k) => k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, cl = (v) => Math.max(0, Math.min(1, v));
      const lerp = (a, b, k) => a + (b - a) * k, V = (x, y, z) => new THREE.Vector3(x, y, z);
      function camShot(t) {
        if (t < s02) { const k = ease(cl((t - T_HOUSE) / (s02 - T_HOUSE))), a = lerp(0, .38, k), r = lerp(12.5, 9.5, k);
          return [V(Math.sin(a) * r, lerp(2.9, 2.5, k), Math.cos(a) * r), V(0, lerp(1.7, 1.6, k), 0)]; }
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
        FL.forEach((f) => { const u = f.userData, n = Math.sin(t * 9 + u.k * 1.7) * .5 + Math.sin(t * 14.3 + u.k * 2.9) * .3; f.scale.set((u.big ? 1.1 : .6) * (1 + n * .15), (u.big ? 1.9 : 1.1) * (1 + n * .25), 1); f.position.x = u.bx + Math.sin(t * 6 + u.k) * .06; f.position.y = (u.big ? 1.0 : .75) + n * .1; f.material.rotation = Math.sin(t * 5 + u.k) * .12; });
        GLOW.material.opacity = .26 + Math.sin(t * 11) * .05; fireL.intensity = 2.6 + Math.sin(t * 13) * .5;
        EMB.forEach((e, k) => { const ph = (t * (.35 + hash(k, 40) * .4) + hash(k, 41)) % 1; e.position.set(PZ.x + (hash(k, 42) - .5) * .8 + Math.sin(t * 2 + k) * .3 * ph, .8 + ph * 4.5, PZ.z + (hash(k, 43) - .5) * .8); e.material.opacity = (1 - ph) * .95; e.scale.setScalar(.08 + (1 - ph) * .08); });
        // Spaziergänger
        WALK.forEach((p) => { const u = p.userData; let x = u.x0 + u.v * t; x = ((x + 32) % 64 + 64) % 64 - 32; p.position.set(x, .12, u.row + 3.9 + (u.v > 0 ? .45 : -.45)); p.rotation.y = u.v > 0 ? Math.PI / 2 : -Math.PI / 2; pose(p, t, "walk"); });
        SIT.forEach((p, k) => { p.lookAt(PZ.x, 0, PZ.z); pose(p, t, "sit"); if (k % 2) { p.userData.head.rotation.y = Math.sin(t * 2 + k) * .35; p.userData.arms[0].rotation.x = -1.1 + Math.sin(t * 4 + k) * .3; } });
        PW.forEach((p, k) => { const a = p.userData.ang + t * .22, r = 5.2; p.position.set(PZ.x + Math.cos(a) * r, 0, PZ.z + Math.sin(a) * r); p.rotation.y = -a; pose(p, t, k === 1 ? "wave" : "walk"); if (k === 1) { const u = p.userData; u.legs.forEach((l, j) => l.rotation.x = (j ? -1 : 1) * Math.sin(t * 7) * .5); } });
        // Nachbarn: laufen aufeinander zu und klatschen ab
        const vis = t >= s04 && t < s05; N1.visible = N2.visible = vis;
        if (vis) { const k = ease(cl((t - (s04 + .4)) / (T_HI - s04 - .4))); N1.position.set(lerp(-.3, 4.0, k), .12, 3.4); N2.position.set(lerp(9.3, 4.9, k), .12, 3.4);
          N1.rotation.y = Math.PI / 2; N2.rotation.y = -Math.PI / 2; pose(N1, t, k < 1 ? "walk" : "stand"); pose(N2, t, k < 1 ? "walk" : "stand");
          if (t >= T_HI) { const h = Math.min(1, (t - T_HI) / .15); N1.userData.arms[1].rotation.z = 0; N1.userData.arms[1].rotation.x = -2.6 * h; N2.userData.arms[0].rotation.x = -2.6 * h; } }
        foam.scale.setScalar(1 + Math.sin(t * 1.4) * .004);
        const [p, l] = camShot(t); cam.position.copy(p); cam.lookAt(l); R.render(S, cam); }
      const tl = gsap.timeline({ paused: true }), o = { t: 0 };
      tl.to(o, { t: C.__dur, duration: C.__dur, ease: "none", onUpdate: () => draw(o.t) }, 0);
      tl.to([cv, document.querySelector(".w-root")], { opacity: 0, duration: .6, ease: "power1.inOut" }, C.s05[0] + 1.2);
      draw(0);
      window.__timelines["world"] = tl;
"""

TPL = """<template>
  <style>
    #root { position: absolute; inset: 0; background: linear-gradient(180deg, #5fc4ee 0%, #9fdcf5 38%, #e8f7fb 52%, #bfe8f5 60%); }
    #w-cv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
  </style>
  <div id="root" class="w-root" data-composition-id="world" data-start="0" data-duration="__DUR__" data-width="1080" data-height="1920">
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
