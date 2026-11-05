#!/usr/bin/env python3
"""Generate natural-voice audio for one Daily Reading A2 day file and write the audio map into it.

Usage:  (cd content) python3 ../kit/gen_audio.py days/2026-11-06.json
Needs:  pip install --break-system-packages kokoro-onnx soundfile ; ffmpeg on PATH.
Model files are downloaded once into ./tts-model/ from the kokoro-onnx GitHub release.

Voices: each of the day's 3 texts (with its words, examples, key sentences and grammar examples)
is read by a different voice. 12 voices rotate in the fixed order below (US female, US male,
UK female, UK male, ...), 3 per day, so the cycle repeats every 4 days. 2026-11-06 starts at voice 1.

Output: audio/<date>/a{n}-p{i}.mp3 (paragraphs), a{n}-w-*.mp3 / a{n}-ex-*.mp3 (words, examples),
        a{n}-ks{i}.mp3 (key sentences), a{n}-g{i}.mp3 (grammar examples).
        The day file gets "audio" {text: path}; each article gets "voice" (a short label for the page).
"""
import datetime, json, os, re, subprocess, sys, urllib.request

MODEL_DIR = "tts-model"
REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
VOICES = [  # (kokoro voice, language, label shown to students)
    ("af_heart",    "en-us", "American English · female"),
    ("am_michael",  "en-us", "American English · male"),
    ("bf_emma",     "en-gb", "British English · female"),
    ("bm_george",   "en-gb", "British English · male"),
    ("af_bella",    "en-us", "American English · female"),
    ("am_fenrir",   "en-us", "American English · male"),
    ("bf_isabella", "en-gb", "British English · female"),
    ("bm_fable",    "en-gb", "British English · male"),
    ("af_nicole",   "en-us", "American English · female"),
    ("am_puck",     "en-us", "American English · male"),
    ("bf_alice",    "en-gb", "British English · female"),
    ("bm_lewis",    "en-gb", "British English · male"),
]
START = datetime.date(2026, 11, 6)

def voices_for(date):
    d = (datetime.date.fromisoformat(date) - START).days
    first = (d * 3) % len(VOICES)
    return [VOICES[(first + i) % len(VOICES)] for i in range(3)]

def fetch(name):
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, name)
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        print("downloading", name); urllib.request.urlretrieve(REL + name, path)
    return path

def main(day_path):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(fetch("kokoro-v1.0.onnx"), fetch("voices-v1.0.bin"))
    day = json.load(open(day_path))
    date = day["date"]; out = f"audio/{date}"; os.makedirs(out, exist_ok=True)
    amap = {}

    for ai, (a, (voice, lang, label)) in enumerate(zip(day["articles"], voices_for(date)), 1):
        a["voice"] = label
        print(f"text {ai}: {voice} ({label})")

        def gen(text, name, speed=0.9):
            path = f"{out}/{name}.mp3"
            if text in amap: return  # same sentence already recorded for this day
            if not os.path.exists(path):
                samples, sr = k.create(text, voice=voice, speed=speed, lang=lang)
                sf.write("_tmp.wav", samples, sr)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "_tmp.wav", "-ac", "1", "-b:a", "48k", path], check=True)
            amap[text] = path

        for pi, p in enumerate(a["paras"], 1): gen(p, f"a{ai}-p{pi}")
        for w in a["words"]:
            slug = re.sub(r"[^a-z]+", "-", w["w"].lower()).strip("-")
            gen(w["w"], f"a{ai}-w-{slug}", 0.8); gen(w["ex"], f"a{ai}-ex-{slug}")
        for si, ks in enumerate(a.get("keySentences", []), 1): gen(ks["text"], f"a{ai}-ks{si}")
        for gi, ex in enumerate(a.get("grammar", {}).get("examples", []), 1): gen(ex["text"], f"a{ai}-g{gi}")

    day["audio"] = amap
    json.dump(day, open(day_path, "w"), ensure_ascii=False, indent=1)
    if os.path.exists("_tmp.wav"): os.remove("_tmp.wav")
    used = {os.path.basename(p) for p in amap.values()}
    for f in os.listdir(out):
        if f not in used: os.remove(os.path.join(out, f))
    print(f"{len(amap)} audio files in {out}")

if __name__ == "__main__":
    main(sys.argv[1])
