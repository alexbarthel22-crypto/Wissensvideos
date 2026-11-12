# Muschel-Tal 3D (nur für Videos)

`insel3d.html` baut die Insel aus der fertigen Homepage (`muscheltal/site/index.html`, vorher `python3 muscheltal/bau.py`) in 3D nach – Hütten, Läden, Palast, Brunnen, Wege, Palmen, Laternen, Baustellen, Yacht. Nicht auf der Homepage verlinkt, wird nicht veröffentlicht.

Öffnen über einen lokalen Webserver ab dem Repo-Ordner:

    python3 -m http.server 8077
    http://localhost:8077/videos/muscheltal-3d/insel3d.html?flug=1

Parameter: `still=1` (ein Standbild) · `fx=0` (ohne Nachbearbeitung) · `sonne=Grad` · `ziel=x,y` · `insel=0|1` · `zeit=tag|nacht` · `name=@user` (Hütte mit Pin) · `fokus=1` (Kamera auf die Hütte) · `flug=1` (Kamera kreist) · `winkel=Grad` · `hoehe=0..1` · `zoom=Faktor` · `w=1080&h=1920` (feste Größe). `window.BEREIT` wird `true`, sobald die Szene steht.
