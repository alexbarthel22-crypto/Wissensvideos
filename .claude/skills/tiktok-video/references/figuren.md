# Serienbibel „Prophet Peter – Ich gründe eine Sekte“

**Vor jeder neuen Folge komplett lesen.** Alles hier ist verbindlich (vom Nutzer abgenommen). Neue Folgen bauen auf Tag 1 auf
(`videos/prophet-peter-tag-1/` – Vorlage für Pipeline, Szenen, Sounds; neue Folge = Projekt kopieren, `script.json` + Szenen anpassen).
Format: TikTok 9:16, ≤ 60 s, Deutsch, Ich-Perspektive von Prophet Peter, Satire/Comedy.

## 1. Prophet Peter (Avatar – NIE verändern)

Code: `tools/characters/prophet-peter.js` → `peter(parent, pre, x, y, s, o)` (Ursprung zwischen den Füßen, Höhe ≈ 940 × s inkl. Discokugel/Heiligenschein). Nie neu zeichnen.

| Merkmal | Aussehen |
| --- | --- |
| Kopfbedeckung | selbst gebastelte goldene Bischofsmitra, **schief** (7°), zwei graue Klebeband-Streifen, vorne pinkes Neon-Auge im Dreieck |
| Heiligenschein | pinker Neon-Ring hinter dem Kopf (`o.halo = false` blendet ihn aus) |
| Gesicht | runde Sonnenbrille mit Goldrand, pink-violett verspiegelt; buschige rotblonde Augenbrauen |
| Bart | großer rotblonder Vollbart mit geflochtenem Zopf und Goldperle |
| Kleidung | lila Talar mit Goldsaum, weißer Kollar (Priesterkragen), goldene Stola mit pinken Augen-/Dreieck-Symbolen und Fransen, weite Ärmel mit Goldrand |
| Stab | Holzstab (Besenstiel) mit **Discokugel**, in seiner rechten Hand (links im Bild) |
| Füße | braune Sandalen mit weißen **Tennissocken** (roter + blauer Streifen) |

Animierbar: `armL` (Geste, `rotation: -150` = Arm hoch/segnen), `armR` (hält Stab), `mouth` + `talk(tl, P, t0, t1)`, `glint` (Brillenglanz),
`spark` (Discokugel-Funkeln, `svgOrigin: "-187 -850"`), `ball`, `mitre`, `halo`, `brows`.
Profilbild: `videos/prophet-peter-profilbild/` (Brustbild als Heiliger, goldener Heiligenschein, Lichtstrahlen, segnende Hand).
Name im Video: „Ich bin Prophet Peter!“ (nie „Gestatten …“). Persönlichkeit: euphorischer, größenwahnsinniger Fernsehprediger, selbstironisch.

## 2. Stimme & Ton

- **Gemini-TTS** `gemini-2.5-pro-preview-tts`, Stimme **`Puck`**, Schlüssel `$GEMINI_API_KEY`, **ganzer Text in EINER Aufnahme** (`"tts_single": true`, sonst klingt die Stimme je Zeile anders).
  Regie in `script.json` → `style` (euphorischer Fernsehprediger, schnell, flüssig, weich verbunden, keine Kunstpausen, „Sekte“ korrekt „SEK-te“, erstes Wort gebrüllt).
  `python3 tools/tts_de.py videos/<slug> --backend gemini --voice Puck --speed 1.08 --max-gap 0.22`
- Danach **immer** `python3 tools/check_cuts.py videos/<slug>` (jede Zeile wird abgeschrieben; „!!“ = falscher Schnitt → `"cut_shift": {"L13": 1}` = Grenze vor L13 eine Pause später, `-1` = früher).
  `"audio": "pfad.wav"` = eigene Aufnahme für eine Zeile (Tempo wie die Zeile). `"skip": true` = Zeile bleibt in der Aufnahme, wird aber nicht verwendet. `"join_prev": true` = Zeile gehört zur vorigen Aufnahme, wird intern geteilt (z. B. „WARTE!!!“ | „Tag eins! …“ mit eigenem Tempo).
- Lautstärke Stimme: `"voice_lufs": -13` (Kompressor + Limiter, Stimme klar vor der Musik; Musik unter Sprache ~ -10 dB). Tempo: Anfang sehr schnell (Szene 1 speed 1.8, Gesetz 1.25, Vorstellung 1.35, Erbe 1.35), Ende flott (1.22), Standzeit am Schluss ≈ 1,2 s. Gesamt ≤ 60 s.
- Musik: eigene Komposition „Kirchenchoral“ (`tools/make_music.py <out> <Gesamtdauer> --style hymn --duck assets/voice/narration.wav`: Orgel + Chor + Pedalbass, 70 BPM, ohne Schlagzeug), sfx `music-hymn` Lautstärke 0.4, nach jeder Neuvertonung neu erzeugen. Weitere Stile: `epic` (Heiliger Trailer), `gospel`.
- Abgelehnt: Chirp-3-HD-Stimmen (zu wenig Emotion), Fenrir (abgehackt), harte Pausenschnitte, Glocke am Anfang.
- Sounds (`tools/make_church.py videos/<slug>/assets/sfx --choir <chor.mp3>`): Frame 0 = Engelschor `choir-intro` (hochgeladene Datei `assets/sfx/src/heavenly-choir-322708.mp3`, 1. Bogen), Peters Vorstellung = `choir-intro2` (2. Bogen), „Aber ich sehe mehr“ = Engelschor; außerdem `shimmer`, `bell-hit`, `coin`, `goat`, `crack` (Ast), `record-scratch` + `sad-trombone` (0 Anhänger), `pop`/`click`/`notification`.

## 3. Das Grundstück (Kulisse)

Code: `tools/characters/grundstueck.js` → `grundstueck(svg, pre, { mood: "dusk"|"day"|"night", w, chairX, treeX, goatX, goatS, goatFlip, dy })`.
Erbe von **Onkel Heinz** (Testament: „… vermache ich meinem Neffen Peter mein gesamtes Grundstück. Mach was draus, Junge.“).
- **2 Hektar = 20.000 m²**, total verwahrlost: kaputter Zaun, Reifen, Müllsäcke, Rostfass, Pfützen, Steine, Unkraut, Dornenbüsche.
- **Ein einziger Holzstuhl unter einem kargen Baum** (letztes Blatt). In Tag 1 **bricht ein Ast ab** (`G.brk`) → in Folgefolgen liegt der Ast am Boden / fehlt am Baum.
- **Die Ziege** (Bewohnerin, grast, meckert; `goatX`, `chew()`). Wiederkehrende Nebenfigur.
- Weiter hinten (Panorama `w: 3240`): Autowrack ohne Räder, Schuppen-Ruine mit eingesacktem Dach, Badewanne mit Brackwasser, umgekippter Einkaufswagen, Reifenstapel, Schild „BETRETEN AUF EIGENE GEFAHR“.
- Kamera auf `G.land` über das `transform`-Attribut steuern (siehe s05 in Tag 1), nicht per GSAP-Transform.
- Wenn die Sekte wächst (Kollekte), **Bauteile ergänzen statt die Kulisse auszutauschen** (Stuhl, Baum, Ziege bleiben).
- Look: `filmLook()`, `floatDust()`, Abendrot („dusk“) als Standard, „day“ für die nüchterne Grundstücks-Totale.

## 4. Inhalt Tag 1 (Kanon)

Szenen (Kapitel-Marke): 1) **„KNIE NIEDER!“** (gebrüllt wie zuvor „WARTE!“: eigene Aufnahme `assets/voice/knie-nieder.wav` per `"audio"` an Zeile L1a, Text `KNIE_NIEDER!!!|WARTE!!!` damit die Gesamtaufnahme gleich bleibt; roter Kasten) + „TAG 1 – ICH GRÜNDE EINE SEKTE“ (finale Fassung mit WARTE; Variante ohne = L1a `"skip": true`) (farbige Wortkästen, Wort-Zoom, Peter links, goldene Visions-Umrisse von Tempel/Gärten/Pilgerstraße, Himmelslicht)
→ 2) **DAS GESETZ**: „Ab heute gilt ein heiliges Gesetz: Jeder neue Follower wird Anhänger und bringt einen Euro in die Kollekte!“ (Klingelbeutel mittig, echte 1-€-Münze fällt hinein, Kollekte 0 € → 1 €)
→ 3) **DER GRÜNDER**: „Ich bin Prophet Peter! Gründer! Erleuchteter! Und ab heute euer Anführer!“
→ 4) **DAS ERBE**: Testament, Stempel „GEERBT“, „Hier entsteht unser Heiligtum!“ (Baum + Stuhl im goldenen Heiligenschein, Schild „ZUKÜNFTIGES HEILIGTUM“)
→ 5) **DAS GRUNDSTÜCK**: Totale über alles, Zooms: „zwei Hektar Wildnis“ (Schrott & Ruinen) – „Eine Ziege wohnt hier schon“ – „genau einen Stuhl“ – „Unter einem kargen Baum“ (Ast bricht)
→ 6) **DIE VISION**: Tempel, Gärten, Pilgerstraße als goldene Linien → Weltkugel, Anhänger-Zähler rast in die Millionen → „Aktueller Stand: null Anhänger.“ (Absturz auf 0, Stempel „0 ANHÄNGER“)
→ 7) **DIE RÄNGE**: Pyramide Hohepriester – Erzdiakon – Tempelwächter – Anhänger (ohne Zahlen): „Sei einer der ersten Anhänger und sichere dir einen hohen Rang in meiner Sekte!“
→ 8) **DER NAME**: „Nur eins fehlt noch: ein Name! Wie soll unsere Sekte heißen?“ („SEKTE DER ____“)
→ 9) **TAG 1 · AUFRUF**: „Schreib's in die Kommentare! Aber Achtung: Ich lese nur Kommentare, die mit Prophet Peter beginnen! Und: Was kaufen wir morgen von der ersten Kollekte? Der Top-Kommentar entscheidet!“ (Beispiel-Kommentar „Prophet Peter, kauf uns eine Hüpfburg!“, Button „+ FOLGEN = 1 € IN DIE KOLLEKTE“).

**Stand nach Tag 1:** 0 Anhänger, Kollekte 0 € (Regel: 1 € pro neuem Follower), Ausstattung 1 Stuhl, 1 karger Baum (ein Ast weniger), 1 Ziege, viel Schrott.
**Offene Schleifen für Tag 2+:** (1) Name der Sekte (Top-Kommentar), (2) was von der ersten Kollekte gekauft wird (Top-Kommentar), (3) wer die ersten Anhänger sind / Ränge vergeben,
(4) Visionen Tempel/Gärten/Pilgerstraße Stück für Stück bauen, (5) Running Gags: Ziege, Stuhl, Baum, Socken in Sandalen, schiefe Mitra.
Regeln für Zuschauer: Kommentare beginnen mit „Prophet Peter“; Folgen = Anhänger = 1 € in die Kollekte; „Top-Kommentar entscheidet“.

## 5. Gestaltung & Technik (gilt für alle Folgen)

- `"hud": "pop"`, `"safe": true`, `"shift": 110` in script.json; Szenen-Vordergrund im Container `.fgwrap` (+110 px; `noshift`-Ebenen bleiben stehen). Nicht per CSS `translate` auf animierten Elementen.
- **Sicherheitsbereiche:** oben 0–140 px frei, rechts x > 940 zwischen y 860–1600 (Buttons) frei, unten ab y 1560 frei. Untertitel rechts bis x 910. Vor dem Rendern Standbilder mit eingezeichneten Bereichen prüfen.
- Szene 1 ohne Untertitel (`nocap`), Text steht groß im Bild ab Frame 0; Peters Name in Szene 2 ohne Untertitel (Namensschild).
- Kapitel-Marken in Versalien, z. B. „DAS GESETZ“, „DAS GRUNDSTÜCK“, „TAG 1 · AUFRUF“ → in Folgen „TAG 2 · …“.
- **Cover:** roter Kasten „KNIE NIEDER!“ oben, Himmelslicht, groß „TAG n“ + Hook-Satz, Peter segnend links, roter Stempel mit Zahl (z. B. „ANHÄNGER 0“), unten gelber Rahmen mit Aufruf; alles Wichtige im 3:4-Ausschnitt (y 240–1680). Vorlage: `videos/prophet-peter-tag-1/cover/gen_cover.py`.
- **Beschreibung:** Hook + Stand + Frage, „Top-Kommentar entscheidet“, Hashtags `#fürdich #fyp #comedy #religion #prophetpeter` (in Beschreibung/Hashtags „Religion“ statt „Sekte“) (Marke `#prophetpeter` immer). Vorlage: `videos/prophet-peter-tag-1/BESCHREIBUNG.md`.
