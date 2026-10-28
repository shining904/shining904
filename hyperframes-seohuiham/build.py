# 서희함 진수 축하 영상 — 웅장한 버전 「천 년의 지혜, 바다를 지키다」 (1920x1080, 73 s).
# Focus on the two heroes: Seo Hui and the submarine. Cut to the Lyria trailer score (epic.mp3):
#   0-7    open      Canvas 2D   darkness, sonar rings, narration 1
#   7-15   cliff     Seedance    Seo Hui on the dawn cliff, crane shot, name card
#   15-23  front     Seedance    the submarine emerges head-on from the deep, narration 3
#   23-31  side      Seedance    the submarine glides under the sunlit surface
#   31-47  title     Canvas+Blender  deep sea, Meshy/Blender submarine, Seo Hui double exposure,
#                                   "서희함" title slam on the score's big hit (36 s)
#   46-62  speech    Seedance+lipsync  Seo Hui's congratulation
#   61-73  finale    Seedance    the submarine surfaces at sunrise, closing card
# The earlier, history-led cut lives in build_v1.py. Run: python3 build.py
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, DUR = 1920, 1080, 73
GOLD = "#e3b25a"
FONTS = {
    "myeongjo": [("Nanum Myeongjo", 800, "nanum-myeongjo-latin-800-normal", "U+0000-00FF"),
                 ("Nanum Myeongjo", 800, "nanum-myeongjo-korean-800-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF, U+4E00-9FFF")],
    "noto": [("Noto Sans KR", w, f"noto-sans-kr-{s}-{w}-normal", r) for w in (500, 800)
             for s, r in (("latin", "U+0000-00FF, U+2160-216F"), ("korean", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"))],
}


def faces(*names):
    return "".join(f'''        @font-face {{
          font-family: "{f}";
          font-weight: {w};
          src: url("fonts/{n}.woff2") format("woff2");
          unicode-range: {r};
        }}
''' for k in names for f, w, n, r in FONTS[k])


def comp(cid, fonts, css, body, js):
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{faces(*fonts)}        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
        }}
{css}      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{js}        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
'''


def pop(sel, a, y=30, dur=0.9, ease="power3.out"):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "{ease}" }}, {a});\n'


def out(sel, a, dur=0.6):
    return f'        tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {a});\n'


def reveal(sel, a, dur=1.2):
    """letters fade up out of a blur, like a film title"""
    return (f'        tl.fromTo("{sel}", {{ opacity: 0, scale: 1.12, filter: "blur(14px)" }}, '
            f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: {dur}, ease: "power2.out" }}, {a});\n')


TITLE_CSS = f'''        .ttl {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          color: #f7efe0;
          text-shadow: 0 6px 40px rgba(0, 0, 0, 0.7);
        }}
        .gold {{
          background: linear-gradient(180deg, #fff3cf 0%, {GOLD} 45%, #9a6a1c 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          text-shadow: none;
          filter: drop-shadow(0 4px 24px rgba(0, 0, 0, 0.6));
        }}
'''


def clip(cid, src, dur, extra_css="", extra_body="", extra_js="", fade_in=0.8, push=(1.0, 1.06), grade=""):
    return comp(cid, ["myeongjo", "noto"], f'''        #{cid}-fade {{
          position: absolute;
          inset: 0;
          background: #000;
        }}
        #{cid}-video {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          {grade}
        }}
        #{cid}-bars {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.55) 0%, rgba(0, 0, 0, 0) 18%, rgba(0, 0, 0, 0) 78%, rgba(0, 0, 0, 0.6) 100%);
        }}
{TITLE_CSS}{extra_css}''', f'''        <div id="{cid}-fade">
          <video id="{cid}-video" src="{src}" data-start="0" data-duration="{dur}" muted playsinline></video>
          <div id="{cid}-bars"></div>
{extra_body}        </div>
''', f'''        tl.fromTo("#{cid}-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_in}, ease: "none" }}, 0);
        tl.fromTo("#{cid}-video", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {dur}, ease: "none" }}, 0);
{extra_js}''')


SCENES = [("open", 0, 7.6, 0), ("cliff", 7.0, 8.4, 1), ("front", 15.0, 8.4, 2), ("side", 23.0, 8.4, 3),
          ("title", 31.0, 15.9, 4), ("speech", 46.4, 15.3, 5), ("finale", 61.4, 11.6, 6)]
LINES = [("e1.mp3", 1.6, 4.68, "천 년 전, 칼 대신 지혜로 나라를 지킨 사람이 있었습니다."),
         ("e2.mp3", 9.6, 2.1, "고려의 외교관, 서희."),
         ("e3.mp3", 17.2, 2.86, "이제 그 이름이, 바다를 지킵니다."),
         ("s1.mp3", 46.5, 14.7, None)]
SPEECH = [(0.0, 1.23, "서희함 장병 여러분."), (1.83, 5.59, "천 년 전 저는 칼 대신 지혜로 이 땅을 지켰습니다."),
          (6.15, 9.9, "이제 제 이름이 바다 깊은 곳에서 나라를 지킵니다."),
          (10.72, 14.7, "이천시민들과 함께, 서희함의 안전한 항해를 응원합니다.")]
files = {}

# ---------------------------------------------------------------- open: sonar in the dark (Canvas 2D)
files["open"] = comp("open", [], '''        #open-cv {
          position: absolute;
          inset: 0;
        }
''', '        <canvas id="open-cv" width="1920" height="1080"></canvas>\n', '''        const cv = document.getElementById("open-cv"), ctx = cv.getContext("2d");
        const rnd = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
        function render(t) {
          ctx.fillStyle = "#01060c";
          ctx.fillRect(0, 0, 1920, 1080);
          // a faint deep-blue glow breathing in the centre
          const up = Math.min(1, t / 2.5);
          const g = ctx.createRadialGradient(960, 560, 0, 960, 560, 900);
          g.addColorStop(0, `rgba(10,50,90,${0.55 * up})`);
          g.addColorStop(1, "rgba(1,6,12,0)");
          ctx.fillStyle = g;
          ctx.fillRect(0, 0, 1920, 1080);
          // sonar pings: rings expanding every 2.2 s
          for (let k = 0; k < 4; k++) {
            const age = t - 0.4 - k * 2.2;
            if (age < 0 || age > 3.2) continue;
            const r = 40 + age * 420, a = Math.max(0, 1 - age / 3.2);
            ctx.strokeStyle = `rgba(120,210,255,${0.55 * a})`;
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.arc(960, 560, r, 0, Math.PI * 2);
            ctx.stroke();
          }
          // drifting particles
          for (let i = 0; i < 160; i++) {
            const x = (rnd(i, 1) * 1920 + t * (6 + rnd(i, 2) * 12)) % 1920;
            const y = (rnd(i, 3) * 1080 - t * (4 + rnd(i, 4) * 8) + 1080) % 1080;
            ctx.fillStyle = `rgba(170,215,255,${(0.1 + rnd(i, 5) * 0.3) * up})`;
            ctx.beginPath();
            ctx.arc(x, y, 0.8 + rnd(i, 6) * 1.8, 0, Math.PI * 2);
            ctx.fill();
          }
          // fade to white-gold at the very end (dawn cut)
          const w = Math.max(0, (t - 6.9) / 0.7);
          if (w > 0) {
            ctx.fillStyle = `rgba(255,236,200,${w})`;
            ctx.fillRect(0, 0, 1920, 1080);
          }
        }
        const state = { t: 0 };
        tl.to(state, { t: 7.6, duration: 7.6, ease: "none", onUpdate: () => render(state.t) }, 0);
''')

# ---------------------------------------------------------------- cliff (Seo Hui)
files["cliff"] = clip("cliff", "assets/clips/cliff.mp4", 8.4, '''        #cliff-name {
          left: 140px;
          right: auto;
          top: 700px;
          text-align: left;
          font-size: 120px;
        }
        #cliff-sub {
          left: 146px;
          right: auto;
          top: 850px;
          text-align: left;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 30px;
          letter-spacing: 10px;
        }
''', '''          <div id="cliff-name" class="ttl gold">서희 徐熙</div>
          <div id="cliff-sub" class="ttl">고려의 외교관 · 942–998</div>
''', reveal("#cliff-name", 2.8, 1.6) + pop("#cliff-sub", 3.6, 14) + out("#cliff-name, #cliff-sub", 7.2, 0.8),
    fade_in=0.9, push=(1.04, 1.0))

# ---------------------------------------------------------------- submarine clips
files["front"] = clip("front", "assets/clips/sub-front.mp4", 8.4, fade_in=1.0, push=(1.0, 1.08))
files["side"] = clip("side", "assets/clips/sub-side.mp4", 8.4, fade_in=0.6, push=(1.0, 1.05))

# ---------------------------------------------------------------- title: the name slams in on the big hit
files["title"] = comp("title", ["myeongjo", "noto"], TITLE_CSS + f'''        #title-cv {{
          position: absolute;
          inset: 0;
        }}
        #title-ghost {{
          position: absolute;
          left: -80px;
          top: -40px;
          width: 1100px;
          height: 1160px;
          object-fit: cover;
          object-position: 50% 30%;
          mix-blend-mode: screen;
          -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 42%, #000 40%, transparent 85%);
          mask-image: radial-gradient(ellipse 50% 50% at 50% 42%, #000 40%, transparent 85%);
          filter: grayscale(0.4) sepia(0.4) hue-rotate(170deg) brightness(0.9);
        }}
        #title-sub {{
          position: absolute;
          left: 0;
          top: 330px;
          width: 1920px;
          height: 1080px;
        }}
        #title-subv {{
          width: 100%;
          height: 100%;
        }}
        #title-flash {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 45%, rgba(255, 240, 200, 0.95) 0%, rgba(255, 240, 200, 0) 60%);
          mix-blend-mode: screen;
          opacity: 0;
        }}
        #title-name {{
          top: 200px;
          font-size: 230px;
          letter-spacing: 30px;
        }}
        #title-en {{
          top: 470px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 34px;
          letter-spacing: 26px;
          color: #bfe3ff;
        }}
        #title-facts {{
          top: 540px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 32px;
          color: #e7f2ff;
        }}
        #title-facts b {{
          color: {GOLD};
          font-weight: 800;
        }}
        #title-motto {{
          top: 640px;
          font-size: 60px;
        }}
''', '''        <canvas id="title-cv" width="1920" height="1080"></canvas>
        <img id="title-ghost" src="assets/img/portrait.png" alt="" />
        <div id="title-sub"><video id="title-subv" src="assets/3d/sub.webm" data-start="0" data-duration="15.9" muted playsinline></video></div>
        <div id="title-flash"></div>
        <div id="title-name" class="ttl gold">서희함</div>
        <div id="title-en" class="ttl">ROKS SEO HUI</div>
        <div id="title-facts" class="ttl"><b>장보고-Ⅲ 배치-Ⅱ</b> 2번함 · <b>3,600톤급</b> 잠수함 · <b>2026. 11. 3.</b> 진수</div>
        <div id="title-motto" class="ttl">천 년의 지혜, 바다를 지키다</div>
''', '''        const cv = document.getElementById("title-cv"), ctx = cv.getContext("2d");
        const rnd = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
        function render(t) {
          const g = ctx.createLinearGradient(0, 0, 0, 1080);
          g.addColorStop(0, "#0c3f6e");
          g.addColorStop(0.55, "#04203d");
          g.addColorStop(1, "#010a16");
          ctx.fillStyle = g;
          ctx.fillRect(0, 0, 1920, 1080);
          ctx.globalCompositeOperation = "lighter";
          for (let i = 0; i < 8; i++) {
            const x = 120 + i * 240 + Math.sin(t * 0.35 + i) * 50, w = 60 + rnd(i, 1) * 110;
            const s = ctx.createLinearGradient(0, 0, 0, 1080);
            s.addColorStop(0, "rgba(120,200,255,0.14)");
            s.addColorStop(1, "rgba(120,200,255,0)");
            ctx.fillStyle = s;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x + w, 0);
            ctx.lineTo(x + w * 2.4 - 260, 1080);
            ctx.lineTo(x - 260, 1080);
            ctx.fill();
          }
          ctx.globalCompositeOperation = "source-over";
          for (let i = 0; i < 200; i++) {
            const x = (rnd(i, 4) * 1920 + t * (10 + rnd(i, 5) * 22)) % 1920;
            const y = (rnd(i, 6) * 1080 + t * (6 + rnd(i, 7) * 12)) % 1080;
            ctx.fillStyle = `rgba(200,230,255,${0.12 + rnd(i, 8) * 0.3})`;
            ctx.beginPath();
            ctx.arc(x, y, 1 + rnd(i, 9) * 2, 0, Math.PI * 2);
            ctx.fill();
          }
        }
        const state = { t: 0 };
        tl.to(state, { t: 15.9, duration: 15.9, ease: "none", onUpdate: () => render(state.t) }, 0);
        tl.fromTo("#title-cv", { opacity: 0 }, { opacity: 1, duration: 0.8, ease: "none" }, 0);
        // Seo Hui's face appears over the sea like a memory, the submarine passes beneath
        tl.fromTo("#title-ghost", { opacity: 0, scale: 1.08 }, { opacity: 0.42, scale: 1.0, duration: 3.0, ease: "power2.out" }, 0.6);
        tl.to("#title-ghost", { opacity: 0.18, duration: 1.0, ease: "none" }, 5.2);
        tl.fromTo("#title-sub", { opacity: 0, x: 260 }, { opacity: 1, x: 0, duration: 2.2, ease: "power2.out" }, 0.4);
        tl.to("#title-sub", { x: -80, duration: 13, ease: "none" }, 2.6);
        // the hit (score at ~36.3 s = 5.3 s into this scene)
        tl.fromTo("#title-flash", { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, 5.25);
        tl.to("#title-flash", { opacity: 0, duration: 1.2, ease: "power2.out" }, 5.33);
        tl.fromTo("#title-name", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power4.out" }, 5.25);
''' + pop("#title-en", 6.0, 10) + pop("#title-facts", 6.8, 10) + reveal("#title-motto", 8.6, 1.4)
    + out("#title-name, #title-en, #title-facts, #title-motto, #title-sub, #title-ghost", 14.6, 1.0))

# ---------------------------------------------------------------- speech (lipsynced)
files["speech"] = clip("speech", "assets/clips/speech-lip.mp4", 15.3, fade_in=1.0, push=(1.0, 1.04))

# ---------------------------------------------------------------- finale
files["finale"] = clip("finale", "assets/clips/sub-surface.mp4", 11.6, '''        #fin-1 {
          top: 210px;
          font-size: 96px;
        }
        #fin-2 {
          top: 340px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 36px;
          letter-spacing: 4px;
        }
        #fin-from {
          top: 780px;
          font-size: 52px;
        }
        #fin-logo {
          position: absolute;
          left: 50%;
          top: 870px;
          margin-left: -110px;
          width: 220px;
          padding: 10px 18px;
          border-radius: 16px;
          background: #ffffff;
        }
        #fin-logo img {
          display: block;
          width: 100%;
        }
        #fin-ai {
          position: absolute;
          right: 26px;
          bottom: 16px;
          font-family: "Noto Sans KR", sans-serif;
          font-size: 18px;
          color: rgba(255, 255, 255, 0.6);
        }
        #fin-shade {
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          height: 520px;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.45) 60%, rgba(0, 0, 0, 0) 100%);
        }
        #fin-shade2 {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          height: 420px;
          background: linear-gradient(0deg, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0) 100%);
        }
        #fin-black {
          position: absolute;
          inset: 0;
          background: #000;
          opacity: 0;
        }
''', '''          <div id="fin-shade"></div>
          <div id="fin-shade2"></div>
          <div id="fin-1" class="ttl"><span class="gold">서희함</span>의 진수를 진심으로 축하합니다</div>
          <div id="fin-2" class="ttl">천 년의 지혜와 함께, 안전한 항해를 기원합니다</div>
          <div id="fin-from" class="ttl">이천시민 일동</div>
          <div id="fin-logo"><img src="assets/img/icheon-logo.png" alt="이천시" /></div>
          <div id="fin-ai">본 영상은 AI로 제작되었으며 일부 장면은 연출입니다</div>
          <div id="fin-black"></div>
''', '        tl.fromTo("#fin-shade, #fin-shade2", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "none" }, 1.0);\n' + reveal("#fin-1", 1.4, 1.6) + pop("#fin-2", 2.8, 14) + pop("#fin-from", 4.6, 14) + pop("#fin-logo", 5.2, 14)
    + pop("#fin-ai", 5.2, 0) + '        tl.to("#fin-black", { opacity: 1, duration: 1.4, ease: "none" }, 10.2);\n',
    fade_in=1.0, push=(1.0, 1.06))

# ---------------------------------------------------------------- captions
caps = [(s, s + d, c) for _, s, d, c in LINES if c] + [(46.5 + a, 46.5 + b, c) for a, b, c in SPEECH]
files["caps"] = comp("caps", ["noto"], '''        .caps-line {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 40px;
          text-align: center;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 38px;
          color: #ffffff;
          opacity: 0;
        }
        .caps-line span {
          display: inline-block;
          padding: 8px 26px;
          border-radius: 12px;
          background: rgba(0, 0, 0, 0.5);
        }
''', "".join(f'        <div id="caps-c{k}" class="caps-line"><span>{c}</span></div>\n' for k, (_, _, c) in enumerate(caps)),
    "".join(f'        tl.fromTo("#caps-c{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "none" }}, {round(a, 2)});\n'
            f'        tl.to("#caps-c{k}", {{ opacity: 0, duration: 0.25, ease: "none" }}, {round(b + 0.25, 2)});\n'
            for k, (a, b, _) in enumerate(caps)))

for k, v in files.items():
    with open(f"compositions/{k}.html", "w") as fh:
        fh.write(v)

tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i}" data-width="{W}" data-height="{H}"></div>
''' for c, s, d, i in SCENES)
with open("index.html", "w") as fh:
    fh.write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>천 년의 지혜, 바다를 지키다</title>
    <script src="gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: {W}px;
        height: {H}px;
        overflow: hidden;
        background: #000;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #000;
      }}
    </style>
  </head>
  <body>
    <!-- 서희함 진수 축하 영상 (웅장한 버전). Clips: Magnific Seedance 2.5 (+ veed lipsync); title-scene
         submarine: Meshy 7.1 rendered in Blender Cycles; sea and sonar: Canvas 2D; score: Lyria 3 Pro. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html"
        data-start="0" data-duration="{DUR}" data-track-index="7" data-width="{W}" data-height="{H}"></div>
      <audio id="soundtrack" src="assets/audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="8"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
os.makedirs("work", exist_ok=True)
with open("work/lines.json", "w") as fh:
    json.dump([[f, s, d] for f, s, d, _ in LINES], fh)
print("ok")
