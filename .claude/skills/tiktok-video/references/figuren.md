# Serienfiguren (immer gleich aussehen lassen)

## Prophet Peter (Serie „Ich gründe eine Sekte“, ab `videos/prophet-peter-tag-1/`)

Ich-Erzähler, Gründer der Sekte. Ziel: Weltreligion. Code: `tools/characters/prophet-peter.js` → `peter(parent, pre, x, y, s, o)`
(Ursprung = zwischen den Füßen, Höhe ≈ 940 × s inkl. Discokugel/Heiligenschein). Nie neu zeichnen, nur diese Funktion verwenden.

| Merkmal | Aussehen |
| --- | --- |
| Kopfbedeckung | Selbst gebastelte goldene Bischofsmitra, **schief** (7°), zwei graue Klebeband-Streifen, vorne pinkes Neon-Auge im Dreieck |
| Heiligenschein | Pinker Neon-Ring hinter dem Kopf (`o.halo = false` blendet ihn aus) |
| Gesicht | Runde Sonnenbrille mit Goldrand und pink-violett verspiegelten Gläsern, buschige rotblonde Augenbrauen |
| Bart | Großer rotblonder Vollbart mit geflochtenem Zopf und Goldperle am Ende |
| Kleidung | Lila Talar mit Goldsaum, weißer Kollar (Priesterkragen), goldene Stola mit pinken Augen-Symbolen und Fransen, weite Ärmel mit Goldrand |
| Stab | Holzstab (Besenstiel) mit **Discokugel** oben, in seiner rechten Hand (links im Bild) |
| Füße | Braune Sandalen mit weißen **Tennissocken** (roter + blauer Streifen) |

Animierbare Teile: `armL` (Geste, z. B. `rotation: -150` = Arm hoch), `armR` (hält Stab), `mouth` (+ `talk(tl, P, t0, t1)`), `glint` (Brillen-Glanz),
`spark` (Discokugel-Funkeln, `svgOrigin: "-187 -850"`), `ball`, `mitre`, `halo`, `brows`.

Stimme: **Gemini-TTS, ganzer Text in EINER Aufnahme** (`"tts_single": true` – sonst klingt die Stimme je Zeile anders; Zeilen-Schnitt über Gemini-Zeitstempel + Pausen),  (`gemini-2.5-pro-preview-tts`, Stimme `Puck` (Fenrir klang dem Nutzer abgehackt), Schlüssel `$GEMINI_API_KEY`) mit Regieanweisung „euphorischer Fernsehprediger, sehr schnell, ohne Pausen“ (`style` in script.json) + Emotion pro Zeile (`style` an der Zeile): `python3 tools/tts_de.py videos/<slug> --backend gemini --voice Fenrir --speed 1.05 --max-gap 0.3 (Regie: zügig, flüssig, weich verbunden; Pausenschnitte mit Überblendung – kein starkes atempo, keine harten Schnitte), `lead_in` 0 = Text ab Sekunde 0`. Chirp 3 HD war dem Nutzer zu wenig emotional. Aufnahmen liegen pro Zeile in `assets/voice/cache/` (Rate-Limit beim Pro-Modell!).
Sound-Signatur: Frame 0 = lautester Schlag aus `assets/sfx/src/church-bell-5993.mp3` (`tools/make_church.py … --bell`), Peter steht ab Frame 0 links im Bild (Szene 1). Engelschor = hochgeladene Datei `assets/sfx/src/heavenly-choir-322708.mp3` (erste 2,6 s → `choir-intro.wav`, `make_church.py --choir`), wenn Peter erscheint und bei „Aber ich sehe mehr“. Name nie als „Gestatten …“ einleiten; Custom-IPA wird von Chirp 3 HD abgelehnt.

Hintergrundmusik der Serie: leiser, „göttlicher“ Klangteppich `tools/make_pad.py videos/<slug>/assets/sfx/divine-pad.wav <Gesamtdauer> --duck videos/<slug>/assets/voice/narration.wav`, als sfx `divine-pad` bei `s01+0.0`, Lautstärke 0.3 (≈18 dB unter der Stimme, unter Sprache zusätzlich −6 dB). Szenen 1–2 sehr schnell sprechen (speed 1.35–1.4 pro Zeile).

## Das Grundstück (Kulisse)

`tools/characters/grundstueck.js` → `grundstueck(svg, pre, { mood: "dusk"|"day"|"night", chairX, treeX, dy })`:
verwahrlostes Erbe von Onkel Heinz, **2 Hektar (20.000 m²)** groß – kaputter Zaun, Reifen, Müllsäcke, Rostfass, Pfützen, Unkraut, **ein einziger Holzstuhl unter einem kargen Baum** (in Tag 1 bricht ein Ast ab: `G.brk`/`G.brkBase`) und **eine grasende Ziege** (`goatX`, `chew(tl, G, t, dur)`). Mit `w: 3240` entsteht ein Panorama für Kamerafahrten (Autowrack, Schuppen-Ruine, Badewanne, Einkaufswagen, Reifenstapel, Schild „Betreten auf eigene Gefahr“); `G.land`/`G.far` (Parallaxe ×0,12) per `x` schwenken.
Wenn die Sekte wächst (Kollekte), hier neue Bauteile ergänzen statt die Kulisse auszutauschen. Dazu `filmLook(svg, pre)` (Vignette + Korn) und `floatDust(tl, G, dur)`.

## Serien-Fakten (Kontinuität)

- Tag 1: Gründung, 0 Anhänger, Kollekte 0 €, 1 € pro neuem Follower = 1 Ziegelstein für den Tempel.
- Ränge: Hohepriester (Platz 1) · Erzdiakon (2–10) · Tempelwächter (11–100) · Anhänger (101+). (Kein „Rasenmäher“-Rang – vom Nutzer gestrichen.)
- Tag 1 sagt: „Aktueller Stand: null Anhänger“ (Zähler stürzt von Millionen auf 0, Plattenkratzer + traurige Posaune). Cover-Stil: Himmelslicht, TAG 1, „ICH GRÜNDE EINE SEKTE“, roter Stempel „ANHÄNGER 0“, unten „WERDE MEIN 1. ANHÄNGER!“.
- Offene Fragen an die Community: Name der Sekte + „Was kaufen wir morgen von der ersten Kollekte? Top-Kommentar entscheidet“ (beides in Tag 2 auflösen). Zuschauer sollen Peter in den Kommentaren mit „Prophet Peter“ ansprechen.
- Ränge ohne Platz-Zahlen; Text: „Sei von Anfang an dabei und sichere dir einen hohen Rang in meiner Sekte“. Folgen = 1 € in die Kollekte.
- Layout der Serie: `"shift": 110` in script.json (Kapitel-Marke + Untertitel tiefer), Szenen-Vordergrund im Container `.fgwrap` (+110 px) – **nicht** per CSS `translate` auf animierten Elementen (GSAP überschreibt das).
