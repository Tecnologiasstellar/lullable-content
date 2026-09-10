#!/usr/bin/env python3
"""Batch driver: convert all story texts (pause-scale 1.25), submit Polly tasks,
poll, download, master. State in batch-state.json so steps are resumable."""
import json, re, html, sys, time, subprocess, pathlib
import boto3

BUCKET = "lullable-audio-864981744724"
REGION = "us-east-1"
SCALE = 1.25
BASE = pathlib.Path("/mnt/user-data/uploads/Stories")
WORK = pathlib.Path("/home/claude/polly/batchout")
WORK.mkdir(exist_ok=True)
STATE = pathlib.Path("/home/claude/polly/batch-state.json")

CAST = {  # storyID -> (voice, engine)
    "a-roman-bathhouse-at-closing-time": ("Arthur", "neural"),
    "the-building-of-a-cathedral": ("Arthur", "neural"),
    "the-great-library-of-alexandria": ("Arthur", "neural"),
    "the-joinery-of-japan-s-wooden-temples": ("Arthur", "neural"),
    "floating-through-the-pillars-of-creation": ("Amy", "generative"),
    "mapping-the-cosmic-web": ("Amy", "generative"),
    "the-life-cycle-of-a-red-dwarf-star": ("Amy", "generative"),
    "the-moons-of-jupiter-europa-s-ice-and-ocean": ("Amy", "generative"),
    "the-rings-of-saturn": ("Amy", "generative"),
    "voyager-1-a-journey-to-interstellar-space": ("Amy", "generative"),
    "the-observatory-on-ben-nevis": ("Patrick", "long-form"),
    "the-slow-life-of-a-redwood": ("Patrick", "long-form"),
    "the-bakery-before-dawn": ("Niamh", "generative"),
    "the-clockmaker-s-workshop": ("Niamh", "generative"),
    "the-journey-of-a-glacial-river": ("Niamh", "generative"),
    "the-midnight-sleeper-train-across-the-alps": ("Niamh", "generative"),
    "the-bay-that-glows-at-night": ("Brian", "generative"),
    # the-deep-ocean-trenches: already rendered with correct recipe (Brian + 1.25)
}

BREAK_RE = re.compile(r'<break\s+time="([0-9.]+)(s|ms)"\s*/?>')

def scale_breaks(raw):
    def r(m):
        s = float(m.group(1)) * (0.001 if m.group(2) == "ms" else 1.0) * SCALE
        return f'<break time="{min(round(s,1),10.0)}s"/>'
    return BREAK_RE.sub(r, raw)

def esc(t):
    parts = re.split(r"(<break\s+[^>]*/?>)", t)
    return "".join(p if i % 2 else html.escape(p, quote=False) for i, p in enumerate(parts))

def to_ssml(sid):
    src = BASE / sid / "upload-to-elevenlabs.txt"
    if sid == "the-bay-that-glows-at-night":
        src = pathlib.Path("/home/claude/polly/episode.txt")
    raw = scale_breaks(src.read_text())
    ssml = f'<speak>\n{esc(raw)}\n</speak>\n'
    out = WORK / f"{sid}.ssml"
    out.write_text(ssml)
    return ssml

def load():
    return json.loads(STATE.read_text()) if STATE.exists() else {}

def save(st):
    STATE.write_text(json.dumps(st, indent=1))

def submit():
    polly = boto3.Session(region_name=REGION).client("polly")
    st = load()
    for sid, (voice, engine) in CAST.items():
        if st.get(sid, {}).get("task"):
            continue
        ssml = to_ssml(sid)
        for attempt in range(8):
            try:
                t = polly.start_speech_synthesis_task(
                    Text=ssml, TextType="ssml", VoiceId=voice, Engine=engine,
                    OutputFormat="mp3", SampleRate="24000",
                    OutputS3BucketName=BUCKET, OutputS3KeyPrefix=f"stories/{sid}/")
                st[sid] = {"task": t["SynthesisTask"]["TaskId"], "voice": voice,
                           "engine": engine, "status": "submitted"}
                print(f"submitted {sid} -> {voice}/{engine}")
                break
            except Exception as e:
                if "Throttl" in str(e) or "Rate" in str(e):
                    time.sleep(3 + attempt * 2)
                else:
                    st[sid] = {"status": "submit-failed", "error": str(e)[:200]}
                    print(f"FAILED submit {sid}: {e}", file=sys.stderr)
                    break
        save(st)
        time.sleep(1.3)  # generative/long-form task APIs are 1 TPS

def poll():
    ses = boto3.Session(region_name=REGION)
    polly, s3 = ses.client("polly"), ses.client("s3")
    st = load()
    pending = True
    while pending:
        pending = False
        for sid, rec in st.items():
            if rec.get("status") in ("done", "failed", "submit-failed"):
                continue
            t = polly.get_speech_synthesis_task(TaskId=rec["task"])["SynthesisTask"]
            if t["TaskStatus"] == "completed":
                key = f"stories/{sid}/.{rec['task']}.mp3"
                dest = WORK / f"{sid}.raw.mp3"
                s3.download_file(BUCKET, key, str(dest))
                rec["status"] = "done"
                print(f"done {sid} ({rec['voice']})")
            elif t["TaskStatus"] == "failed":
                rec["status"] = "failed"
                rec["error"] = t.get("TaskStatusReason", "?")[:200]
                print(f"FAILED {sid}: {rec['error']}", file=sys.stderr)
            else:
                pending = True
        save(st)
        if pending:
            time.sleep(20)

def master():
    st = load()
    for sid, rec in st.items():
        if rec.get("status") != "done" or rec.get("mastered"):
            continue
        raw = WORK / f"{sid}.raw.mp3"
        m4a = WORK / f"{sid}.delivery.m4a"
        chain = ("atempo=0.93,equalizer=f=180:t=q:w=0.9:g=1.5,"
                 "equalizer=f=7000:t=q:w=1.0:g=-2,"
                 "acompressor=threshold=-18dB:ratio=2.5:attack=25:release=400,"
                 "loudnorm=I=-20:TP=-2:LRA=7,aresample=44100")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", chain,
                        "-ac", "1", "-c:a", "aac", "-profile:a", "aac_low",
                        "-b:a", "96k", "-ar", "44100", str(m4a)], check=True)
        rec["mastered"] = True
        d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", str(m4a)])
        rec["final_min"] = round(float(d) / 60, 1)
        save(st)
        print(f"mastered {sid}: {rec['final_min']} min")

if __name__ == "__main__":
    {"submit": submit, "poll": poll, "master": master}[sys.argv[1]]()
