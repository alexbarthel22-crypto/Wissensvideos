// Text für die Stimme vorbereiten (gilt für Leda/Gemini, Chirp, Kerstin und die Mac-Stimme):
// • Zahlen als Wörter („50.“ würde sonst als „fünfzigste“ gelesen, „1.234“ falsch betont)
// • keine Satzzeichen am Anfang eines Stücks (sonst liest die Stimme „Ausrufezeichen“ vor)
const EINS = ['null', 'eins', 'zwei', 'drei', 'vier', 'fünf', 'sechs', 'sieben', 'acht', 'neun', 'zehn', 'elf', 'zwölf', 'dreizehn', 'vierzehn', 'fünfzehn', 'sechzehn', 'siebzehn', 'achtzehn', 'neunzehn'];
const ZEHN = ['', '', 'zwanzig', 'dreißig', 'vierzig', 'fünfzig', 'sechzig', 'siebzig', 'achtzig', 'neunzig'];
function unter100(n) { if (n < 20) return EINS[n]; const e = n % 10, z = Math.floor(n / 10); return e ? (e === 1 ? 'ein' : EINS[e]) + 'und' + ZEHN[z] : ZEHN[z]; }
function unter1000(n) { const h = Math.floor(n / 100), r = n % 100; return (h ? (h === 1 ? '' : EINS[h]) + 'hundert' : '') + (r ? unter100(r) : ''); }
export function zahlWort(n) {
  n = Math.floor(Math.abs(n)); if (n === 0) return 'null';
  if (n >= 1e9) return String(n);
  const mio = Math.floor(n / 1e6), tsd = Math.floor((n % 1e6) / 1000), rest = n % 1000;
  let s = '';
  if (mio) s += (mio === 1 ? 'eine Million' : unter1000(mio) + ' Millionen') + (tsd || rest ? ' ' : '');
  if (tsd) s += (tsd === 1 ? '' : unter1000(tsd)) + 'tausend';
  if (rest) s += unter1000(rest);
  return s.replace(/eins(tausend|hundert)/g, 'ein$1');
}
export function sprechText(t) {
  return String(t || '')
    .replace(/\d{1,3}(?:\.\d{3})+(?!\d)|\d+/g, m => zahlWort(+m.replace(/\./g, '')))   // 1.234 → eintausendzweihundertvierunddreißig
    .replace(/^[\s,.!?…:;–-]+/, '')                                                      // nichts Vorlesbares am Anfang
    .replace(/\s+([,.!?])/g, '$1').replace(/\s{2,}/g, ' ').trim();
}
