# Muschel-Tal 🏝️

Die Inselstadt aus Followern von @muscheltal. Webseite: https://muscheltal.de

| Datei | Zweck |
|---|---|
| `daten/einwohner.csv` | Einwohnerliste. Reihenfolge = Hütten-Nummer. Neue Namen nur **hinten** anhängen. |
| `daten/insel.json` | Tag, Ämter (Häuptling, Villa …), News, Chronik, Viertel |
| `vorlage.html` | Aussehen der Webseite |
| `bau.py` | baut `site/index.html` + `site/einwohner.json` (Daten fürs Video) |
| `site/` | fertige Webseite – dieser Ordner wird veröffentlicht |

## Tägliches Update
```bash
python3 muscheltal/bau.py --import ~/Downloads/user_data_tiktok.json   # TikTok-Export einlesen
python3 muscheltal/bau.py                                              # oder nur neu bauen nach Hand-Änderungen
```
Danach committen + pushen → der Hoster veröffentlicht automatisch.

Vorschau mit Testnamen (nie veröffentlichen): `python3 muscheltal/bau.py --demo 3000 --out /tmp/demo`

Vor dem Livegang: Platzhalter in `site/impressum.html` und `site/datenschutz.html` ausfüllen.
