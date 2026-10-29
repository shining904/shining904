# Dialogue preview: mayor (left) + AI Seohui (right) in the hanok scene, with a virtual camera.
# Step 1 (ffmpeg) builds the "stage": the Seohui track over the clean plate, with the mayor's
# cut-out (background removed) overlaid at a fixed spot. Step 2 writes a HyperFrames project that
# plays the stage inside a moving camera window, plus subtitles, name tags, the gold shimmer when
# Seohui appears, and the mixed soundtrack.
#
# The mayor footage stands in for the real shoot (his greeting video, background removed), so
# every mayor-derived file lives in WORK, outside the repo. Lines he has not filmed yet play his
# greeting picture muted and are tagged "촬영 예정 대사".
#
#   WORK=/path/to/scratch python3 seohuiham-mayor/build_preview.py
#   (then: cd $WORK/preview && npx hyperframes render -o ../dialogue-preview.mp4)
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS, ASSETS = os.path.join(HERE, "clips"), os.path.join(HERE, "assets")
WORK = os.environ["WORK"]
CUT = os.path.join(WORK, "bgtest")  # mayor alpha chunks: cut1..3.webm
SHORTS = os.path.join(HERE, "..", "hyperframes-seohuiham-shorts")
MAYOR_SRC = os.path.join(SHORTS, "shared/assets/mayor/src/greeting-orig.mp4")
DUR, FPS = 67.8, 25
SW, SH = 1920, 1088  # stage = Seohui clip frame

# Mayor cut-out placement on the stage (fits the Seohui eyeline; his frame edge stays below the
# lowest camera window).
MX, MY, MH = 345, 258, 545
# Greeting source time covered by each background-removed chunk.
CHUNKS = [(0.8, 17.0), (17.8, 17.0), (34.8, 8.5)]
LISTEN = (4.25, 1.4)  # still pause after "성수석입니다", ping-ponged while he listens

# Mayor picture track: (preview start, source start or "listen", duration, real audio?)
MAYOR = [
    (0.0, 0.8, 4.0, True),      # 1 안녕하십니까. 이천시장 성수석입니다.
    (4.0, 8.7, 4.6, True),      # 2 서희함의 진수를 … 축하드립니다.
    (8.6, 4.4, 4.6, False),     # 3 부득이한 일정으로 … (to be filmed)
    (13.2, 13.9, 8.7, True),    # 4 서희 선생님은 … 역사의 뿌리입니다.
    (21.9, 36.1, 2.6, False),   # 5 그래서 특별한 분을 … (to be filmed)
    (24.5, "listen", 10.7, False),
    (35.2, 13.9, 5.0, False),   # 7 그런데 서희 대사님 … (to be filmed)
    (40.2, "listen", 10.9, False),
    (51.1, 30.6, 5.3, True),    # 9 서희함을 위해 애써 주신 …
    (56.4, 22.95, 7.4, True),   # 10 (greeting stand-in) 이제 그 이름이 …
    (63.8, 8.76, 2.5, False),   # 11 together (Seohui's voice carries it)
    (66.3, 41.75, 1.5, False),
]

# Seohui track: (preview start, clip, clip start, duration, speed)
SEOHUI = [
    (23.0, "E-listen-front.mp4", 0.0, 1.8, 1.0),
    (24.8, "A-greet-dw.mp4", 0.0, 10.12, 1.0),
    (34.92, "D-listen-left.mp4", 6.6, 5.6, 1.0),
    (40.52, "B-reply-dw.mp4", 0.0, 10.24, 1.0),
    (50.76, "E-listen-front.mp4", 0.0, 12.2, 13.04 / 12.2),
    (63.8, "C-together-dw.mp4", 0.0, 2.52, 1.0),
    (66.32, "C-together.mp4", 2.52, 1.52, 1.0),
]
SEOHUI_VOICE = [(24.8, "dw6t.mp3"), (40.52, "dw8.mp3"), (63.8, "dw11t.mp3")]
APPEAR = 23.0  # Seohui fades in over the plate

# Subtitles: (start, end, text, to-be-filmed?)
SUBS = [
    (0.45, 3.75, "안녕하십니까. 이천시장 성수석입니다.", False),
    (4.05, 8.3, "서희함의 진수를 이천시민과 함께/진심으로 축하드립니다.", False),
    (8.65, 12.95, "부득이한 일정으로 진수식에 함께하지 못하게 되어,/영상으로 인사드립니다.", True),
    (13.25, 17.75, "서희 선생님은 나라를 지킨/고려의 외교가이자", False),
    (18.05, 21.65, "우리 이천의 정신과/역사의 뿌리입니다.", False),
    (21.95, 24.4, "그래서 특별한 분을 한 분 모셨습니다.", True),
    (24.85, 28.65, "안녕하세요,/이천시 AI 홍보대사 서희입니다!", False),
    (29.45, 31.9, "제 이름을 단 함정이 바다로 나간다니,", False),
    (32.3, 34.75, "천 년 만에 이렇게 설레기는 처음이에요.", False),
    (35.25, 40.15, "그런데 서희 대사님, 말씀으로 나라를 지키신 분인데,/서희함은 잠수함이라 아주 조용히 다니겠네요.", True),
    (40.6, 47.85, "괜찮습니다. 진짜 강한 사람은/말을 아낄 줄 알거든요.", False),
    (48.4, 50.8, "조용히, 그러나 든든하게!/대한민국 바다를 잘 지켜 줄 거예요.", False),
    (51.15, 56.1, "서희함을 위해 애써 주신 모든 분들과/해군 장병 여러분께 감사드리며,", False),
    (56.45, 63.4, "이제 그 이름이 바닷속에서 조용히,/그리고 든든하게 대한민국을 지키게 되었습니다.", False),
    (63.85, 66.3, "서희함, 진수를 축하합니다!", False),
]

# Camera windows on the stage: x, y, width (height = width * 9/16).
MED = (311, 195, 1067)
MCU = (430, 250, 830)
TWO = (500, 195, 1067)
SCU = (995, 250, 830)
# (time, window, move duration into it) — eased push-ins, pulls and pans, no cuts.
CAMERA = [
    (0.0, MED, 0),
    (0.0, (338, 205, 1000), 3.8),        # slow drift in on the opening line
    (4.0, MCU, 2.5),                     # into the mayor's close-up
    (6.5, (445, 255, 800), 15.1),        # breathe
    (21.9, TWO, 1.7),                    # pull back as Seohui appears
    (27.3, SCU, 1.6),                    # Seohui turns from the mayor to camera
    (28.9, (1010, 258, 800), 5.9),
    (34.8, TWO, 1.4),                    # back to the two-shot for the mayor's question
    (36.2, (520, 205, 1000), 4.0),
    (43.0, SCU, 1.6),                    # Seohui's answer, after his glance at the mayor
    (44.6, (1010, 258, 800), 6.2),
    (50.8, MCU, 1.0),                    # mayor's thanks
    (51.8, (445, 255, 800), 11.4),
    (63.2, TWO, 1.4),                    # together
    (64.6, (540, 215, 980), 3.2),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def chunk_pieces(src, dur):
    """split a greeting source range into (chunk index, offset, length) pieces"""
    out = []
    while dur > 1e-3:
        k = max(i for i, (s, _) in enumerate(CHUNKS) if s <= src + 0.05)
        s, n = CHUNKS[k]
        take = min(dur, s + n - src)
        if take < 0.04:  # ran past the last chunk
            raise ValueError(f"greeting source {src:.2f}s is outside the cut-out chunks")
        out.append((k, src - s, take))
        src, dur = src + take, dur - take
    return out


def build_listen():
    """forward/backward loop of the mayor's still pause (alpha webm)"""
    path = os.path.join(WORK, "mayor-listen.webm")
    k, off, _ = chunk_pieces(LISTEN[0], LISTEN[1])[0]
    run(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-ss", str(off), "-t", str(LISTEN[1]),
         "-i", os.path.join(CUT, f"cut{k + 1}.webm"), "-filter_complex",
         "[0]format=yuva420p,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1,loop=loop=6:size=300,fps=25",
         "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "8M", "-auto-alt-ref", "0", path])
    return path


def chain(segs, out, pix, codec):
    """join segments in order with short crossfades: segs = [(start, input args, filter, fade in)]
    Each segment is padded by its successor's fade so the successor starts exactly on time
    (keeps lip-sync). Sequential xfades keep memory flat, unlike timestamp-offset overlays."""
    ins, fil = [], []
    for i, (start, args, filt, _) in enumerate(segs):
        end = segs[i + 1][0] if i + 1 < len(segs) else DUR
        pad = segs[i + 1][3] if i + 1 < len(segs) else 0
        ins += args
        fil.append(f"[{i}]{filt},trim=duration={end - start:.3f},setpts=PTS-STARTPTS,"
                   f"tpad=stop_mode=clone:stop_duration={pad + 0.04}[v{i}]")
    last = "v0"
    for i in range(1, len(segs)):
        fil.append(f"[{last}][v{i}]xfade=transition=fade:duration={segs[i][3]}:offset={segs[i][0]:.3f}[x{i}]")
        last = f"x{i}"
    fil.append(f"[{last}]trim=0:{DUR},format={pix}[out]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[out]",
         "-r", str(FPS), *codec, out])


def build_stage():
    listen = build_listen()
    norm = f"fps={FPS},scale={SW}:{SH},format=yuv420p"
    plate = os.path.join(ASSETS, "plate3-hanok.png")
    segs = [(0.0, ["-loop", "1", "-framerate", str(FPS), "-t", str(APPEAR + 2), "-i", plate], norm, 0)]
    for start, clip, cs, d, speed in SEOHUI:
        fade = 1.2 if start == APPEAR else 0.2  # Seohui's first appearance fades in slowly
        segs.append((start, ["-ss", str(cs), "-t", str(d), "-i", os.path.join(CLIPS, clip)],
                     f"{norm},setpts={speed:.4f}*(PTS-STARTPTS)", fade))
    seohui = os.path.join(WORK, "track-seohui.mp4")
    if not os.path.exists(seohui) or os.environ.get("FRESH"):
        chain(segs, seohui, "yuv420p", ["-c:v", "libx264", "-crf", "12", "-preset", "fast"])

    grade = (f"fps={FPS},scale=-1:{MH},colorbalance=rs=.05:gs=.01:bs=-.06:rm=.03:bm=-.04,"
             "eq=brightness=-0.04:saturation=0.93,format=yuva420p")
    # Decode and grade each mayor piece to a small lossless file first: a single graph with ~16
    # alpha VP9 decoders runs out of memory.
    segs, pieces = [], os.path.join(WORK, "mayor-pieces")
    os.makedirs(pieces, exist_ok=True)

    def piece(t, args, fade):
        f = os.path.join(pieces, f"p{len(segs):02d}.mkv")
        run(["ffmpeg", "-v", "error", "-y", *args, "-vf", grade, "-c:v", "ffv1", f])
        segs.append((t, ["-i", f], "null", fade))

    for start, src, d, _ in MAYOR:
        if src == "listen":
            piece(start, ["-c:v", "libvpx-vp9", "-t", str(d + 0.5), "-i", listen], 0.2)
            continue
        t = start
        for j, (k, off, take) in enumerate(chunk_pieces(src, d)):
            piece(t, ["-c:v", "libvpx-vp9", "-ss", str(off), "-t", str(take + 0.5), "-i",
                      os.path.join(CUT, f"cut{k + 1}.webm")], 0.2 if j == 0 else 0.04)
            t += take
    mayor = os.path.join(WORK, "track-mayor.mkv")
    chain(segs, mayor, "yuva420p", ["-c:v", "ffv1"])

    out = os.path.join(WORK, "preview", "assets", "stage.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", seohui, "-i", mayor, "-filter_complex",
         f"[0][1]overlay={MX}:{MY},format=yuv420p[out]", "-map", "[out]", "-r", str(FPS),
         "-c:v", "libx264", "-crf", "14", "-preset", "medium", out])


def build_audio():
    ins, fil, mix = [], [], []
    for i, (start, src, d, real) in enumerate(MAYOR):
        if not real:
            continue
        n = len(ins) // 6
        ins += ["-ss", str(src), "-t", str(d), "-i", MAYOR_SRC]
        fil.append(f"[{n}:a]afade=t=in:d=0.08,afade=t=out:st={d - 0.12:.2f}:d=0.12,"
                   f"loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,adelay={int(start * 1000)}:all=1[m{n}]")
        mix.append(f"[m{n}]")
    for start, f in SEOHUI_VOICE:
        n = len(ins) // 6
        ins += ["-ss", "0", "-t", "30", "-i", os.path.join(ASSETS, f)]
        fil.append(f"[{n}:a]loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,"
                   f"adelay={int(start * 1000)}:all=1[s{n}]")
        mix.append(f"[s{n}]")
    n = len(ins) // 6
    ins += ["-ss", "0", "-t", "300", "-i", os.path.join(ASSETS, "idle-roomtone.mp3")]
    fil.append(f"[{n}:a]aloop=loop=-1:size=2e9,atrim=0:{DUR},volume=0.35,aresample=48000[rt]")
    mix.append("[rt]")
    n = len(ins) // 6
    ins += ["-ss", "4.9", "-t", "300", "-i", os.path.join(SHORTS, "shared/assets/music-gold3.mp3")]
    fil.append(f"[{n}:a]aloop=loop=-1:size=211680,atrim=0:{DUR},volume=0.09,"
               f"afade=t=in:d=1.5,afade=t=out:st={DUR - 2.5}:d=2.5,aresample=48000[bed]")
    mix.append("[bed]")
    fil.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,"
               f"atrim=0:{DUR},alimiter=limit=0.89[a]")
    out = os.path.join(WORK, "preview", "assets", "mix.mp3")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[a]",
         "-c:a", "libmp3lame", "-b:a", "192k", out])


def cam_js():
    js = ""
    for t, (x, y, w), d in CAMERA:
        s = 1920 / w
        props = f"x: {-x * s:.1f}, y: {-y * s:.1f}, scale: {s:.4f}"
        if d == 0:
            js += f'        tl.set("#stage", {{ {props} }}, {t});\n'
        else:
            ease = "sine.inOut" if d > 3 else "power2.inOut"
            js += f'        tl.to("#stage", {{ {props}, duration: {d}, ease: "{ease}" }}, {t});\n'
    return js


def write_project():
    d = os.path.join(WORK, "preview")
    os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
    for f in ("Pretendard-Bold.woff2", "Pretendard-Medium.woff2"):
        run(["cp", os.path.join(ASSETS, f), os.path.join(d, "fonts", f)])
    for name, target in (("gsap.min.js", os.path.join(SHORTS, "shared/gsap.min.js")),
                         ("node_modules", os.path.join(HERE, "..", "hyperframes-kra-film/node_modules"))):
        p = os.path.join(d, name)
        if not os.path.lexists(p):
            os.symlink(os.path.abspath(target), p)
    open(os.path.join(d, "package.json"), "w").write(
        '{\n  "name": "seohuiham-dialogue-preview",\n  "private": true,\n  "type": "module",\n'
        '  "devDependencies": {\n    "hyperframes": "0.8.82"\n  }\n}\n')
    open(os.path.join(d, "hyperframes.json"), "w").write(
        '{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n'
        '  "paths": { "blocks": "compositions", "assets": "assets" },\n  "media": { "autoProxy": true }\n}\n')

    subs, js = "", ""
    for i, (a, b, text, todo) in enumerate(SUBS):
        tag = '<span class="todo">시장님 촬영 예정 대사</span>' if todo else ""
        subs += f'        <div id="s{i}" class="sub">{tag}{text.replace("/", "<br />")}</div>\n'
        js += f'        tl.fromTo("#s{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});\n'
        js += f'        tl.to("#s{i}", {{ opacity: 0, duration: 0.2 }}, {b - 0.2:.2f});\n'
    # name tags, gold shimmer on Seohui's entrance, closing fade
    js += '        tl.fromTo("#tag-m", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.6);\n'
    js += '        tl.to("#tag-m", { opacity: 0, duration: 0.4 }, 4.6);\n'
    js += '        tl.fromTo("#tag-s", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 25.2);\n'
    js += '        tl.to("#tag-s", { opacity: 0, duration: 0.4 }, 30.0);\n'
    js += '        tl.fromTo("#glow", { opacity: 0, scale: 0.6 }, { opacity: 0.85, scale: 1.1, duration: 0.9, ease: "power2.out" }, 22.8);\n'
    js += '        tl.to("#glow", { opacity: 0, scale: 1.4, duration: 1.1, ease: "power1.in" }, 23.7);\n'
    js += '        tl.fromTo("#ai-note", { opacity: 0 }, { opacity: 1, duration: 0.6 }, 23.5);\n'
    js += f'        tl.to("#fade", {{ opacity: 1, duration: 0.8 }}, {DUR - 0.8});\n'

    css = f'''        @font-face {{ font-family: "Pretendard"; font-weight: 700; src: url("fonts/Pretendard-Bold.woff2") format("woff2"); }}
        @font-face {{ font-family: "Pretendard"; font-weight: 500; src: url("fonts/Pretendard-Medium.woff2") format("woff2"); }}
        #root {{ position: absolute; inset: 0; overflow: hidden; background: #000; font-family: "Pretendard"; }}
        #stage {{ position: absolute; left: 0; top: 0; width: {SW}px; height: {SH}px; transform-origin: 0 0; }}
        #stage video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
        #glow {{ position: absolute; left: 1110px; top: 160px; width: 600px; height: 900px; border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255,226,150,0.95), rgba(227,178,90,0.55) 45%, rgba(227,178,90,0) 100%);
          mix-blend-mode: screen; opacity: 0; }}
        .sub {{ position: absolute; left: 0; right: 0; bottom: 92px; text-align: center; color: #fff; font-weight: 700;
          font-size: 46px; line-height: 1.38; text-shadow: 0 2px 8px rgba(0,0,0,0.85), 0 0 24px rgba(0,0,0,0.5); opacity: 0; }}
        .todo {{ display: block; width: max-content; margin: 0 auto 10px; padding: 4px 14px; border-radius: 6px;
          font-size: 24px; font-weight: 500; color: #1a1a1a; background: rgba(227,178,90,0.92); text-shadow: none; }}
        .tag {{ position: absolute; top: 640px; padding: 14px 26px; color: #fff; font-weight: 700; font-size: 34px;
          background: rgba(10,10,10,0.55); border-left: 5px solid #e3b25a; opacity: 0; }}
        .tag small {{ display: block; font-size: 22px; font-weight: 500; color: #e3b25a; margin-bottom: 2px; }}
        #tag-m {{ left: 110px; }}
        #tag-s {{ right: 110px; border-left: 0; border-right: 5px solid #e3b25a; text-align: right; }}
        #badge {{ position: absolute; left: 36px; top: 30px; padding: 6px 14px; font-size: 22px; font-weight: 500;
          color: #fff; background: rgba(0,0,0,0.5); border-radius: 6px; }}
        #ai-note {{ position: absolute; left: 0; right: 0; bottom: 30px; text-align: center; font-size: 21px; font-weight: 500;
          color: rgba(255,255,255,0.8); text-shadow: 0 1px 4px rgba(0,0,0,0.9); opacity: 0; }}
        #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
'''
    body = f'''        <div id="stage">
          <video id="v-stage" src="assets/stage.mp4" data-start="0" data-duration="{DUR}" muted playsinline></video>
          <div id="glow"></div>
        </div>
        <div id="tag-m" class="tag"><small>이천시장</small>성수석</div>
        <div id="tag-s" class="tag"><small>이천시 AI 홍보대사</small>서희</div>
{subs}        <div id="badge">미리보기 · 시장님 화면은 인사말 영상으로 임시 합성</div>
        <div id="ai-note">이 영상은 생성형 AI로 제작되었으며, AI 서희 등 일부 장면은 실제 촬영이 아닌 가상 연출입니다.</div>
        <div id="fade"></div>
'''
    os.makedirs(os.path.join(d, "compositions"), exist_ok=True)
    open(os.path.join(d, "compositions", "dialogue.html"), "w").write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{css}      </style>
      <div id="root" data-composition-id="dialogue" data-width="1920" data-height="1080">
{body}      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{cam_js()}{js}        window.__timelines["dialogue"] = tl;
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
    <title>서희함 · 시장님과 AI 서희 대화 미리보기</title>
    <script src="gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <div id="dialogue" data-composition-id="dialogue" data-composition-src="compositions/dialogue.html"
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
    json.dump({"subs": SUBS}, open(os.path.join(d, "subs.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    steps = os.environ.get("STEPS", "stage,audio,project").split(",")
    if "stage" in steps:
        build_stage()
    if "audio" in steps:
        build_audio()
    if "project" in steps:
        write_project()
