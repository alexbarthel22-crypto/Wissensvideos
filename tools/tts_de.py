#!/usr/bin/env python3
"""Deutsche Sprachspur + Wort-Timings aus script.json.

Erzeugt <projekt>/assets/voice/narration.wav und <projekt>/assets/voice/timings.json.

Backends:
  coqui  – Thorsten VITS (22 kHz, natürlicher), braucht das coqui-venv
  piper  – Piper-Stimmen (16 kHz), schneller Fallback

Wort-Timings: Piper/Coqui liefern keine Wortzeiten. Jede Zeile wird einzeln
synthetisiert; Pausen in der Zeile werden per Energie erkannt und den
Satzzeichen zugeordnet, innerhalb eines Abschnitts wird nach Silben verteilt.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

CACHE = Path(os.environ.get("TIKTOK_CACHE", Path.home() / ".cache" / "tiktok-tts"))
SR = 44100
GAP_LINE = 0.22      # Pause zwischen Zeilen derselben Szene
GAP_SCENE = 0.38     # Pause zwischen Szenen
LEAD_IN = 0.25       # Stille am Anfang
COLOR_RE = re.compile(r"^\*([yrpgb]):")
PUNCT_RE = re.compile(r"[,.;:?!…]+[\"“”]?$")


def parse_tokens(text):
    """'*y:19.|neunzehnten' -> {display, spoken, color, group}."""
    words, group = [], 0
    for raw in text.split():
        if raw == "/":
            group += 1
            continue
        color = None
        m = COLOR_RE.match(raw)
        if m:
            color, raw = m.group(1), raw[m.end():]
        display, _, spoken = raw.partition("|")
        spoken = spoken or display
        words.append({
            "display": display.replace("_", " "),
            "spoken": spoken.replace("_", " ").replace("-", " ") if "|" in raw else spoken.replace("_", " "),
            "color": color,
            "group": group,
        })
    return words


def syllables(word):
    w = re.sub(r"[^a-zäöüß]", "", word.lower())
    n = len(re.findall(r"[aeiouäöüy]+", w))
    return max(1, n) + len(w) * 0.04


def synth_piper(texts, voice_dir, scales, noise):
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    model = next(Path(voice_dir).glob("*.onnx"))
    voice = PiperVoice.load(str(model))
    out = []
    for t, ls in zip(texts, scales):
        cfg = SynthesisConfig(length_scale=ls, noise_scale=noise, noise_w_scale=0.9)
        chunks = [c.audio_float_array for c in voice.synthesize(t, syn_config=cfg)]
        out.append((np.concatenate(chunks), voice.config.sample_rate))
    return out


def synth_coqui(texts, model_dir, python, scales, noise, noise_dp=0.8):
    """Läuft im separaten venv; schreibt WAVs in ein Temp-Verzeichnis."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "lines.json").write_text(json.dumps({"texts": texts, "scales": scales}, ensure_ascii=False))
    model = next(p for p in Path(model_dir).iterdir() if p.name.startswith("model_file"))
    code = f"""
import json
from TTS.api import TTS
job = json.load(open({str(tmp / 'lines.json')!r}))
tts = TTS(model_path={str(model)!r}, config_path={str(Path(model_dir) / 'config.json')!r})
m = tts.synthesizer.tts_model
m.inference_noise_scale = {noise}
m.inference_noise_scale_dp = {noise_dp}
kw = {{}}
if tts.is_multi_speaker and tts.speakers: kw["speaker"] = tts.speakers[0]
if tts.is_multi_lingual and tts.languages: kw["language"] = tts.languages[0]
for i, (t, ls) in enumerate(zip(job["texts"], job["scales"])):
    m.length_scale = ls
    # ganze Zeile in einem Durchgang: natürliche Satzmelodie, keine harten Satz-Schnitte
    tts.tts_to_file(text=t, file_path={str(tmp)!r} + f'/{{i:03d}}.wav', split_sentences=False, **kw)
"""
    subprocess.run([python, "-c", code], check=True)
    out = []
    for i in range(len(texts)):
        a, sr = sf.read(tmp / f"{i:03d}.wav", dtype="float32")
        out.append((a, sr))
    return out


def synth_google(texts, voice, scales, prons=None):
    """Google Cloud TTS (Chirp 3 HD): echte, natürliche Stimmen. Schlüssel aus $GOOGLE_TTS_API_KEY.
    prons: {"Relaxo": "ʁeˈlakso"} – Aussprache in IPA für Namen, die die Stimme falsch liest."""
    import base64
    import io
    import urllib.request
    key = os.environ.get("GOOGLE_TTS_API_KEY")
    if not key:
        raise SystemExit("GOOGLE_TTS_API_KEY fehlt (in den Umgebungs-Einstellungen hinterlegen).")
    out = []
    for t, ls in zip(texts, scales):
        inp = {"text": t}
        used = [{"phrase": w, "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": ipa} for w, ipa in (prons or {}).items() if w in t]
        if used:
            inp["customPronunciations"] = {"pronunciations": used}
        body = {"input": inp, "voice": {"languageCode": "de-DE", "name": voice},
                "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "speakingRate": round(1 / ls, 3)}}
        req = urllib.request.Request(
            f"https://texttospeech.googleapis.com/v1/text:synthesize?key={key}",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            wav = base64.b64decode(json.loads(r.read())["audioContent"])
        a, sr = sf.read(io.BytesIO(wav), dtype="float32")
        out.append((a, sr))
    return out


GEMINI_STYLE = ("Lies den folgenden deutschen Text als extrem charismatischer, euphorischer Fernsehprediger und Sektengründer vor: "
                "mit maximaler Energie, überschäumender Begeisterung, großen Emotionen, lauter, mitreißender Stimme, "
                "dramatischen Betonungen und zügigem Tempo. Sprich nur den Text, nichts anderes. Text: ")


def synth_gemini(texts, voice, scales, style=None, line_styles=None, cache_dir=None, model="gemini-2.5-pro-preview-tts"):
    """Gemini-TTS (Regieanweisung steuert Emotion/Energie). Schlüssel aus $GEMINI_API_KEY.
    Ergebnisse werden pro Zeile im Cache abgelegt (gleicher Text + Stil = gleiche Aufnahme); Tempo per ffmpeg atempo."""
    import base64
    import hashlib
    import urllib.request
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY fehlt (in den Umgebungs-Einstellungen hinterlegen).")
    out = []
    for i, (t, ls) in enumerate(zip(texts, scales)):
        prompt = (style or GEMINI_STYLE)
        if line_styles and line_styles[i]:
            prompt = prompt.replace("Text: ", f"Für diesen Satz: {line_styles[i]}. Text: ")
        h = hashlib.sha1(f"{model}|{voice}|{prompt}{t}".encode()).hexdigest()[:16]
        cf = cache_dir / f"{h}.wav" if cache_dir else None
        if cf and cf.exists():
            a, sr = sf.read(cf, dtype="float32")
        else:
            body = {"contents": [{"parts": [{"text": prompt + t}]}],
                    "generationConfig": {"responseModalities": ["AUDIO"],
                                         "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
            words = len(t.split())
            for attempt in range(4):  # Ausreißer (liest Anweisung mit / bricht ab) verwerfen
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                import time
                for wait in (0, 30, 60, 90, 120, 180, 240):  # 429 = Rate-Limit: warten und erneut
                    time.sleep(wait)
                    try:
                        with urllib.request.urlopen(req, timeout=180) as r:
                            d = json.loads(r.read())["candidates"][0]["content"]["parts"][0]["inlineData"]
                        break
                    except urllib.error.HTTPError as e:
                        if e.code not in (429, 500, 503):
                            raise
                        print(f"  Zeile {i + 1}: HTTP {e.code}, warte …", flush=True)
                else:
                    raise SystemExit("Gemini-Rate-Limit: später erneut starten (fertige Zeilen liegen im Cache).")
                a = np.frombuffer(base64.b64decode(d["data"]), dtype="<i2").astype("float32") / 32768
                sr = int(d["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in d["mimeType"] else 24000
                rate = words / (len(a) / sr)
                if 1.0 < rate < 5.0:
                    break
                print(f"  Zeile {i + 1}: {rate:.1f} Wörter/s – neuer Versuch")
            if cf:
                cf.parent.mkdir(parents=True, exist_ok=True)
                sf.write(cf, a, sr)
        if abs(ls - 1.0) > 0.01:  # Tempo ohne Tonhöhenänderung
            with tempfile.TemporaryDirectory() as dd:
                src, dst = Path(dd) / "a.wav", Path(dd) / "b.wav"
                sf.write(src, a, sr)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter:a", f"atempo={1 / ls:.4f}", dst], check=True)
                a, sr = sf.read(dst, dtype="float32")
        out.append((a, sr))
    return out


def gemini_request(prompt, voice, model, cache_file):
    """Ein Gemini-TTS-Aufruf mit Cache und Wartezeit bei Rate-Limit. Rückgabe (audio, sr)."""
    import base64
    import time
    import urllib.request
    if cache_file and cache_file.exists():
        return sf.read(cache_file, dtype="float32")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY fehlt (in den Umgebungs-Einstellungen hinterlegen).")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for wait in (0, 30, 60, 90, 120, 180, 240, 300):
        time.sleep(wait)
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())["candidates"][0]["content"]["parts"][0]["inlineData"]
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 503):
                raise
            print(f"  HTTP {e.code}, warte …", flush=True)
    else:
        raise SystemExit("Gemini-Rate-Limit: später erneut starten.")
    a = np.frombuffer(base64.b64decode(d["data"]), dtype="<i2").astype("float32") / 32768
    sr = int(d["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in d["mimeType"] else 24000
    if cache_file:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        sf.write(cache_file, a, sr)
    return a, sr


def gemini_line_starts(audio, sr, texts, cache_file, model="gemini-3.1-pro-preview"):
    """Lässt Gemini die Aufnahme hören und die Startzeit jeder Zeile schätzen (Sekunden). Ergebnis wird gecacht."""
    import base64
    import io
    import time
    import urllib.request
    T = len(audio) / sr

    def plausible(sp):
        if len(sp) != len(texts):
            return None
        flat = [x for p in sp for x in p]
        if max(flat) < T / 20:  # Antwort im Format Minuten.Sekunden (0.52 = 52 s)
            sp = [[int(x) * 60 + round((x - int(x)) * 100, 2) for x in p] for p in sp]
        flat = [x for p in sp for x in p]
        ok = all(b >= a for a, b in zip(flat, flat[1:])) and sp[-1][0] > 0.5 * T and flat[-1] <= T + 0.5
        return sp if ok else None

    if cache_file.exists():
        return json.loads(cache_file.read_text())
    key = os.environ["GEMINI_API_KEY"]
    buf = io.BytesIO(); sf.write(buf, audio, sr, format="WAV", subtype="PCM_16")
    q = ("Hier ist eine deutsche Sprachaufnahme. Sie enthält nacheinander genau diese Zeilen:\n"
         + "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts))
         + f"\nDie Aufnahme ist {T:.1f} Sekunden lang. Gib für jede Zeile [Beginn des ersten Wortes, Ende des letzten Wortes] in Sekunden seit Beginn "
         "(Dezimalzahlen, z. B. 12.34 – NICHT Minuten:Sekunden) als JSON-Liste von Paaren zurück, sonst nichts.")
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}}, {"text": q}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    for wait in (0, 30, 60, 120):
        time.sleep(wait)
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            r = json.loads(urllib.request.urlopen(req, timeout=300).read())
            starts = plausible([[float(x) for x in p] for p in json.loads(r["candidates"][0]["content"]["parts"][-1]["text"])])
            if starts:
                cache_file.write_text(json.dumps(starts))
                return starts
        except Exception as e:  # noqa: BLE001
            print(f"  Zeitstempel-Abfrage: {e}", flush=True)
    return None


def _norm(w):
    return re.sub(r"[^a-zäöüß0-9]", "", w.lower())


def verify_cuts(a, cuts, P, texts, cache_file, model="gemini-3.8-flash"):
    """Kontrolle: Gemini hört die geschnittenen Stücke (getrennt durch Stille) und schreibt sie ab. Rutscht das erste Wort
    einer Zeile ans Ende der vorigen (oder umgekehrt), wird der Schnitt auf die Pause davor/danach verschoben."""
    import base64
    import io
    import urllib.request
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return cuts
    for rnd in range(6):
        edges = [0.0] + cuts + [len(a) / SR]
        gap = np.zeros(int(SR * 1.0), dtype="float32")
        parts = []
        for i in range(len(texts)):
            parts += [a[int(edges[i] * SR): int(edges[i + 1] * SR)], gap]
        buf = io.BytesIO(); sf.write(buf, np.concatenate(parts), SR, format="WAV", subtype="PCM_16")
        q = (f"Die Aufnahme besteht aus genau {len(texts)} Abschnitten, getrennt durch je eine Sekunde Stille. "
             "Schreibe jeden Abschnitt wörtlich ab (deutsch). Antworte nur mit einer JSON-Liste von Strings, ein Eintrag pro Abschnitt.")
        body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}}, {"text": q}]}],
                "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            got = json.loads(json.loads(urllib.request.urlopen(req, timeout=300).read())["candidates"][0]["content"]["parts"][-1]["text"])
        except Exception as e:  # noqa: BLE001
            print(f"  Schnitt-Kontrolle übersprungen: {e}")
            return cuts
        if len(got) != len(texts):
            print("  Schnitt-Kontrolle: Abschnittszahl passt nicht, übersprungen"); return cuts
        mids = sorted((x + y) / 2 for x, y in P)
        changed = False
        def overlap(x, y):  # längstes Ende von x, das ein Anfang von y ist (max. 5 Wörter)
            return max([n for n in range(1, min(5, len(x), len(y)) + 1) if x[-n:] == y[:n]], default=0)
        for k in range(1, len(texts)):
            exp_cur = [_norm(w) for w in texts[k].split()]; exp_prev = [_norm(w) for w in texts[k - 1].split()]
            g_prev = [_norm(w) for w in got[k - 1].split() if _norm(w)]; g_cur = [_norm(w) for w in got[k].split() if _norm(w)]
            if overlap(g_prev, exp_cur) and not (g_cur and g_cur[0] == exp_cur[0]):  # Anfang hängt am Ende davor -> früher schneiden
                earlier = [m for m in mids if m < cuts[k - 1] - 0.08 and (k == 1 or m > cuts[k - 2] + 0.3)]
                if earlier:
                    print(f"  Schnitt {k}: Anfang von Zeile {k + 1} hing an Zeile {k} – {cuts[k - 1]:.2f} → {earlier[-1]:.2f}"); cuts[k - 1] = earlier[-1]; changed = True
            elif overlap(exp_prev, g_cur) and not (g_prev and g_prev[-1] == exp_prev[-1]):  # Ende davor steckt im Anfang -> später schneiden
                later = [m for m in mids if m > cuts[k - 1] + 0.08 and (k == len(cuts) or m < cuts[k] - 0.3)]
                if later:
                    print(f"  Schnitt {k}: Ende von Zeile {k} hing an Zeile {k + 1} – {cuts[k - 1]:.2f} → {later[0]:.2f}"); cuts[k - 1] = later[0]; changed = True
        if not changed:
            print(f"  Schnitt-Kontrolle ok ({len(texts)} Zeilen)")
            break
    return cuts


def _transcribe_pair(left, right, model="gemini-3.8-flash"):
    """Zwei kurze Stücke (getrennt durch Stille) abschreiben lassen -> (text_links, text_rechts)."""
    import base64
    import io
    import time
    import urllib.request
    key = os.environ["GEMINI_API_KEY"]
    buf = io.BytesIO(); sf.write(buf, np.concatenate([left, np.zeros(int(SR * 1.2), dtype="float32"), right]), SR, format="WAV", subtype="PCM_16")
    q = ("Zwei kurze deutsche Sprach-Abschnitte, getrennt durch Stille. Schreibe beide wörtlich ab, auch angeschnittene oder sehr kurze Wörter "
         "am Anfang und Ende. Antworte nur mit einer JSON-Liste aus 2 Strings.")
    body = {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(buf.getvalue()).decode()}}, {"text": q}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
    for wait in (0, 15, 45, 90):
        time.sleep(wait)
        try:
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                                         data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            got = json.loads(json.loads(urllib.request.urlopen(req, timeout=200).read())["candidates"][0]["content"]["parts"][-1]["text"])
            if len(got) == 2:
                return got
        except Exception as e:  # noqa: BLE001
            print(f"    (Abschrift: {e})", flush=True)
    return None


def refine_cuts(a, cuts, P, texts, cache_file):
    """Jede Zeilengrenze an der Pause festmachen, bei der links das letzte Wort der Zeile endet und rechts das erste Wort
    der nächsten beginnt – geprüft per Abschrift der 2 s davor/danach. Ergebnis wird gecacht."""
    if cache_file and cache_file.exists():
        return json.loads(cache_file.read_text())
    if not os.environ.get("GEMINI_API_KEY"):
        return cuts
    mids = sorted((x + y) / 2 for x, y in P)
    same = lambda g, e: bool(g) and bool(e) and (g == e or (len(e) >= 4 and g[:4] == e[:4]))
    syl = [sum(syllables(w) for w in t.split()) for t in texts]
    T = len(a) / SR
    out = list(cuts)
    for k in range(len(cuts)):
        first = _norm(texts[k + 1].split()[0]); last = _norm(texts[k].split()[-1])
        prev = out[k - 1] if k else 0.0
        # Erwartung: vorige Grenze + Silbenanteil der Restzeit; zusätzlich der bisherige Schätzwert
        est = prev + (T - prev) * syl[k] / sum(syl[k:])
        lo = prev + 0.4
        pool = [m for m in mids if m > lo and m < prev + 12]
        cand = sorted(pool, key=lambda m: min(abs(m - est), abs(m - cuts[k])))[:10]
        best = None
        for m in cand:
            L = a[max(0, int((m - 2.0) * SR)): int(m * SR)]; R = a[int(m * SR): int((m + 2.0) * SR)]
            got = _transcribe_pair(L, R)
            if not got:
                break
            gl = [_norm(w) for w in got[0].split() if _norm(w)]; gr = [_norm(w) for w in got[1].split() if _norm(w)]
            if gl and gr and same(gl[-1], last) and same(gr[0], first):
                best = m; break
        if best is None:
            print(f"  Grenze {k + 1}: keine eindeutige Pause gefunden – bleibt bei {out[k]:.2f}")
            out[k] = max(out[k], lo)
        else:
            if abs(best - out[k]) > 0.01:
                print(f"  Grenze {k + 1} („{texts[k].split()[-1]}“ | „{texts[k + 1].split()[0]}“): {out[k]:.2f} → {best:.2f}", flush=True)
            out[k] = best
    if cache_file:
        cache_file.write_text(json.dumps(out))
    return out


def synth_gemini_single(lines_words, texts, voice, scales, style, cache_dir, model, line_ids=None, cut_shift=None, joins=None):
    """Zeilen mit join_prev werden für Aufnahme + Schnitt mit der vorigen zusammengelegt und danach an einer Pause geteilt."""
    joins = joins or [False] * len(texts)
    if not any(joins):
        return _synth_gemini_single(lines_words, texts, voice, scales, style, cache_dir, model, line_ids, cut_shift)
    groups = []  # Listen von Original-Indizes
    for i, j in enumerate(joins):
        if j and groups:
            groups[-1].append(i)
        else:
            groups.append([i])
    m_texts = [" ".join(texts[i] for i in g) for g in groups]
    m_words = [sum((lines_words[i] for i in g), []) for g in groups]
    m_ids = [line_ids[g[0]] for g in groups] if line_ids else None
    m_shift = {k: v for k, v in (cut_shift or {}).items() if not m_ids or k in m_ids}
    raw = _synth_gemini_single(m_words, m_texts, voice, [1.0] * len(groups), style, cache_dir, model, m_ids, m_shift)
    out = []
    for g, (seg, sr) in zip(groups, raw):
        if len(g) == 1:
            out.append((seg, sr)); continue
        P = pauses(seg, min_len=0.07); mids = [(x + y) / 2 for x, y in P]
        pieces, start = [], 0.0
        for gi in range(len(g) - 1):
            last = _norm(texts[g[gi]].split()[-1]); first = _norm(texts[g[gi + 1]].split()[0])
            share = sum(syllables(w) for w in texts[g[gi]].split()) / sum(syllables(w) for i in g[gi:] for w in texts[i].split())
            est = start + (len(seg) / SR - start) * share
            cut = None
            for m in sorted([m for m in mids if m > start + 0.15], key=lambda m: abs(m - est))[:6]:
                got = _transcribe_pair(seg[max(0, int((m - 2) * SR)): int(m * SR)], seg[int(m * SR): int((m + 2) * SR)])
                if got:
                    gl = [_norm(w) for w in got[0].split() if _norm(w)]; gr = [_norm(w) for w in got[1].split() if _norm(w)]
                    if gl and gr and gl[-1][:4] == last[:4] and gr[0][:4] == first[:4]:
                        cut = m; break
            cut = cut if cut is not None else (min(mids, key=lambda m: abs(m - est)) if mids else est)
            print(f"  intern geteilt: „{texts[g[gi]]}“ | „{texts[g[gi + 1]][:20]}…“ bei {cut:.2f} s")
            pieces.append(seg[int(start * SR): int(cut * SR)]); start = cut
        pieces.append(seg[int(start * SR):])
        for i, p in zip(g, pieces):
            out.append((p, sr))
    # Tempo pro Original-Zeile
    res = []
    for (seg, sr), ls in zip(out, scales):
        if abs(ls - 1.0) > 0.01:
            with tempfile.TemporaryDirectory() as dd:
                src, dst = Path(dd) / "a.wav", Path(dd) / "b.wav"
                sf.write(src, seg, sr)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter:a", f"atempo={1 / ls:.4f}", dst], check=True)
                seg, sr = sf.read(dst, dtype="float32")
        res.append((seg, sr))
    return res


def _synth_gemini_single(lines_words, texts, voice, scales, style, cache_dir, model, line_ids=None, cut_shift=None, joins=None):
    """Ganzer Text in EINER Gemini-Aufnahme (gleichbleibende Stimme), danach an Pausen in Zeilen geschnitten.
    Schnittpunkte: dynamische Programmierung über die Pausen – nahe an der erwarteten Position (Silbenanteil) und möglichst lang."""
    import hashlib
    joins = joins or [False] * len(texts)  # join_prev: Zeile gehört im Sprechtext zur vorigen (gleiche Aufnahme, nur intern getrennt)
    prompt = (style or GEMINI_STYLE) + "\n" + "".join(("" if i == 0 else (" " if joins[i] else "\n")) + t for i, t in enumerate(texts))
    h = hashlib.sha1(f"single|{model}|{voice}|{prompt}".encode()).hexdigest()[:16]
    a, sr = gemini_request(prompt, voice, model, cache_dir / f"{h}.wav" if cache_dir else None)
    starts = gemini_line_starts(a, sr, texts, cache_dir / f"{h}.spans.json") if cache_dir else None
    a = resample(a.astype("float32"), sr)
    T = len(a) / SR
    P = pauses(a, min_len=0.07)
    if starts:  # Schnitt = längste Pause zwischen Ende der Zeile davor und Anfang der Zeile (beides von Gemini geschätzt)
        cuts = []
        for k in range(1, len(starts)):
            e_prev, s_next = starts[k - 1][1], starts[k][0]
            cand = [(y - x, (x + y) / 2) for x, y in P if x >= e_prev - 0.35 and y <= s_next + 0.35 and (not cuts or (x + y) / 2 > cuts[-1] + 0.3)]
            if cand:
                cuts.append(max(cand)[1])
            else:
                mid = (e_prev + s_next) / 2
                near = [(abs((x + y) / 2 - mid), (x + y) / 2) for x, y in P if (not cuts or (x + y) / 2 > cuts[-1] + 0.3)]
                cuts.append(min(near)[1] if near else mid)
        cuts = refine_cuts(a, cuts, P, texts, cache_dir / f"{h}.cuts.json" if cache_dir else None)
        if os.environ.get("TTS_VERIFY", "0") == "1":  # automatische Nachkontrolle (unzuverlässig, Standard aus) – lieber tools/check_cuts.py
            cuts = verify_cuts(a, cuts, P, texts, cache_dir / f"{h}.verify.json" if cache_dir else None)
    else:  # Notlösung: dynamische Programmierung über die Pausen nach Silbenanteil
        syl = [sum(syllables(w["spoken"]) for w in ws) for ws in lines_words]
        cum = np.cumsum(syl)[:-1] / sum(syl)
        mids = [(x + y) / 2 for x, y in P]
        lens = [y - x for x, y in P]
        N, M = len(cum), len(P)
        sig = max(0.6, 0.04 * T)
        cost = lambda k, j: ((mids[j] - cum[k] * T) / sig) ** 2 - 3.0 * np.log(lens[j] / 0.07 + 1)
        INF = 1e18
        D = np.full((N, M), INF); B = np.zeros((N, M), dtype=int)
        for j in range(M):
            D[0, j] = cost(0, j)
        for k in range(1, N):
            best, bj = INF, -1
            for j in range(M):
                if j > 0 and D[k - 1, j - 1] < best:
                    best, bj = D[k - 1, j - 1], j - 1
                if bj >= 0:
                    D[k, j] = best + cost(k, j); B[k, j] = bj
        j = int(np.argmin(D[N - 1])); cuts = [j]
        for k in range(N - 1, 0, -1):
            j = int(B[k, j]); cuts.append(j)
        cuts = [mids[j] for j in reversed(cuts)]
    # manuelle Korrektur aus script.json: "cut_shift": {"L17": -1} = Schnitt vor L17 um eine Pause früher
    if cut_shift and line_ids:
        mids_all = sorted((x + y) / 2 for x, y in P)
        for lid, n in cut_shift.items():
            k = line_ids.index(lid) - 1
            for _ in range(abs(n)):
                cand = [m for m in mids_all if (m < cuts[k] - 0.05 if n < 0 else m > cuts[k] + 0.05)]
                if cand:
                    print(f"  manuell: Schnitt vor {lid} {cuts[k]:.2f} → {(cand[-1] if n < 0 else cand[0]):.2f}")
                    cuts[k] = cand[-1] if n < 0 else cand[0]
    edges = [0.0] + cuts + [T]
    out = []
    for i, ls in enumerate(scales):
        seg = a[int(edges[i] * SR): int(edges[i + 1] * SR)]
        if abs(ls - 1.0) > 0.01:
            with tempfile.TemporaryDirectory() as dd:
                src, dst = Path(dd) / "a.wav", Path(dd) / "b.wav"
                sf.write(src, seg, SR)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter:a", f"atempo={1 / ls:.4f}", dst], check=True)
                seg, _ = sf.read(dst, dtype="float32")
        out.append((seg, SR))
        print(f"  Zeile {i + 1}: {edges[i]:6.2f}–{edges[i + 1]:6.2f} s  {len(texts[i].split()) / max(0.1, edges[i + 1] - edges[i]):.1f} Wörter/s  {texts[i][:40]}")
    return out


def resample(audio, sr):
    if sr == SR:
        return audio
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "a.wav", Path(d) / "b.wav"
        sf.write(src, audio, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", str(SR), "-ac", "1", dst], check=True)
        a, _ = sf.read(dst, dtype="float32")
    return a


# Sprachverständlichkeit: Rumpeln weg, Präsenz (2–4 kHz) und Luft anheben, gleichmäßige Lautstärke
CLARITY = ("highpass=f=70,equalizer=f=220:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1.4:g=2,"
           "deesser=i=0.4,acompressor=threshold=-18dB:ratio=2:attack=20:release=250")


def clarity(audio):
    with tempfile.TemporaryDirectory() as d:
        src, dst = Path(d) / "a.wav", Path(d) / "b.wav"
        sf.write(src, audio, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", CLARITY, dst], check=True)
        a, _ = sf.read(dst, dtype="float32")
    return a


def voiced_frames(audio, thresh_db=-36, min_blip=4):
    """Pro 10-ms-Frame: Sprache ja/nein. Ausreißer kürzer als min_blip Frames (Knackser, Atem) zählen als Stille."""
    hop = int(0.01 * SR)
    n = len(audio) // hop
    rms = np.sqrt(np.mean(audio[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    v = 20 * np.log10(rms) > thresh_db
    i = 0
    while i < n:
        if v[i]:
            j = i
            while j < n and v[j]:
                j += 1
            if j - i < min_blip:
                v[i:j] = False
            i = j
        else:
            i += 1
    return v


def trim(audio):
    v = np.where(voiced_frames(audio))[0]
    if len(v) == 0:
        return audio
    hop = int(0.01 * SR)
    return audio[max(0, v[0] * hop - int(0.03 * SR)): min(len(audio), (v[-1] + 1) * hop + int(0.08 * SR))]


def pauses(audio, min_len=0.11):
    """Stille-Abschnitte innerhalb der Zeile: [(start, end), ...] in Sekunden."""
    v = voiced_frames(audio)
    res, start = [], None
    for i, voiced in enumerate(v):
        if not voiced and start is None:
            start = i
        elif voiced and start is not None:
            if (i - start) * 0.01 >= min_len and start > 3:
                res.append((start * 0.01, i * 0.01))
            start = None
    return res


def compress_pauses(audio, max_gap=0.3, fade=0.015):
    """Kürzt Sprechpausen innerhalb einer Zeile auf max_gap – mit weicher Überblendung an jedem Schnitt (sonst klingt es abgehackt/klickt)."""
    out, last = [], 0
    nf = int(fade * SR)
    for a, b in pauses(audio, min_len=max_gap):
        cut_a = int((a + max_gap / 2) * SR)
        cut_b = int((b - max_gap / 2) * SR)
        if cut_b > cut_a + nf:
            seg = audio[last:cut_a].copy()
            if len(seg) > nf:
                seg[-nf:] *= np.linspace(1, 0, nf)
            out.append(seg)
            last = cut_b
    seg = audio[last:].copy()
    if last and len(seg) > nf:
        seg[:nf] *= np.linspace(0, 1, nf)
    out.append(seg)
    return np.concatenate(out)


def edge_fade(audio, fade=0.012):
    n = min(int(fade * SR), len(audio) // 2)
    if n > 0:
        audio = audio.copy(); audio[:n] *= np.linspace(0, 1, n); audio[-n:] *= np.linspace(1, 0, n)
    return audio


def word_times(words, duration, audio):
    """Verteilt die Wörter auf die Sprechabschnitte zwischen den Pausen."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if PUNCT_RE.search(w["display"]) and i < len(words) - 1:
            chunks.append(cur)
            cur = []
    chunks.append(cur)
    gaps = sorted(pauses(audio), key=lambda p: p[1] - p[0], reverse=True)[: len(chunks) - 1]
    gaps = sorted(gaps)
    if len(gaps) == len(chunks) - 1:
        bounds, t = [], 0.0
        for g in gaps:
            bounds.append((t, g[0]))
            t = g[1]
        bounds.append((t, duration))
    else:  # Fallback: ganze Zeile nach Silben
        chunks, bounds = [list(range(len(words)))], [(0.0, duration)]
    times = [None] * len(words)
    for chunk, (a, b) in zip(chunks, bounds):
        weights = [syllables(words[i]["spoken"]) for i in chunk]
        total, t = sum(weights), a
        for i, wt in zip(chunk, weights):
            d = (b - a) * wt / total
            times[i] = (round(t, 3), round(t + d, 3))
            t += d
    return times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--backend", choices=["gemini", "google", "coqui", "piper"], default="coqui")
    ap.add_argument("--voice-dir", help="Piper-Stimmenordner oder Coqui-Modellordner (Standard: aus tools/setup.sh)")
    ap.add_argument("--coqui-python", default=str(CACHE / "coqui" / "bin" / "python"))
    ap.add_argument("--speed", type=float, default=1.0, help="Grundtempo (>1 = schneller); pro Zeile mit 'speed' feinjustierbar")
    ap.add_argument("--voice", default="thorsten-vits", help="Stimme im Cache: css10 (weiblich, coqui), thorsten-vits (männlich, coqui), "
                    "voice-de-kerstin-low / voice-de-ramona-low (weiblich, piper), voice-de-thorsten-low")
    ap.add_argument("--noise-dp", type=float, default=0.8, help="Variation im Sprechrhythmus/Betonung (coqui), höher = lebendiger")
    ap.add_argument("--max-gap", type=float, default=0.55, help="längste Pause innerhalb einer Zeile in Sekunden")
    ap.add_argument("--noise", type=float, default=0.667, help="Ausdruck/Variation der Stimme (0.33 monoton … 0.9 lebhaft)")
    args = ap.parse_args()

    if not args.voice_dir:
        args.voice_dir = "" if args.backend in ("google", "gemini") else str(CACHE / (args.voice if args.voice != "css10" else "css10-vits"))
    project = Path(args.project)
    script = json.loads((project / "script.json").read_text())
    lines = []
    for si, scene in enumerate(script["scenes"]):
        for li, line in enumerate(scene["lines"]):
            words = parse_tokens(line["text"])
            spoken = " ".join(w["spoken"] for w in words)
            lines.append({"scene": scene["id"], "id": line["id"], "words": words, "spoken": spoken,
                          "new_scene": li == 0 and si > 0, "pause": line.get("pause", 0.0),
                          "scale": round(1.0 / (args.speed * line.get("speed", 1.0)), 3), "skip": line.get("skip", False)})

    texts = [l["spoken"] for l in lines]
    scales = [l["scale"] for l in lines]
    if args.backend == "gemini" and script.get("tts_single"):  # eine Aufnahme für alles = eine Stimme
        raw = synth_gemini_single([l["words"] for l in lines], texts, args.voice, scales, script.get("style"),
                                  project / "assets" / "voice" / "cache", script.get("tts_model", "gemini-2.5-pro-preview-tts"),
                                  [l["id"] for l in lines], script.get("cut_shift"),
                                  [ln.get("join_prev", False) for sc in script["scenes"] for ln in sc["lines"]])
    elif args.backend == "gemini":  # --voice z. B. Fenrir/Puck; Stil aus script.json "style", pro Zeile "style"
        raw = synth_gemini(texts, args.voice, scales, script.get("style"),
                           [ln.get("style") for sc in script["scenes"] for ln in sc["lines"]], project / "assets" / "voice" / "cache",
                           script.get("tts_model", "gemini-2.5-pro-preview-tts"))
    elif args.backend == "google":
        raw = synth_google(texts, args.voice if args.voice.startswith("de-DE") else "de-DE-Chirp3-HD-Puck", scales,
                           script.get("pronunciations"))
    elif args.backend == "piper":
        raw = synth_piper(texts, args.voice_dir, scales, args.noise)
    else:
        raw = synth_coqui(texts, args.voice_dir, args.coqui_python, scales, args.noise, args.noise_dp)

    keep = [i for i, l in enumerate(lines) if not l["skip"]]  # "skip": true = Zeile bleibt in der Aufnahme, fliegt aber raus
    lines, raw = [lines[i] for i in keep], [raw[i] for i in keep]
    if lines:
        lines[0]["new_scene"] = False
    out_dir = project / "assets" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    lead = script.get("lead_in", LEAD_IN)
    pieces, t = [np.zeros(int(lead * SR), dtype="float32")], lead
    for line, (audio, sr) in zip(lines, raw):
        audio = resample(audio.astype("float32"), sr)
        if args.backend not in ("google", "gemini"):  # echte Stimme braucht keine Klang-Reparatur
            audio = clarity(audio)
        audio = edge_fade(compress_pauses(trim(audio), args.max_gap))
        if line["new_scene"]:
            gap = GAP_SCENE
        elif len(pieces) > 1:
            gap = GAP_LINE
        else:
            gap = 0
        gap += line["pause"]
        pieces.append(np.zeros(int(gap * SR), dtype="float32"))
        t += gap
        dur = len(audio) / SR
        for w, (a, b) in zip(line["words"], word_times(line["words"], dur, audio)):
            w["start"], w["end"] = round(t + a, 3), round(t + b, 3)
        line["start"], line["end"] = round(t, 3), round(t + dur, 3)
        pieces.append(audio)
        t += dur
    pieces.append(np.zeros(int(0.5 * SR), dtype="float32"))
    audio = np.concatenate(pieces)
    audio = audio / max(1e-6, np.max(np.abs(audio))) * 0.89  # ~ -1 dBFS Spitze
    raw_path = out_dir / "narration_raw.wav"
    sf.write(raw_path, audio, SR)
    # Lautheit für Social Media: -16 LUFS, True Peak -1.5 dB
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw_path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", str(SR), out_dir / "narration.wav"], check=True)
    raw_path.unlink()
    for l in lines:
        for k in ("new_scene", "pause", "scale"):
            l.pop(k)
    (out_dir / "timings.json").write_text(json.dumps({"duration": round(len(audio) / SR, 3), "lines": lines},
                                                     ensure_ascii=False, indent=1))
    print(f"narration.wav: {len(audio) / SR:.2f} s, {len(lines)} Zeilen")


if __name__ == "__main__":
    main()
