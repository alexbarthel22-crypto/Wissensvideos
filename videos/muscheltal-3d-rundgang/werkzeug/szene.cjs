// Baut rundgang.html: 3D-Ansicht der Haupt-Insel aus welt.json (echte Kartendaten), Kamera in Augenhöhe.
// node werkzeug/szene.cjs   →  rundgang.html (nur lokal/für Videos, nicht veröffentlicht)
const fs=require('fs'),path=require('path');const D=path.resolve(__dirname,'..');
const welt=fs.readFileSync(path.join(D,'welt.json'),'utf8');
const html=`<!doctype html><html><head><meta charset="utf-8"><title>Muschel-Tal 3D (intern)</title>
<style>html,body{margin:0;background:#9fdcf0;overflow:hidden}canvas{display:block;position:relative;z-index:1}#sky{position:fixed;inset:0;background:linear-gradient(#5ec3ef 0%,#a9e3f7 55%,#e9f8ff 100%)}</style></head>
<body><div id="sky"></div><canvas id="cv"></canvas><script src="three.min.js"></script><script>
const WELT=${welt};
${fs.readFileSync(path.join(__dirname,'szene_code.js'),'utf8')}
</script></body></html>`;
fs.writeFileSync(path.join(D,'rundgang.html'),html);console.log('rundgang.html geschrieben');
