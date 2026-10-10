# Builds out/letter.mp4: title card -> the ten letters (file-time order) -> thank-you card.
# Every clip is fitted to 1920x1080 (narrow/vertical ones over a blurred copy of themselves),
# speech is loudness-matched to -16 LUFS, clips dissolve into each other, and the piano bed
# sits about 16 dB under the voices (fuller on the title and end cards).
import os, subprocess, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
U = "/root/.claude/uploads/30b06dac-850a-5f38-b785-a51192120c1a"
CLIPS = ["0cb828eb-2026_10_07_21_45", "1c694908-2026_10_07_22_02", "244042fe-2026_10_08_06_58",
         "1c46b6b6-2026_10_08_06_58_1", "411ff7e2-2026_10_08_12_24", "202fc31e-2026_10_08_12_26",
         "c9744781-2026_10_08_12_26_1", "8d875fb2-2026_10_08_12_52", "5610a1bf-KakaoTalk_20261011_004352865",
         "3c80efe5-KakaoTalk_20261011_004403880"]
X = 0.6  # dissolve length
os.makedirs("work", exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True)
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
FIT = ("[0:v]split=2[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:4,eq=brightness=-0.06[bg];"
       "[b]scale=1920:1080:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p,setsar=1[v]")
parts = []
for name, src in [("title", "out/title-16x9.mp4")] + [(f"c{i:02d}", f"{U}/{c}.mp4") for i, c in enumerate(CLIPS)] + [("end", "out/end-16x9.mp4")]:
    out = f"work/{name}.mp4"
    if not os.path.exists(out):
        if name in ("title", "end"):
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", FIT,
                 "-map", "[v]", "-map", "1:a", "-shortest", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-ar", "48000", out])
        else:
            run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", FIT + ";[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo[a]",
                 "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", out])
    parts.append((name, out, dur(out)))
    print(name, round(parts[-1][2], 2))
# dissolve chain
inputs, vf, af = [], "", ""
off, vlast, alast = 0.0, "0:v", "0:a"
for i, (_, f, d) in enumerate(parts):
    inputs += ["-i", f]
starts = [0.0]
for i in range(1, len(parts)):
    off += parts[i - 1][2] - X
    starts.append(off)
    vf += f"[{vlast}][{i}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[v{i}];"
    af += f"[{alast}][{i}:a]acrossfade=d={X}:c1=tri:c2=tri[a{i}];"
    vlast, alast = f"v{i}", f"a{i}"
total = off + parts[-1][2]
speech_a, speech_b = starts[1], starts[-1] + X  # letters run from the first clip to the end card
# piano bed: loop the 150 s track with crossfades until it covers the whole film
bed = "[%d:a]aresample=48000,aformat=channel_layouts=stereo,asplit=3[b0][b1][b2];[b0][b1]acrossfade=d=4[b01];[b01][b2]acrossfade=d=4,atrim=0:%.3f," % (len(parts), total)
bed += ("volume=eval=frame:volume='0.09+(0.37-0.09)*(clip((%.3f-t)/1.5\\,0\\,1)+clip((t-%.3f)/1.5\\,0\\,1))'," % (speech_a + 0.3, speech_b - 0.3))
bed += "afade=t=in:d=1.5,afade=t=out:st=%.3f:d=3[bed];" % (total - 3)
mix = f"[{alast}][bed]amix=inputs=2:normalize=0,alimiter=limit=0.89[aout]"
cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", "assets/audio/bgm.mp3", "-filter_complex", vf + af + bed + mix,
       "-map", f"[{vlast}]", "-map", "[aout]", "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/letter.mp4"]
run(cmd)
json.dump({"starts": starts, "total": total}, open("work/timeline.json", "w"))
print("total", round(total, 2), "clip starts", [round(s, 1) for s in starts])
