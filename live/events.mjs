// Muschel-Tal LIVE – Überraschungs-Events (alle 5 Minuten) und Geschenk-Shows.
// Alle Events laufen komplett im Stream: mitmachen per Like oder Kommentar, niemand muss den Stream verlassen.
// Verlosungen sind nie an Geschenke gebunden (TikTok-Regeln).

import { normal } from './filter.mjs';
// Wort vergleichen, kleine Tippfehler erlaubt (ab 6 Buchstaben einer)
function wortGleich(text, wort) {
  const a = normal(text), b = normal(wort); if (!a) return false; if (a === b || a.includes(b)) return true;
  if (b.length < 6 || Math.abs(a.length - b.length) > 1) return false;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]); for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length] <= 1;
}
const zufall = a => a[Math.floor(Math.random() * a.length)];
const klemme = (x, a, b) => Math.max(a, Math.min(b, x));
// Wer ohne Team liked, kommt ins Team mit den wenigsten Mitgliedern
const kleinstes = (wahl, teams) => { const z = Object.fromEntries(teams.map(t => [t, 0])); Object.values(wahl).forEach(t => z[t]++); return teams.sort((a, b) => z[a] - z[b])[0]; };
// Einzahl/Mehrzahl: anz(1,'Fan bekommt','Fans bekommen') → „1 Fan bekommt“
const anz = (n, ein, mehr) => n === 1 ? `1 ${ein}` : `${n} ${mehr}`;
// Like-Ziel: ca. 80 % des normalen Like-Tempos über die Event-Dauer – schaffbar, wenn alle mitmachen
const likeZiel = (rate, sek, min) => klemme(Math.round(rate * sek / 60 * .8 / 10) * 10, min, 50000);
const zahl = n => Math.round(n).toLocaleString('de-DE');

export function macheEvents(api) {
  const { CFG } = api;
  const MIN = (CFG.events?.alleMinuten ?? 5) * 60000;
  let ev = null, ergebnis = null, naechstes = Date.now() + (api.test ? 25000 : MIN), verlauf = [];

  const DEFS = {
    sturmflut: {
      titel: 'Sturmflut!', icon: '🌊', dauer: 60,
      start(e) { e.ziel = likeZiel(api.likeRate(), 60, 100); e.stand = 0; e.dabei = new Set();
        return `Achtung, Sturmflut! Liked zusammen ${zahl(e.ziel)} mal in 60 Sekunden, damit der Deich hält!`; },
      like(e, p, n) { e.stand += n; e.dabei.add(p); if (e.stand >= e.ziel) e.frueh = true; },
      anzeige: e => ({ text: `Liked gemeinsam – der Deich muss halten!`, balken: [{ name: '🧱 Deich', wert: e.stand, max: e.ziel, farbe: '#3fa0e8' }] }),
      ende(e) {
        if (e.stand >= e.ziel) { e.dabei.forEach(p => api.belohne(p, 20)); return { text: `Der Deich hält! 🌈 Alle Helfer bekommen 20 🐚`, sag: `Geschafft! Der Deich hält! Alle Helfer bekommen 20 Muscheln.`, gut: true }; }
        return { text: `Die Flut war zu stark … nächstes Mal schaffen wir das!`, sag: `Oh nein, die Flut war zu stark. Nächstes Mal schaffen wir das!` };
      },
    },
    gluecksrad: {
      titel: 'Muschel-Glücksrad', icon: '🎡', dauer: 16, moeglich: () => api.aktive(10).length >= 2,
      start(e) {
        const kand = api.aktive(10); e.namen = kand.slice(0, 40).map(p => p.name);
        e.gewinner = zufall(kand); e.preis = zufall([{ t: '150 Muscheln', m: 150 }, { t: '300 Muscheln', m: 300 }, { t: 'ein goldenes Dach', farbe: '#E0B43A', m: 50 }, { t: 'einen Pool', anbau: 'pool', m: 150 }, { t: '500 Muscheln', m: 500 }]);
        return `Das Muschel-Glücksrad dreht sich! Alle, die gerade aktiv sind, sind im Lostopf.`;
      },
      anzeige: e => ({ text: 'Im Lostopf: alle, die in den letzten 10 Min. geliked oder kommentiert haben', rad: { namen: e.namen, gewinner: e.gewinner.name } }),
      ende(e) { api.belohne(e.gewinner, e.preis.m, e.preis); return { text: `${e.gewinner.name} gewinnt ${e.preis.t}! 🎉`, sag: `${api.name(e.gewinner)} gewinnt ${e.preis.t}! Glückwunsch!`, gut: true, id: e.gewinner.id }; },
    },
    krabbenrennen: {
      titel: 'Krabbenrennen', icon: '🦀', dauer: 60,
      start(e) { e.teams = { rot: 0, blau: 0, gelb: 0, gruen: 0 }; e.wahl = {}; e.ziel = likeZiel(api.likeRate() * .4, 60, 50);
        return `Krabbenrennen! Schreibt rot, blau, gelb oder grün für euer Team, oder liked einfach, dann bekommt ihr ein Team!`; },
      kommentar(e, p, t) { const m = { rot: 'rot', blau: 'blau', gelb: 'gelb', grün: 'gruen', gruen: 'gruen' }[t]; if (m) { e.wahl[p.id] = m; return true; } },
      like(e, p, n) { const tm = e.wahl[p.id] || (e.wahl[p.id] = kleinstes(e.wahl, Object.keys(e.teams))); e.teams[tm] += n; if (e.teams[tm] >= e.ziel) e.frueh = true; },
      anzeige: e => ({ text: 'Team wählen: rot · blau · gelb · grün – oder einfach liken!', rennen: Object.entries(e.teams).map(([k, v]) => ({ name: k, wert: v, max: e.ziel })) }),
      ende(e) {
        const [sieger, w] = Object.entries(e.teams).sort((a, b) => b[1] - a[1])[0];
        if (!w) return { text: 'Keine Krabbe ist losgelaufen …', sag: 'Die Krabben haben sich nicht bewegt. Nächstes Mal!' };
        const fans = Object.entries(e.wahl).filter(([, t]) => t === sieger).map(([id]) => api.spieler(id)); fans.forEach(p => api.belohne(p, 25));
        const nm = { rot: 'Rot', blau: 'Blau', gelb: 'Gelb', gruen: 'Grün' }[sieger];
        return { text: `Team ${nm} gewinnt! ${anz(fans.length, 'Fan bekommt', 'Fans bekommen')} 25 🐚`, sag: `Team ${nm} gewinnt das Krabbenrennen!`, gut: true };
      },
    },
    teamduell: {
      titel: 'Team-Duell', icon: '⚔️', dauer: 75,
      start(e) { e.t = { muschel: 0, kokos: 0 }; e.wahl = {}; return `Team-Duell! Schreibt muschel oder kokos und liked für euer Team!`; },
      kommentar(e, p, t) { if (t === 'muschel' || t === 'kokos') { e.wahl[p.id] = t; return true; } },
      like(e, p, n) { const tm = e.wahl[p.id] || (e.wahl[p.id] = kleinstes(e.wahl, ['muschel', 'kokos'])); e.t[tm] += n; },
      anzeige: e => { const m = Math.max(10, e.t.muschel + e.t.kokos); return { text: '„muschel“ oder „kokos“ schreiben – oder einfach liken!', balken: [{ name: '🐚 Team Muschel', wert: e.t.muschel, max: m, farbe: '#ff8fb8' }, { name: '🥥 Team Kokos', wert: e.t.kokos, max: m, farbe: '#b07a45' }] }; },
      ende(e) {
        if (e.t.muschel === e.t.kokos) return { text: 'Unentschieden!', sag: 'Unentschieden! Was für ein Duell.' };
        const s = e.t.muschel > e.t.kokos ? 'muschel' : 'kokos'; const fans = Object.entries(e.wahl).filter(([, t]) => t === s).map(([id]) => api.spieler(id)); fans.forEach(p => api.belohne(p, 30));
        return { text: `Team ${s === 'muschel' ? '🐚 Muschel' : '🥥 Kokos'} gewinnt! Jeder im Team bekommt 30 🐚`, sag: `Team ${s === 'muschel' ? 'Muschel' : 'Kokos'} gewinnt das Duell!`, gut: true };
      },
    },
    hausbesuch: {
      titel: 'Hausbesuch', icon: '🏠', dauer: 22, moeglich: () => api.aktive(15).length > 0,
      start(e) { e.p = zufall(api.aktive(15)); api.belohne(e.p, 25); api.sende({ typ: 'kamera', id: e.p.id, ms: 20000 });
        const st = CFG.stufen[e.p.stufe].name, an = e.p.anbauten.map(a => CFG.anbauten[a]?.name).filter(Boolean);
        return `Hausbesuch! Wir schauen bei ${api.name(e.p)} vorbei. ${api.artikel(st)}${an.length ? ' mit ' + an.join(' und ') : ''}. Schön hier! Dafür gibt's 25 Muscheln.`; },
      anzeige: e => ({ text: `Zu Besuch bei ${e.p.name} · +25 🐚` }),
      ende: e => ({ text: `Danke für den Besuch bei ${e.p.name}!` }),
    },
    muschelregen: {
      titel: 'Muschelregen', icon: '✨', dauer: 60, faktor: 2,
      start() { return 'Muschelregen! Eine Minute lang zählt jedes Like doppelt für euer Haus!'; },
      anzeige: () => ({ text: 'Jedes Like zählt doppelt für dein Haus!' }),
      ende: () => ({ text: 'Der Muschelregen ist vorbei.' }),
    },
    zahlenraten: {
      titel: 'Zahlenraten', icon: '🔢', dauer: 60,
      start(e) { e.zahl = 1 + Math.floor(Math.random() * 100); e.tipps = new Map(); return 'Zahlenraten! Ich denke an eine Zahl zwischen 1 und 100. Wer sie errät, gewinnt 100 Muscheln!'; },
      kommentar(e, p, t) { if (/^\d{1,3}$/.test(t)) { const z = +t; if (z < 1 || z > 100) return true; if (!e.tipps.has(p.id)) e.tipps.set(p.id, z); if (z === e.zahl && !e.treffer) { e.treffer = p; e.frueh = true; } else e.hinweis = z < e.zahl ? `${z} ist zu klein ⬆️` : `${z} ist zu groß ⬇️`; return true; } },
      anzeige: e => ({ text: `Zahl zwischen 1 und 100 schreiben!${e.hinweis ? '  ' + e.hinweis : ''}` }),
      ende(e) {
        if (e.treffer) { api.belohne(e.treffer, 100); return { text: `${e.treffer.name} hat die ${e.zahl} erraten! +100 🐚`, sag: `${api.name(e.treffer)} hat die ${e.zahl} erraten!`, gut: true, id: e.treffer.id }; }
        let best = null, d = 1e9; e.tipps.forEach((z, id) => { if (Math.abs(z - e.zahl) < d) { d = Math.abs(z - e.zahl); best = id; } });
        if (!best) return { text: `Die Zahl war ${e.zahl}.`, sag: `Die Zahl war ${e.zahl}.` };
        const p = api.spieler(best); api.belohne(p, 50); return { text: `Die Zahl war ${e.zahl} – am nächsten dran: ${p.name} (+50 🐚)`, sag: `Die Zahl war ${e.zahl}. Am nächsten dran war ${api.name(p)}!`, gut: true, id: p.id };
      },
    },
    strandparty: {
      titel: 'Strandparty', icon: '🎉', dauer: 60,
      start(e) { e.ziel = likeZiel(api.likeRate(), 60, 100); e.stand = 0; e.dabei = new Set(); return `Strandparty! Liked die Stimmung auf ${zahl(e.ziel)}, dann gibt's ein Feuerwerk!`; },
      like(e, p, n) { e.stand += n; e.dabei.add(p); if (e.stand >= e.ziel && !e.boom) { e.boom = true; api.sende({ typ: 'feuerwerk' }); api.sag('Die Party kocht! Feuerwerk!', 0); } },
      anzeige: e => ({ text: 'Liken = Stimmung! Bei vollem Balken: Feuerwerk', balken: [{ name: '🔊 Stimmung', wert: e.stand, max: e.ziel, farbe: '#ff6fa3' }], extra: { party: true } }),
      ende(e) { if (e.boom) { e.dabei.forEach(p => api.belohne(p, 15)); return { text: `Mega Party! Alle Feiernden bekommen 15 🐚`, sag: 'Was für eine Party! Alle Feiernden bekommen 15 Muscheln.', gut: true }; } return { text: 'Die Party war ein bisschen ruhig …', sag: 'Die Party war heute eher gemütlich.' }; },
    },
    moewenalarm: {
      titel: 'Möwenalarm!', icon: '🐦', dauer: 45,
      start(e) { e.faenger = []; return 'Möwenalarm! Eine Möwe klaut Muscheln vom Strand! Die ersten fünf, die fang schreiben, holen sie zurück!'; },
      kommentar(e, p, t) { if (/fang/.test(t) && !e.faenger.includes(p) && e.faenger.length < 5) { e.faenger.push(p); api.belohne(p, 20); if (e.faenger.length >= 5) e.frueh = true; return true; } },
      anzeige: e => ({ text: `Schreib „fang“! (${e.faenger.length}/5 gefangen)`, extra: { moewe: true } }),
      ende: e => ({ text: e.faenger.length ? `Gefangen von ${e.faenger.map(p => p.name).join(', ')}` : 'Die Möwe ist entkommen!', sag: e.faenger.length ? 'Die Muscheln sind zurück!' : 'Die Möwe ist entkommen!', gut: e.faenger.length > 0 }),
    },
    bauturbo: {
      titel: 'Bau-Turbo', icon: '⚡', dauer: 45, faktor: 3,
      start() { return 'Bau-Turbo! 45 Sekunden lang zählt jedes Like dreifach für euer Haus!'; },
      anzeige: () => ({ text: 'Jedes Like zählt dreifach für dein Haus!' }),
      ende: () => ({ text: 'Bau-Turbo vorbei – die Krabben machen Pause.' }),
    },
    sternschnuppe: {
      titel: 'Sternschnuppe', icon: '🌠', dauer: 40,
      start(e) { e.wuensche = new Set(); return 'Eine Sternschnuppe! Schreibt wunsch, und einer von euch bekommt einen Anbau geschenkt!'; },
      kommentar(e, p, t) { if (/wunsch/.test(t)) { e.wuensche.add(p); return true; } },
      anzeige: e => ({ text: `Schreib „wunsch“! (${e.wuensche.size} Wünsche)`, extra: { stern: true } }),
      ende(e) {
        if (!e.wuensche.size) return { text: 'Niemand hat sich etwas gewünscht …' };
        const p = zufall([...e.wuensche]), frei = Object.keys(CFG.anbauten).filter(a => !p.anbauten.includes(a));
        const a = frei.length ? zufall(frei) : null; api.belohne(p, 60, a ? { anbau: a, frei: true } : null);
        return { text: `${p.name}s Wunsch geht in Erfüllung: ${a ? CFG.anbauten[a].name : '60 Muscheln'}!`, sag: `Der Wunsch von ${api.name(p)} geht in Erfüllung!`, gut: true, id: p.id };
      },
    },
    // ======================= 15 weitere Events =======================
    wortjagd: {
      titel: 'Wortjagd', icon: '⌨️', dauer: 45,
      start(e) { e.wort = zufall(['KOKOSNUSS', 'SANDBURG', 'SEESTERN', 'PALMENSTRAND', 'MUSCHELKASSE', 'SONNENSCHIRM', 'LEUCHTTURM', 'FLIPFLOP', 'ANANAS', 'DELFIN']); e.sieger = [];
        return `Wortjagd! Die ersten drei, die ${e.wort.toLowerCase()} schreiben, gewinnen!`; },
      kommentar(e, p, t) { if (wortGleich(t, e.wort) && !e.sieger.includes(p) && e.sieger.length < 3) { e.sieger.push(p); api.belohne(p, [40, 25, 15][e.sieger.length - 1]); if (e.sieger.length >= 3) e.frueh = true; return true; } },
      anzeige: e => ({ text: `Schreib so schnell du kannst: ${e.wort}  (${e.sieger.length}/3)` }),
      ende: e => e.sieger.length ? { text: `Am schnellsten: ${e.sieger.map(p => p.name).join(', ')}`, sag: `Am schnellsten war ${api.name(e.sieger[0])}!`, gut: true, id: e.sieger[0].id } : { text: 'Niemand war schnell genug …', sag: 'Diesmal war niemand schnell genug.' },
    },
    cocktail: {
      titel: 'Cocktail-Mix', icon: '🍹', dauer: 60,
      start(e) { e.w = {}; return 'Cocktail-Mix! Welche Zutat kommt in den Insel-Cocktail? Schreibt mango, kokos oder ananas!'; },
      kommentar(e, p, t) { const m = ['mango', 'kokos', 'ananas'].find(x => t.includes(x)); if (m) { e.w[p.id] = m; return true; } },
      anzeige: e => { const z = { mango: 0, kokos: 0, ananas: 0 }; Object.values(e.w).forEach(x => z[x]++); const m = Math.max(1, ...Object.values(z)); return { text: 'Schreib: mango, kokos oder ananas', balken: [['🥭 Mango', 'mango', '#ffb02e'], ['🥥 Kokos', 'kokos', '#b07a45'], ['🍍 Ananas', 'ananas', '#ffd23f']].map(([n, k, f]) => ({ name: n, wert: z[k], max: m, farbe: f })) }; },
      ende(e) { const z = { mango: 0, kokos: 0, ananas: 0 }; Object.values(e.w).forEach(x => z[x]++); const s = Object.keys(z).sort((a, b) => z[b] - z[a])[0];
        if (!z[s]) return { text: 'Der Cocktail bleibt leer …' };
        const fans = Object.entries(e.w).filter(([, x]) => x === s).map(([id]) => api.spieler(id)); fans.forEach(p => api.belohne(p, 15));
        const n = { mango: 'Mango', kokos: 'Kokos', ananas: 'Ananas' }[s]; return { text: `Heute gibt's ${n}-Cocktail! ${anz(fans.length, 'Fan bekommt', 'Fans bekommen')} 15 🐚`, sag: `Der Insel-Cocktail wird mit ${n} gemixt! Prost!`, gut: true }; },
    },
    ballons: {
      titel: 'Ballon-Platzen', icon: '🎈', dauer: 60,
      start(e) { e.schritt = Math.max(5, Math.round(likeZiel(api.likeRate(), 60, 60) / 12)); e.stand = 0; e.geplatzt = 0; e.wer = {}; return 'Ballon-Platzen! Jedes Mal, wenn ihr genug liked, platzt ein Ballon. Wer ihn zum Platzen bringt, bekommt 10 Muscheln!'; },
      like(e, p, n) { e.stand += n; while (e.stand >= e.schritt && e.geplatzt < 12) { e.stand -= e.schritt; e.geplatzt++; e.wer[p.id] = (e.wer[p.id] || 0) + 1; api.belohne(p, 10); api.sende({ typ: 'ballonPlatzt', name: p.name }); } if (e.geplatzt >= 12) e.frueh = true; },
      anzeige: e => ({ text: `Liken lässt die Ballons platzen! ${e.geplatzt}/12 geplatzt`, balken: [{ name: '🎈 nächster Ballon', wert: e.stand, max: e.schritt, farbe: '#ff6fa3' }], extra: { ballons: 12 - e.geplatzt } }),
      ende: e => ({ text: `${e.geplatzt} Ballons geplatzt!`, sag: e.geplatzt >= 12 ? 'Alle Ballons sind geplatzt! Super!' : `${e.geplatzt} Ballons sind geplatzt.`, gut: e.geplatzt > 0 }),
    },
    blumen: {
      titel: 'Blumenwiese', icon: '🌺', dauer: 50,
      start(e) { e.p = new Set(); e.ziel = 25; return 'Wir pflanzen eine Blumenwiese! Jeder, der blume schreibt, pflanzt eine Blume. Bei 25 Blumen gibt es Muscheln für alle!'; },
      kommentar(e, p, t) { if (/blum/.test(t)) { e.p.add(p); return true; } },
      anzeige: e => ({ text: 'Schreib „blume“ und pflanze eine Blume!', balken: [{ name: '🌺 Blumen', wert: e.p.size, max: e.ziel, farbe: '#ff8fb8' }], extra: { blumen: e.p.size } }),
      ende(e) { if (e.p.size >= e.ziel) { e.p.forEach(p => api.belohne(p, 15)); return { text: `${e.p.size} Blumen! Alle Gärtner bekommen 15 🐚`, sag: 'Was für eine schöne Blumenwiese!', gut: true }; } e.p.forEach(p => api.belohne(p, 5, { trost: true })); return { text: `${e.p.size} Blumen gepflanzt · je 5 🐚`, sag: `${e.p.size} Blumen sind gewachsen.`, gut: e.p.size > 0 }; },
    },
    emojiraetsel: {
      titel: 'Emoji-Rätsel', icon: '🧩', dauer: 60,
      start(e) { const r = zufall([['🌴 + 🥥', 'kokospalme', 'Kokospalme'], ['🏖️ + 🏰', 'sandburg', 'Sandburg'], ['⭐ + 🌊', 'seestern', 'Seestern'], ['☀️ + 🧴', 'sonnencreme', 'Sonnencreme'], ['🍦 + 🚗', 'eiswagen', 'Eiswagen'], ['🐚 + 💰', 'muschelkasse', 'Muschelkasse'], ['🏄 + 🌊', 'surfen', 'Surfen'], ['💡 + 🗼', 'leuchtturm', 'Leuchtturm']]);
        e.bild = r[0]; e.loesung = r[1]; e.anzeigeLoesung = r[2]; return `Emoji-Rätsel! Welches Wort ist gemeint? Schreibt die Lösung in den Chat!`; },
      kommentar(e, p, t) { if (!e.sieger && wortGleich(t, e.loesung)) { e.sieger = p; e.frueh = true; api.belohne(p, 50); return true; } },
      anzeige: e => ({ text: `Was ist das?   ${e.bild}   → Lösung in den Chat schreiben!` }),
      ende: e => e.sieger ? { text: `${e.sieger.name} hat's: ${e.anzeigeLoesung}! +50 🐚`, sag: `Richtig! ${e.anzeigeLoesung}! ${api.name(e.sieger)} war am schnellsten.`, gut: true, id: e.sieger.id } : { text: `Die Lösung war: ${e.anzeigeLoesung}`, sag: `Die Lösung war ${e.anzeigeLoesung}.` },
    },
    volleyball: {
      titel: 'Beachvolleyball', icon: '🏐', dauer: 70,
      start(e) { e.t = { links: 0, rechts: 0 }; e.wahl = {}; return 'Beachvolleyball! Schreibt links oder rechts für euer Team, oder liked einfach los!'; },
      kommentar(e, p, t) { if (t.includes('links') || t.includes('rechts')) { e.wahl[p.id] = t.includes('links') ? 'links' : 'rechts'; return true; } },
      like(e, p, n) { const tm = e.wahl[p.id] || (e.wahl[p.id] = kleinstes(e.wahl, ['links', 'rechts'])); e.t[tm] += n; },
      anzeige: e => { const m = Math.max(10, e.t.links + e.t.rechts); return { text: '„links“ oder „rechts“ schreiben – oder einfach liken!', balken: [{ name: '⬅️ Team Links', wert: e.t.links, max: m, farbe: '#3fa0e8' }, { name: '➡️ Team Rechts', wert: e.t.rechts, max: m, farbe: '#ff8a2a' }] }; },
      ende(e) { if (e.t.links === e.t.rechts) return { text: 'Unentschieden – Satzball vertagt!', sag: 'Unentschieden!' }; const s = e.t.links > e.t.rechts ? 'links' : 'rechts'; const fans = Object.entries(e.wahl).filter(([, x]) => x === s).map(([id]) => api.spieler(id)); fans.forEach(p => api.belohne(p, 25)); return { text: `Team ${s === 'links' ? 'Links' : 'Rechts'} gewinnt! Je 25 🐚`, sag: `Punkt für Team ${s === 'links' ? 'Links' : 'Rechts'}!`, gut: true }; },
    },
    eiswagen: {
      titel: 'Eiswagen', icon: '🍦', dauer: 55,
      start(e) { e.ziel = likeZiel(api.likeRate(), 55, 90); e.stand = 0; e.dabei = new Set(); return `Hitzewelle! Der Eiswagen kommt, wenn ihr ${zahl(e.ziel)} mal liked. Dann gibt's Eis für alle!`; },
      like(e, p, n) { e.stand += n; e.dabei.add(p); if (e.stand >= e.ziel) e.frueh = true; },
      anzeige: e => ({ text: 'Liken holt den Eiswagen!', balken: [{ name: '🍦 Eiswagen', wert: e.stand, max: e.ziel, farbe: '#ffb3d1' }] }),
      ende(e) { if (e.stand >= e.ziel) { e.dabei.forEach(p => api.belohne(p, 15)); return { text: 'Eis für alle! 15 🐚 für jeden, der geliked hat', sag: 'Der Eiswagen ist da! Eis für alle!', gut: true }; } return { text: 'Der Eiswagen ist woanders hingefahren …', sag: 'Schade, der Eiswagen ist weitergefahren.' }; },
    },
    glueckszahl: {
      titel: 'Glückszahl', icon: '🍀', dauer: 45,
      start(e) { e.zahl = 1 + Math.floor(Math.random() * 10); e.tipps = {}; return 'Glückszahl! Schreibt eine Zahl von eins bis zehn. Alle mit der richtigen Zahl gewinnen!'; },
      kommentar(e, p, t) { if (/^(10|[1-9])$/.test(t)) { e.tipps[p.id] = +t; return true; } },
      anzeige: e => ({ text: `Schreib eine Zahl von 1 bis 10!  (${Object.keys(e.tipps).length} Tipps)` }),
      ende(e) { const ok = Object.entries(e.tipps).filter(([, z]) => z === e.zahl).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 30)); return { text: `Die Glückszahl war ${e.zahl}! ${anz(ok.length, 'Gewinner bekommt', 'Gewinner bekommen')} 30 🐚`, sag: `Die Glückszahl war die ${e.zahl}!`, gut: ok.length > 0 }; },
    },
    strandquiz: {
      titel: 'Strand-Quiz', icon: '❓', dauer: 50,
      start(e) { e.f = zufall([['Wie viele Arme hat ein Seestern meistens?', ['3', '5', '8'], 1], ['Was ist kein Meerestier?', ['Delfin', 'Qualle', 'Kamel'], 2], ['Woraus besteht eine Sandburg?', ['Sand', 'Schnee', 'Holz'], 0], ['Welche Frucht hat eine harte, haarige Schale?', ['Kokosnuss', 'Banane', 'Erdbeere'], 0], ['Was zeigt einem Schiff nachts den Weg?', ['Leuchtturm', 'Sandburg', 'Liegestuhl'], 0], ['Welches Tier hat Scheren?', ['Krabbe', 'Möwe', 'Delfin'], 0], ['Was braucht man zum Surfen?', ['Brett', 'Schlitten', 'Ski'], 0], ['Welches Meer ist salzig?', ['Jedes', 'Keins', 'Nur die Ostsee'], 0]]);
        e.a = {}; return `Strand-Quiz! ${e.f[0]} Schreibt A, B oder C!`; },
      kommentar(e, p, t) { const i = 'abc'.indexOf(t); if (t.length === 1 && i >= 0) { e.a[p.id] = i; return true; } },
      anzeige: e => { const z = [0, 0, 0]; Object.values(e.a).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: e.f[0] + '  Schreib A, B oder C!', balken: e.f[1].map((o, i) => ({ name: 'ABC'[i] + '  ' + o, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8'][i] })) }; },
      ende(e) { const ok = Object.entries(e.a).filter(([, i]) => i === e.f[2]).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 20)); return { text: `Richtig: ${'ABC'[e.f[2]]} – ${e.f[1][e.f[2]]}! ${anz(ok.length, 'richtige Antwort', 'richtige Antworten')} (+20 🐚)`, sag: `Richtig ist ${'ABC'[e.f[2]]}, ${e.f[1][e.f[2]]}!`, gut: ok.length > 0 }; },
    },
    surfcontest: {
      titel: 'Surf-Contest', icon: '🏄', dauer: 60,
      start(e) { e.punkte = {}; return 'Surf-Contest! Schreibt surf, um mitzumachen. Danach bringt jedes Like Punkte. Wer die meisten hat, gewinnt!'; },
      kommentar(e, p, t) { if (/surf/.test(t)) { if (!(p.id in e.punkte)) e.punkte[p.id] = 0; return true; } },
      like(e, p, n) { if (p.id in e.punkte) e.punkte[p.id] += n; },
      anzeige: e => { const top = Object.entries(e.punkte).sort((a, b) => b[1] - a[1]).slice(0, 3); const m = Math.max(1, ...top.map(x => x[1])); return { text: `„surf“ schreiben, dann liken! (${Object.keys(e.punkte).length} Surfer)`, balken: top.map(([id, v], i) => ({ name: '🏄 ' + api.spieler(id).name, wert: v, max: m, farbe: ['#3fa0e8', '#7fe0c8', '#b58ad0'][i] })) }; },
      ende(e) { const top = Object.entries(e.punkte).sort((a, b) => b[1] - a[1]); if (!top.length || !top[0][1]) return { text: 'Keine Welle erwischt …', sag: 'Heute keine Welle erwischt.' }; const p = api.spieler(top[0][0]); api.belohne(p, 60); return { text: `${p.name} ist Surf-Champion! +60 🐚`, sag: `${api.name(p)} reitet die größte Welle!`, gut: true, id: p.id }; },
    },
    kokoswurf: {
      titel: 'Kokosnuss-Weitwurf', icon: '🥥', dauer: 45,
      start(e) { e.w = {}; return 'Kokosnuss-Weitwurf! Schreibt wurf, und eure Kokosnuss fliegt. Der weiteste Wurf gewinnt!'; },
      kommentar(e, p, t) { if (/wurf|wirf/.test(t) && !(p.id in e.w)) { e.w[p.id] = Math.round(5 + Math.random() * 45); return true; } },
      anzeige: e => { const top = Object.entries(e.w).sort((a, b) => b[1] - a[1]).slice(0, 3); return { text: `Schreib „wurf“! (${Object.keys(e.w).length} Würfe)`, balken: top.map(([id, v], i) => ({ name: `🥥 ${api.spieler(id).name}`, wert: v, max: 50, farbe: ['#ffd23f', '#c9d1d9', '#d9a66a'][i] })) }; },
      ende(e) { const top = Object.entries(e.w).sort((a, b) => b[1] - a[1]); if (!top.length) return { text: 'Keine Kokosnuss geflogen …' }; const p = api.spieler(top[0][0]); api.belohne(p, 40); Object.keys(e.w).forEach(id => id !== p.id && api.belohne(api.spieler(id), 5, { trost: true })); return { text: `${p.name} wirft ${top[0][1]} Meter! +40 🐚`, sag: `${top[0][1]} Meter! ${api.name(p)} gewinnt den Weitwurf!`, gut: true, id: p.id }; },
    },
    inselfoto: {
      titel: 'Inselfoto', icon: '📸', dauer: 40,
      start(e) { e.f = []; return 'Gruppenfoto! Wer aufs Inselfoto will, schreibt cheese!'; },
      kommentar(e, p, t) { if (/chee|chis|käse|kaese/.test(t) && !e.f.includes(p)) { e.f.push(p); api.belohne(p, 8); return true; } },
      anzeige: e => ({ text: `Schreib „cheese“ für das Gruppenfoto! (${e.f.length} auf dem Foto)` }),
      ende: e => e.f.length ? { text: `📸 ${e.f.slice(0, 8).map(p => p.name).join(', ')}${e.f.length > 8 ? ` und ${e.f.length - 8} weitere` : ''}`, sag: `Klick! ${e.f.length} von euch sind auf dem Inselfoto!`, gut: true } : { text: 'Niemand wollte aufs Foto …' },
    },
    // ======================= 10 weitere Events (40 insgesamt) =======================
    tauziehen: {
      titel: 'Tauziehen', icon: '🪢', dauer: 60,
      start(e) { e.t = { muschel: 0, seestern: 0 }; e.wahl = {}; return 'Tauziehen! Team Muschel gegen Team Seestern! Schreibt muschel oder seestern, oder liked einfach, dann zieht ihr mit!'; },
      kommentar(e, p, t) { const m = t.includes('seestern') ? 'seestern' : t.includes('muschel') ? 'muschel' : null; if (m) { e.wahl[p.id] = m; return true; } },
      like(e, p, n) { const tm = e.wahl[p.id] || (e.wahl[p.id] = kleinstes(e.wahl, ['muschel', 'seestern'])); e.t[tm] += n; },
      anzeige: e => { const sum = Math.max(1, e.t.muschel + e.t.seestern); return { text: '„muschel“ oder „seestern“ schreiben – oder einfach liken!', seil: (e.t.muschel - e.t.seestern) / sum, balken: [{ name: '🐚 Team Muschel', wert: e.t.muschel, max: sum, farbe: '#ff8fb8' }, { name: '⭐ Team Seestern', wert: e.t.seestern, max: sum, farbe: '#ff8a2a' }] }; },
      ende(e) { if (e.t.muschel === e.t.seestern) return { text: 'Unentschieden – das Seil hält!', sag: 'Unentschieden!' }; const s = e.t.muschel > e.t.seestern ? 'muschel' : 'seestern'; Object.entries(e.wahl).filter(([, x]) => x === s).forEach(([id]) => api.belohne(api.spieler(id), 25)); return { text: `Team ${s === 'muschel' ? 'Muschel' : 'Seestern'} zieht am stärksten! Je 25 🐚`, sag: `Team ${s === 'muschel' ? 'Muschel' : 'Seestern'} gewinnt das Tauziehen!`, gut: true }; },
    },
    buchstabensalat: {
      titel: 'Buchstabensalat', icon: '🔤', dauer: 60,
      start(e) { e.wort = zufall(['STRAND', 'MUSCHEL', 'PALME', 'WELLE', 'INSEL', 'SONNE', 'KRABBE', 'HAFEN', 'MOEWE', 'LAGUNE', 'KORALLE', 'BOOT']); let m; do { m = e.wort.split('').sort(() => Math.random() - .5).join(''); } while (m === e.wort); e.salat = m;
        return 'Buchstabensalat! Die Buchstaben sind durcheinander. Wer zuerst das richtige Wort schreibt, gewinnt!'; },
      kommentar(e, p, t) { if (!e.sieger && wortGleich(t, e.wort)) { e.sieger = p; e.frueh = true; api.belohne(p, 50); return true; } },
      anzeige: e => ({ text: `Welches Wort ist das?   ${e.salat.split('').join(' ')}   → in den Chat schreiben!` }),
      ende: e => e.sieger ? { text: `${e.sieger.name} hat's: ${e.wort}! +50 🐚`, sag: `Richtig! ${e.wort.toLowerCase()}!`, gut: true, id: e.sieger.id } : { text: `Das Wort war: ${e.wort}`, sag: `Das Wort war ${e.wort.toLowerCase()}.` },
    },
    wuerfeln: {
      titel: 'Muschel-Würfeln', icon: '🎲', dauer: 45,
      start(e) { e.w = {}; return 'Muschel-Würfeln! Schreibt würfel, und ihr würfelt einmal. Wer eine Sechs würfelt, gewinnt!'; },
      kommentar(e, p, t) { if (/w(ue|ü|u)rf/.test(t) && !(p.id in e.w)) { e.w[p.id] = 1 + Math.floor(Math.random() * 6); return true; } },
      anzeige: e => { const z = [0, 0, 0, 0, 0, 0]; Object.values(e.w).forEach(v => z[v - 1]++); const m = Math.max(1, ...z); return { text: `Schreib „würfel“! (${Object.keys(e.w).length} gewürfelt)`, balken: [{ name: '🎲 Sechsen', wert: z[5], max: Math.max(1, Object.keys(e.w).length), farbe: '#ffd23f' }] }; },
      ende(e) { const ok = Object.entries(e.w).filter(([, v]) => v === 6).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 30)); Object.entries(e.w).filter(([, v]) => v !== 6).forEach(([id]) => api.belohne(api.spieler(id), 3, { trost: true })); return { text: ok.length ? `${anz(ok.length, 'Sechs', 'Sechsen')} gewürfelt! Je 30 🐚` : 'Keine Sechs dabei … Trostpreis: 3 🐚', sag: ok.length ? 'Sechs! Glückwunsch!' : 'Keine Sechs dabei. Alle bekommen einen kleinen Trostpreis.', gut: Object.keys(e.w).length > 0 }; },
    },
    papagei: {
      titel: 'Papagei', icon: '🦜', dauer: 45,
      start(e) { e.satz = zufall(['ALOHA MUSCHELTAL', 'ICH LIEBE DIE INSEL', 'KOKOS FÜR ALLE', 'SONNE SAND UND MEER', 'HALLO KRABBE']); e.sieger = []; return 'Der Papagei will etwas hören! Die ersten fünf, die seinen Satz nachsprechen, gewinnen!'; },
      kommentar(e, p, t) { if (normal(t).includes(normal(e.satz)) && !e.sieger.includes(p) && e.sieger.length < 5) { e.sieger.push(p); api.belohne(p, 20); if (e.sieger.length >= 5) e.frueh = true; return true; } },
      anzeige: e => ({ text: `Schreib nach: „${e.satz.toLowerCase()}“  (${e.sieger.length}/5)` }),
      ende: e => e.sieger.length ? { text: `Der Papagei ist glücklich! ${e.sieger.map(p => p.name).join(', ')}`, sag: 'Der Papagei ist glücklich!', gut: true } : { text: 'Der Papagei ist beleidigt weggeflogen …' },
    },
    regenbogen: {
      titel: 'Regenbogen malen', icon: '🌈', dauer: 60,
      start(e) { e.f = {}; return 'Wir malen einen Regenbogen! Schreibt die Farben rot, orange, gelb, grün, blau und lila. Sind alle sechs da, bekommen alle Maler Muscheln!'; },
      kommentar(e, p, t) { const f = ['rot', 'orange', 'gelb', 'grün', 'gruen', 'blau', 'lila'].find(x => t.includes(x)); if (f) { const k = f === 'gruen' ? 'grün' : f; (e.f[k] ||= new Set()).add(p); if (Object.keys(e.f).length >= 6) e.frueh = true; return true; } },
      anzeige: e => ({ text: 'Schreib eine Farbe: rot · orange · gelb · grün · blau · lila', regenbogen: ['rot', 'orange', 'gelb', 'grün', 'blau', 'lila'].map(f => !!e.f[f]) }),
      ende(e) { const maler = new Set(); Object.values(e.f).forEach(s => s.forEach(p => maler.add(p))); const voll = Object.keys(e.f).length >= 6; maler.forEach(p => api.belohne(p, voll ? 20 : 5, voll ? null : { trost: true })); return { text: voll ? `Der Regenbogen ist komplett! ${maler.size} Maler bekommen 20 🐚` : `${Object.keys(e.f).length} von 6 Farben … je 5 🐚`, sag: voll ? 'Was für ein Regenbogen!' : 'Fast! Ein paar Farben haben gefehlt.', gut: maler.size > 0 }; },
    },
    likerekord: {
      titel: 'Like-Rekord', icon: '🏆', dauer: 30,
      start(e) { e.stand = 0; e.dabei = new Set(); e.rekord = api.rekord(); return `Like-Rekord! Schafft ihr in dreißig Sekunden mehr als ${zahl(e.rekord)} Likes? Los!`; },
      like(e, p, n) { e.stand += n; e.dabei.add(p); },
      anzeige: e => ({ text: `30 Sekunden: Rekord brechen!`, balken: [{ name: '🏆 Rekord', wert: e.stand, max: Math.max(e.rekord, 1), farbe: '#ffd23f' }] }),
      ende(e) { if (e.stand > e.rekord) { api.rekord(e.stand); e.dabei.forEach(p => api.belohne(p, 25)); return { text: `Neuer Rekord: ${zahl(e.stand)} Likes! Je 25 🐚`, sag: `Neuer Rekord! ${zahl(e.stand)} Likes!`, gut: true }; } e.dabei.forEach(p => api.belohne(p, 5, { trost: true })); return { text: `${zahl(e.stand)} Likes – der Rekord bleibt bei ${zahl(e.rekord)}`, sag: 'Knapp! Der Rekord hält noch.' }; },
    },
    motto: {
      titel: 'Motto des Tages', icon: '🎭', dauer: 60,
      start(e) { e.wahl = zufall([['Piratentag', 'Hawaii-Party', 'Muschel-Tag'], ['Strandgala', 'Surfertag', 'Tropennacht'], ['Insel-Disko', 'Picknicktag', 'Sandburgen-Tag']]); e.st = {}; return `Motto des Tages! Schreibt 1 für ${e.wahl[0]}, 2 für ${e.wahl[1]} oder 3 für ${e.wahl[2]}!`; },
      kommentar(e, p, t) { if (/^[123]$/.test(t)) { e.st[p.id] = +t - 1; return true; } },
      anzeige: e => { const z = [0, 0, 0]; Object.values(e.st).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: 'Welches Motto? Schreib 1, 2 oder 3', balken: e.wahl.map((w, i) => ({ name: `${i + 1}  ${w}`, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8'][i] })) }; },
      ende(e) { const z = [0, 0, 0]; Object.values(e.st).forEach(i => z[i]++); const m = z.indexOf(Math.max(...z)); if (!z[m]) return { text: 'Kein Motto heute …' }; Object.entries(e.st).filter(([, i]) => i === m).forEach(([id]) => api.belohne(api.spieler(id), 10)); return { text: `Heute ist ${e.wahl[m]}! Je 10 🐚 für alle, die es gewählt haben`, sag: `Das Motto heute: ${e.wahl[m]}!`, gut: true }; },
    },
    mysterybox: {
      titel: 'Mystery-Box', icon: '🎁', dauer: 40,
      start(e) { e.b = {}; return 'Mystery-Box! Schreibt box, und jeder bekommt eine Überraschung, zwischen einer und fünfzig Muscheln!'; },
      kommentar(e, p, t) { if (/box/.test(t) && !(p.id in e.b)) { const r = Math.random(); e.b[p.id] = r < .05 ? 50 : r < .25 ? 20 : r < .6 ? 10 : 3; api.belohne(p, e.b[p.id]); return true; } },
      anzeige: e => ({ text: `Schreib „box“ für eine Überraschung! (${Object.keys(e.b).length} Boxen offen)` }),
      ende(e) { const top = Object.entries(e.b).sort((a, b) => b[1] - a[1])[0]; if (!top) return { text: 'Keine Box wurde geöffnet …' }; const p = api.spieler(top[0]); return { text: `${Object.keys(e.b).length} Boxen geöffnet – den Hauptgewinn (${top[1]} 🐚) hat ${p.name}!`, sag: `Den größten Gewinn hat ${api.name(p)}!`, gut: true, id: p.id }; },
    },
    werbinich: {
      titel: 'Wer bin ich?', icon: '🕵️', dauer: 60,
      start(e) { e.r = zufall([['krabbe', 'Krabbe', ['Ich laufe seitwärts.', 'Ich habe Scheren.', 'Auf der Insel helfe ich beim Bauen!']], ['moewe', 'Möwe', ['Ich kann fliegen.', 'Ich klaue gern Pommes.', 'Ich kreische am Strand.']], ['seestern', 'Seestern', ['Ich wohne im Meer.', 'Ich habe meistens fünf Arme.', 'Ich sehe aus wie ein Stern.']], ['delfin', 'Delfin', ['Ich schwimme sehr schnell.', 'Ich springe gern aus dem Wasser.', 'Ich bin sehr schlau und pfeife.']], ['schildkroete', 'Schildkröte', ['Ich trage mein Haus auf dem Rücken.', 'Ich lege Eier in den Sand.', 'Ich bin langsam an Land.']]]);
        e.t0 = Date.now(); return `Wer bin ich? Ich gebe euch drei Hinweise. Erster Hinweis: ${e.r[2][0]}`; },
      kommentar(e, p, t) { if (!e.sieger && (normal(t).includes(normal(e.r[0])) || wortGleich(t, e.r[1]))) { e.sieger = p; e.frueh = true; api.belohne(p, 50); return true; } },
      anzeige: e => { const n = Math.min(3, 1 + Math.floor((Date.now() - e.t0) / 20000)); return { text: `Hinweis: ${e.r[2].slice(0, n).join('  ·  ')}  → Antwort in den Chat!` }; },
      ende: e => e.sieger ? { text: `${e.sieger.name} hat's erraten: ${e.r[1]}! +50 🐚`, sag: `Richtig, ich bin ${e.r[1] === 'Delfin' || e.r[1] === 'Seestern' ? 'ein' : 'eine'} ${e.r[1]}!`, gut: true, id: e.sieger.id } : { text: `Gesucht war: ${e.r[1]}`, sag: `Ich war ${e.r[1] === 'Delfin' || e.r[1] === 'Seestern' ? 'ein' : 'eine'} ${e.r[1]}!` },
    },
    hausparty: {
      titel: 'Hausparty!', icon: '🎉', dauer: 45, moeglich: () => api.aktive(15).length > 0,
      start(e) { e.p = zufall(api.aktive(15)); e.g = new Set(); api.sende({ typ: 'kamera', id: e.p.id, ms: 40000 });
        return `Hausparty bei ${api.name(e.p)}! Schreibt party, dann seid ihr eingeladen!`; },
      kommentar(e, p, t) { if (/part/.test(t) && p !== e.p && !e.g.has(p.id)) { e.g.add(p.id); api.belohne(p, 10); return true; } },
      anzeige: e => ({ text: `Party bei ${e.p.name}! Schreib „party“ (${e.g.size} Gäste)` }),
      ende(e) { const n = e.g.size; if (n) api.belohne(e.p, Math.min(100, n * 5)); return { text: n ? `${anz(n, 'Gast', 'Gäste')} gefeiert! ${e.p.name} bekommt ${Math.min(100, n * 5)} 🐚` : 'Keiner kam zur Party …', sag: n ? `Was für eine Party bei ${api.name(e.p)}!` : 'Schade, keiner kam zur Party.', gut: n > 0, id: e.p.id }; },
    },
    leuchtturm: {
      titel: 'Leuchtturm anzünden', icon: '🗼', dauer: 60,
      start(e) { e.ziel = likeZiel(api.likeRate(), 60, 100); e.stand = 0; e.dabei = new Set();
        return `Es wird dunkel auf dem Meer! Liked zusammen ${zahl(e.ziel)} mal, damit der Leuchtturm leuchtet!`; },
      like(e, p, n) { e.stand += n; e.dabei.add(p); if (e.stand >= e.ziel) e.frueh = true; },
      anzeige: e => ({ text: 'Liked gemeinsam – der Leuchtturm braucht Strom!', balken: [{ name: '💡 Licht', wert: e.stand, max: e.ziel, farbe: '#ffd23f' }] }),
      ende(e) { if (e.stand >= e.ziel) { e.dabei.forEach(p => api.belohne(p, 20)); return { text: 'Der Leuchtturm leuchtet! 💡 Alle Helfer bekommen 20 🐚', sag: 'Der Leuchtturm leuchtet! Alle Helfer bekommen zwanzig Muscheln.', gut: true }; }
        return { text: 'Noch zu dunkel … nächstes Mal!', sag: 'Fast! Nächstes Mal leuchtet er.' }; },
    },
    nachbarhilfe: {
      titel: 'Nachbarschaftshilfe', icon: '🤝', dauer: 50, moeglich: () => api.aktive(15).length > 1,
      start(e) { const a = api.aktive(15); e.p = a.reduce((m, x) => x.stufe < m.stufe ? x : m, a[0]); e.h = {}; e.summe = 0; api.sende({ typ: 'kamera', id: e.p.id, ms: 45000 });
        return `Nachbarschaftshilfe! ${api.name(e.p)} hat noch ein kleines Haus. Jedes Like von euch baut jetzt auch bei ${api.name(e.p)} mit!`; },
      like(e, p, n) { if (p === e.p || e.summe >= 300) return; const m = Math.min(n, 300 - e.summe); e.summe += m; e.h[p.id] = (e.h[p.id] || 0) + m; api.belohne(e.p, m, { trost: true }); },
      anzeige: e => ({ text: `Liken hilft ${e.p.name} beim Bauen!`, balken: [{ name: '🔨 Hilfe', wert: e.summe, max: 300, farbe: '#7fe0c8' }] }),
      ende(e) { const t = Object.entries(e.h).sort((a, b) => b[1] - a[1])[0]; if (!t) return { text: `${e.p.name} baut allein weiter …` }; const h = api.spieler(t[0]); api.belohne(h, 30);
        return { text: `${e.summe} Muscheln für ${e.p.name}! Fleißigster Helfer: ${h.name} (+30 🐚)`, sag: `Danke! Am meisten geholfen hat ${api.name(h)}.`, gut: true, id: e.p.id }; },
    },
    inselgruss: {
      titel: 'Inselgruß', icon: '👋', dauer: 40,
      start(e) { e.g = new Set(); return 'Inselgruß! Schreibt moin oder hallo – jeder Gruß bringt zehn Muscheln!'; },
      kommentar(e, p, t) { if (/^(moin|hallo|hi|hey|servus|hallöchen|ahoi)\b/.test(t) && !e.g.has(p.id)) { e.g.add(p.id); api.belohne(p, 10); return true; } },
      anzeige: e => ({ text: `Schreib „moin“ oder „hallo“! (${e.g.size} Grüße)` }),
      ende(e) { const n = e.g.size; return { gut: n > 0, text: n ? `${anz(n, 'Gruß', 'Grüße')} – je 10 🐚` : 'Heute grüßt keiner …', sag: n ? `Moin zurück an alle ${n === 1 ? '' : n + ' '}!`.replace(' !', '!') : 'Na gut, dann eben später!' }; },
    },
    schatzkiste: {
      titel: 'Schatzkiste', icon: '🧰', dauer: 45,
      start(e) { e.los = Math.floor(Math.random() * 3); e.w = {}; return 'Drei Schatzkisten! Nur in einer liegt Gold. Schreibt 1, 2 oder 3!'; },
      kommentar(e, p, t) { if (/^[123]$/.test(t)) { e.w[p.id] = +t - 1; return true; } },
      anzeige: e => { const z = [0, 0, 0]; Object.values(e.w).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: 'Welche Kiste? Schreib 1, 2 oder 3', balken: [0, 1, 2].map(i => ({ name: `🧰 Kiste ${i + 1}`, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8'][i] })) }; },
      ende(e) { const ok = Object.entries(e.w).filter(([, i]) => i === e.los).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 30));
        return { text: `Das Gold lag in Kiste ${e.los + 1}! ${ok.length ? anz(ok.length, 'Gewinner', 'Gewinner') + ' (+30 🐚)' : 'Diesmal hat keiner richtig getippt.'}`, sag: `Das Gold lag in Kiste ${e.los + 1}!`, gut: ok.length > 0 }; },
    },
    wahrfalsch: {
      titel: 'Wahr oder falsch?', icon: '🤔', dauer: 45,
      start(e) { e.f = zufall([['Seesterne haben kein Gehirn.', true], ['Möwen können nicht schwimmen.', false], ['Kokosnüsse können übers Meer schwimmen.', true], ['Delfine schlafen mit einem offenen Auge.', true], ['Krabben laufen am liebsten rückwärts.', false], ['Das Meer ist salzig, weil Fische weinen.', false], ['Schildkröten gibt es schon seit den Dinosauriern.', true], ['Sand wird im Sommer nie heiß.', false]]);
        e.a = {}; return `Wahr oder falsch? ${e.f[0]} Schreibt wahr oder falsch!`; },
      kommentar(e, p, t) { if (/^(wahr|stimmt|ja)\b/.test(t)) { e.a[p.id] = true; return true; } if (/^(falsch|nein|stimmt nicht)\b/.test(t)) { e.a[p.id] = false; return true; } },
      anzeige: e => { const w = Object.values(e.a).filter(Boolean).length, f = Object.values(e.a).length - w, m = Math.max(1, w, f); return { text: `${e.f[0]}  Schreib „wahr“ oder „falsch“`, balken: [{ name: '✅ wahr', wert: w, max: m, farbe: '#7fe0c8' }, { name: '❌ falsch', wert: f, max: m, farbe: '#ff8fb8' }] }; },
      ende(e) { const ok = Object.entries(e.a).filter(([, v]) => v === e.f[1]).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 20));
        return { text: `Das ist ${e.f[1] ? 'wahr' : 'falsch'}! ${ok.length ? anz(ok.length, 'richtige Antwort', 'richtige Antworten') + ' (+20 🐚)' : 'Diesmal lag keiner richtig.'}`, sag: `Das ist ${e.f[1] ? 'wahr' : 'falsch'}!`, gut: ok.length > 0 }; },
    },
    inselkoenig: {
      titel: 'Inselkönig', icon: '👑', dauer: 60,
      start(e) { e.l = {}; return 'Wer wird Inselkönig? Wer in einer Minute am meisten liked, bekommt die Krone und sechzig Muscheln!'; },
      like(e, p, n) { e.l[p.id] = (e.l[p.id] || 0) + n; },
      anzeige: e => { const t = Object.entries(e.l).sort((a, b) => b[1] - a[1]).slice(0, 3), m = Math.max(1, ...t.map(x => x[1])); return { text: 'Am meisten Likes = Krone! 👑', balken: t.length ? t.map(([id, v], i) => ({ name: `${i + 1}. ${api.spieler(id)?.name || ''}`, wert: v, max: m, farbe: ['#ffd23f', '#d9d9d9', '#e0a070'][i] })) : [{ name: 'Noch keiner …', wert: 0, max: 1, farbe: '#ffd23f' }] }; },
      ende(e) { const t = Object.entries(e.l).sort((a, b) => b[1] - a[1])[0]; if (!t) return { text: 'Der Thron bleibt leer …' }; const k = api.spieler(t[0]); api.belohne(k, 60);
        return { text: `👑 ${k.name} ist Inselkönig! +60 🐚`, sag: `Neuer Inselkönig: ${api.name(k)}!`, gut: true, id: k.id }; },
    },
    abstimmung: {
      titel: 'Abstimmung', icon: '🗳️', dauer: 90, moeglich: () => !api.hatProjekt() && api.offeneProjekte().length >= 2,
      start(e) { e.wahl = api.offeneProjekte().slice(0, 3).sort(() => Math.random() - .5); e.st = {};
        return `Abstimmung! Was bauen wir als Nächstes? ${e.wahl.map((w, i) => `${i + 1} für ${w.name}`).join(', ')}.`; },
      kommentar(e, p, t) { if (/^[123]$/.test(t) && +t <= e.wahl.length) { e.st[p.id] = +t - 1; return true; } },
      anzeige: e => { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: 'Was bauen wir? Schreib 1, 2 oder 3', balken: e.wahl.map((w, i) => ({ name: `${i + 1}  ${w.name}`, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8'][i] })) }; },
      ende(e) { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const w = e.wahl[z.indexOf(Math.max(...z))]; api.projektStarten(w); return { text: `Entschieden: ${w.name}! Gebaut wird mit der Muschelkasse.`, sag: `Entschieden: Wir bauen ${w.ein || w.name}! … Jedes Like hilft mit.`, gut: true }; },
    },
  };

  // Live-Kommentare während der Events (Anna kommentiert, solange nichts anderes ansteht)
  const TEAMNAME = { rot: 'Rot', blau: 'Blau', gelb: 'Gelb', gruen: 'Grün', muschel: 'Muschel', kokos: 'Kokos' };
  const rest = e => Math.max(0, Math.round((e.ende - Date.now()) / 1000));
  const LIVE = {
    sturmflut: e => { const f = e.ziel - e.stand; return f <= 0 ? null : zufall([`Noch ${zahl(f)} Likes … der Deich wackelt!`, `${rest(e)} Sekunden … noch ${zahl(f)} Likes! … Haltet den Deich!`, f < e.ziel * .25 ? 'Fast geschafft … nur noch ein bisschen!' : `Die Wellen werden höher … liked, liked, liked!`]); },
    krabbenrennen: e => { const r = Object.entries(e.teams).sort((a, b) => b[1] - a[1]); if (!r[0][1]) return 'Die Krabben stehen am Start … wählt ein Team oder liked einfach los!'; return zufall([`Team ${TEAMNAME[r[0][0]]} liegt vorne! … Aber ${TEAMNAME[r[1][0]]} holt auf!`, `Was für ein Rennen … ${TEAMNAME[r[0][0]]} vorne, … ${TEAMNAME[r[1][0]]} direkt dahinter!`, `Noch ${rest(e)} Sekunden … Team ${TEAMNAME[r[0][0]]} führt!`]); },
    teamduell: e => { const [a, b] = e.t.muschel >= e.t.kokos ? ['muschel', 'kokos'] : ['kokos', 'muschel']; return e.t[a] === e.t[b] ? 'Gleichstand! … Wer legt nach?' : zufall([`Team ${TEAMNAME[a]} liegt vorne … ${zahl(e.t[a])} zu ${zahl(e.t[b])}!`, `Kommt schon, Team ${TEAMNAME[b]} … ihr könnt das noch drehen!`]); },
    gluecksrad: () => ['Das Rad dreht sich … und dreht sich …', 'Wer wird es? … Spannung!', 'Langsamer … langsamer …'],
    zahlenraten: e => e.hinweis ? zufall([`${e.hinweis.replace(/ ⬆️| ⬇️/, '')} … weiter raten!`, `Heiß oder kalt? … ${e.hinweis.replace(/ ⬆️| ⬇️/, '')}!`]) : 'Eine Zahl zwischen eins und hundert … wer traut sich?',
    strandparty: e => e.boom ? 'Die Party kocht! … Weiter so!' : `Noch ${zahl(Math.max(0, e.ziel - e.stand))} Likes … bis zum Feuerwerk!`,
    moewenalarm: e => [`Noch ${5 - e.faenger.length} Plätze … schreibt fang!`, 'Die Möwe fliegt Kreise … fangt sie!', e.faenger.length ? `${e.faenger.length} haben schon zugegriffen … wer noch?` : 'Noch hat niemand die Möwe erwischt!'],
    muschelregen: e => [`Noch ${rest(e)} Sekunden … jedes Like zählt doppelt!`, 'Es regnet Muscheln … jetzt liken lohnt sich doppelt!', 'Die Häuser wachsen gerade doppelt so schnell!'],
    bauturbo: e => [`Noch ${rest(e)} Sekunden Bau-Turbo … dreifache Muscheln!`, 'Die Krabben bauen im Turbo-Tempo!', 'Jetzt liken … dreifach für euer Haus!'],
    sternschnuppe: e => [`${e.wuensche.size} Wünsche … schnell, schreibt wunsch!`, 'Was wünscht ihr euch? … Schreibt wunsch!', 'Augen zu … und wünschen!'],
    wortjagd: e => [`Das Wort ist ${e.wort.toLowerCase()} … wer ist am schnellsten?`, `Noch ${3 - e.sieger.length} Plätze … schnell tippen!`],
    cocktail: () => ['Mango, Kokos oder Ananas … was kommt in den Cocktail?', 'Lecker … ich bin gespannt, was ihr mixt!'],
    ballons: e => [`Schon ${e.geplatzt} Ballons geplatzt … liked weiter!`, 'Peng! … Wer bringt den nächsten Ballon zum Platzen?'],
    blumen: e => [`Schon ${e.p.size} Blumen … schreibt blume!`, 'Die Wiese wird immer bunter!'],
    emojiraetsel: () => ['Schaut euch die Emojis an … welches Wort ist gemeint?', 'Kleiner Tipp … es hat mit dem Strand zu tun!', 'Wer errät es zuerst?'],
    volleyball: e => { const [a, b] = e.t.links >= e.t.rechts ? ['Links', 'Rechts'] : ['Rechts', 'Links']; return [`Team ${a} liegt vorne … Team ${b}, gebt alles!`, 'Was für ein Ballwechsel!']; },
    eiswagen: e => [`Noch ${zahl(Math.max(0, e.ziel - e.stand))} Likes … bis zum Eiswagen!`, 'Ich höre schon die Eiswagen-Musik …'],
    glueckszahl: e => [`Schon ${Object.keys(e.tipps).length} Tipps … eins bis zehn!`, 'Welche Zahl bringt heute Glück?'],
    strandquiz: e => [`${e.f[0]} … A, B oder C?`, 'Wer weiß es?'],
    surfcontest: e => { const t = Object.entries(e.punkte).sort((a, b) => b[1] - a[1])[0]; return [t && t[1] ? `${api.name(api.spieler(t[0]))} reitet gerade ganz vorne!` : 'Schreibt surf, dann liked!', 'Was für Wellen heute!']; },
    kokoswurf: e => { const t = Object.entries(e.w).sort((a, b) => b[1] - a[1])[0]; return [t ? `Bester Wurf bisher … ${t[1]} Meter!` : 'Schreibt wurf … und die Kokosnuss fliegt!', 'Wer wirft am weitesten?']; },
    inselfoto: e => [`Schon ${e.f.length} auf dem Foto … schreibt cheese!`, 'Alle lächeln … gleich mache ich das Foto!'],
    tauziehen: e => { const [a, b] = e.t.muschel >= e.t.seestern ? ['Muschel', 'Seestern'] : ['Seestern', 'Muschel']; return [`Team ${a} zieht gerade stärker … Team ${b}, haltet dagegen!`, 'Hau ruck! … Hau ruck!']; },
    buchstabensalat: () => ['Schaut euch die Buchstaben genau an …', 'Wer bringt die Buchstaben in die richtige Reihenfolge?'],
    wuerfeln: e => [`Schon ${Object.keys(e.w).length} Würfe … schreibt würfel!`, 'Wer würfelt eine Sechs?'],
    papagei: e => [`Noch ${5 - e.sieger.length} Plätze … sprecht dem Papagei nach!`, 'Der Papagei wartet …'],
    regenbogen: e => { const fehlt = ['rot', 'orange', 'gelb', 'grün', 'blau', 'lila'].filter(f => !e.f[f]); return fehlt.length ? [`Es fehlen noch … ${fehlt.join(', ')}!`] : null; },
    likerekord: e => [`Schon ${zahl(e.stand)} Likes … der Rekord liegt bei ${zahl(e.rekord)}!`, 'Schneller, schneller!'],
    motto: e => { const z = [0, 0, 0]; Object.values(e.st).forEach(i => z[i]++); const m = z.indexOf(Math.max(...z)); return z[m] ? [`${e.wahl[m]} liegt vorne!`] : ['Eins, zwei oder drei?']; },
    mysterybox: e => [`Schon ${Object.keys(e.b).length} Boxen offen … schreibt box!`, 'Was wohl in eurer Box ist?'],
    werbinich: e => { const n = Math.min(3, 1 + Math.floor((Date.now() - e.t0) / 20000)); return [`${['Erster', 'Zweiter', 'Dritter'][n - 1]} Hinweis: ${e.r[2][n - 1]}`]; },
    hausparty: e => [`Schon ${e.g.size} Gäste … schreibt party!`, `Bei ${api.name(e.p)} ist was los!`],
    leuchtturm: e => { const f = e.ziel - e.stand; return f <= 0 ? null : [`Noch ${zahl(f)} Likes … dann leuchtet er!`, 'Es flackert schon … weiter liken!']; },
    nachbarhilfe: e => [`Schon ${e.summe} Muscheln für ${api.name(e.p)} … liked weiter!`, 'Gemeinsam baut es sich schneller!'],
    inselgruss: e => [e.g.size ? `Schon ${e.g.size} Grüße … schreibt moin!` : 'Sagt doch mal moin!', 'Jeder Gruß bringt zehn Muscheln!'],
    schatzkiste: () => ['Eins, zwei oder drei … wo ist das Gold?', 'Nur eine Kiste ist die richtige!'],
    wahrfalsch: e => [`${e.f[0]} … wahr oder falsch?`, 'Was meint ihr?'],
    inselkoenig: e => { const t = Object.entries(e.l).sort((a, b) => b[1] - a[1])[0]; return [t ? `${api.name(api.spieler(t[0]))} sitzt gerade auf dem Thron!` : 'Der Thron ist noch frei … liked los!', 'Wer holt sich die Krone?']; },
    abstimmung: e => { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const m = z.indexOf(Math.max(...z)), sum = z.reduce((a, b) => a + b, 0);
      if (!sum) return ['Was sollen wir bauen? … 1, 2 oder 3!', `${e.wahl.map((w, i) => `${i + 1} … ${w.name}`).join(', ')}. … Ihr entscheidet!`];
      const zweit = z.map((v, i) => [v, i]).sort((a, b) => b[0] - a[0])[1];
      return [`${e.wahl[m].name} liegt vorne … mit ${z[m] === 1 ? 'einer Stimme' : z[m] + ' Stimmen'}!`, sum === 1 ? `Die erste Stimme ist da … für ${e.wahl[m].name}!` : `Schon ${sum} Stimmen … ${e.wahl[m].name} führt!`, zweit && zweit[0] ? `${e.wahl[zweit[1]].name} ist dicht dran … noch ist alles offen!` : `Wer stimmt noch ab? … 1, 2 oder 3!`, `Noch ${rest(e)} Sekunden … stimmt ab!`]; },
  };

  const PREIS = {
    sturmflut: 'Hält der Deich, bekommen alle Helfer zwanzig Muscheln.', gluecksrad: 'Der Gewinner bekommt bis zu fünfhundert Muscheln, ein goldenes Dach oder einen Pool.',
    krabbenrennen: 'Das Siegerteam bekommt fünfundzwanzig Muscheln.', teamduell: 'Jeder im Siegerteam bekommt dreißig Muscheln.',     zahlenraten: 'Wer die Zahl errät, bekommt hundert Muscheln.',
    strandparty: 'Ist die Stimmung voll, gibt es ein Feuerwerk und fünfzehn Muscheln für alle.', moewenalarm: 'Jeder Fänger bekommt zwanzig Muscheln.',
    sternschnuppe: 'Einer von euch bekommt einen Anbau geschenkt.', abstimmung: 'Das Gebäude mit den meisten Stimmen wird gebaut.',
    wortjagd: 'Die Schnellsten bekommen vierzig, fünfundzwanzig und fünfzehn Muscheln.', cocktail: 'Wer die beliebteste Zutat wählt, bekommt fünfzehn Muscheln.',
    emojiraetsel: 'Die richtige Lösung bringt fünfzig Muscheln.',
    volleyball: 'Das Siegerteam bekommt fünfundzwanzig Muscheln.', eiswagen: 'Kommt der Eiswagen, gibt es fünfzehn Muscheln für jeden, der geliked hat.',
    glueckszahl: 'Alle mit der richtigen Zahl bekommen dreißig Muscheln.', strandquiz: 'Jede richtige Antwort bringt zwanzig Muscheln.',     surfcontest: 'Der beste Surfer bekommt sechzig Muscheln.', kokoswurf: 'Der weiteste Wurf bringt vierzig Muscheln.', inselfoto: 'Alle auf dem Foto bekommen acht Muscheln.',
    tauziehen: 'Das stärkste Team bekommt fünfundzwanzig Muscheln.', buchstabensalat: 'Die richtige Lösung bringt fünfzig Muscheln.', wuerfeln: 'Jede Sechs bringt dreißig Muscheln.',
    papagei: 'Die ersten fünf bekommen je zwanzig Muscheln.',     likerekord: 'Brecht ihr den Rekord, bekommt jeder fünfundzwanzig Muscheln.', motto: 'Wer das Gewinner-Motto wählt, bekommt zehn Muscheln.', werbinich: 'Wer mich zuerst errät, bekommt fünfzig Muscheln.',
    hausbesuch: 'Der Besuchte bekommt fünfundzwanzig Muscheln.', muschelregen: 'Eine Minute lang wächst jedes Haus doppelt so schnell.', bauturbo: 'Eine Dreiviertelminute lang wächst jedes Haus dreimal so schnell.',
    ballons: 'Jeder geplatzte Ballon bringt zehn Muscheln.', blumen: 'Bei fünfundzwanzig Blumen bekommen alle Gärtner fünfzehn Muscheln.', regenbogen: 'Ist der Regenbogen komplett, bekommen alle Maler zwanzig Muscheln.',
    hausparty: 'Jeder Gast bekommt zehn Muscheln, der Gastgeber fünf pro Gast.', leuchtturm: 'Leuchtet er, bekommen alle Helfer zwanzig Muscheln.',
    nachbarhilfe: 'Der fleißigste Helfer bekommt dreißig Muscheln.', inselgruss: 'Jeder Gruß bringt zehn Muscheln.', schatzkiste: 'Wer die richtige Kiste wählt, bekommt dreißig Muscheln.',
    wahrfalsch: 'Jede richtige Antwort bringt zwanzig Muscheln.', inselkoenig: 'Der Inselkönig bekommt sechzig Muscheln.',
    mysterybox: 'In jeder Box stecken zwischen drei und fünfzig Muscheln.',
  };
  // Wer während eines Events Muscheln bekommt, zählt als Gewinner (für die Ansage am Ende)
  const belohneEcht = api.belohne;
  api.belohne = (p, n, x) => { if (ev && p && !x?.trost) (ev._belohnt ||= new Map()).set(p.id, p); belohneEcht(p, n, x); };
  const namenText = ps => { const n = ps.map(p => api.name(p)); return n.length <= 3 ? n.join(n.length === 2 ? ' und ' : ', ').replace(/, ([^,]*)$/, ' und $1') : `${n.slice(0, 3).join(', ')} und ${n.length - 3} weitere`; };

  function starte(id) {
    const d = DEFS[id]; ev = { id, d, t0: Date.now(), ende: Date.now() + d.dauer * 1000 }; ergebnis = null;
    const ansage = d.start(ev) + (PREIS[id] ? ' … ' + PREIS[id] : ''); verlauf = [id, ...verlauf].slice(0, 12);
    api.sende({ typ: 'eventStart', id });
    api.sag(ansage, 0); api.zustand();
  }
  function beende() {
    const r = ev.d.ende(ev) || {}, gew = [...(ev._belohnt?.values() || [])];
    // Gewinner immer nennen (gesprochen und im Ergebnis), falls der Satz sie noch nicht enthält
    if (gew.length && ev.id !== 'hausbesuch') {
      const erster = api.name(gew[0]);
      if (!r.sag || !r.sag.includes(erster)) r.sag = (r.sag ? r.sag + ' … ' : '') + (gew.length === 1 ? `Gewonnen hat ${erster}!` : `Gewonnen haben ${namenText(gew)}!`);
      r.gewinnerText = '🏆 ' + gew.slice(0, 4).map(p => p.name).join(', ') + (gew.length > 4 ? ` +${gew.length - 4}` : '');
    }
    ergebnis = { ...r, titel: ev.titel || ev.d.titel, icon: ev.icon || ev.d.icon, id: ev.id, bis: Date.now() + 10000 };
    api.sende({ typ: 'eventEnde', id: ev.id, gut: !!r.gut, spielerId: r.id });
    if (r.sag) api.sag(r.sag, 0);
    ev = null; naechstes = Date.now() + MIN - 10000; api.zustand();
  }
  function waehle() {
    const moegl = Object.keys(DEFS).filter(id => !verlauf.slice(0, 10).includes(id) && (!DEFS[id].moeglich || DEFS[id].moeglich()));
    if (moegl.includes('abstimmung') && Math.random() < .5) return 'abstimmung';
    return zufall(moegl.filter(x => x !== 'abstimmung').length ? moegl.filter(x => x !== 'abstimmung') : moegl);
  }
  setInterval(() => {
    if (ev && (Date.now() >= ev.ende || ev.frueh)) beende();
    if (!ev && Date.now() >= naechstes) starte(waehle());
    if (ergebnis && Date.now() > ergebnis.bis) ergebnis = null;
  }, 500);

  // ---------- Geschenk-Shows: nach Wert gestaffelt, mit Namen des Spenders ----------
  function geschenkShow(p, gift, anzahl, coins) {
    const art = coins >= 1000 ? 'megashow' : coins >= 100 ? zufall(['feuerwerk', 'yacht', 'goldregen']) : coins >= 10 ? zufall(['delfin', 'ballon', 'flugzeug']) : zufall(['herzregen', 'muschelkonfetti', 'seifenblasen']);
    api.sende({ typ: 'show', art, id: p.id, name: p.name, gift: gift.name, anzeige: gift.anzeige, fuer: gift.fuer, anzahl, coins });
  }

  return {
    like(p, n) { if (ev?.d.like) ev.d.like(ev, p, n); return ev?.d.faktor || 1; },
    kommentar(p, t) { return !!(ev?.d.kommentar && ev.d.kommentar(ev, p, t)); },
    geschenkShow,
    naechstesIn: () => ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)),
    oeffentlich() {
      const a = ev ? { id: ev.id, titel: ev.titel || ev.d.titel, icon: ev.icon || ev.d.icon, rest: Math.max(0, Math.round((ev.ende - Date.now()) / 1000)), dauer: ev.d.dauer, faktor: ev.d.faktor || 1, ...ev.d.anzeige(ev) } : null;
      if (a) a.preis = PREIS[ev.id] || '';
      return { event: a, ergebnis: ergebnis && { titel: ergebnis.titel, icon: ergebnis.icon, text: ergebnis.text, id: ergebnis.id, gut: !!ergebnis.gut, extra: ergebnis.extra, gewinner: ergebnis.gewinnerText }, eventIn: ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)) };
    },
    laeuft: () => !!ev,
    id: () => ev?.id || null,
    liveSatz() {                                          // abwechslungsreich: nie derselbe Satz wie zuletzt
      if (!ev || ev.frueh || rest(ev) <= 3 || !LIVE[ev.id]) return null;
      const opts = [].concat(LIVE[ev.id](ev)).filter(x => x && x !== ev.letzterLive);
      if (!opts.length) return null; ev.letzterLive = zufall(opts); return ev.letzterLive;
    },
    restSek: () => ev ? rest(ev) : null,
    starte(id) { if (ev) beende(); ergebnis = null; starte(id); },   // nur für den Test-Modus
    beendeJetzt() { if (ev) beende(); },                             // nur für den Test-Modus
  };
}
