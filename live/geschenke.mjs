// TikTok-Geschenke auf Deutsch – mit Geschlecht und Mehrzahl, damit Anna richtig spricht:
// „Danke für die Rose“, „für den Löwen“, „für das Parfüm“, „für 3 Rosen“.
// Format: englischer TikTok-Name (klein) → [deutscher Name, Geschlecht m/w/s, Mehrzahl, Akkusativ (nur wenn anders)]
const LISTE = {
  'rose': ['Rose', 'w', 'Rosen'],
  'tiktok': ['TikTok', 's', 'TikToks'],
  'finger heart': ['Fingerherz', 's', 'Fingerherzen'],
  'heart me': ['Herz für dich', 's', 'Herzen für dich'],
  'hearts': ['Herzen', 'p', 'Herzen'],
  'heart': ['Herz', 's', 'Herzen'],
  'love you': ['Ich liebe dich', 's', 'Ich liebe dich'],
  'gg': ['GG', 's', 'GGs'],
  'ice cream cone': ['Eistüte', 'w', 'Eistüten'],
  'ice cream': ['Eis', 's', 'Eis'],
  'doughnut': ['Donut', 'm', 'Donuts'],
  'donut': ['Donut', 'm', 'Donuts'],
  'perfume': ['Parfüm', 's', 'Parfüms'],
  'hand hearts': ['Handherzen', 'p', 'Handherzen'],
  'hand heart': ['Handherz', 's', 'Handherzen'],
  'sunglasses': ['Sonnenbrille', 'w', 'Sonnenbrillen'],
  'confetti': ['Konfetti', 's', 'Konfetti'],
  'money gun': ['Geldpistole', 'w', 'Geldpistolen'],
  'corgi': ['Corgi', 'm', 'Corgis'],
  'galaxy': ['Galaxie', 'w', 'Galaxien'],
  'lion': ['Löwe', 'm', 'Löwen', 'Löwen'],
  'tiktok universe': ['TikTok-Universum', 's', 'TikTok-Universen'],
  'universe': ['Universum', 's', 'Universen'],
  'universe+': ['Universum plus', 's', 'Universum plus'],
  'whale diving': ['Wal-Tauchgang', 'm', 'Wal-Tauchgänge'],
  'private jet': ['Privatjet', 'm', 'Privatjets'],
  'fire phoenix': ['Feuerphönix', 'm', 'Feuerphönixe'],
  'pegasus': ['Pegasus', 'm', 'Pegasusse'],
  'tiktok stars': ['TikTok-Sterne', 'p', 'TikTok-Sterne'],
  'swan': ['Schwan', 'm', 'Schwäne'],
  'train': ['Zug', 'm', 'Züge'],
  'sports car': ['Sportwagen', 'm', 'Sportwagen'],
  'motorcycle': ['Motorrad', 's', 'Motorräder'],
  'rocket': ['Rakete', 'w', 'Raketen'],
  'hat and mustache': ['Hut mit Schnurrbart', 'm', 'Hüte mit Schnurrbart'],
  'cap': ['Kappe', 'w', 'Kappen'],
  'mic': ['Mikrofon', 's', 'Mikrofone'],
  'paper crane': ['Papierkranich', 'm', 'Papierkraniche'],
  'little crown': ['Krönchen', 's', 'Krönchen'],
  'crown': ['Krone', 'w', 'Kronen'],
  'wishing bottle': ['Wunschflasche', 'w', 'Wunschflaschen'],
  'butterfly': ['Schmetterling', 'm', 'Schmetterlinge'],
  'star': ['Stern', 'm', 'Sterne'],
  'balloon': ['Ballon', 'm', 'Ballons'],
  'cake': ['Kuchen', 'm', 'Kuchen'],
  'birthday cake': ['Geburtstagskuchen', 'm', 'Geburtstagskuchen'],
  'coffee': ['Kaffee', 'm', 'Kaffees'],
  'teddy bear': ['Teddybär', 'm', 'Teddybären', 'Teddybären'],
  'panda': ['Panda', 'm', 'Pandas', 'Panda'],
  'cat': ['Katze', 'w', 'Katzen'],
  'dog': ['Hund', 'm', 'Hunde'],
  'unicorn': ['Einhorn', 's', 'Einhörner'],
  'unicorn fantasy': ['Einhorn-Traum', 'm', 'Einhorn-Träume'],
  'castle': ['Schloss', 's', 'Schlösser'],
  'yacht': ['Yacht', 'w', 'Yachten'],
  'diamond': ['Diamant', 'm', 'Diamanten', 'Diamanten'],
  'diamond ring': ['Diamantring', 'm', 'Diamantringe'],
  'gold mine': ['Goldmine', 'w', 'Goldminen'],
  'fireworks': ['Feuerwerk', 's', 'Feuerwerke'],
  'rainbow': ['Regenbogen', 'm', 'Regenbögen'],
  'sun': ['Sonne', 'w', 'Sonnen'],
  'lollipop': ['Lolli', 'm', 'Lollis'],
  'kiss': ['Kuss', 'm', 'Küsse'],
  'thumbs up': ['Daumen hoch', 'm', 'Daumen hoch'],
  'cheer you up': ['Aufmunterung', 'w', 'Aufmunterungen'],
  'gamepad': ['Gamepad', 's', 'Gamepads'],
  'rosa': ['Rosa', 'w', 'Rosas'],
  'flower': ['Blume', 'w', 'Blumen'],
  'bouquet': ['Blumenstrauß', 'm', 'Blumensträuße'],
  'airplane': ['Flugzeug', 's', 'Flugzeuge'],
  'concert': ['Konzert', 's', 'Konzerte'],
  'interstellar': ['Weltraumreise', 'w', 'Weltraumreisen'],
  'sunset speedway': ['Sonnenuntergangs-Rennen', 's', 'Sonnenuntergangs-Rennen'],
};
const ART = { m: ['der', 'den', 'ein', 'einen'], w: ['die', 'die', 'eine', 'eine'], s: ['das', 'das', 'ein', 'ein'], p: ['die', 'die', '', ''] };

// Liefert alle Formen für Sätze: name, mehr, fuerDen ("für den Löwen"), einAkk ("einen Löwen"), einNom ("ein Löwe")
export function geschenkFormen(englisch, anzahl = 1) {
  if (!String(englisch || '').trim()) {                           // kein Name übermittelt: neutral „dein Geschenk“
    return anzahl > 1 ? { name: 'Geschenke', anzeige: `${anzahl} Geschenke`, fuer: `deine ${anzahl} Geschenke`, einAkk: `${anzahl} Geschenke`, einNom: `${anzahl} Geschenke` }
      : { name: 'Geschenk', anzeige: 'Geschenk', fuer: 'dein Geschenk', einAkk: 'ein Geschenk', einNom: 'ein Geschenk' };
  }
  const e = LISTE[String(englisch || '').toLowerCase().trim()];
  const [name, g, mehr, akk] = e || [String(englisch || 'Geschenk'), 's', String(englisch || 'Geschenke')];
  const a = ART[g], plural = anzahl > 1 || g === 'p';
  if (!e) {                                                       // unbekanntes Geschenk: neutral umschreiben
    return { name, anzeige: anzahl > 1 ? `${anzahl}× ${name}` : name,
      fuer: anzahl > 1 ? `${anzahl} Geschenke „${name}“` : `das Geschenk „${name}“`, einAkk: anzahl > 1 ? `${anzahl} Geschenke „${name}“` : `ein Geschenk „${name}“`, einNom: anzahl > 1 ? `${anzahl} Geschenke „${name}“` : `ein Geschenk „${name}“` };
  }
  if (anzahl > 1) return { name, anzeige: `${anzahl} ${mehr}`, fuer: `${anzahl} ${mehr}`, einAkk: `${anzahl} ${mehr}`, einNom: `${anzahl} ${mehr}` };
  if (plural) return { name, anzeige: name, fuer: `die ${name}`, einAkk: name, einNom: name };
  return { name, anzeige: name, fuer: `${a[1]} ${akk || name}`, einAkk: `${a[3]} ${akk || name}`, einNom: `${a[2]} ${name}` };
}
