# News "video link" version of the dialogue: the mayor full-frame from the waist up in his real
# office (his greeting footage; lines he never said are that footage lip-synced to his cloned
# voice, with his consent), and AI Seohui in a picture-in-picture window, top right, that opens
# when the mayor introduces him. Both look into the lens, as on a TV link-up.
#
# Mayor-derived media lives in WORK, outside the repo:
#   mayor-ai/ls-Lxx.mp4, m*.mp3   lip-synced mayor lines and their cloned-voice audio
#   seohui/*.mp4, v*pad.mp3       Seohui clips and the exact audio they were lip-synced to
#
#   WORK=/path/to/scratch python3 seohuiham-mayor/build_news.py
#   (then: cd $WORK/news && npx hyperframes render -o ../news.mp4)
import os
import subprocess

from build_dialogue import (ASSETS, DUR, FPS, GREETING, LISTEN, MAI, MAYOR, MAYOR_VOICE, SEO,
                            SHORTS, SUBS, WORK, chain, run)

PIP_OPEN = 24.6       # the window opens on "특별한 분을 한 분 모셨습니다"
# Seohui window track: (start, clip, clip start, duration); "loop" = front-facing listening loop
SEOHUI = [
    (0.0, "loop", 0.0, None),             # hidden until the window opens
    (26.6, "N6-sync.mp4", 0.0, None),     # 6 인사
    (36.4, "loop", 3.0, None),
    (44.6, "N8-sync.mp4", 0.0, None),     # 8 답변
    (56.5, "loop", 7.0, None),
    (72.8, "N11-sync.mp4", 0.0, None),    # 11 함께
    (77.0, "loop", 1.0, None),
]
# the exact (padded) audio each lip-sync was made from, so voice and mouth line up
SEOHUI_VOICE = [(26.6, "v6pad.mp3"), (44.6, "v8pad.mp3"), (72.8, "v11pad.mp3")]
TALK = [(26.4, 36.2), (44.4, 56.3), (72.6, 75.8)]  # window grows while Seohui speaks
CROP = (770, 222, 840)  # Seohui's head and shoulders in the 1920x1080 Seohui clips


# The mayor is his cut-out (background removed) over a clean plate of his own office, widened
# to the right, so the camera can pan and leave him on the left when Seohui's window opens.
# The plate is softly blurred: the strip behind his head is AI-filled and must not read as the
# city's real sign lettering.
PLATE = os.path.join(WORK, "office-plate.png")   # 2340x1080: clean office + right extension
PAN, PAN_T0, PAN_D = 380, PIP_OPEN - 1.0, 1.6
# Mayor track, cut line by line: (start, kind, a, b) — real: source start a; synced: lip-synced
# file a, source start b (b < 0: footage was reversed, window -b); listen: listening bank offset a
NEWS_MAYOR = [
    (0.0, "real", 0.8, None),               # 1
    (3.9, "real", 8.6, None),               # 2
    (8.4, "synced", "ls-L03.mp4", 31.0),    # 3
    (13.9, "real", 13.8, None),             # 4
    (22.8, "synced", "ls-L05.mp4", 36.3),   # 5
    (25.76, "listen", 0.0, None),           # 6 (Seohui)
    (36.3, "synced", "ls-L07.mp4", 22.9),   # 7
    (44.3, "listen", 11.0, None),           # 8 (Seohui)
    (56.4, "synced", "ls-L09.mp4", -8.4),   # 9 (footage from 14.0 s, played backwards)
    (64.9, "synced", "ls-L10.mp4", -7.5),   # 10 (footage from 0.9 s, played backwards)
    (72.8, "synced", "ls-L11.mp4", 5.5),    # 11
    (75.6, "listen", 5.0, None),
]
REVERSED_FROM = {"ls-L09.mp4": 14.0, "ls-L10.mp4": 0.9}
# every moment of the greeting where he is quiet: the listening shots are woven from these
PAUSES = [(4.15, 1.5), (12.93, 0.95), (19.43, 0.6), (29.92, 0.62), (8.12, 0.6), (35.55, 0.45),
          (38.65, 0.5), (15.1, 0.45)]
# framing per line (scale about the mayor's face); a change of size at each cut turns a pose jump
# into an ordinary edit, and the close-ups hide the hands in the reversed lines
FRAMING = [(0.0, 1.0), (3.9, 1.3), (8.4, 1.05), (13.9, 1.28), (22.8, 1.0), (36.3, 1.3),
           (44.3, 1.0), (56.4, 1.32), (64.9, 1.15), (72.8, 1.0)]


def cutout_piece(name, src, dur, video=None, reverse_window=None):
    """the mayor's cut-out as a lossless yuva file: his greeting chunks (src..src+dur), or a
    lip-synced file with the matte of the footage it was made from"""
    from build_dialogue import chunk_inputs
    out = os.path.join(WORK, "news-pieces", name + ".mkv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    frames = round(dur * FPS)
    args, n = chunk_inputs(src, reverse_window or dur + 0.2)
    body = "".join(f"[{j}]format=yuva420p,fps={FPS},setpts=PTS-STARTPTS[c{j}];" for j in range(n))
    joined = "".join(f"[c{j}]" for j in range(n)) + f"concat=n={n}:v=1"
    if video is None:
        fil = body + joined + f",trim=end_frame={frames},setpts=PTS-STARTPTS[out]"
    else:
        args += ["-i", video]
        alpha = joined + ",alphaextract"
        if reverse_window:
            alpha += f",trim=end_frame={round(reverse_window * FPS)},reverse"
        fil = (body + alpha + f",trim=end_frame={frames},setpts=PTS-STARTPTS[al];"
               f"[{n}:v]fps={FPS},scale=1920:1080,trim=end_frame={frames},setpts=PTS-STARTPTS,format=rgb24[lv];"
               f"[lv][al]alphamerge,format=yuva420p[out]")
    run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", fil, "-map", "[out]",
         "-frames:v", str(frames), "-c:v", "ffv1", out])
    return out


def build_listen_bank():
    """his quiet moments, each played forward then back, then the set again in another order"""
    parts = []
    for i, (s, d) in enumerate(PAUSES):
        f = cutout_piece(f"pause{i}", s, d)
        r = os.path.join(WORK, "news-pieces", f"pause{i}r.mkv")
        run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vf", "reverse", "-c:v", "ffv1", r])
        parts += [f, r]
    order = parts + parts[::-1][2:] + parts
    out = os.path.join(WORK, "news-pieces", "listen-bank.mkv")
    ins, fil, t, last = [], [], 0.0, "b0"
    for i, p in enumerate(order):
        ins += ["-i", p]
        fil.append(f"[{i}]fps={FPS},settb=1/{FPS},setpts=PTS-STARTPTS[b{i}]")
    for i in range(1, len(order)):
        t += float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                   "csv=p=0", order[i - 1]], capture_output=True, text=True).stdout) - 0.16
        fil.append(f"[{last}][b{i}]xfade=transition=fade:duration=0.16:offset={t:.3f}[k{i}]")
        last = f"k{i}"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", f"[{last}]",
         "-c:v", "ffv1", out])
    return out


def build_mayor():
    bank = build_listen_bank()
    segs = []
    for i, (start, kind, a, b) in enumerate(NEWS_MAYOR):
        end = NEWS_MAYOR[i + 1][0] if i + 1 < len(NEWS_MAYOR) else DUR
        d = end - start + 0.3
        if kind == "real":
            f = cutout_piece(f"line{i}", a, d)
        elif kind == "synced" and b < 0:
            f = cutout_piece(f"line{i}", REVERSED_FROM[a], d, os.path.join(MAI, a), -b)
        elif kind == "synced":
            f = cutout_piece(f"line{i}", b, d, os.path.join(MAI, a))
        else:
            f = None
        if f:
            segs.append((start, ["-i", f], f"fps={FPS},settb=1/{FPS},tpad=stop_mode=clone:stop_duration=1", 0.04))
        else:
            segs.append((start, ["-ss", str(a), "-i", bank], f"fps={FPS},settb=1/{FPS}",
                         0.25 if NEWS_MAYOR[i - 1][0] >= 22.8 and FRAMING_AT(start) == FRAMING_AT(NEWS_MAYOR[i - 1][0]) else 0.04))
    track = os.path.join(WORK, "news-mayor.mkv")
    chain(segs, track, "yuva420p", ["-c:v", "ffv1"], DUR)

    # composite on the widened, softened office and pan the camera right as the window opens
    s = f"((t-{PAN_T0})/{PAN_D})"
    px = f"if(lt(t\\,{PAN_T0})\\,0\\,if(gt(t\\,{PAN_T0 + PAN_D})\\,{PAN}\\,{PAN}*(3*pow({s}\\,2)-2*pow({s}\\,3))))"
    out = os.path.join(WORK, "news", "assets", "mayor.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", PLATE,
         "-i", track, "-filter_complex",
         f"[0]gblur=sigma=2.5,eq=brightness=-0.02[bg];[bg][1]overlay=0:0:eof_action=endall,"
         f"crop=1920:1080:x='{px}':y=0,format=yuv420p[out]", "-map", "[out]", "-t", str(DUR),
         "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium", out])


def FRAMING_AT(t):
    return [s for (u, s) in FRAMING if u <= t + 1e-6][-1]


def build_seohui():
    x, y, w = CROP
    loop = os.path.join(WORK, "seohui", "N-loop.mp4")
    # front-facing listening loop from the first 5.5 s of S1 (before his glance aside)
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0.3", "-t", "5.5", "-i", os.path.join(SEO, "S1.mp4"),
         "-filter_complex", f"[0]fps={FPS},scale=1920:1080,split[f][r0];[r0]reverse[r];[f][r]concat=n=2:v=1,"
         "loop=loop=3:size=300", "-an", "-c:v", "libx264", "-crf", "14", loop])
    segs = []
    for i, (start, clip, cs, _) in enumerate(SEOHUI):
        src = loop if clip == "loop" else os.path.join(SEO, clip)
        segs.append((start, ["-ss", str(cs), "-i", src], f"fps={FPS},scale=1920:1080,settb=1/{FPS}",
                     0.0 if i == 0 else 0.2))
    full = os.path.join(WORK, "seohui", "N-track.mp4")
    chain(segs, full, "yuv420p", ["-c:v", "libx264", "-crf", "12", "-preset", "fast"], DUR)
    out = os.path.join(WORK, "news", "assets", "seohui.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", full, "-vf",
         f"crop={w}:{round(w * 9 / 16)}:{x}:{y},scale=1280:720:flags=lanczos", "-c:v", "libx264",
         "-crf", "14", out])


def build_audio():
    ins, fil, mix = [], [], []

    def add(args, chain_, label):
        n = sum(1 for a in ins if a == "-i")
        ins.extend(args)
        fil.append(f"[{n}:a]{chain_}[{label}]")
        mix.append(f"[{label}]")

    norm = "loudnorm=I=-16:TP=-2:LRA=7,aresample=48000"
    for i, (start, kind, a, b, c) in enumerate(MAYOR):
        if kind == "real":
            add(["-ss", str(a), "-t", str(b), "-i", GREETING],
                f"afade=t=in:d=0.06,afade=t=out:st={b - 0.1:.2f}:d=0.1,{norm},adelay={int(start * 1000)}:all=1", f"m{i}")
        elif kind == "synced":
            add(["-i", os.path.join(MAI, MAYOR_VOICE[a])], f"{norm},adelay={int(start * 1000)}:all=1", f"m{i}")
    for j, (start, f) in enumerate(SEOHUI_VOICE):
        add(["-i", os.path.join(SEO, f)], f"{norm},adelay={int(start * 1000)}:all=1", f"s{j}")
    add(["-ss", "4.3", "-t", "1.3", "-i", GREETING],
        f"aloop=loop=-1:size=57330,atrim=0:{DUR},volume=0.9,aresample=48000", "air")
    add(["-ss", "4.9", "-t", "300", "-i", os.path.join(SHORTS, "shared/assets/music-gold3.mp3")],
        f"aloop=loop=-1:size=211680,atrim=0:{DUR},volume=0.1,afade=t=in:d=1.5,"
        f"afade=t=out:st={DUR - 3:.1f}:d=3,aresample=48000", "bed")
    fil.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,"
               f"atrim=0:{DUR},alimiter=limit=0.89[a]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[a]",
         "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(WORK, "news", "assets", "mix.mp3")])


def write_project():
    d = os.path.join(WORK, "news")
    os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
    os.makedirs(os.path.join(d, "compositions"), exist_ok=True)
    for f in ("Pretendard-Bold.woff2", "Pretendard-Medium.woff2"):
        run(["cp", os.path.join(ASSETS, f), os.path.join(d, "fonts", f)])
    here = os.path.dirname(os.path.abspath(__file__))
    for name, target in (("gsap.min.js", os.path.join(SHORTS, "shared/gsap.min.js")),
                         ("node_modules", os.path.join(here, "..", "hyperframes-kra-film/node_modules"))):
        p = os.path.join(d, name)
        if not os.path.lexists(p):
            os.symlink(os.path.abspath(target), p)
    open(os.path.join(d, "package.json"), "w").write(
        '{\n  "name": "seohuiham-news",\n  "private": true,\n  "type": "module",\n'
        '  "devDependencies": {\n    "hyperframes": "0.8.82"\n  }\n}\n')
    open(os.path.join(d, "hyperframes.json"), "w").write(
        '{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n'
        '  "paths": { "blocks": "compositions", "assets": "assets" },\n  "media": { "autoProxy": true }\n}\n')

    subs, js = "", ""
    for i, (a, b, text) in enumerate(SUBS):
        subs += f'        <div id="s{i}" class="sub">{text.replace("/", "<br />")}</div>\n'
        js += f'        tl.fromTo("#s{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});\n'
        js += f'        tl.to("#s{i}", {{ opacity: 0, duration: 0.2 }}, {b - 0.2:.2f});\n'
    # mayor: one framing per line, scaled about his face (which sits left after the pan);
    # each line holds a slow push-in so the frame is never dead still
    cuts = FRAMING + [(DUR, None)]
    for (t, sc), (t2, _) in zip(FRAMING, cuts[1:]):
        fx = 1020 if t < PAN_T0 else 1020 - PAN
        js += f'        tl.set("#mayor", {{ scale: {sc}, transformOrigin: "{fx}px 330px" }}, {t});\n'
        js += f'        tl.to("#mayor", {{ scale: {sc + 0.025:.3f}, duration: {t2 - t:.2f}, ease: "none" }}, {t});\n'
    # the window opens with a gold flash, then grows while Seohui speaks
    js += f'        tl.fromTo("#pip", {{ opacity: 0, scale: 0.55 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.4)" }}, {PIP_OPEN});\n'
    js += f'        tl.fromTo("#pip-flash", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.9, ease: "power2.out" }}, {PIP_OPEN + 0.3});\n'
    for a, b in TALK:
        js += f'        tl.to("#pip", {{ scale: 1.2, duration: 0.6, ease: "power2.inOut" }}, {a});\n'
        js += f'        tl.to("#pip", {{ scale: 1, duration: 0.6, ease: "power2.inOut" }}, {b - 0.4:.1f});\n'
    js += '        tl.fromTo("#tag-m", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.5);\n'
    js += '        tl.to("#tag-m", { opacity: 0, duration: 0.4 }, 5.0);\n'
    js += f'        tl.to("#fade", {{ opacity: 1, duration: 0.8 }}, {DUR - 0.8});\n'

    css = '''        @font-face { font-family: "Pretendard"; font-weight: 700; src: url("fonts/Pretendard-Bold.woff2") format("woff2"); }
        @font-face { font-family: "Pretendard"; font-weight: 500; src: url("fonts/Pretendard-Medium.woff2") format("woff2"); }
        #root { position: absolute; inset: 0; overflow: hidden; background: #000; font-family: "Pretendard"; }
        #mayor { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; transform-origin: 0 0; }
        #mayor video { position: absolute; inset: 0; width: 100%; height: 100%; }
        #pip { position: absolute; right: 50px; top: 50px; width: 800px; height: 450px; transform-origin: 100% 0;
          border: 3px solid #e3b25a; border-radius: 6px; overflow: hidden; background: #000; opacity: 0;
          box-shadow: 0 12px 40px rgba(0,0,0,0.55); }
        #pip video { position: absolute; inset: 0; width: 100%; height: 100%; }
        #pip-flash { position: absolute; inset: 0; background: radial-gradient(closest-side, rgba(255,230,160,0.95), rgba(227,178,90,0.4) 60%, rgba(227,178,90,0)); opacity: 0; }
        #pip-live { position: absolute; left: 12px; top: 10px; padding: 3px 10px; font-size: 16px; font-weight: 700;
          color: #1a1a1a; background: #e3b25a; border-radius: 4px; letter-spacing: 0.04em; }
        #pip-name { position: absolute; left: 0; right: 0; bottom: 0; padding: 10px 16px; font-size: 26px; font-weight: 700;
          color: #fff; background: linear-gradient(transparent, rgba(0,0,0,0.75)); }
        #pip-name small { font-size: 16px; font-weight: 500; color: #e3b25a; margin-right: 8px; }
        .sub { position: absolute; left: 0; right: 0; bottom: 92px; text-align: center; color: #fff; font-weight: 700;
          font-size: 46px; line-height: 1.38; text-shadow: 0 2px 8px rgba(0,0,0,0.85), 0 0 24px rgba(0,0,0,0.5); opacity: 0; }
        #tag-m { position: absolute; left: 90px; bottom: 250px; padding: 14px 26px; color: #fff; font-weight: 700; font-size: 34px;
          background: rgba(10,10,10,0.6); border-left: 5px solid #e3b25a; opacity: 0; }
        #tag-m small { display: block; font-size: 22px; font-weight: 500; color: #e3b25a; margin-bottom: 2px; }
        #badge { position: absolute; left: 36px; top: 30px; padding: 6px 14px; font-size: 22px; font-weight: 500;
          color: #fff; background: rgba(0,0,0,0.5); border-radius: 6px; }
        #ai-note { position: absolute; left: 0; right: 0; bottom: 30px; text-align: center; font-size: 21px; font-weight: 500;
          color: rgba(255,255,255,0.85); text-shadow: 0 1px 4px rgba(0,0,0,0.9); }
        #fade { position: absolute; inset: 0; background: #000; opacity: 0; }
'''
    body = f'''        <div id="mayor">
          <video id="v-mayor" src="assets/mayor.mp4" data-start="0" data-duration="{DUR}" muted playsinline></video>
        </div>
        <div id="pip">
          <video id="v-seohui" src="assets/seohui.mp4" data-start="0" data-duration="{DUR}" muted playsinline></video>
          <div id="pip-live">화상 연결</div>
          <div id="pip-name"><small>이천시 AI 홍보대사</small>서희</div>
          <div id="pip-flash"></div>
        </div>
        <div id="tag-m"><small>이천시장</small>성수석</div>
{subs}        <div id="badge">시장님 검토용 시안</div>
        <div id="ai-note">이 영상은 생성형 AI를 활용해 제작되었으며, 일부 장면과 음성은 AI로 연출되었습니다.</div>
        <div id="fade"></div>
'''
    open(os.path.join(d, "compositions", "news.html"), "w").write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{css}      </style>
      <div id="root" data-composition-id="news" data-width="1920" data-height="1080">
{body}      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{js}        window.__timelines["news"] = tl;
      </script>
    </template>
  </body>
</html>
''')
    open(os.path.join(d, "index.html"), "w").write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>서희함 · 시장님과 AI 서희 화상 연결</title>
    <script src="gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <div id="news" data-composition-id="news" data-composition-src="compositions/news.html"
        data-start="0" data-duration="{DUR}" data-track-index="0" data-width="1920" data-height="1080"></div>
      <audio id="soundtrack" src="assets/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')


if __name__ == "__main__":
    steps = os.environ.get("STEPS", "mayor,seohui,audio,project").split(",")
    if "mayor" in steps:
        build_mayor()
    if "seohui" in steps:
        build_seohui()
    if "audio" in steps:
        build_audio()
    if "project" in steps:
        write_project()
