      // TikTok-Kommentar: Herz füllt sich rot, Zahl zählt hoch, Herzen schnellen nach oben
      const HEART = '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2 4.5 5.6 4c2-.3 3.6.6 4.4 2 .8-1.4 2.4-2.3 4.4-2 3.6.5 5.2 4.4 3.6 7.7C19.5 16.4 12 21 12 21z" fill="none" stroke="#8a8b91" stroke-width="2"/></svg>';
      const HEART_R = '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2 4.5 5.6 4c2-.3 3.6.6 4.4 2 .8-1.4 2.4-2.3 4.4-2 3.6.5 5.2 4.4 3.6 7.7C19.5 16.4 12 21 12 21z" fill="#fe2c55"/></svg>';
      const fmtK = (n) => n >= 10000 ? (n / 1000).toFixed(1).replace(".", ",") + " Tsd." : Math.round(n).toLocaleString("de-DE");
      function tkLike(tl, id, t, from, to, dur = 1.4, seed = 1) {
        const box = document.querySelector(id + " .tk-l"), num = box.querySelector("i"), hz = box.querySelector(".hz");
        hz.innerHTML = HEART + '<span class="red" style="position:absolute;inset:0;opacity:0">' + HEART_R + "</span>";
        const R = rng(seed);
        for (let k = 0; k < 7; k++) { const f = document.createElement("div"); f.className = "tk-fh"; f.innerHTML = HEART_R; box.appendChild(f);
          const dx = (R() - .5) * 160, up = 200 + R() * 220, t0 = t + k * .11;
          tl.fromTo(f, { opacity: 0, x: 0, y: 0, scale: .5, rotation: 0 }, { opacity: 1, x: dx * .4, y: -60, scale: 1.1, rotation: (R() - .5) * 40, duration: .15, ease: "power2.out" }, t0);
          tl.to(f, { x: dx, y: -up, scale: .7, opacity: 0, duration: .7, ease: "power1.in" }, t0 + .15); }
        tl.fromTo(hz.querySelector(".red"), { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .25, ease: "back.out(3)" }, t);
        tl.fromTo(hz, { scale: 1 }, { scale: 1.3, duration: .12, yoyo: true, repeat: 1, ease: "power2.out" }, t);
        const o = { v: from }; num.textContent = fmtK(from);
        tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { num.textContent = fmtK(o.v); } }, t);
      }
      // Textbox füllt immer genau den Text: jede Zeile bekommt ihren eigenen Balken
      function wrapBt(scope) { document.querySelectorAll(scope + " .bt").forEach((el) => { if (!el.querySelector(":scope > .bx")) el.innerHTML = '<span class="bx">' + el.innerHTML + "</span>"; }); }
