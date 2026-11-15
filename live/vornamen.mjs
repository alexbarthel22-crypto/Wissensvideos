// Muschel-Tal LIVE – Klarnamen in TikTok-Namen erkennen: „lara91554“, „_44lara_66“, „lara.xo“ → „Lara“.
// Nur echte, häufige Vornamen (Deutschland + international). Nichts gefunden → null.
const LISTE = `
anna lara lea leah lena lina mia emma emilia ella sophia sofia sophie sofie hannah hanna marie maria mila nele luisa louisa clara klara
johanna lilly lilli lili emily amelie greta paula ida frieda frida mathilda matilda charlotte lotta lotte luna zoe zoey nora leonie
helena elena isabella jana julia juli julie laura lisa nina sarah sara selina celina vanessa jessica jasmin yasmin melina melanie michelle
alina aleyna elif zeynep aylin ayla amira lia liya alena antonia carla carlotta carolin caroline katharina kathrin katrin kim lucy lucia
maja maya marlene merle milena miriam nadine natalie nathalie nicole olivia pia rebecca romy ronja rosa ruby sina stella svenja tamara
tina valentina valerie vivien viktoria victoria finja fiona franziska hailey hayley jule josephine joséphine jessy jenny jennifer
annika anika anja andrea angelina ann annabell annabelle anne annie ava bella bianca carina chantal chiara daniela denise diana
dilara elisa eliza ellen emely emmi enya esra eva evelyn fatima feli felicitas fenja greta hilal ines irina isabel isabell jacqueline
janina jasmina joana joanna josie jule kaja kiara kira lana larissa leila leyla liana lilia lisa lou louise lucie luise madita
malia mara marie mariam marina marla martina mayla medina melissa meryem mina mira nadja naomi nela nelly nia noemi noemie
paulina pauline philippa rania rieke sabrina saskia selin seyma shirin sienna svea tabea talia tessa theresa tilda tuana vera
yara yaren ylvi zara zehra lucia mariella
ben paul leon luis louis lukas lucas finn fynn jonas elias noah felix max maximilian henry henri emil anton theo theodor jakob jacob
david liam leo milan moritz niklas nicolas nico tim tom timo jan julian julius samuel simon tobias vincent oskar oscar alexander
alex adrian andreas anton arne benedikt benjamin bastian carl karl christian daniel dennis dominik erik eric fabian florian
frederik friedrich gabriel hannes jannik janik jannis janis jason jonathan joshua justin kai kevin konstantin lars lennard lennart
lenny levi linus lorenz luca lukas malte marc marcel mario marius mark marko markus marvin mats matteo mattis matthias maurice
michael mika mike nils noel ole oliver patrick peter philipp phil rafael raphael robin ruben sebastian stefan steffen sven thomas
till valentin yannick yusuf emir ali can deniz eren mehmet mustafa omar omer ömer said hamza ibrahim ahmed ahmet yasin kerem
aaron alessio amir arda bruno cedric colin dario elia emilio enno ferdinand finnley georg hugo ilyas jamie jayden joel johann
johannes jonah josef joseph karim kilian levin luan lion lio mailo malik mats milo nael nick niko noa
pascal quentin rayan ryan sami sascha tarik tyler ben ian yunus luke jack james john harry charlie george sam
`.split(/\s+/).filter(Boolean);
const NAMEN = new Set(LISTE);
const ANHANG = /^(x|xx|xxx|xo|xd|chen|lein|official|offiziell|tv|live|ttv|yt|tiktok|mausi|maus|baby|bby|love|lover)$/;

export function klarname(benutzer) {
  const roh = String(benutzer || '').replace(/^@/, '').toLowerCase();
  const teile = roh.split(/[^a-zäöüéèçß]+/).filter(t => t.length >= 2);
  for (const t0 of teile) {
    const t = t0.replace(/^x{2,}|x{2,}$/g, '') || t0;            // „xxlea“ → „lea“
    if (NAMEN.has(t)) return gross(t);
    // „laraxo“, „lenachen“: Name + bekannter Anhang
    for (let n = Math.min(t.length - 1, 10); n >= 3; n--) { const a = t.slice(0, n), b = t.slice(n); if (NAMEN.has(a) && ANHANG.test(b)) return gross(a); }
  }
  return null;
}
const gross = t => t.charAt(0).toUpperCase() + t.slice(1);
