// Leuchtturm-Rennen – 45 weitere Events (zusammen mit events.mjs: 60). Alles läuft über den Chat.
// Bausteine: Schnellste (die ersten N), Gemeinschafts-Ziel, Emoji, Quiz, Städte-Spiele, Duelle, Glück, Spezial.
import { normal } from './filter.mjs';

export function extraEvents(api, h) {
  const { zufall, wortGleich, listeTxt, anz, stadtVon } = h;
  const klein = t => String(t || '').toLowerCase().trim();
  const D = {}, P = {};
  const name = p => api.name(p);

  // ---------- A) Die Schnellsten: die ersten N mit dem Wort bringen ihrer Stadt Meter ----------
  const schnell = (id, titel, icon, wort, ansage, meter = 12, n = 5) => {
    D[id] = { titel, icon,
      start(e) { e.s = []; return `${ansage} Die ersten ${n === 5 ? 'fünf' : n} bringen ihrer Stadt ${meter} Meter!`; },
      kommentar(e, p, t) { if (!wortGleich(t, wort) || klein(t).length > wort.length + 6) return; if (!e.s.includes(p) && e.s.length < n) { e.s.push(p); api.turmWachsen(p.stadt, meter, p); if (e.s.length >= n) e.frueh = true; } return true; },
      anzeige: e => ({ text: `Schreib „${wort}“! Die ersten ${n} bringen ihrer Stadt +${meter} m  (${e.s.length}/${n})` }),
      ende: e => e.s.length ? { text: `Am schnellsten: ${e.s.map(p => p.stadt ? `${p.name} (${p.stadt})` : p.name).join(', ')}`, sag: `Am schnellsten war ${name(e.s[0])}!`, gut: true } : { text: 'Diesmal war niemand dabei.' } };
    P[id] = `Die ersten ${n} bringen ihrer Stadt je ${meter} Meter.`;
  };
  schnell('ahoi', 'Ahoi-Ruf', '⚓', 'ahoi', 'Ahoi-Ruf! Schreibt ahoi in den Chat!');
  schnell('anker', 'Anker werfen', '⚓', 'anker', 'Anker werfen! Schreibt Anker in den Chat!');
  schnell('moewe', 'Möwen-Ruf', '🐦', 'kreisch', 'Möwen-Ruf! Schreibt kreisch, so laut wie eine Möwe!');
  schnell('kompass', 'Kompass', '🧭', 'norden', 'Kompass-Runde! Wo zeigt die Nadel hin? Schreibt Norden!');
  schnell('leinenlos', 'Leinen los', '⛵', 'leinen los', 'Leinen los! Schreibt leinen los in den Chat!', 15);
  schnell('rettungsring', 'Mann über Bord', '🛟', 'ring', 'Mann über Bord! Werft den Rettungsring, schreibt Ring!');
  schnell('fernrohr', 'Fernrohr', '🔭', 'land in sicht', 'Schaut durchs Fernrohr! Schreibt land in sicht!', 15);
  schnell('schatzkarte', 'Schatzkarte', '🗺️', 'schatz', 'Eine Schatzkarte ist angespült! Schreibt Schatz!');

  // ---------- B) Gemeinschafts-Ziel: schaffen genug Leute das Wort, bekommen alle ihre Städte Meter ----------
  const ziel = (id, titel, icon, wort, ansage, zielN, meter) => {
    D[id] = { titel, icon,
      start(e) { e.w = new Map(); return `${ansage} Schaffen wir ${zielN} Leute, bekommen alle ihre Städte ${meter} Meter!`; },
      kommentar(e, p, t) { if (!wortGleich(t, wort) || klein(t).length > wort.length + 6) return; e.w.set(p.id, p); return true; },
      anzeige: e => ({ text: `Schreib „${wort}“! Gemeinsam ${zielN} Leute schaffen!`, balken: [{ name: `${icon} Mitmacher`, wert: e.w.size, max: zielN, farbe: '#57b85a' }] }),
      ende(e) { if (e.w.size >= zielN) { const st = new Set([...e.w.values()].map(p => p.stadt).filter(Boolean)); st.forEach(s => api.turmWachsen(s, meter)); return { text: `Geschafft – ${e.w.size} Leute! ${anz(st.size, 'Stadt bekommt', 'Städte bekommen')} +${meter} m`, sag: 'Geschafft! Gemeinsam seid ihr unschlagbar!', gut: true }; }
        return { text: `${e.w.size} von ${zielN} – knapp daneben!`, sag: 'Knapp daneben! Beim nächsten Mal klappt es!' }; } };
    P[id] = `Bei ${zielN} Leuten bekommen alle ihre Städte ${meter} Meter.`;
  };
  ziel('laternen', 'Laternen-Kette', '🏮', 'licht', 'Laternen-Kette! Schreibt Licht und zündet eine Laterne an!', 10, 10);
  ziel('olawelle', 'La-Ola-Welle', '🌊', 'ola', 'La-Ola-Welle über alle Inseln! Schreibt ola!', 15, 8);
  ziel('feuerwerk', 'Feuerwerk', '🎆', 'boom', 'Feuerwerk über dem Meer! Schreibt boom!', 12, 10);
  ziel('rueckenwind', 'Rückenwind', '💨', 'wind', 'Rückenwind für alle! Schreibt Wind!', 10, 8);
  ziel('seemannschor', 'Seemanns-Chor', '🎶', 'hoho', 'Seemanns-Chor! Singt mit, schreibt hoho!', 10, 10);

  // ---------- C) Emoji-Runden: jeder einmal, mit dem passenden Emoji ----------
  const emoji = (id, titel, zeichen, ansage, meter = 3) => {
    D[id] = { titel, icon: zeichen,
      start(e) { e.w = new Set(); return `${ansage} Jeder bringt seiner Stadt ${meter} Meter!`; },
      kommentar(e, p, t) { if (!String(t).includes(zeichen)) return; if (!e.w.has(p.id)) { e.w.add(p.id); api.turmWachsen(p.stadt, meter, p); } return true; },
      anzeige: e => ({ text: `Schreib ${zeichen} in den Chat! Jeder einmal +${meter} m  (${e.w.size} dabei)` }),
      ende: e => e.w.size ? { text: `${anz(e.w.size, 'Person hat', 'Leute haben')} mitgemacht!`, sag: 'Wunderschön! Danke fürs Mitmachen!', gut: true } : { text: 'Diesmal blieb es ruhig.' } };
    P[id] = `Jeder bringt seiner Stadt einmal ${meter} Meter.`;
  };
  emoji('fischschwarm', 'Fischschwarm', '🐟', 'Ein Fischschwarm zieht vorbei! Schreibt einen Fisch, also das Fisch-Emoji!');
  emoji('sternenhimmel', 'Sternenhimmel', '⭐', 'Sternenhimmel über dem Meer! Schreibt einen Stern in den Chat!');
  emoji('delfinshow', 'Delfin-Show', '🐬', 'Delfin-Show! Schreibt das Delfin-Emoji in den Chat!');
  emoji('muschelsuche', 'Muschelsuche', '🐚', 'Muschelsuche am Strand! Schreibt das Muschel-Emoji in den Chat!');

  // ---------- D) Quiz: die ersten fünf Richtigen ----------
  const quiz = (id, titel, icon, fragen, meter = 10) => {
    D[id] = { titel, icon,
      start(e) { e.f = typeof fragen === 'function' ? fragen() : zufall(fragen); e.s = []; return `${titel}! ${e.f[0]} Die ersten fünf Richtigen bringen ihrer Stadt ${meter} Meter!`; },
      kommentar(e, p, t) { const a = [].concat(e.f[1]); if (!a.some(x => wortGleich(t, x) && klein(t).length <= String(x).length + 4)) return; if (!e.s.includes(p) && e.s.length < 5) { e.s.push(p); api.turmWachsen(p.stadt, meter, p); if (e.s.length >= 5) e.frueh = true; } return true; },
      anzeige: e => ({ text: `${e.f[0]}  (${e.s.length}/5 richtig)` }),
      ende: e => { const l = [].concat(e.f[1])[0], L = String(l).charAt(0).toUpperCase() + String(l).slice(1); return e.s.length ? { text: `Richtig: ${L}! Am schnellsten: ${e.s.map(p => p.name).join(', ')}`, sag: `Richtig! Am schnellsten war ${name(e.s[0])}!`, gut: true } : { text: `Lösung: ${L}`, sag: 'Diesmal hatte es niemand.' }; } };
    P[id] = `Die ersten fünf Richtigen bringen ihrer Stadt ${meter} Meter.`;
  };
  quiz('hauptstadtquiz', 'Hauptstadt-Quiz', '🏛️', [['Was ist die Hauptstadt von Deutschland?', 'berlin'], ['Was ist die Hauptstadt von Österreich?', 'wien'], ['Was ist die Hauptstadt der Schweiz?', 'bern'],
    ['Was ist die Hauptstadt von Frankreich?', 'paris'], ['Was ist die Hauptstadt von Italien?', 'rom'], ['Was ist die Hauptstadt von Spanien?', 'madrid'], ['Was ist die Hauptstadt von Bayern?', 'münchen'],
    ['Was ist die Hauptstadt von Sachsen?', 'dresden'], ['Was ist die Hauptstadt von Niedersachsen?', 'hannover'], ['Was ist die Hauptstadt von Tirol?', 'innsbruck'], ['Was ist die Hauptstadt der Steiermark?', 'graz'], ['Was ist die Hauptstadt von England?', 'london']]);
  quiz('meerestierquiz', 'Meerestier-Quiz', '🐙', [['Wie viele Arme hat ein Oktopus?', ['acht', '8']], ['Welches Tier ist das größte der Welt?', ['blauwal', 'wal']], ['Welches Meerestier hat einen Panzer und legt Eier am Strand?', ['schildkröte', 'schildkroete']],
    ['Welcher Fisch hat eine Rückenflosse und viele scharfe Zähne?', 'hai'], ['Welches Tier hat fünf Arme und liegt am Strand?', 'seestern'], ['Welches Meerestier läuft seitwärts?', 'krabbe'], ['Welcher Vogel kreischt am Hafen?', 'möwe']]);
  quiz('matheblitz', 'Mathe-Blitz', '➕', () => { const a = 2 + Math.floor(Math.random() * 18), b = 2 + Math.floor(Math.random() * 9); return [`Was ist ${a} plus ${b}?`, String(a + b)]; });
  quiz('flussquiz', 'Fluss-Quiz', '🏞️', [['Welcher Fluss fließt durch Köln?', 'rhein'], ['Welcher Fluss fließt durch Hamburg?', 'elbe'], ['Welcher Fluss fließt durch Wien?', 'donau'], ['Welcher Fluss fließt durch Berlin?', 'spree'],
    ['Welcher Fluss fließt durch München?', 'isar'], ['Welcher Fluss fließt durch Frankfurt?', 'main'], ['Welcher Fluss fließt durch Dresden?', 'elbe'], ['Welcher Fluss fließt durch Düsseldorf?', 'rhein']]);
  quiz('farbenquiz', 'Farben-Quiz', '🎨', [['Welche Farbe hat eine Banane?', 'gelb'], ['Welche Farbe hat Gras?', 'grün'], ['Welche Farbe hat Schnee?', 'weiß'], ['Welche Farbe hat ein Flamingo?', ['rosa', 'pink']],
    ['Welche Farbe hat das Meer auf Karten?', 'blau'], ['Welche Farbe hat eine Tomate?', 'rot'], ['Welche Farbe hat eine Orange?', 'orange']]);
  quiz('raetsel', 'Rätsel-Runde', '❓', [['Wie viele Tage hat eine Woche?', ['sieben', '7']], ['Was hat Zähne, beißt aber nicht?', 'kamm'], ['Was wird nass, während es trocknet?', 'handtuch'],
    ['Wie viele Beine hat eine Spinne?', ['acht', '8']], ['Was leuchtet nachts den Schiffen den Weg?', 'leuchtturm'], ['Wie viele Monate hat ein Jahr?', ['zwölf', '12']]]);
  const SALAT = ['hamburg', 'berlin', 'münchen', 'köln', 'wien', 'zürich', 'bremen', 'dresden', 'leipzig', 'hannover', 'salzburg', 'stuttgart'];
  quiz('buchstabensalat', 'Buchstabensalat', '🔤', () => { const w = zufall(SALAT); let m; do { m = [...w].sort(() => Math.random() - .5).join(''); } while (m === w); return [`Welche Stadt ist das: ${m.toUpperCase().split('').join(' ')}?`, w]; });
  quiz('emojiraetsel', 'Emoji-Rätsel', '🧩', [['Welche Stadt ist das: Bier, Brezel und Oktoberfest?', 'münchen'], ['Welche Stadt ist das: Hafen, Fischbrötchen und Elbe?', 'hamburg'], ['Welche Stadt ist das: Bär und Brandenburger Tor?', 'berlin'],
    ['Welche Stadt ist das: Riesenrad, Prater und Sachertorte?', 'wien'], ['Welche Stadt ist das: Dom und Karneval?', 'köln'], ['Welche Stadt ist das: Mozart und Festspiele?', 'salzburg'], ['Welche Stadt ist das: Stadtmusikanten?', 'bremen']]);

  // ---------- E) Städte-Spiele: die geschriebene Stadt ist die Antwort ----------
  const stadtSpiel = (id, titel, icon, start, pruefe, anzeigeT, preis) => {
    D[id] = { titel, icon, stadt: true, start,
      kommentar(e, p, t) { const st = api.stadtAus(t); if (!st) return; return pruefe(e, p, st) !== false; },
      anzeige: e => ({ text: anzeigeT(e) }),
      ende: e => e.l.length ? { text: `Dabei: ${listeTxt(e.l.slice(0, 6))}${e.l.length > 6 ? ' …' : ''}`, sag: 'Starke Runde!', gut: true } : { text: 'Diesmal hat es niemand geschafft.' } };
    P[id] = preis;
  };
  const BUCHST = 'BDFHKLMSW';
  stadtSpiel('buchstabenjagd', 'Buchstaben-Jagd', '🔠', e => { e.b = zufall([...BUCHST]); e.l = []; return `Buchstaben-Jagd! Schreibt Städte mit ${e.b} am Anfang! Jede bekommt fünf Meter!`; },
    (e, p, st) => { if (!st.toUpperCase().startsWith(e.b) || e.l.includes(st)) return; e.l.push(st); api.stadtNeu(st, p); api.turmWachsen(st, 5, p); }, e => `Städte mit ${e.b}… schreiben! Jede +5 m  (${e.l.length} gefunden)`, 'Jede passende Stadt bekommt fünf Meter.');
  stadtSpiel('langenamen', 'Lange Namen', '📏', e => { e.l = []; return 'Lange Namen! Schreibt Orte mit mindestens neun Buchstaben! Jeder bekommt sechs Meter!'; },
    (e, p, st) => { if (st.replace(/[^\p{L}]/gu, '').length < 9 || e.l.includes(st)) return; e.l.push(st); api.stadtNeu(st, p); api.turmWachsen(st, 6, p); }, e => `Orte mit 9+ Buchstaben! Jeder +6 m  (${e.l.length} gefunden)`, 'Jeder lange Ortsname bekommt sechs Meter.');
  stadtSpiel('staedtekette', 'Städte-Kette', '🔗', e => { e.l = []; e.z = 'A'; return 'Städte-Kette! Die nächste Stadt muss mit dem letzten Buchstaben der vorherigen anfangen. Wir starten mit A! Jedes Glied bringt acht Meter!'; },
    (e, p, st) => { if (!st.toUpperCase().startsWith(e.z) || e.l.includes(st)) return; e.l.push(st); e.z = st.replace(/[^\p{L}]/gu, '').slice(-1).toUpperCase(); api.stadtNeu(st, p); api.turmWachsen(st, 8, p); }, e => `Nächste Stadt mit „${e.z}“!  (Kette: ${e.l.length})`, 'Jedes Glied der Kette bringt acht Meter.');
  stadtSpiel('dorfpower', 'Dorf-Power', '🏡', e => { e.l = []; return 'Dorf-Power! Jetzt zählen die kleinen Orte! Jeder Ort unter hundert Metern bekommt zehn Meter!'; },
    (e, p, st) => { const s = api.stadt(st); if ((s?.stock || 0) >= 100 || e.l.includes(st)) return; e.l.push(st); api.stadtNeu(st, p); api.turmWachsen(st, 10, p); }, e => `Kleine Orte schreiben! Unter 100 m: +10 m  (${e.l.length} Orte)`, 'Jeder Ort unter hundert Metern bekommt zehn Meter.');
  stadtSpiel('freundschaft', 'Städte-Freundschaft', '🤝', e => { e.l = []; e.p = new Set(); return 'Städte-Freundschaft! Schreibt zwei Städte in einen Kommentar! Beide bekommen drei Meter!'; },
    () => false, e => `Zwei Städte in einen Kommentar! Beide +3 m  (${e.p.size} Freundschaften)`, 'Beide Städte bekommen drei Meter.');
  D.freundschaft.kommentar = (e, p, t) => { const w = String(t).split(/\s*(?:und|&|\+|,|\/)\s*/i); if (w.length < 2) return; const a = api.stadtAus(w[0]), b = api.stadtAus(w.slice(1).join(' ')); if (!a || !b || a === b) return;
    const k = [a, b].sort().join('+'); if (!e.p.has(k + p.id)) { e.p.add(k + p.id); for (const s of [a, b]) { api.stadtNeu(s, p); api.turmWachsen(s, 3, p); if (!e.l.includes(s)) e.l.push(s); } } return true; };
  stadtSpiel('grenzenlos', 'Grenzenlos', '🌍', e => { e.l = []; e.p = new Set(); return 'Grenzenlos! Schreibt eine Stadt aus einem anderen Land als eurem! Beide Städte bekommen fünf Meter!'; },
    (e, p, st) => { const h = stadtVon(p), s = api.stadt(st); if (!h || !s || s.land === h.land || e.p.has(p.id)) return; e.p.add(p.id); api.turmWachsen(st, 5, p); api.turmWachsen(h.name, 5, p); if (!e.l.includes(st)) e.l.push(st); },
    e => `Stadt aus einem anderen Land schreiben! Beide +5 m  (${e.p.size} dabei)`, 'Beide Städte bekommen fünf Meter.');
  D.rettetletzten = { titel: 'Rettet den Letzten', icon: '🆘', stadt: true, moeglich: () => api.staedte().length >= 6,
    start(e) { const l = api.staedte().slice(0, 20); e.ziel = l[l.length - 1].name; e.w = new Set(); return `Rettet den Letzten! ${e.ziel} braucht Hilfe! Schreibt ${e.ziel} in den Chat, jeder Helfer bringt drei Meter!`; },
    kommentar(e, p, t) { if (api.stadtAus(t) !== e.ziel) return; if (!e.w.has(p.id)) { e.w.add(p.id); api.turmWachsen(e.ziel, 3, p); } return true; },
    anzeige: e => ({ text: `Schreib „${e.ziel}“! Jeder Helfer +3 m`, balken: [{ name: '🆘 Helfer', wert: e.w.size, max: Math.max(10, e.w.size), farbe: '#ff8a2a' }] }),
    ende: e => e.w.size ? { text: `${e.ziel} wurde gerettet – ${anz(e.w.size, 'Helfer', 'Helfer')}!`, sag: `${e.ziel} ist gerettet!`, gut: true, stadt: e.ziel } : { text: `${e.ziel} wartet noch auf Hilfe …` } };
  P.rettetletzten = 'Jeder Helfer bringt drei Meter.';
  D.anfeuern = { titel: 'Anfeuer-Runde', icon: '📣', stadt: true, moeglich: () => api.staedte().length >= 4,
    start(e) { const l = api.staedte().slice(3, 15); e.ziel = zufall(l.length ? l : api.staedte()).name; e.w = new Set(); return `Anfeuer-Runde für ${e.ziel}! Schreibt ${e.ziel} in den Chat, jeder bringt zwei Meter!`; },
    kommentar(e, p, t) { if (api.stadtAus(t) !== e.ziel) return; if (!e.w.has(p.id)) { e.w.add(p.id); api.turmWachsen(e.ziel, 2, p); } return true; },
    anzeige: e => ({ text: `📣 Feuert ${e.ziel} an! Jeder +2 m`, balken: [{ name: '📣 Fans', wert: e.w.size, max: Math.max(10, e.w.size), farbe: '#9b5de5' }] }),
    ende: e => e.w.size ? { text: `${anz(e.w.size, 'Fan', 'Fans')} für ${e.ziel}!`, sag: `Was für eine Stimmung für ${e.ziel}!`, gut: true, stadt: e.ziel } : { text: 'Leise Runde …' } };
  P.anfeuern = 'Jeder Fan bringt zwei Meter.';

  // ---------- F) Duelle: zwei Lager, wer hat mehr Leute im Chat? ----------
  const duell = (id, titel, icon, ansage, lager, namen, meter, moeglich) => {
    D[id] = { titel, icon, moeglich,
      start(e) { e.w = { a: new Set(), b: new Set() }; e.ziel = typeof namen === 'function' ? namen() : namen; return `${ansage} Welche Seite hat mehr Leute im Chat? Alle Städte der Sieger bekommen ${meter} Meter!`; },
      kommentar(e, p) { const s = stadtVon(p); const k = s && lager(s, e); if (k) e.w[k].add(p.id); return false; },
      anzeige: e => { const a = e.w.a.size, b = e.w.b.size, m = Math.max(1, a, b); return { text: `${e.ziel[0]} gegen ${e.ziel[1]}! Schreib in den Chat!`, balken: [{ name: e.ziel[0], wert: a, max: m, farbe: '#3fa0e8' }, { name: e.ziel[1], wert: b, max: m, farbe: '#ff8fb8' }] }; },
      ende(e) { const a = e.w.a.size, b = e.w.b.size; if (a === b) return { text: `Unentschieden ${a}:${b}!`, sag: 'Unentschieden!' }; const k = a > b ? 'a' : 'b', st = new Set([...e.w[k]].map(id => api.spieler(id)?.stadt).filter(Boolean)); st.forEach(s => api.turmWachsen(s, meter));
        const n = e.ziel[k === 'a' ? 0 : 1]; return { text: `${n} gewinnt ${Math.max(a, b)}:${Math.min(a, b)}! ${anz(st.size, 'Stadt bekommt', 'Städte bekommen')} +${meter} m`, sag: `${n.replace(/^\S+\s/, '')} gewinnt!`, gut: true }; } };
    P[id] = `Alle Städte der Sieger bekommen ${meter} Meter.`;
  };
  duell('nordsued', 'Nord gegen Süd', '🧭', 'Nord gegen Süd!', s => s.lat == null ? null : s.lat >= 50.5 ? 'a' : 'b', ['⬆️ Norden', '⬇️ Süden'], 12);
  duell('ostwest', 'Ost gegen West', '🧭', 'Ost gegen West!', s => s.lng == null ? null : s.lng >= 10.5 ? 'a' : 'b', ['➡️ Osten', '⬅️ Westen'], 12);
  duell('grossklein', 'Groß gegen Klein', '🐘', 'Die großen Türme gegen die kleinen!', s => api.staedte().findIndex(x => x.name === s.name) < 5 ? 'a' : 'b', ['🐘 Top 5', '🐭 Alle anderen'], 10, () => api.staedte().length >= 7);
  D.dreikampf = { titel: 'Dreikampf', icon: '🥇', moeglich: () => api.staedte().length >= 3,
    start(e) { e.st = api.staedte().slice(0, 3).map(s => s.name); e.w = Object.fromEntries(e.st.map(n => [n, new Set()])); api.sende({ typ: 'duell', a: e.st[0], b: e.st[1] }); return `Dreikampf! ${listeTxt(e.st)}! Welche Stadt hat die meisten Leute im Chat? Der Sieger bekommt dreißig Meter!`; },
    kommentar(e, p) { if (p.stadt && e.w[p.stadt]) e.w[p.stadt].add(p.id); return false; },
    anzeige: e => { const m = Math.max(1, ...e.st.map(n => e.w[n].size)); return { text: 'Top 3 – wer hat die meisten Leute im Chat?', balken: e.st.map((n, i) => ({ name: '🗼 ' + n, wert: e.w[n].size, max: m, farbe: ['#ffd23f', '#c0c8d8', '#e0a070'][i] })) }; },
    ende(e) { const [a, b] = [...e.st].sort((x, y) => e.w[y].size - e.w[x].size); if (!e.w[a].size || e.w[a].size === e.w[b].size) return { text: 'Kein klarer Sieger!', sag: 'Kein klarer Sieger!' }; api.turmWachsen(a, 30); return { text: `${a} gewinnt den Dreikampf! +30 m`, sag: `${a} gewinnt den Dreikampf!`, gut: true, stadt: a }; } };
  P.dreikampf = 'Die Siegerstadt bekommt dreißig Meter.';

  // ---------- G) Glück ----------
  const lotto = (id, titel, icon, wort, ansage, preise) => {
    D[id] = { titel, icon,
      start(e) { e.l = new Map(); return ansage; },
      kommentar(e, p, t) { if (!wortGleich(t, wort) || klein(t).length > wort.length + 6) return; if (p.stadt) e.l.set(p.id, p); return true; },
      anzeige: e => ({ text: `Schreib „${wort}“!  (${e.l.size} im Topf)` }),
      ende(e) { const g = [...e.l.values()].sort(() => Math.random() - .5).slice(0, preise.length); if (!g.length) return { text: 'Niemand im Topf …' }; g.forEach((p, i) => api.turmWachsen(p.stadt, preise[i], p));
        return { text: `Gewonnen: ${g.map((p, i) => `${p.name} (+${preise[i]} m)`).join(', ')}`, sag: `Gewonnen hat ${listeTxt(g.map(name))}!`, gut: true }; } };
    P[id] = `Gewinner bringen ihrer Stadt bis zu ${preise[0]} Meter.`;
  };
  lotto('schatzkiste', 'Schatzkiste', '💰', 'auf', 'Eine Schatzkiste! Schreibt auf, um sie zu öffnen! Am Ende gewinnt einer dreißig Meter!', [30]);
  lotto('flaschenpost', 'Flaschenpost', '🍾', 'post', 'Flaschenpost! Schreibt Post, und ihr landet im Topf! Zwei Gewinner bekommen zwanzig und zehn Meter!', [20, 10]);
  D.glueckszahl = { titel: 'Glückszahl', icon: '🍀',
    start(e) { e.z = 1 + Math.floor(Math.random() * 10); e.t = new Map(); return 'Glückszahl! Schreibt eine Zahl von eins bis zehn! Wer die Glückszahl trifft, bringt seiner Stadt fünfzehn Meter!'; },
    kommentar(e, p, t) { const m = klein(t).match(/^(10|[1-9])$/); if (!m) return; if (!e.t.has(p.id)) e.t.set(p.id, +m[1]); return true; },
    anzeige: e => ({ text: `Zahl von 1 bis 10 schreiben!  (${e.t.size} Tipps)` }),
    ende(e) { const g = [...e.t].filter(([, z]) => z === e.z).map(([id]) => api.spieler(id)).filter(p => p?.stadt); g.forEach(p => api.turmWachsen(p.stadt, 15, p));
      return g.length ? { text: `Glückszahl ${e.z}! Getroffen: ${g.slice(0, 6).map(p => p.name).join(', ')}`, sag: `Die Glückszahl war ${e.z}!`, gut: true } : { text: `Die Glückszahl war ${e.z} – niemand hat sie getroffen.`, sag: `Die Glückszahl war ${e.z}!` }; } };
  P.glueckszahl = 'Wer die Glückszahl trifft, bringt seiner Stadt fünfzehn Meter.';
  D.wuerfel = { titel: 'Würfel-Runde', icon: '🎲',
    start(e) { e.w = new Map(); return 'Würfel-Runde! Schreibt würfeln, und eure Stadt bekommt so viele Meter, wie der Würfel zeigt, doppelt!'; },
    kommentar(e, p, t) { if (!wortGleich(t, 'würfeln') && !wortGleich(t, 'wuerfeln')) return; if (!e.w.has(p.id)) { const z = 1 + Math.floor(Math.random() * 6); e.w.set(p.id, z); api.turmWachsen(p.stadt, z * 2, p); } return true; },
    anzeige: e => ({ text: `Schreib „würfeln“! Augenzahl × 2 Meter  (${e.w.size} gewürfelt)` }),
    ende: e => e.w.size ? { text: `${anz(e.w.size, 'Wurf', 'Würfe')} – ${[...e.w.values()].filter(z => z === 6).length}× eine Sechs!`, sag: 'Was für eine Würfel-Runde!', gut: true } : { text: 'Keiner hat gewürfelt.' } };
  P.wuerfel = 'Jeder Wurf bringt Augenzahl mal zwei Meter.';
  D.moewenlotto = { titel: 'Möwen-Lotto', icon: '🐦',
    start(e) { e.z = 1 + Math.floor(Math.random() * 5); e.t = new Map(); return 'Möwen-Lotto! Auf welcher Insel landet die Möwe? Schreibt eine Zahl von eins bis fünf! Richtige Tipps bringen zwölf Meter!'; },
    kommentar(e, p, t) { const m = klein(t).match(/^([1-5])$/); if (!m) return; if (!e.t.has(p.id)) e.t.set(p.id, +m[1]); return true; },
    anzeige: e => ({ text: `Zahl von 1 bis 5 – wo landet die Möwe?  (${e.t.size} Tipps)` }),
    ende(e) { const g = [...e.t].filter(([, z]) => z === e.z).map(([id]) => api.spieler(id)).filter(p => p?.stadt); g.forEach(p => api.turmWachsen(p.stadt, 12, p));
      return { text: `Die Möwe landet auf Insel ${e.z}! ${g.length ? anz(g.length, 'Treffer', 'Treffer') : 'Kein Treffer.'}`, sag: `Die Möwe landet auf Insel ${e.z}!`, gut: g.length > 0 }; } };
  P.moewenlotto = 'Richtige Tipps bringen zwölf Meter.';

  // ---------- H) Spezial ----------
  D.doppelmeter = { titel: 'Doppel-Meter', icon: '✖️', stadt: true,
    start(e) { e.n = 0; return 'Doppel-Meter! Jetzt bringt jede Stadt, die ihr schreibt, zwei Meter statt einem!'; },
    anzeige: e => ({ text: `Jede geschriebene Stadt = +2 m!  (${e.n} m extra)` }),
    ende: e => ({ text: `Doppel-Meter vorbei – ${e.n} Meter extra!`, sag: 'Doppel-Meter vorbei!', gut: e.n > 0 }) };
  P.doppelmeter = 'Jede geschriebene Stadt bringt zwei Meter.';
  D.marathon = { titel: 'Städte-Marathon', icon: '🏃', stadt: true,
    start(e) { e.n = 0; e.st = new Set(); return 'Städte-Marathon! Schreibt so viele Städte wie möglich! Schaffen wir fünfzig, bekommen alle Städte zehn Meter extra!'; },
    kommentar(e, p, t) { const st = api.stadtAus(t); if (!st) return; e.n++; e.st.add(st); return false; },
    anzeige: e => ({ text: 'Städte schreiben! Gemeinsam 50 schaffen!', balken: [{ name: '🏃 Städte geschrieben', wert: e.n, max: 50, farbe: '#57b85a' }] }),
    ende(e) { if (e.n >= 50) { e.st.forEach(s => api.stadt(s) && api.turmWachsen(s, 10)); return { text: `Marathon geschafft! ${e.st.size} Städte +10 m`, sag: 'Marathon geschafft! Unglaublich!', gut: true }; } return { text: `${e.n} von 50 – fast!`, sag: 'Fast geschafft!' }; } };
  P.marathon = 'Bei fünfzig Städten bekommen alle zehn Meter.';
  D.zaehlen = { titel: 'Zählen bis 20', icon: '🔢',
    start(e) { e.z = 0; e.l = new Set(); return 'Wir zählen gemeinsam bis zwanzig! Schreibt die nächste Zahl, wir starten mit eins! Jede richtige Zahl bringt zwei Meter!'; },
    kommentar(e, p, t) { const m = klein(t).match(/^(\d{1,2})$/); if (!m) return; if (+m[1] === e.z + 1) { e.z++; if (p.stadt) { api.turmWachsen(p.stadt, 2, p); e.l.add(p.stadt); } if (e.z >= 20) e.frueh = true; } return true; },
    anzeige: e => ({ text: `Nächste Zahl: ${e.z + 1}`, balken: [{ name: '🔢 Gezählt', wert: e.z, max: 20, farbe: '#3fa0e8' }] }),
    ende(e) { if (e.z >= 20) { e.l.forEach(s => api.turmWachsen(s, 10)); return { text: 'Bis 20 gezählt! Alle Zähler-Städte +10 m', sag: 'Zwanzig! Geschafft!', gut: true }; } return { text: `Bis ${e.z} gezählt!`, sag: `Bis ${e.z} gezählt, stark!` }; } };
  P.zaehlen = 'Jede richtige Zahl bringt zwei Meter.';

  return { D, P };
}
