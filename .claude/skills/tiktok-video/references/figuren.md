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

Stimme: Google Chirp 3 HD `de-DE-Chirp3-HD-Fenrir`, `--speed 1.1`.

## Das Grundstück (Kulisse)

`tools/characters/grundstueck.js` → `grundstueck(svg, pre, { mood: "dusk"|"day"|"night", chairX, treeX, dy })`:
verwahrlostes Erbe von Onkel Heinz – kaputter Zaun, alter Reifen, Unkraut, **ein einziger Holzstuhl unter einem kargen Baum mit einem letzten Blatt**.
Wenn die Sekte wächst (Kollekte), hier neue Bauteile ergänzen statt die Kulisse auszutauschen. Dazu `filmLook(svg, pre)` (Vignette + Korn) und `floatDust(tl, G, dur)`.

## Serien-Fakten (Kontinuität)

- Tag 1: Gründung, 0 Anhänger, Kollekte 0 €, 1 € pro neuem Follower = 1 Ziegelstein für den Tempel.
- Ränge: Hohepriester (Platz 1) · Erzdiakon (2–10) · Tempelwächter (11–100) · Anhänger (101+) · Rasenmäher (der Letzte).
- Offene Frage an die Community: Name der Sekte (Antwort in Tag 2 auflösen).
