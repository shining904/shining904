# Full dialogue video: the mayor (real greeting footage, cut out; lines he never said are his
# own footage lip-synced to his cloned voice, with his consent) and AI Seohui (Kling clips of
# scene4, his lines lip-synced to Dong Wook v4) in the symmetric hanok hall, with the virtual
# camera, subtitles, name tags and soundtrack.
#
# Everything derived from the mayor lives in WORK (outside the repo). Inputs expected there:
#   bgtest/cut1..3.webm           background-removed greeting chunks (see build_preview.py)
#   mayor-ai/ls-Lxx.mp4, m*.mp3   lip-synced mayor lines and their cloned-voice audio
#   seohui/Sx.mp4                 Seohui clips (silent Kling takes or lip-synced)
#
#   WORK=/path/to/scratch python3 seohuiham-mayor/build_dialogue.py
#   (then: cd $WORK/dialogue && npx hyperframes render -o ../dialogue.mp4)
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
WORK = os.environ["WORK"]
CUT, MAI, SEO = (os.path.join(WORK, d) for d in ("bgtest", "mayor-ai", "seohui"))
SHORTS = os.path.join(HERE, "..", "hyperframes-seohuiham-shorts")
GREETING = os.path.join(SHORTS, "shared/assets/mayor/src/greeting-orig.mp4")
FPS, SW, SH = 25, 1920, 1080

LAYOUT = json.load(open(os.path.join(HERE, "layout-scene4.json")))
MH, MX, MY = (LAYOUT["greeting_cutout"][k] for k in ("height", "x", "y"))
CHUNKS = [(0.8, 17.0), (17.8, 17.0), (34.8, 8.5)]
LISTEN = (4.25, 1.4)  # still pause after "성수석입니다", ping-ponged while he listens

# Mayor track: (start, kind, a, b, c)
#   real:   greeting source start a, duration b                     (his own words and voice)
#   synced: lip-synced file a, greeting source start b; c = None, or the length of the source
#           window when that footage was played backwards before lip-sync (cloned voice)
#   listen: duration a
MAYOR = [
    (0.0, "real", 0.8, 3.6, None),             # 1 안녕하십니까. 이천시장 성수석입니다.
    (3.6, "listen", 0.3, None, None),
    (3.9, "real", 8.6, 4.5, None),             # 2 서희함의 진수를 … 축하드립니다.
    (8.4, "synced", "ls-L03.mp4", 31.0, None),  # 3 부득이한 일정으로 …
    (13.6, "listen", 0.3, None, None),
    (13.9, "real", 13.8, 8.7, None),           # 4 서희 선생님은 … 역사의 뿌리입니다.
    (22.6, "listen", 0.2, None, None),
    (22.8, "synced", "ls-L05.mp4", 36.3, None),  # 5 그래서 특별한 분을 …
    (25.76, "listen", 10.54, None, None),      # 6 (Seohui greets)
    (36.3, "synced", "ls-L07.mp4", 22.9, None),  # 7 그런데 서희 대사님 …
    (44.3, "listen", 12.1, None, None),        # 8 (Seohui answers)
    (56.4, "synced", "ls-L09.mp4", 14.0, 8.4),   # 9 서희함을 위해 애써 주신 …
    (64.64, "listen", 0.26, None, None),
    (64.9, "synced", "ls-L10.mp4", 0.9, 7.5),    # 10 서희 선생님의 지혜와 용기처럼 …
    (72.3, "listen", 0.5, None, None),
    (72.8, "synced", "ls-L11.mp4", 5.5, None),   # 11 서희함, 진수를 축하합니다!
    (75.6, "listen", 1.6, None, None),
]
DUR = 77.2
MAYOR_VOICE = {"ls-L03.mp4": "m03.mp3", "ls-L05.mp4": "m05.mp3", "ls-L07.mp4": "m07b.mp3",
               "ls-L09.mp4": "m09.mp3", "ls-L10.mp4": "m10.mp3", "ls-L11.mp4": "m11.mp3"}

# Seohui track over the clean plate: (start, clip, clip start, duration, speed, reversed)
APPEAR = 24.8
SEOHUI = [
    (APPEAR, "S1.mp4", 0.0, 1.8, 1.0, False),
    (26.6, "S2-sync.mp4", 0.0, 9.7, 1.0, False),    # 6 greets the mayor, then the camera
    (36.3, "S3.mp4", 0.0, 8.3, 1.0, False),         # 7 turns to the mayor and listens
    (44.6, "S4-sync.mp4", 0.0, 11.8, 1.0, False),   # 8 answers him, then the camera
    (56.4, "S1.mp4", 1.8, 8.2, 1.0, False),         # 9-10 listens
    (64.6, "S1.mp4", 0.0, 8.2, 1.0, True),
    (72.8, "S5-sync.mp4", 0.0, 4.4, 1.0, False),    # 11 together
]
SEOHUI_VOICE = [(26.6, "dwv4_6.mp3"), (44.6, "dwv4_8t.mp3"), (72.8, "dwv4_11t.mp3")]

SUBS = [
    (0.1, 3.5, "안녕하십니까. 이천시장 성수석입니다."),
    (3.95, 8.3, "서희함의 진수를 이천시민과 함께/진심으로 축하드립니다."),
    (8.45, 13.5, "부득이한 일정으로 진수식에 함께하지 못하게 되어,/영상으로 인사드립니다."),
    (13.95, 18.4, "서희 선생님은 나라를 지킨/고려의 외교가이자"),
    (18.7, 22.5, "우리 이천의 정신과/역사의 뿌리입니다."),
    (22.85, 25.7, "그래서 특별한 분을 한 분 모셨습니다."),
    (26.65, 30.0, "안녕하세요,/이천시 AI 홍보대사 서희입니다!"),
    (30.4, 35.8, "제 이름을 단 함정이 바다로 나간다니,/천 년 만에 이렇게 설레기는 처음이에요."),
    (36.35, 44.2, "그런데 서희 대사님, 말씀으로 나라를 지키신 분인데,/서희함은 잠수함이라 아주 조용히 다니겠네요."),
    (44.65, 50.9, "괜찮습니다. 진짜 강한 사람은/말을 아낄 줄 알거든요."),
    (51.2, 55.9, "조용히, 그러나 든든하게!/대한민국 바다를 잘 지켜 줄 거예요."),
    (56.45, 64.5, "서희함을 위해 애써 주신 모든 분들과, 앞으로 서희함과/함께할 해군 장병 여러분께 깊이 감사드립니다."),
    (64.95, 72.2, "서희 선생님의 지혜와 용기처럼, 서희함이/대한민국의 바다를 든든하게 지켜 주기를 바랍니다."),
    (72.85, 75.6, "서희함, 진수를 축하합니다!"),
]

# Camera windows on the 1920x1080 stage: x, y, width (height = width * 9/16)
MED = (197, 200, 1067)
MCU = (315, 244, 830)
TWO = (427, 200, 1067)
SCU = (775, 244, 830)
CAMERA = [
    (0.0, MED, 0),
    (0.0, (232, 215, 1000), 3.6),
    (3.9, MCU, 2.4),
    (6.3, (330, 252, 800), 16.3),
    (22.8, TWO, 2.0),                     # pull back as Seohui appears
    (28.8, SCU, 1.6),                     # after greeting the mayor he turns to camera
    (30.4, (790, 252, 800), 5.4),
    (35.9, TWO, 1.3),                     # mayor's question; Seohui turns to him
    (37.2, (447, 210, 1010), 7.1),
    (47.6, SCU, 1.6),                     # Seohui's answer turns to camera
    (49.2, (790, 252, 800), 6.8),
    (56.0, MCU, 1.0),                     # mayor's thanks
    (57.0, (330, 252, 800), 15.0),
    (72.0, TWO, 1.4),                     # together
    (73.4, (447, 210, 1000), DUR - 73.4),
]

GRADE = (f"scale=-1:{MH}:flags=lanczos,format=yuva420p,split=2[m0][m1];"
         "[m1]alphaextract,split=3[a1][a2][a3];[a2]erosion,erosion,erosion[ae];"
         "[a1][ae]blend=all_mode=difference,gblur=sigma=3,"
         "geq=lum='lum(X,Y)*0.55*clip(1.5-Y/H*1.7\\,0\\,1)'[edge];"
         "[m0]colortemperature=temperature=4900:mix=0.65,eq=contrast=1.1:brightness=-0.02:saturation=0.9,"
         "gblur=sigma=0.6,noise=alls=4:allf=t,format=rgb24[mg];"
         "color=c=0xfff0d8:s=16x16,format=rgb24[w0];[w0][mg]scale2ref[w][mg2];[w][edge]alphamerge[rim];"
         "[mg2][rim]overlay=0:0,format=rgba[mr];[mr][a3]alphamerge,format=yuva420p")


def run(cmd):
    subprocess.run(cmd, check=True)


def chunk_inputs(src, dur):
    """greeting source range -> ffmpeg inputs for the cut-out chunks that cover it"""
    args, n = [], 0
    while dur > 0.02:
        k = max(i for i, (s, _) in enumerate(CHUNKS) if s <= src + 0.05)
        s, length = CHUNKS[k]
        take = min(dur, s + length - src)
        if take < 0.04:
            raise ValueError(f"greeting source {src:.2f}s is outside the cut-out chunks")
        args += ["-c:v", "libvpx-vp9", "-ss", f"{src - s:.3f}", "-t", f"{take:.3f}",
                 "-i", os.path.join(CUT, f"cut{k + 1}.webm")]
        src, dur, n = src + take, dur - take, n + 1
    return args, n


def mayor_piece(i, kind, a, b, c, dur):
    """one graded mayor cut-out piece as a small lossless file"""
    out = os.path.join(WORK, "dialogue-pieces", f"m{i:02d}.mkv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    frames = round(dur * FPS)
    if kind == "listen":
        args, n = chunk_inputs(*LISTEN)
        fil = ("[0]format=yuva420p,fps=25,split[f][r0];[r0]reverse[r];[f][r]concat=n=2:v=1,"
               f"loop=loop=-1:size=300,trim=end_frame={frames},setpts=PTS-STARTPTS,{GRADE}[out]")
    else:
        src, rev = (a, False) if kind == "real" else (b, c)
        if kind == "real":
            args, n = chunk_inputs(src, dur + 0.2)
            body = "".join(f"[{j}]format=yuva420p,fps=25,setpts=PTS-STARTPTS[c{j}];" for j in range(n))
            fil = (body + "".join(f"[c{j}]" for j in range(n)) + f"concat=n={n}:v=1,trim=end_frame={frames},"
                   f"setpts=PTS-STARTPTS,{GRADE}[out]")
        else:
            args, n = chunk_inputs(src, rev if rev else dur + 0.4)
            args += ["-i", os.path.join(MAI, a)]
            body = "".join(f"[{j}]format=yuva420p,fps=25,setpts=PTS-STARTPTS[c{j}];" for j in range(n))
            alpha = "".join(f"[c{j}]" for j in range(n)) + f"concat=n={n}:v=1,alphaextract"
            if rev:  # that footage was played backwards before lip-sync; so is its matte
                alpha += f",trim=end_frame={round(rev * FPS)},reverse"
            fil = (body + alpha + f",trim=end_frame={frames},setpts=PTS-STARTPTS[al];"
                   f"[{n}:v]fps=25,trim=end_frame={frames},setpts=PTS-STARTPTS,format=rgb24[lv];"
                   f"[lv][al]alphamerge,{GRADE}[out]")
    # -frames:v bounds the output: the rim light's colour source never ends on its own
    run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", fil, "-map", "[out]",
         "-frames:v", str(frames), "-c:v", "ffv1", out])
    return out


def chain(segs, out, pix, codec, total):
    """join segments in order with short crossfades; each starts exactly on its time"""
    ins, fil = [], []
    for i, (start, args, filt, _) in enumerate(segs):
        end = segs[i + 1][0] if i + 1 < len(segs) else total
        pad = segs[i + 1][3] if i + 1 < len(segs) else 0
        ins += args
        fil.append(f"[{i}]{filt},trim=duration={end - start:.3f},setpts=PTS-STARTPTS,"
                   f"tpad=stop_mode=clone:stop_duration={pad + 0.08}[v{i}]")
    last = "v0"
    for i in range(1, len(segs)):
        fil.append(f"[{last}][v{i}]xfade=transition=fade:duration={segs[i][3]}:offset={segs[i][0]:.3f}[x{i}]")
        last = f"x{i}"
    fil.append(f"[{last}]trim=0:{total},format={pix}[out]")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fil), "-map", "[out]",
         "-r", str(FPS), *codec, out])


def build_stage():
    mayor = os.path.join(WORK, "dialogue-mayor.mkv")
    if not os.path.exists(mayor) or os.environ.get("FRESH"):
        segs = []
        for i, (start, kind, a, b, c) in enumerate(MAYOR):
            end = MAYOR[i + 1][0] if i + 1 < len(MAYOR) else DUR
            f = mayor_piece(i, kind, a, b, c, end - start + 0.4)
            segs.append((start, ["-i", f], "null", 0.12 if kind != "listen" else 0.2))
        chain(segs, mayor, "yuva420p", ["-c:v", "ffv1"], DUR)

    norm = f"fps={FPS},scale={SW}:{SH},format=yuv420p"
    plate = os.path.join(ASSETS, "plate4-hanok.png")
    segs = [(0.0, ["-loop", "1", "-framerate", str(FPS), "-t", str(APPEAR + 2), "-i", plate], norm, 0)]
    for start, clip, cs, d, speed, rev in SEOHUI:
        f = f"{norm},setpts={speed:.4f}*(PTS-STARTPTS)" + (",reverse" if rev else "")
        segs.append((start, ["-ss", str(cs), "-t", str(d), "-i", os.path.join(SEO, clip)], f,
                     1.2 if start == APPEAR else 0.25))
    seohui = os.path.join(WORK, "dialogue-seohui.mp4")
    chain(segs, seohui, "yuv420p", ["-c:v", "libx264", "-crf", "12", "-preset", "fast"], DUR)

    out = os.path.join(WORK, "dialogue", "assets", "stage.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", seohui, "-i", mayor, "-filter_complex",
         f"[0][1]overlay={MX}:{MY},format=yuv420p[out]", "-map", "[out]", "-r", str(FPS),
         "-c:v", "libx264", "-crf", "14", "-preset", "medium", out])


def build_audio():
    ins, fil, mix = [], [], []

    def add(args, chain_, label):
        n = sum(1 for a in ins if a == "-i")
        ins.extend(args)
        fil.append(f"[{n}:a]{chain_}[{label}]")
        mix.append(f"[{label}]")

    for i, (start, kind, a, b, c) in enumerate(MAYOR):
        if kind == "real":
            add(["-ss", str(a), "-t", str(b), "-i", GREETING],
                f"afade=t=in:d=0.06,afade=t=out:st={b - 0.1:.2f}:d=0.1,loudnorm=I=-16:TP=-2:LRA=7,"
                f"aresample=48000,adelay={int(start * 1000)}:all=1", f"m{i}")
        elif kind == "synced":
            add(["-i", os.path.join(MAI, MAYOR_VOICE[a])],
                f"loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,adelay={int(start * 1000)}:all=1", f"m{i}")
    for j, (start, f) in enumerate(SEOHUI_VOICE):
        add(["-i", os.path.join(ASSETS, f)],
            f"loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,adelay={int(start * 1000)}:all=1", f"s{j}")
    # the office's own air under the mayor's cloned lines, so his pauses never drop to digital silence
    add(["-ss", "4.3", "-t", "1.3", "-i", GREETING],
        f"aloop=loop=-1:size=57330,atrim=0:{DUR},volume=0.9,aresample=48000", "air")
    add(["-ss", "4.9", "-t", "300", "-i", os.path.join(SHORTS, "shared/assets/music-gold3.mp3")],
        f"aloop=loop=-1:size=211680,atrim=0:{DUR},volume=0.1,afade=t=in:d=1.5,"
        f"afade=t=out:st={DUR - 3:.1f}:d=3,aresample=48000", "bed")
    fil.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,"
               f"atrim=0:{DUR},alimiter=limit=0.89[a]")
    out = os.path.join(WORK, "dialogue", "assets", "mix.mp3")
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
            js += f'        tl.to("#stage", {{ {props}, duration: {d:.2f}, ease: "{ease}" }}, {t});\n'
    return js


def write_project():
    d = os.path.join(WORK, "dialogue")
    os.makedirs(os.path.join(d, "fonts"), exist_ok=True)
    os.makedirs(os.path.join(d, "compositions"), exist_ok=True)
    for f in ("Pretendard-Bold.woff2", "Pretendard-Medium.woff2"):
        run(["cp", os.path.join(ASSETS, f), os.path.join(d, "fonts", f)])
    for name, target in (("gsap.min.js", os.path.join(SHORTS, "shared/gsap.min.js")),
                         ("node_modules", os.path.join(HERE, "..", "hyperframes-kra-film/node_modules"))):
        p = os.path.join(d, name)
        if not os.path.lexists(p):
            os.symlink(os.path.abspath(target), p)
    open(os.path.join(d, "package.json"), "w").write(
        '{\n  "name": "seohuiham-dialogue",\n  "private": true,\n  "type": "module",\n'
        '  "devDependencies": {\n    "hyperframes": "0.8.82"\n  }\n}\n')
    open(os.path.join(d, "hyperframes.json"), "w").write(
        '{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n'
        '  "paths": { "blocks": "compositions", "assets": "assets" },\n  "media": { "autoProxy": true }\n}\n')

    x, y, w = CAMERA[0][1]
    s = 1920 / w
    first = f"translate({-x * s:.1f}px, {-y * s:.1f}px) scale({s:.4f})"
    subs, js = "", ""
    for i, (a, b, text) in enumerate(SUBS):
        subs += f'        <div id="s{i}" class="sub">{text.replace("/", "<br />")}</div>\n'
        js += f'        tl.fromTo("#s{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {a});\n'
        js += f'        tl.to("#s{i}", {{ opacity: 0, duration: 0.2 }}, {b - 0.2:.2f});\n'
    js += '        tl.fromTo("#tag-m", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 0.5);\n'
    js += '        tl.to("#tag-m", { opacity: 0, duration: 0.4 }, 4.4);\n'
    js += '        tl.fromTo("#tag-s", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }, 27.0);\n'
    js += '        tl.to("#tag-s", { opacity: 0, duration: 0.4 }, 31.4);\n'
    js += f'        tl.fromTo("#glow", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 0.85, scale: 1.1, duration: 0.9, ease: "power2.out" }}, {APPEAR - 0.2});\n'
    js += f'        tl.to("#glow", {{ opacity: 0, scale: 1.4, duration: 1.1, ease: "power1.in" }}, {APPEAR + 0.7});\n'
    js += f'        tl.to("#fade", {{ opacity: 1, duration: 0.8 }}, {DUR - 0.8});\n'
    css = f'''        @font-face {{ font-family: "Pretendard"; font-weight: 700; src: url("fonts/Pretendard-Bold.woff2") format("woff2"); }}
        @font-face {{ font-family: "Pretendard"; font-weight: 500; src: url("fonts/Pretendard-Medium.woff2") format("woff2"); }}
        #root {{ position: absolute; inset: 0; overflow: hidden; background: #000; font-family: "Pretendard"; }}
        #stage {{ position: absolute; left: 0; top: 0; width: {SW}px; height: {SH}px; transform-origin: 0 0; transform: {first}; }}
        #stage video {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
        #glow {{ position: absolute; left: 950px; top: 180px; width: 480px; height: 760px; border-radius: 50%;
          background: radial-gradient(closest-side, rgba(255,226,150,0.95), rgba(227,178,90,0.55) 45%, rgba(227,178,90,0) 100%);
          mix-blend-mode: screen; opacity: 0; }}
        .sub {{ position: absolute; left: 0; right: 0; bottom: 92px; text-align: center; color: #fff; font-weight: 700;
          font-size: 46px; line-height: 1.38; text-shadow: 0 2px 8px rgba(0,0,0,0.85), 0 0 24px rgba(0,0,0,0.5); opacity: 0; }}
        .tag {{ position: absolute; top: 120px; padding: 14px 26px; color: #fff; font-weight: 700; font-size: 34px;
          background: rgba(10,10,10,0.55); border-left: 5px solid #e3b25a; opacity: 0; }}
        .tag small {{ display: block; font-size: 22px; font-weight: 500; color: #e3b25a; margin-bottom: 2px; }}
        #tag-m {{ left: 110px; }}
        #tag-s {{ right: 110px; border-left: 0; border-right: 5px solid #e3b25a; text-align: right; }}
        #badge {{ position: absolute; left: 36px; top: 30px; padding: 6px 14px; font-size: 22px; font-weight: 500;
          color: #fff; background: rgba(0,0,0,0.5); border-radius: 6px; }}
        #ai-note {{ position: absolute; left: 0; right: 0; bottom: 30px; text-align: center; font-size: 21px; font-weight: 500;
          color: rgba(255,255,255,0.8); text-shadow: 0 1px 4px rgba(0,0,0,0.9); }}
        #fade {{ position: absolute; inset: 0; background: #000; opacity: 0; }}
'''
    body = f'''        <div id="stage">
          <video id="v-stage" src="assets/stage.mp4" data-start="0" data-duration="{DUR}" muted playsinline></video>
          <div id="glow"></div>
        </div>
        <div id="tag-m" class="tag"><small>이천시장</small>성수석</div>
        <div id="tag-s" class="tag"><small>이천시 AI 홍보대사</small>서희</div>
{subs}        <div id="badge">시장님 검토용 시안</div>
        <div id="ai-note">이 영상은 생성형 AI를 활용해 제작되었으며, 일부 장면과 음성은 AI로 연출되었습니다.</div>
        <div id="fade"></div>
'''
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
    <title>서희함 · 시장님과 AI 서희 대화</title>
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


if __name__ == "__main__":
    steps = os.environ.get("STEPS", "stage,audio,project").split(",")
    if "stage" in steps:
        build_stage()
    if "audio" in steps:
        build_audio()
    if "project" in steps:
        write_project()
