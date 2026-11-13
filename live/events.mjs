// Muschel-Tal LIVE – Überraschungs-Events (alle 5 Minuten) und Geschenk-Shows.
// Alle Events laufen komplett im Stream: mitmachen per Like oder Kommentar, niemand muss den Stream verlassen.
// Verlosungen sind nie an Geschenke gebunden (TikTok-Regeln).

const zufall = a => a[Math.floor(Math.random() * a.length)];
const klemme = (x, a, b) => Math.max(a, Math.min(b, x));
// Wer ohne Team liked, kommt ins Team mit den wenigsten Mitgliedern
const kleinstes = (wahl, teams) => { const z = Object.fromEntries(teams.map(t => [t, 0])); Object.values(wahl).forEach(t => z[t]++); return teams.sort((a, b) => z[a] - z[b])[0]; };
const zahl = n => Math.round(n).toLocaleString('de-DE');

export function macheEvents(api) {
  const { CFG } = api;
  const MIN = (CFG.events?.alleMinuten ?? 5) * 60000;
  let ev = null, ergebnis = null, naechstes = Date.now() + (api.test ? 25000 : MIN), verlauf = [];

  const DEFS = {
    sturmflut: {
      titel: 'Sturmflut!', icon: '🌊', dauer: 60,
      start(e) { e.ziel = klemme(Math.round(api.likeRate() * 1.2 / 10) * 10, 150, 50000); e.stand = 0; e.dabei = new Set();
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
      anzeige: e => ({ text: 'Alle Aktiven der letzten 10 Minuten sind im Lostopf!', rad: { namen: e.namen, gewinner: e.gewinner.name } }),
      ende(e) { api.belohne(e.gewinner, e.preis.m, e.preis); return { text: `${e.gewinner.name} gewinnt ${e.preis.t}! 🎉`, sag: `${api.name(e.gewinner)} gewinnt ${e.preis.t}! Glückwunsch!`, gut: true, id: e.gewinner.id }; },
    },
    krabbenrennen: {
      titel: 'Krabbenrennen', icon: '🦀', dauer: 60,
      start(e) { e.teams = { rot: 0, blau: 0, gelb: 0, gruen: 0 }; e.wahl = {}; e.ziel = klemme(Math.round(api.likeRate() * .45 / 10) * 10, 60, 20000);
        return `Krabbenrennen! Schreibt rot, blau, gelb oder grün für euer Team, oder liked einfach, dann bekommt ihr ein Team!`; },
      kommentar(e, p, t) { const m = { rot: 'rot', blau: 'blau', gelb: 'gelb', grün: 'gruen', gruen: 'gruen' }[t]; if (m) { e.wahl[p.id] = m; return true; } },
      like(e, p, n) { const tm = e.wahl[p.id] || (e.wahl[p.id] = kleinstes(e.wahl, Object.keys(e.teams))); e.teams[tm] += n; if (e.teams[tm] >= e.ziel) e.frueh = true; },
      anzeige: e => ({ text: 'Team wählen: rot · blau · gelb · grün – oder einfach liken!', rennen: Object.entries(e.teams).map(([k, v]) => ({ name: k, wert: v, max: e.ziel })) }),
      ende(e) {
        const [sieger, w] = Object.entries(e.teams).sort((a, b) => b[1] - a[1])[0];
        if (!w) return { text: 'Keine Krabbe ist losgelaufen …', sag: 'Die Krabben haben sich nicht bewegt. Nächstes Mal!' };
        const fans = Object.entries(e.wahl).filter(([, t]) => t === sieger).map(([id]) => api.spieler(id)); fans.forEach(p => api.belohne(p, 25));
        const nm = { rot: 'Rot', blau: 'Blau', gelb: 'Gelb', gruen: 'Grün' }[sieger];
        return { text: `Team ${nm} gewinnt! ${fans.length} Fans bekommen 25 🐚`, sag: `Team ${nm} gewinnt das Krabbenrennen!`, gut: true };
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
    flaschenpost: {
      titel: 'Flaschenpost!', icon: '🍾', dauer: 60,
      start(e) { return `Da treibt eine Flaschenpost ans Ufer! Wer zuerst flasche schreibt, darf sie öffnen.`; },
      kommentar(e, p, t) { if (!e.finder && /flasche/.test(t)) { e.finder = p; e.frueh = true; return true; } },
      anzeige: e => ({ text: 'Wer zuerst „flasche“ schreibt, öffnet sie!' }),
      ende(e) {
        if (!e.finder) return { text: 'Die Flasche ist wieder rausgetrieben …', sag: 'Schade, die Flasche ist wieder aufs Meer getrieben.' };
        const pr = zufall([{ t: '80 Muscheln', m: 80 }, { t: 'eine Palme und 40 Muscheln', anbau: 'palme', m: 40 }, { t: 'eine Laterne und 40 Muscheln', anbau: 'laterne', m: 40 }, { t: '150 Muscheln', m: 150 }]);
        api.belohne(e.finder, pr.m, pr); return { text: `${e.finder.name} öffnet die Flasche: ${pr.t}!`, sag: `${api.name(e.finder)} hat die Flaschenpost geöffnet und bekommt ${pr.t}!`, gut: true, id: e.finder.id };
      },
    },
    meeresbesuch: {
      titel: 'Besuch vom Meer', icon: '🐋', dauer: 45,
      start(e) { e.art = zufall(['wal', 'delfine', 'piraten']); e.gruss = new Set(); e.titel = { wal: 'Ein Wal!', delfine: 'Delfine!', piraten: 'Piratenschiff!' }[e.art]; e.icon = { wal: '🐋', delfine: '🐬', piraten: '🏴‍☠️' }[e.art];
        return { wal: 'Schaut mal, ein Wal schwimmt an der Insel vorbei! Schreibt hallo, um ihn zu begrüßen!', delfine: 'Delfine springen vor der Küste! Schreibt hallo!', piraten: 'Ein Piratenschiff! Schreibt hallo, vielleicht sind sie freundlich!' }[e.art]; },
      kommentar(e, p, t) { if (/^(hallo|hi|hey|ahoi|moin)\b/.test(t) && !e.gruss.has(p.id)) { e.gruss.add(p.id); api.belohne(p, 10); return true; } },
      anzeige: e => ({ text: `Schreib „hallo“ – jeder Gruß bringt 10 🐚 (${e.gruss.size} Grüße)`, extra: { art: e.art } }),
      ende(e) { const n = e.gruss.size; return { text: n === 1 ? '1 Bewohner hat gegrüßt!' : `${n} Bewohner haben gegrüßt!`, sag: n > 1 ? `${n} von euch haben gegrüßt. Tschüss!` : n === 1 ? 'Einer von euch hat gegrüßt. Tschüss!' : 'Tschüss!' }; },
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
    schatzsuche: {
      titel: 'Schatzsuche', icon: '🗺️', dauer: 45,
      start(e) { e.seed = Math.floor(Math.random() * 1e6); e.loesung = Math.floor(Math.random() * 4); e.tipp = {}; return 'Schatzsuche! Auf der Insel sind vier Kreuze: A, B, C und D. Wo ist der Schatz vergraben? Schreibt den Buchstaben!'; },
      kommentar(e, p, t) { const i = 'abcd'.indexOf(t); if (t.length === 1 && i >= 0) { e.tipp[p.id] = i; return true; } },
      anzeige: e => { const z = [0, 0, 0, 0]; Object.values(e.tipp).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: 'Schreib A, B, C oder D!', balken: 'ABCD'.split('').map((b, i) => ({ name: '❌ ' + b, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8', '#b58ad0'][i] })), extra: { seed: e.seed } }; },
      ende(e) { const b = 'ABCD'[e.loesung], ok = Object.entries(e.tipp).filter(([, i]) => i === e.loesung).map(([id]) => api.spieler(id)); ok.forEach(p => api.belohne(p, 30));
        return { text: `Der Schatz lag bei ${b}! ${ok.length} Schatzsucher bekommen 30 🐚`, sag: `Der Schatz lag bei ${b}! ${ok.length} von euch lagen richtig.`, gut: ok.length > 0, extra: { seed: e.seed, loesung: e.loesung } }; },
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
      start(e) { e.ziel = klemme(Math.round(api.likeRate() / 10) * 10, 120, 40000); e.stand = 0; e.dabei = new Set(); return `Strandparty! Liked die Stimmung auf ${zahl(e.ziel)}, dann gibt's ein Feuerwerk!`; },
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
    abstimmung: {
      titel: 'Abstimmung', icon: '🗳️', dauer: 90, moeglich: () => !api.hatProjekt() && api.offeneProjekte().length >= 2,
      start(e) { e.wahl = api.offeneProjekte().sort(() => Math.random() - .5).slice(0, 3); e.st = {};
        return `Abstimmung! Was bauen wir als Nächstes? ${e.wahl.map((w, i) => `${i + 1} für ${w.name}`).join(', ')}.`; },
      kommentar(e, p, t) { if (/^[123]$/.test(t) && +t <= e.wahl.length) { e.st[p.id] = +t - 1; return true; } },
      anzeige: e => { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const m = Math.max(1, ...z); return { text: 'Was bauen wir? Schreib 1, 2 oder 3', balken: e.wahl.map((w, i) => ({ name: `${i + 1}  ${w.name}`, wert: z[i], max: m, farbe: ['#ffd23f', '#7fe0c8', '#ff8fb8'][i] })) }; },
      ende(e) { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const w = e.wahl[z.indexOf(Math.max(...z))]; api.projektStarten(w); return { text: `Entschieden: ${w.name}! Gebaut wird mit der Muschelkasse.`, sag: `Entschieden: Wir bauen ${w.name}!`, gut: true }; },
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
    schatzsuche: e => { const z = [0, 0, 0, 0]; Object.values(e.tipp).forEach(i => z[i]++); const m = z.indexOf(Math.max(...z)); return z[m] ? zufall([`Die meisten tippen auf ${'ABCD'[m]} … aber stimmt das?`, `${'ABCD'[m]} ist gerade beliebt … ich sag nichts!`]) : 'A, B, C oder D? … Wo ist der Schatz?'; },
    zahlenraten: e => e.hinweis ? zufall([`${e.hinweis.replace(/ ⬆️| ⬇️/, '')} … weiter raten!`, `Heiß oder kalt? … ${e.hinweis.replace(/ ⬆️| ⬇️/, '')}!`]) : 'Eine Zahl zwischen eins und hundert … wer traut sich?',
    strandparty: e => e.boom ? 'Die Party kocht! … Weiter so!' : `Noch ${zahl(Math.max(0, e.ziel - e.stand))} Likes … bis zum Feuerwerk!`,
    flaschenpost: () => ['Die Flasche treibt näher … wer schreibt zuerst flasche?', 'Was da wohl drin ist? … Schreibt flasche!', 'Noch hat sie keiner … schnell, flasche schreiben!'],
    moewenalarm: e => [`Noch ${5 - e.faenger.length} Plätze … schreibt fang!`, 'Die Möwe fliegt Kreise … fangt sie!', e.faenger.length ? `${e.faenger.length} haben schon zugegriffen … wer noch?` : 'Noch hat niemand die Möwe erwischt!'],
    meeresbesuch: e => [e.gruss.size ? `Schon ${e.gruss.size} Grüße … schreibt hallo!` : 'Sagt doch mal hallo!', 'Schaut mal, wie schön … so nah an der Insel!', 'Jeder Gruß bringt zehn Muscheln … schreibt hallo!'],
    muschelregen: e => [`Noch ${rest(e)} Sekunden … jedes Like zählt doppelt!`, 'Es regnet Muscheln … jetzt liken lohnt sich doppelt!', 'Die Häuser wachsen gerade doppelt so schnell!'],
    bauturbo: e => [`Noch ${rest(e)} Sekunden Bau-Turbo … dreifache Muscheln!`, 'Die Krabben bauen im Turbo-Tempo!', 'Jetzt liken … dreifach für euer Haus!'],
    sternschnuppe: e => [`${e.wuensche.size} Wünsche … schnell, schreibt wunsch!`, 'Was wünscht ihr euch? … Schreibt wunsch!', 'Augen zu … und wünschen!'],
    abstimmung: e => { const z = e.wahl.map(() => 0); Object.values(e.st).forEach(i => z[i]++); const m = z.indexOf(Math.max(...z)), sum = z.reduce((a, b) => a + b, 0);
      if (!sum) return ['Was sollen wir bauen? … 1, 2 oder 3!', `${e.wahl.map((w, i) => `${i + 1} … ${w.name}`).join(', ')}. … Ihr entscheidet!`];
      const zweit = z.map((v, i) => [v, i]).sort((a, b) => b[0] - a[0])[1];
      return [`${e.wahl[m].name} liegt vorne … mit ${z[m] === 1 ? 'einer Stimme' : z[m] + ' Stimmen'}!`, sum === 1 ? `Die erste Stimme ist da … für ${e.wahl[m].name}!` : `Schon ${sum} Stimmen … ${e.wahl[m].name} führt!`, zweit && zweit[0] ? `${e.wahl[zweit[1]].name} ist dicht dran … noch ist alles offen!` : `Wer stimmt noch ab? … 1, 2 oder 3!`, `Noch ${rest(e)} Sekunden … stimmt ab!`]; },
  };

  function starte(id) {
    const d = DEFS[id]; ev = { id, d, t0: Date.now(), ende: Date.now() + d.dauer * 1000 }; ergebnis = null;
    const ansage = d.start(ev); verlauf = [id, ...verlauf].slice(0, 6);
    api.sende({ typ: 'eventStart', id });
    api.sag(ansage, 0); api.zustand();
  }
  function beende() {
    const r = ev.d.ende(ev) || {}; ergebnis = { ...r, titel: ev.titel || ev.d.titel, icon: ev.icon || ev.d.icon, id: ev.id, bis: Date.now() + 9000 };
    api.sende({ typ: 'eventEnde', id: ev.id, gut: !!r.gut, spielerId: r.id });
    if (r.sag) api.sag(r.sag, 0);
    ev = null; naechstes = Date.now() + MIN - 10000; api.zustand();
  }
  function waehle() {
    const moegl = Object.keys(DEFS).filter(id => !verlauf.slice(0, 4).includes(id) && (!DEFS[id].moeglich || DEFS[id].moeglich()));
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
    api.sende({ typ: 'show', art, id: p.id, name: p.name, gift, anzahl, coins });
  }

  return {
    like(p, n) { if (ev?.d.like) ev.d.like(ev, p, n); return ev?.d.faktor || 1; },
    kommentar(p, t) { return !!(ev?.d.kommentar && ev.d.kommentar(ev, p, t)); },
    geschenkShow,
    naechstesIn: () => ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)),
    oeffentlich() {
      const a = ev ? { id: ev.id, titel: ev.titel || ev.d.titel, icon: ev.icon || ev.d.icon, rest: Math.max(0, Math.round((ev.ende - Date.now()) / 1000)), dauer: ev.d.dauer, faktor: ev.d.faktor || 1, ...ev.d.anzeige(ev) } : null;
      return { event: a, ergebnis: ergebnis && { titel: ergebnis.titel, icon: ergebnis.icon, text: ergebnis.text, id: ergebnis.id, gut: !!ergebnis.gut, extra: ergebnis.extra }, eventIn: ev ? 0 : Math.max(0, Math.round((naechstes - Date.now()) / 1000)) };
    },
    laeuft: () => !!ev,
    liveSatz() {                                          // abwechslungsreich: nie derselbe Satz wie zuletzt
      if (!ev || ev.frueh || rest(ev) <= 3 || !LIVE[ev.id]) return null;
      const opts = [].concat(LIVE[ev.id](ev)).filter(x => x && x !== ev.letzterLive);
      if (!opts.length) return null; ev.letzterLive = zufall(opts); return ev.letzterLive;
    },
    restSek: () => ev ? rest(ev) : null,
    starte(id) { if (ev) beende(); ergebnis = null; starte(id); },   // nur für den Test-Modus
  };
}
