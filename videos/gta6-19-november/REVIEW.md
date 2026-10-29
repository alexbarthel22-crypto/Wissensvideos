# Review: GTA VI – 19. November

## Fassung 3 (aktuell)
- Stimme: Thorsten VITS (männlich, Phonem-basiert) statt CSS10 – CSS10 klang abgehackt („Mitternacht“). Jede Zeile in einem Durchgang, keine harten Pausen-Schnitte, sanfter EQ + De-Esser, -16 LUFS.
- Rauschen behoben: `glitch-2` (3,5 s, bei „flackert“) und `whoosh-cinematic` (5,5 s, bei „Schreibtisch leer“) entfernt; nur kurze Whooshes.
- Purge-Sirene (selbst synthetisiert, tools/make_siren.py) auf Frame 0, Stimme setzt nach 0,9 s ein, Sirene danach ~16 dB leiser.
- Länge 68 s, -16,6 LUFS, Spitze -1,6 dBFS.

## Fassung 2
- Weibliche Stimme: Coqui CSS10 VITS (22 kHz), Tempo 1,25, Klarheits-EQ + Kompressor, Pausen ≤ 0,3 s. ~2,8 Wörter/s.
- Frame 0: Eilmeldung „4,1 Milliarden Menschen spielen GTA 6 – gleichzeitig“ + Zähler + pinker Globus; offene Schleife „Um Mitternacht passiert etwas, womit niemand rechnet“ → Auflösung „Noch eine Runde!“.
- Schluss: „Gehörst du am 19. November zu den vier Milliarden? Schreib's in die Kommentare!“ mit Buttons ICH ZOCKE / NEIN.
- Länge 75 s, −16,1 LUFS, Spitze −1,5 dBFS. Zeile „Kaum Verkehr. Kaum Unfälle.“ gestrichen.
- Behaltene Warnung: „24 STUNDEN · 0 PAUSEN“ steht 1,24 s (Untertitel sagt dasselbe).

## Fassung 1

## Kreative Entscheidungen
- Stil B (2D-Neon, deutsch, Karaoke-Untertitel) aus der „Greta“-Referenz, kombiniert mit der Zeitleiter-Dramaturgie der 3D-Referenzen (Kapitel-Marke = Uhrzeit am 19. Nov, 00:00 → 23:59 → 20. Nov 00:00).
- Running Gag: Checkliste oben links füllt sich mit allem, was kaputtgeht (Server, Internet, Stromnetz, Arbeit, Wirtschaft).
- Klammer: Start mit „SPIELER ONLINE“ am Globus, Ende mit demselben Zähler und dem Knopf „NOCH EINE RUNDE“, Abschluss als Kommentar-Frage (JA / NEIN).
- Zahlen sind überschlagen: 8,2 Mrd. Menschen / 2 ≈ 4,1 Mrd.; ~200 W pro Konsole × 4,1 Mrd. ≈ 800 GW ≈ 800 Reaktoren à 1 GW; Weltwirtschaft ~115 Billionen $/Jahr ≈ 300 Mrd. $/Tag, bei halber Belegschaft „über 100 Mrd. $“. Pizza-Bestellungen, Warteschlange (41 Tage) und Verkehr (8 %) sind bewusst satirische Werte.

## Gemessen
- `hyperframes check`: keine Fehler. Bewusst behalten: `timeline_track_too_dense` (Untertitel-Gruppen liegen in einer Datei, damit Studio sie auf einer Spur zeigt), `container_overflow` (Bild-SVGs in abgerundeten Karten).
- Snapshots aller Szenen + Schlüsselmomente angesehen (Layout, Überlappungen, Lesbarkeit).
- Ton gemessen, nicht gehört: Stimme + 13 Effekte + Whooshes an den Szenenwechseln.

## Nicht geprüft / Grenzen
- Die Stimme wurde nicht angehört (kein Audio im Container). Aussprache von „GTA“, „Vice City“, „Energy-Drinks“ ist phonetisch umschrieben und sollte einmal angehört werden.
- Karaoke-Wortzeiten sind geschätzt (Pausen + Silben), Abweichung ~0,1 s möglich.
- Keine Musik: im TikTok-Editor einen Sound darunterlegen.

## Schwächster Moment
- s07 (Weltwirtschaft): Linienchart ist der generischste Shot. Mit mehr Zeit: Börsensaal mit leeren Plätzen oder fallende Geldscheine als Hauptbild.
