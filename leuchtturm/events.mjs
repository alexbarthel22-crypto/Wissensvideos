// Leuchtturm-Rennen – Städte-Events (60 Stück, mit events-extra.mjs). Jede Minute eins, jedes ca. 40 Sekunden.
// Alles läuft über den Chat (keine Belohnung für Herzen/Folgen/Teilen/Geschenke – TikTok-Regeln).
import { normal } from './filter.mjs';
import { extraEvents } from './events-extra.mjs';

const zufall = a => a[Math.floor(Math.random() * a.length)];
const anz = (n, ein, mehr) => n === 1 ? `1 ${ein}` : `${n} ${mehr}`;
const listeTxt = l => l.length <= 1 ? (l[0] || '') : l.slice(0, -1).join(', ') + ' und ' + l[l.length - 1];
function wortGleich(text, wort) {
  const a = normal(text), b = normal(wort); if (!a) return false; if (a === b || a.includes(b)) return true;
  if (Math.abs(a.length - b.length) > 2 || b.length < 5) return false;
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i]); for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length] <= 1;
}
const LAENDER = { DE: '🇩🇪 Deutschland', AT: '🇦🇹 Österreich', CH: '🇨🇭 Schweiz' };

export function macheEvents(api) {
  const { CFG } = api;
  const MIN = (CFG.events?.alleMinuten ?? 2) * 60000, DAUER = CFG.events?.dauerSek ?? 60;
  let ev = null, ergebnis = null, naechstes = Date.now() + (api.test ? 25000 : MIN), verlauf = [], zahl = 0;
  const rest = e => Math.max(0, Math.round((e.ende - Date.now()) / 1000));
  const stadtVon = p => p?.stadt ? api.stadt(p.stadt) : null;
  const km = (a, b) => { const r = Math.PI / 180, x = (b.lng - a.lng) * r * Math.cos((a.lat + b.lat) * r / 2), y = (b.lat - a.lat) * r; return 6371 * Math.hypot(x, y); };
  function nachbarPaar() {                                     // zwei nahe Städte (unter 120 km), möglichst weit oben
    const l = api.staedte().slice(0, 40).filter(s => s.lat != null); let best = null;
    for (let i = 0; i < l.length; i++) for (let j = i + 1; j < l.length; j++) { const d = km(l[i], l[j]); if (d < 120 && d > 1) { const w = i + j; if (!best || w < best[3]) best = [l[i].name, l[j].name, Math.max(1, Math.round(d)), w]; } }
    return best;
  }

  const DEFS = {
    staedteneu: {
      titel: 'Neue Städte willkommen', icon: '🌍',
      start(e) { e.b = []; return 'Neue Städte willkommen! Schreibt eure Stadt in den Chat. Jede Stadt, die jetzt neu dazukommt, startet mit zwanzig Metern!'; },
      kommentar(e, p) { const s = stadtVon(p); if (!s || !(s.seit >= e.t0) || e.b.includes(s.name)) return; e.b.push(s.name); api.turmWachsen(s.name, 20, p); return true; },
      anzeige: e => ({ text: `Schreib deine Stadt! Neue Städte starten mit +20 Metern  (${e.b.length} neu)` }),
      ende: e => e.b.length ? { text: `Neu dabei: ${listeTxt(e.b.slice(0, 6))}${e.b.length > 6 ? ' …' : ''}`, sag: `Willkommen im Rennen, ${listeTxt(e.b.slice(0, 3))}!`, gut: true } : { text: 'Diesmal kam keine neue Stadt dazu.', sag: 'Diesmal kam keine neue Stadt dazu.' },
    },
    baukolonne: {
      titel: 'Bau-Kolonne', icon: '🏗️',
      start(e) { e.leute = new Set(); e.pro = {}; return 'Bau-Kolonne! Schreibt eure Stadt in den Chat. Jeder von euch bringt seiner Stadt einmal fünf Meter!'; },
      kommentar(e, p, t) { if (!p.stadt || e.leute.has(p.id) || api.stadtAus(t) !== p.stadt) return; e.leute.add(p.id); e.pro[p.stadt] = (e.pro[p.stadt] || 0) + 5; api.turmWachsen(p.stadt, 5, p); return true; },
      anzeige: e => ({ text: `Schreib deine Stadt – jeder bringt einmal +5 Meter!  (${e.leute.size} Bauarbeiter)` }),
      ende(e) { const top = Object.entries(e.pro).sort((a, b) => b[1] - a[1])[0]; return top ? { text: `${anz(e.leute.size, 'Bauarbeiter', 'Bauarbeiter')}! Am meisten gebaut: ${top[0]} (+${top[1]})`, sag: `Am fleißigsten gebaut hat ${top[0]}!`, gut: true } : { text: 'Die Bau-Kolonne hatte frei …', sag: 'Diesmal hat keiner mitgebaut.' }; },
    },
    staedteduell: {
      titel: 'Städte-Duell', icon: '⚔️', moeglich: () => api.staedte().length >= 2,
      start(e) { const [a, b] = api.staedte(); e.a = a.name; e.b = b.name; e.w = { [e.a]: new Set(), [e.b]: new Set() }; api.sende({ typ: 'duell', a: e.a, b: e.b }); return `Städte-Duell! ${e.a} gegen ${e.b}! Schreibt jetzt eure Stadt in den Chat! Welche Stadt mehr Leute im Chat hat, gewinnt fünfzig Meter!`; },
      kommentar(e, p) { if (p.stadt && e.w[p.stadt]) e.w[p.stadt].add(p.id); return false; },
      anzeige: e => { const a = e.w[e.a].size, b = e.w[e.b].size, m = Math.max(1, a, b); return { text: `${e.a} gegen ${e.b}! Schreib deine Stadt in den Chat – wer hat mehr Leute?`, balken: [{ name: '🗼 ' + e.a, wert: a, max: m, farbe: '#3fa0e8' }, { name: '🗼 ' + e.b, wert: b, max: m, farbe: '#ff8fb8' }] }; },
      ende(e) { const a = e.w[e.a].size, b = e.w[e.b].size; if (a === b) return { text: `Unentschieden ${a}:${b}!`, sag: 'Unentschieden!' }; const s = a > b ? e.a : e.b; api.turmWachsen(s, 50); return { text: `${s} gewinnt das Duell (${Math.max(a, b)}:${Math.min(a, b)})! +50 Meter`, sag: `${s} gewinnt das Städte-Duell!`, gut: true, stadt: s }; },
    },
    leuchtsignal: {
      titel: 'Leuchtfeuer-Signal', icon: '🔦',
      start(e) { e.signal = Date.now() + 10000 + Math.random() * 18000; e.sieger = []; e.zufrueh = new Set(); e.gesagt = false;
        return 'Leuchtfeuer-Signal! Wartet, bis ich Licht an sage. Dann schreibt licht! Die ersten fünf bringen ihrer Stadt fünfzehn Meter. Wer zu früh schreibt, ist raus!'; },
      tick(e) { if (!e.gesagt && Date.now() >= e.signal) { e.gesagt = true; api.sag('Licht an!', 0); api.sende({ typ: 'blitz' }); api.zustand(); } },
      kommentar(e, p, t) { if (!/^licht/.test(t)) return; if (Date.now() < e.signal) { e.zufrueh.add(p.id); return true; } if (p.stadt && !e.zufrueh.has(p.id) && !e.sieger.includes(p) && e.sieger.length < 5) { e.sieger.push(p); api.turmWachsen(p.stadt, 15, p); if (e.sieger.length >= 5) e.frueh = true; } return true; },
      anzeige: e => ({ text: Date.now() < e.signal ? `Warte auf „Licht an!“ … nicht zu früh! (${e.zufrueh.size} zu früh)` : `🔦 LICHT AN! „licht“ schreiben!  (${e.sieger.length}/5)` }),
      ende: e => e.sieger.length ? { text: `Am schnellsten: ${e.sieger.map(p => `${p.name} (${p.stadt})`).join(', ')}`, sag: `Am schnellsten war ${api.name(e.sieger[0])} für ${e.sieger[0].stadt}!`, gut: true } : { text: 'Niemand hat das Signal erwischt …', sag: 'Diesmal war keiner schnell genug.' },
    },
    turmquiz: {
      titel: 'Städte-Quiz', icon: '🧠',
      start(e) { e.f = zufall([['Wo steht der Kölner Dom?', 'köln'], ['Was ist die Hauptstadt von Deutschland?', 'berlin'], ['In welcher Stadt ist das Oktoberfest?', 'münchen'],
        ['Wo ist der Hamburger Hafen?', 'hamburg'], ['Wo steht der Eiffelturm?', 'paris'], ['Wo steht das Kolosseum?', 'rom'], ['In welcher Stadt steht Big Ben?', 'london'],
        ['Was ist die Hauptstadt von Österreich?', 'wien'], ['Woher kommen die Bremer Stadtmusikanten?', 'bremen'], ['Woher kommen Frankfurter Würstchen?', 'frankfurt'],
        ['Woher kommen Nürnberger Lebkuchen?', 'nürnberg'], ['Wo steht das Brandenburger Tor?', 'berlin']]); e.sieger = [];
        return `Städte-Quiz! ${e.f[0]} Schreibt die Antwort in den Chat! Die ersten fünf Richtigen bringen ihrer Stadt zehn Meter!`; },
      kommentar(e, p, t) { if (!wortGleich(t, e.f[1]) || t.length > e.f[1].length + 4) return; if (!e.sieger.includes(p) && e.sieger.length < 5) { e.sieger.push(p); if (p.stadt) api.turmWachsen(p.stadt, 10, p); if (e.sieger.length >= 5) e.frueh = true; } return true; },
      anzeige: e => ({ text: `${e.f[0]}  (${e.sieger.length}/5 richtig)` }),
      ende: e => e.sieger.length ? { text: `Richtig: ${e.f[1].charAt(0).toUpperCase() + e.f[1].slice(1)}! Am schnellsten: ${e.sieger.map(p => p.name).join(', ')}`, sag: `Richtig! Am schnellsten war ${api.name(e.sieger[0])}!`, gut: true } : { text: `Lösung: ${e.f[1]}`, sag: 'Diesmal hatte es niemand.' },
    },
    aufholjagd: {
      titel: 'Aufholjagd', icon: '🚀', moeglich: () => api.staedte().length >= 4,
      start(e) { e.hinten = new Set(api.staedte().slice(3).map(s => s.name)); e.z = {}; e.plus = {}; return 'Aufholjagd! Schreibt jetzt eure Stadt in den Chat! Alle Städte ab Platz vier wachsen doppelt so schnell!'; },
      kommentar(e, p) { if (!p.stadt || !e.hinten.has(p.stadt) || Date.now() - (e.z[p.id] || 0) < 10000) return; e.z[p.id] = Date.now(); e.plus[p.stadt] = (e.plus[p.stadt] || 0) + 2; api.turmWachsen(p.stadt, 2, p); return false; },
      anzeige: e => ({ text: `Ab Platz 4 wächst jede Stadt doppelt!  (${Object.values(e.plus).reduce((a, b) => a + b, 0)} Meter extra)` }),
      ende(e) { const top = Object.entries(e.plus).sort((a, b) => b[1] - a[1])[0]; return top ? { text: `Am meisten aufgeholt: ${top[0]} (+${top[1]})`, sag: `${top[0]} hat am meisten aufgeholt!`, gut: true } : { text: 'Aufholjagd vorbei.' }; },
    },
    laenderduell: {
      titel: 'Länder-Duell', icon: '🌐',
      start(e) { e.w = { DE: new Set(), AT: new Set(), CH: new Set() }; return 'Länder-Duell! Deutschland, Österreich oder Schweiz! Schreibt eure Stadt in den Chat! Das Land mit den meisten Leuten im Chat gewinnt, alle seine Städte bekommen zehn Meter!'; },
      kommentar(e, p) { const s = stadtVon(p); if (s && e.w[s.land]) e.w[s.land].add(p.id); return false; },
      anzeige: e => { const z = Object.keys(LAENDER).map(k => e.w[k].size), m = Math.max(1, ...z); return { text: 'Schreib deine Stadt in den Chat! Welches Land hat die meisten Leute?', balken: Object.keys(LAENDER).map((k, i) => ({ name: LAENDER[k], wert: z[i], max: m, farbe: ['#e8433c', '#ff8a2a', '#3fa0e8'][i] })) }; },
      ende(e) { const best = Object.keys(LAENDER).sort((a, b) => e.w[b].size - e.w[a].size)[0]; if (!e.w[best].size) return { text: 'Kein Land hat mitgemacht …' };
        const st = new Set(); for (const id of e.w[best]) { const p = api.spieler(id); if (p?.stadt) st.add(p.stadt); } st.forEach(n => api.turmWachsen(n, 10));
        return { text: `${LAENDER[best]} gewinnt! ${anz(st.size, 'Stadt bekommt', 'Städte bekommen')} +10`, sag: `${LAENDER[best].slice(5)} gewinnt das Länder-Duell!`, gut: true }; },
    },
    nachbarduell: {
      titel: 'Nachbar-Duell', icon: '🏘️', moeglich: () => !!nachbarPaar(),
      start(e) { const [a, b, km] = nachbarPaar(); e.a = a; e.b = b; e.w = { [a]: new Set(), [b]: new Set() }; api.sende({ typ: 'duell', a, b }); return `Nachbar-Duell! ${a} gegen ${b}, nur ${km} Kilometer auseinander! Schreibt jetzt eure Stadt in den Chat! Welche Stadt mehr Leute hat, gewinnt vierzig Meter!`; },
      kommentar(e, p) { if (p.stadt && e.w[p.stadt]) e.w[p.stadt].add(p.id); return false; },
      anzeige: e => { const a = e.w[e.a].size, b = e.w[e.b].size, m = Math.max(1, a, b); return { text: `${e.a} gegen ${e.b}! Schreib deine Stadt in den Chat – wer hat mehr Leute?`, balken: [{ name: '🏘️ ' + e.a, wert: a, max: m, farbe: '#3fa0e8' }, { name: '🏘️ ' + e.b, wert: b, max: m, farbe: '#ff8fb8' }] }; },
      ende(e) { const a = e.w[e.a].size, b = e.w[e.b].size; if (a === b) return { text: `Unentschieden ${a}:${b}!`, sag: 'Unentschieden unter Nachbarn!' }; const s = a > b ? e.a : e.b; api.turmWachsen(s, 40); return { text: `${s} gewinnt das Nachbar-Duell (${Math.max(a, b)}:${Math.min(a, b)})! +40 m`, sag: `${s} gewinnt das Nachbar-Duell!`, gut: true, stadt: s }; },
    },
    regionenduell: {
      titel: 'Bundesland-Duell', icon: '🗺️', moeglich: () => new Set(api.staedte().map(s => s.region).filter(Boolean)).size >= 2,
      start(e) { e.w = {}; return 'Bundesland-Duell! Schreibt eure Stadt in den Chat! Das Bundesland oder der Kanton mit den meisten Leuten gewinnt, alle seine Städte bekommen fünfzehn Meter!'; },
      kommentar(e, p) { const s = stadtVon(p); if (s?.region) (e.w[s.region] ||= new Set()).add(p.id); return false; },
      anzeige: e => { const z = Object.entries(e.w).map(([k, v]) => [k, v.size]).sort((a, b) => b[1] - a[1]).slice(0, 3), m = Math.max(1, ...z.map(x => x[1])); return { text: 'Schreib deine Stadt in den Chat! Welches Bundesland hat die meisten Leute?', balken: z.map(([k, n], i) => ({ name: k, wert: n, max: m, farbe: ['#57b85a', '#ffd23f', '#3fa0e8'][i] })) }; },
      ende(e) { const best = Object.entries(e.w).sort((a, b) => b[1].size - a[1].size)[0]; if (!best) return { text: 'Kein Bundesland hat mitgemacht …' };
        const st = new Set(); for (const id of best[1]) { const p = api.spieler(id); if (p?.stadt) st.add(p.stadt); } st.forEach(n => api.turmWachsen(n, 15));
        return { text: `${best[0]} gewinnt! ${anz(st.size, 'Stadt bekommt', 'Städte bekommen')} +15 m`, sag: `${best[0]} gewinnt das Bundesland-Duell!`, gut: true }; },
    },
    herzregen: {
      titel: 'Herz-Regen', icon: '💖',
      start(e) { e.n = 0; api.sende({ typ: 'herzregen' }); return 'Herz-Regen! Schreibt jetzt Herz-Emojis in den Chat! Jedes Herz im Chat bringt eurer Stadt zwei Meter, alle zwei Sekunden!'; },
      anzeige: e => ({ text: '💖 im Chat = +2 m (alle 2 Sekunden)', balken: [{ name: '💖 Meter durch Herzen', wert: e.n, max: Math.max(50, e.n), farbe: '#ff6fa3' }] }),
      ende(e) { return { text: `Herz-Regen vorbei – ${e.n} Meter gebaut!`, sag: 'Herz-Regen vorbei!', gut: e.n > 0 }; },
    },
    turbo: {
      titel: 'Bau-Turbo', icon: '⚡',
      start(e) { e.n = 0; return 'Bau-Turbo! Schreibt jetzt so oft ihr könnt in den Chat! Jeder Kommentar zählt alle zehn Sekunden statt alle dreißig!'; },
      anzeige: e => ({ text: `⚡ Jeder Kommentar zählt alle 10 Sekunden!  (${e.n} Meter im Turbo)` }),
      ende: e => ({ text: `Turbo vorbei – ${e.n} Meter gebaut!`, sag: 'Der Turbo ist vorbei! … Stark gebaut!', gut: e.n > 0 }),
    },
    glueckslos: {
      titel: 'Glückslos', icon: '🎟️',
      start(e) { e.lose = new Set(); return 'Glückslos! Schreibt los, und ihr landet im Lostopf. Am Ende ziehe ich drei Gewinner, ihre Städte bekommen Meter!'; },
      kommentar(e, p, t) { if (/^los+$/.test(t) && p.stadt) { e.lose.add(p); return true; } },
      anzeige: e => ({ text: `Schreib „los“ für den Lostopf!  (${e.lose.size} Lose)` }),
      ende(e) { const l = [...e.lose].sort(() => Math.random() - .5).slice(0, 3); if (!l.length) return { text: 'Der Lostopf blieb leer …' }; l.forEach((p, i) => api.turmWachsen(p.stadt, [25, 15, 10][i], p));
        return { text: `Gezogen: ${l.map(p => `${p.name} (${p.stadt})`).join(', ')}`, sag: `Gewonnen haben ${listeTxt(l.map(p => api.name(p)))}!`, gut: true }; },
    },
    sturm: {
      titel: 'Sturm zieht auf', icon: '🌊',
      start(e) { e.h = new Set(); e.st = new Set(); api.sende({ typ: 'sturm' }); return 'Sturm zieht auf! Schreibt halten, damit eure Leuchttürme stehen bleiben! Jeder bringt drei Meter, und ab zehn Helfern gibt es für alle zehn extra!'; },
      kommentar(e, p, t) { if (!/^halt/.test(t) || !p.stadt || e.h.has(p.id)) return; e.h.add(p.id); e.st.add(p.stadt); api.turmWachsen(p.stadt, 3, p); return true; },
      anzeige: e => ({ text: `Schreib „halten“!  (${e.h.size}/10 Helfer)`, balken: [{ name: '💪 Helfer', wert: e.h.size, max: 10, farbe: '#3fa0e8' }] }),
      ende(e) { if (e.h.size >= 10) { e.st.forEach(n => api.turmWachsen(n, 10)); return { text: `Alle Türme halten! ${anz(e.st.size, 'Stadt bekommt', 'Städte bekommen')} +10 extra`, sag: 'Geschafft! Alle Leuchttürme halten dem Sturm stand!', gut: true }; }
        return { text: `${anz(e.h.size, 'Helfer', 'Helfer')} – der Sturm ist vorbei.`, sag: 'Der Sturm ist vorbei!' }; },
    },
    nebel: {
      titel: 'Nebel auf dem Meer', icon: '🌫️',
      start(e) { e.st = []; api.sende({ typ: 'nebel' }); return 'Nebel auf dem Meer! Schreibt eure Stadt, damit euer Leuchtturm gesehen wird! Die ersten zehn Städte bekommen acht Meter!'; },
      kommentar(e, p, t) { if (!p.stadt || api.stadtAus(t) !== p.stadt || e.st.includes(p.stadt) || e.st.length >= 10) return; e.st.push(p.stadt); api.turmWachsen(p.stadt, 8, p); if (e.st.length >= 10) e.frueh = true; return true; },
      anzeige: e => ({ text: `Schreib deine Stadt – die ersten 10 Städte leuchten durch den Nebel!  (${e.st.length}/10)` }),
      ende: e => e.st.length ? { text: `Durch den Nebel: ${listeTxt(e.st.slice(0, 6))}${e.st.length > 6 ? ' …' : ''}`, sag: 'Der Nebel ist weg!', gut: true } : { text: 'Der Nebel ist weg.' },
    },
    schaetzen: {
      titel: 'Schätz-Runde', icon: '🤔', moeglich: () => api.staedte().length >= 1,
      start(e) { const s = api.staedte()[0]; e.stadt = s.name; e.loes = s.stock; e.t = new Map(); return `Schätz-Runde! Wie hoch ist der Leuchtturm von ${s.name}? Schreibt eine Zahl! Wer am nächsten dran ist, bringt seiner Stadt zwanzig Meter!`; },
      kommentar(e, p, t) { if (/^\d{1,7}$/.test(t)) { e.t.set(p.id, +t); return true; } },
      anzeige: e => ({ text: `Wie viele Meter hat ${e.stadt}?  → Zahl schreiben! (${e.t.size} Tipps)` }),
      ende(e) { const best = [...e.t].sort((a, b) => Math.abs(a[1] - e.loes) - Math.abs(b[1] - e.loes))[0]; if (!best) return { text: `Lösung: ${e.loes}` };
        const p = api.spieler(best[0]); if (p?.stadt) api.turmWachsen(p.stadt, 20, p); return { text: `Lösung: ${e.loes} – am nächsten: ${p.name}${p.stadt ? ' (' + p.stadt + ')' : ''}`, sag: `Am nächsten dran war ${api.name(p)}!`, gut: true }; },
    },
  };

  const X = extraEvents(api, { zufall, wortGleich, listeTxt, anz, stadtVon }); Object.assign(DEFS, X.D);
  for (const id of ['staedteneu', 'baukolonne', 'nebel']) DEFS[id].stadt = true;
  delete DEFS.herzregen;                                       // Herz-Emojis kommen im TikTok-Chat nicht zuverlässig an
  const PREIS = {
    staedteneu: 'Jede neue Stadt startet mit zwanzig Metern.', baukolonne: 'Jeder bringt seiner Stadt fünf Meter.', staedteduell: 'Die Siegerstadt bekommt fünfzig Meter.',
    leuchtsignal: 'Die ersten fünf bringen ihrer Stadt je fünfzehn Meter.', turmquiz: 'Jede richtige Antwort bringt der eigenen Stadt zehn Meter.', aufholjagd: 'Ab Platz vier wächst jede Stadt doppelt.',
    laenderduell: 'Alle Städte des Siegerlandes bekommen zehn Meter.', turbo: 'Jeder Kommentar zählt alle zehn Sekunden.', glueckslos: 'Drei Gewinner bringen ihrer Stadt bis zu fünfundzwanzig Meter.',
    sturm: 'Jeder Helfer bringt drei Meter.', nachbarduell: 'Die Siegerstadt bekommt vierzig Meter.', regionenduell: 'Alle Städte des Siegers bekommen fünfzehn Meter.', herzregen: 'Jedes Herz im Chat bringt zwei Meter.', nebel: 'Die ersten zehn Städte bekommen acht Meter.', schaetzen: 'Wer am nächsten dran ist, bringt seiner Stadt zwanzig Meter.',
    ...X.P,
  };

  function starte(id) {
    const d = DEFS[id]; ev = { id, d, t0: Date.now(), ende: Date.now() + DAUER * 1000 }; ergebnis = null;
    naechstes = Date.now() + MIN;
    const ansage = d.start(ev); verlauf = [id, ...verlauf].slice(0, Math.min(30, Object.keys(DEFS).length - 5));
    api.sende({ typ: 'eventStart', id });
    api.sag(ansage, 0); api.zustand();
  }
  function beende() {
    if (!ev) return;
    const e = ev; let r = {};
    try { r = e.d.ende(e) || {}; } catch (err) { console.log('⚠️  Event-Fehler:', err.message); }
    ergebnis = { titel: e.d.titel, icon: e.d.icon, text: r.text || '', gut: !!r.gut, stadt: r.stadt, bis: Date.now() + 9000 };
    if (r.sag) api.sag(r.sag, 0);
    api.sende({ typ: 'eventEnde', gut: !!r.gut });
    ev = null; naechstes = Math.max(naechstes, Date.now() + 20000); api.zustand();
  }
  // Erstes Event: „Neue Städte willkommen“, danach zufällig (keins der letzten 30)
  function waehle() {
    zahl++;
    if (zahl === 1) return 'staedteneu';
    const moegl = Object.keys(DEFS).filter(id => !verlauf.includes(id) && (!DEFS[id].moeglich || DEFS[id].moeglich()));
    return zufall(moegl.length ? moegl : Object.keys(DEFS));
  }
  setInterval(() => {
    if (ev?.d.tick) ev.d.tick(ev);
    if (ev && (Date.now() >= ev.ende || ev.frueh)) beende();
    if (!ev && Date.now() >= naechstes) starte(waehle());
    if (ergebnis && Date.now() > ergebnis.bis) ergebnis = null;
  }, 500);

  return {
    kommentar(p, t) { return !!(ev?.d.kommentar && ev.d.kommentar(ev, p, t)); },
    waereAntwort(t) {
      if (!ev?.d.kommentar) return false;
      const probe = { id: '__probe__', name: '', stadt: null }, merk = [api.turmWachsen, api.sende, api.sag];
      api.turmWachsen = () => {}; api.sende = () => {}; api.sag = () => {};
      try { const kopie = structuredClone({ ...ev, d: null }); kopie.d = ev.d; return !!ev.d.kommentar(kopie, probe, t); } catch { return false; }
      finally { [api.turmWachsen, api.sende, api.sag] = merk; }
    },
    turbo: () => ev?.id === 'turbo' ? ev : null,
    herzregen: () => ev?.id === 'herzregen' ? ev : null,
    doppel: () => ev?.id === 'doppelmeter' ? ev : null,
    stadtEvent: () => !!ev?.d.stadt,
    anzahl: () => Object.keys(DEFS).length,
    laeuft: () => !!ev, id: () => ev?.id || null,
    naechstesIn: () => ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)),
    restSek: () => ev ? rest(ev) : null,
    preise: () => PREIS,
    starte(id) { if (ev) beende(); starte(id); }, beendeJetzt() { if (ev) beende(); },
    oeffentlich() {
      const a = ev ? { id: ev.id, titel: ev.d.titel, icon: ev.d.icon, rest: rest(ev), dauer: DAUER, preis: PREIS[ev.id] || '', ...ev.d.anzeige(ev) } : null;
      return { event: a, ergebnis: ergebnis && { titel: ergebnis.titel, icon: ergebnis.icon, text: ergebnis.text, gut: ergebnis.gut }, eventIn: ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)) };
    },
  };
}
