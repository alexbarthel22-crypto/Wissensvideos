# TikTok-Videos

Deutsche „Was wäre, wenn …?“-TikToks, komplett im Code mit [HyperFrames](https://hyperframes.heygen.com) gebaut.

- Skill: `.claude/skills/tiktok-video/` (Ablauf + Stilregeln aus den Referenzvideos)
- Werkzeuge: `tools/` (Setup, deutsche Stimme, Build, CLI-Wrapper)
- Videos: `videos/<thema>/` – `script.json` ist die Quelle, `scenes/` die Grafik, `renders/` das fertige MP4

```bash
bash tools/setup.sh                                   # Stimme + CLI
python3 tools/tts_de.py videos/<thema> --backend piper
python3 tools/build_video.py videos/<thema>
cd videos/<thema> && ../../tools/hf.sh render -o renders/<thema>.mp4
```
