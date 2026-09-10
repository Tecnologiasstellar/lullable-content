#!/usr/bin/env python3
"""
lullable_polly.py — take a Lullable ElevenLabs break-tag narration file and
render it with Amazon Polly, keeping the channel's slow rhythm intact.

Subcommands
-----------
  convert   ElevenLabs break-tag .txt  ->  Polly-legal .ssml  (+ cadence/cost report)
  cost      cost estimate per engine, no AWS calls
  audition  render a short excerpt across candidate voices so you can pick one
  render    render the full episode via StartSpeechSynthesisTask (async -> S3)
  master    ffmpeg post-pass: slow, weight, level -> AAC-LC M4A (Lullable audio std)

Design notes
------------
* Polly bills TEXT characters only; SSML tags are free. Break-heavy files are cheap.
* <break time="..."/> caps at 10s in Polly. Lullable maxes at 3.0s, so nothing clips.
* SynthesizeSpeech caps at 3,000 billed chars. A 45-min episode is ~23k, so the
  async StartSpeechSynthesisTask (100k billed / 200k total) is the correct API.
  `--sync` falls back to paragraph-chunked SynthesizeSpeech + ffmpeg concat.
* <prosody rate> is only PARTIALLY supported on long-form/generative engines.
  Do not depend on it. Slow the read deterministically in `master` instead.

Requires: boto3 (render/audition), ffmpeg (master, --sync concat).
"""

import argparse
import html
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------- constants

PRICE_PER_MCHAR = {  # USD per 1,000,000 billed characters
    "standard": 4.00,
    "neural": 16.00,
    "generative": 30.00,
    "long-form": 100.00,
}

# Candidates worth auditioning for a deep/soft sleep read.
AUDITION_SET = [
    # (voice, engine, note)
    ("Patrick",  "long-form",  "en-US male, low + unhurried — closest to a sleep narrator"),
    ("Ruth",     "long-form",  "en-US female, warm and low, built for long-form narration"),
    ("Danielle", "long-form",  "en-US female, softest of the three"),
    ("Gregory",  "generative", "en-US male, deepest/most resonant in the catalogue"),
    ("Stephen",  "generative", "en-US male, calm and measured"),
    ("Brian",    "generative", "en-GB male, dark timbre — strong sleep-story fit"),
    ("Amy",      "generative", "en-GB female, soft and even"),
    ("Matthew",  "generative", "en-US male, warm mid-range"),
]

SYNC_BILLED_LIMIT = 2900   # headroom under Polly's 3,000 billed-char cap
MAX_BREAK_S = 10.0

# ---------------------------------------------------------------- helpers

TAG_RE = re.compile(r"<[^>]+>")
BREAK_RE = re.compile(r'<break\s+time="([0-9.]+)(s|ms)"\s*/?>')


def strip_tags(s: str) -> str:
    return TAG_RE.sub("", s)


def billed_chars(s: str) -> int:
    """Polly bills text only — SSML tags are not counted."""
    return len(strip_tags(s))


def escape_prose(text: str) -> str:
    """XML-escape the prose while leaving existing <break/> tags alone."""
    parts = re.split(r"(<break\s+[^>]*/?>)", text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:                      # a break tag
            out.append(part if part.endswith("/>") else part[:-1] + "/>")
        else:
            out.append(html.escape(part, quote=False))
    return "".join(out)


def paragraphs(text: str):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def cadence_report(raw: str) -> dict:
    plain = strip_tags(raw)
    words = len(plain.split())
    breaks = [float(v) * (0.001 if u == "ms" else 1) for v, u in BREAK_RE.findall(raw)]
    return {
        "words": words,
        "billed_chars": len(plain),
        "breaks": len(breaks),
        "silence_s": round(sum(breaks), 1),
        "max_break_s": max(breaks) if breaks else 0.0,
        "words_per_break": round(words / len(breaks), 2) if breaks else 0.0,
        "exclamations": plain.count("!"),
    }


def estimate_runtime(rep: dict, wpm: float) -> float:
    """Minutes of audio = speech time + engineered silence."""
    return rep["words"] / wpm + rep["silence_s"] / 60.0


# ---------------------------------------------------------------- convert

def scale_breaks(raw: str, factor: float) -> str:
    """Multiply every authored break duration by `factor`, capped at Polly's 10s."""
    def repl(m):
        val, unit = float(m.group(1)), m.group(2)
        secs = val * (0.001 if unit == "ms" else 1.0) * factor
        secs = min(round(secs, 1), MAX_BREAK_S)
        return f'<break time="{secs}s"/>'
    return BREAK_RE.sub(repl, raw)


def cmd_convert(a):
    raw = Path(a.infile).read_text(encoding="utf-8")
    if a.pause_scale != 1.0:
        raw = scale_breaks(raw, a.pause_scale)
    rep = cadence_report(raw)

    problems = []
    if rep["max_break_s"] > MAX_BREAK_S:
        problems.append(f"break of {rep['max_break_s']}s exceeds Polly's {MAX_BREAK_S}s cap")
    if rep["exclamations"]:
        problems.append(f"{rep['exclamations']} exclamation mark(s) — house voice forbids them")
    if rep["words_per_break"] > 15.0:
        problems.append(f"{rep['words_per_break']} words/break exceeds the 15.0 ceiling")
    if problems:
        for p in problems:
            print(f"REFUSING: {p}", file=sys.stderr)
        if not a.force:
            sys.exit(1)

    body = escape_prose(raw)
    if a.paragraph_tags:
        body = "\n".join(f"<p>{escape_prose(p)}</p>" for p in paragraphs(raw))

    ssml = f'<speak xml:lang="{a.lang}">\n{body}\n</speak>\n'
    out = Path(a.out or Path(a.infile).with_suffix(".polly.ssml"))
    out.write_text(ssml, encoding="utf-8")

    print(f"wrote {out}")
    print(f"  words             {rep['words']:,}")
    print(f"  billed characters {rep['billed_chars']:,}   (SSML tags are free)")
    print(f"  break tags        {rep['breaks']}  ->  {rep['silence_s']}s of engineered silence")
    print(f"  words per break   {rep['words_per_break']}   (ceiling 15.0)")
    print(f"  longest break     {rep['max_break_s']}s   (Polly cap {MAX_BREAK_S}s)")
    for wpm in (118, 135, 150):
        print(f"  est. runtime @{wpm} wpm  {estimate_runtime(rep, wpm):.1f} min")
    print()
    _print_cost(rep["billed_chars"], a.episodes)


def _print_cost(chars: int, episodes: int):
    print(f"cost for {chars:,} billed chars x {episodes} episode(s):")
    for eng, price in PRICE_PER_MCHAR.items():
        per = chars * price / 1_000_000
        print(f"  {eng:<11} ${per:>6.2f} / episode    ${per * episodes:>8.2f} total")


def cmd_cost(a):
    raw = Path(a.infile).read_text(encoding="utf-8")
    _print_cost(billed_chars(raw), a.episodes)


# ---------------------------------------------------------------- polly io

def _polly(region):
    import boto3
    return boto3.client("polly", region_name=region)


def cmd_audition(a):
    """Render the opening of the episode across every candidate voice."""
    raw = Path(a.infile).read_text(encoding="utf-8")
    excerpt = "\n\n".join(paragraphs(raw)[: a.paragraphs])
    ssml = f'<speak xml:lang="{a.lang}">\n{escape_prose(excerpt)}\n</speak>'
    if billed_chars(ssml) > SYNC_BILLED_LIMIT:
        print(f"excerpt is {billed_chars(ssml)} billed chars; use fewer --paragraphs",
              file=sys.stderr)
        sys.exit(1)

    outdir = Path(a.outdir); outdir.mkdir(parents=True, exist_ok=True)
    polly = _polly(a.region)
    for voice, engine, note in AUDITION_SET:
        if a.only and voice.lower() not in {v.lower() for v in a.only}:
            continue
        dest = outdir / f"{voice}-{engine}.mp3"
        try:
            r = polly.synthesize_speech(
                Text=ssml, TextType="ssml", VoiceId=voice, Engine=engine,
                OutputFormat="mp3", SampleRate=a.sample_rate,
            )
            dest.write_bytes(r["AudioStream"].read())
            print(f"  {dest.name:<26} {note}")
        except Exception as e:                       # noqa: BLE001
            print(f"  {voice}/{engine}: FAILED — {e}", file=sys.stderr)
    print(f"\naudition written to {outdir}. Listen in the dark, at bedtime volume.")


def cmd_render(a):
    """Full episode via the async task API (the only API that fits 23k chars)."""
    ssml = Path(a.ssml).read_text(encoding="utf-8")
    chars = billed_chars(ssml)
    if chars > 100_000:
        print(f"{chars:,} billed chars exceeds the 100k async cap", file=sys.stderr)
        sys.exit(1)

    polly = _polly(a.region)
    task = polly.start_speech_synthesis_task(
        Text=ssml, TextType="ssml", VoiceId=a.voice, Engine=a.engine,
        OutputFormat=a.format, SampleRate=a.sample_rate,
        OutputS3BucketName=a.bucket,
        OutputS3KeyPrefix=a.prefix,
    )["SynthesisTask"]
    tid = task["TaskId"]
    print(f"task {tid} submitted ({a.voice}/{a.engine}, {chars:,} billed chars, "
          f"${chars * PRICE_PER_MCHAR[a.engine] / 1e6:.2f})")

    while True:
        t = polly.get_speech_synthesis_task(TaskId=tid)["SynthesisTask"]
        status = t["TaskStatus"]
        if status == "completed":
            uri = t["OutputUri"]
            print(f"done -> {uri}")
            if a.download:
                import boto3, urllib.parse
                key = urllib.parse.urlparse(uri).path.split(f"/{a.bucket}/", 1)[-1].lstrip("/")
                boto3.client("s3", region_name=a.region).download_file(a.bucket, key, a.download)
                print(f"downloaded -> {a.download}")
            return
        if status == "failed":
            print(f"FAILED: {t.get('TaskStatusReason')}", file=sys.stderr)
            sys.exit(1)
        time.sleep(a.poll)


# ---------------------------------------------------------------- master

def cmd_master(a):
    """
    Deterministic 'weight and slowness' pass. Polly's prosody support is partial
    on long-form/generative, so shape the audio here instead of in the SSML.

      --tempo 0.94   slows the read without touching pitch
      --semitones -1 drops the voice, pitch-preserving tempo held at 1.0
      then: gentle low shelf, de-ess-ish high shelf, soft limiter, AAC-LC M4A
    """
    rate = 44100
    pitch = 2 ** (a.semitones / 12.0)
    chain = []
    if a.semitones:
        chain.append(f"asetrate={rate}*{pitch:.6f},aresample={rate},atempo={1/pitch:.6f}")
    if a.tempo != 1.0:
        chain.append(f"atempo={a.tempo}")
    chain.append(f"equalizer=f=180:t=q:w=0.9:g={a.warmth}")     # body
    chain.append("equalizer=f=7000:t=q:w=1.0:g=-2")             # take the edge off
    chain.append("acompressor=threshold=-18dB:ratio=2.5:attack=25:release=400")
    chain.append(f"loudnorm=I={a.lufs}:TP=-2:LRA=7")
    chain.append("aresample=44100")

    cmd = ["ffmpeg", "-y", "-i", a.infile, "-af", ",".join(chain),
           "-ac", "1", "-c:a", "aac", "-profile:a", "aac_low", "-b:a", "96k",
           "-ar", "44100", a.out]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"mastered -> {a.out}  (AAC-LC M4A 44.1k mono 96k, {a.lufs} LUFS)")


# ---------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("convert", help="ElevenLabs break-tag txt -> Polly SSML")
    c.add_argument("infile")
    c.add_argument("--out")
    c.add_argument("--lang", default="en-US")
    c.add_argument("--paragraph-tags", action="store_true",
                   help="wrap paragraphs in <p> (adds pause ON TOP of your breaks)")
    c.add_argument("--episodes", type=int, default=1)
    c.add_argument("--pause-scale", type=float, default=1.0,
                   help="multiply every authored break by this factor (1.25 = 25%% more silence)")
    c.add_argument("--force", action="store_true")
    c.set_defaults(func=cmd_convert)

    k = sub.add_parser("cost", help="cost per engine, no AWS calls")
    k.add_argument("infile")
    k.add_argument("--episodes", type=int, default=1)
    k.set_defaults(func=cmd_cost)

    d = sub.add_parser("audition", help="render an excerpt across candidate voices")
    d.add_argument("infile")
    d.add_argument("--outdir", default="audition")
    d.add_argument("--paragraphs", type=int, default=6)
    d.add_argument("--lang", default="en-US")
    d.add_argument("--region", default=os.environ.get("AWS_REGION", "us-east-1"))
    d.add_argument("--sample-rate", default="24000")
    d.add_argument("--only", nargs="*")
    d.set_defaults(func=cmd_audition)

    r = sub.add_parser("render", help="full episode via async task -> S3")
    r.add_argument("ssml")
    r.add_argument("--voice", default="Patrick")
    r.add_argument("--engine", default="long-form", choices=list(PRICE_PER_MCHAR))
    r.add_argument("--bucket", required=True)
    r.add_argument("--prefix", default="lullable/")
    r.add_argument("--format", default="mp3", choices=["mp3", "ogg_vorbis", "pcm"])
    r.add_argument("--sample-rate", default="24000")
    r.add_argument("--region", default=os.environ.get("AWS_REGION", "us-east-1"))
    r.add_argument("--download")
    r.add_argument("--poll", type=int, default=5)
    r.set_defaults(func=cmd_render)

    m = sub.add_parser("master", help="ffmpeg slow/weight/level pass -> M4A")
    m.add_argument("infile")
    m.add_argument("--out", default="master.m4a")
    m.add_argument("--tempo", type=float, default=1.0, help="0.94 = 6%% slower, pitch intact")
    m.add_argument("--semitones", type=float, default=0.0, help="-1 to -2 adds weight")
    m.add_argument("--warmth", type=float, default=1.5, help="dB of low-shelf lift at 180Hz")
    m.add_argument("--lufs", type=float, default=-20.0, help="quiet target for bedtime")
    m.set_defaults(func=cmd_master)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
