# Muschel-Tal 3D-Rundgang (nur für Videos, nicht öffentlich)

3D-Ansicht der Haupt-Insel in Augenhöhe, gebaut aus den **echten Kartendaten der Homepage**:
Inselumriss, Wegeraster, alle 500 Hütten an ihren Plätzen mit @Namen, Palmen, Büsche, Laternen,
Bänke und Steine, eine detaillierte Dönerbude sowie die übrigen Gebäude, Baustellen und der Palast
in vereinfachter Form.

**Nicht für Nutzer:** Der Ordner liegt in `videos/`. Netlify veröffentlicht nur `muscheltal/site`,
und die Homepage verlinkt nichts hiervon.

## Ablauf
1. Homepage lokal bauen: `python3 muscheltal/bau.py` (im Repo-Hauptordner)
2. Weltdaten holen: `node werkzeug/welt_holen.cjs` → `welt.json` (Route: Dönerbude → nächste Küste)
3. Szene bauen: `node werkzeug/szene.cjs` → `rundgang.html`
4. Prüfbilder: `node werkzeug/vorschau.cjs 0 5 10` → `renders/vorschau_*.png`
5. Video: `node werkzeug/aufnahme.cjs` → `renders/rundgang-doener-meer.mp4` (1080×1920, 30 fps)

Parameter in der URL von `rundgang.html`: `?t=Sekunde`, `&tempo=15` (Gehtempo), `&w=…&h=…` (Auflösung).
