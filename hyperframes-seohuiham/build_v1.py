# 서희함 진수 축하 영상 「천 년의 지혜, 바다를 지키다」 (1920x1080, 78 s).
# Generates index.html and compositions/*.html. Run: python3 build.py
#   ink    p5.js      ink-wash map of Goryeo: Khitan ink spreading south, then 강동 6주 in gold
#   camp   Seedance   young Seo Hui walking alone into the Khitan camp
#   tent   Seedance   the negotiation in the general's tent
#   ocean  Canvas 2D  ink turns to deep sea: light shafts, caustics, drifting particles
#   sub    Blender    Meshy submarine rendered with alpha (assets/3d/sub.webm), cruise preset
#   speech Seedance + veed lipsync   mature Seo Hui's congratulation
#   end    HTML/GSAP  closing card
#   caps   subtitles for every spoken line
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, DUR = 1920, 1080, 78
GOLD, INK, PAPER, SEA = "#d9a441", "#1d1a17", "#efe6d2", "#04182e"
FONTS = {
    "myeongjo": [("Nanum Myeongjo", 800, "nanum-myeongjo-latin-800-normal", "U+0000-00FF"),
                 ("Nanum Myeongjo", 800, "nanum-myeongjo-korean-800-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF, U+4E00-9FFF")],
    "brush": [("Nanum Brush Script", 400, "nanum-brush-script-latin-400-normal", "U+0000-00FF"),
              ("Nanum Brush Script", 400, "nanum-brush-script-korean-400-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")],
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


def pop(sel, a, y=30, dur=0.8, ease="power3.out"):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "{ease}" }}, {a});\n'


def out(sel, a, dur=0.6):
    return f'        tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {a});\n'


# scene id, start, duration, track (alternating tracks so neighbours can overlap for dissolves)
SCENES = [("ink", 0, 34.5, 0), ("camp", 10.0, 8.4, 1), ("tent", 18.0, 8.4, 2),
          ("ocean", 33.5, 19.0, 1), ("sub", 36.0, 16.0, 2), ("speech", 52.0, 15.2, 3), ("end", 66.8, 11.2, 4)]
# spoken lines: file, start, speech length, caption
LINES = [("n1.mp3", 1.5, 5.2, "서기 993년. 거란의 대군이 고려의 북쪽 국경을 넘었습니다."),
         ("n2.mp3", 11.0, 5.3, "모두가 땅을 내주자고 할 때, 한 사람이 홀로 적진으로 걸어 들어갔습니다."),
         ("y1.mp3", 18.6, 4.66, "“우리는 고구려를 이은 나라요. 그래서 나라 이름도, 고려입니다.”"),
         ("n3.mp3", 27.0, 6.1, "칼 한 번 쓰지 않고, 압록강까지 강동 6주를 얻어낸 고려의 외교관. 서희."),
         ("n4.mp3", 35.6, 5.96, "그로부터 천 년. 그 이름이 다시, 나라를 지키러 바다로 나아갑니다."),
         ("s1.mp3", 52.0, 14.7, None)]
SPEECH = [(0.0, 1.23, "서희함 장병 여러분."), (1.83, 5.59, "천 년 전 저는 칼 대신 지혜로 이 땅을 지켰습니다."),
          (6.15, 9.9, "이제 제 이름이 바다 깊은 곳에서 나라를 지킵니다."),
          (10.72, 14.7, "이천시민들과 함께, 서희함의 안전한 항해를 응원합니다.")]

files = {}

# ---------------------------------------------------------------- ink map (p5.js)
# rough coastline (lon, lat) of the peninsula, enough for a concept map
COAST = [(124.3, 39.9), (124.7, 39.6), (125.1, 39.5), (125.4, 39.0), (125.1, 38.7), (125.3, 38.3), (124.8, 38.0),
         (125.6, 37.7), (126.1, 37.7), (126.6, 37.5), (126.8, 37.0), (126.5, 36.6), (126.5, 36.0), (126.7, 35.5),
         (126.4, 34.8), (126.6, 34.4), (127.4, 34.6), (128.0, 34.8), (128.6, 34.9), (129.1, 35.1), (129.4, 35.5),
         (129.5, 36.0), (129.4, 36.6), (129.3, 37.1), (128.9, 37.7), (128.5, 38.3), (128.3, 38.6), (127.8, 39.1),
         (127.5, 39.3), (127.6, 39.8), (128.3, 40.0), (128.9, 40.5), (129.7, 40.9), (129.8, 41.4), (130.2, 42.0),
         (130.7, 42.3), (130.0, 42.9), (129.3, 42.4), (128.9, 42.0), (128.1, 42.0), (127.5, 41.7), (126.9, 41.8),
         (126.3, 41.3), (125.4, 40.6), (124.9, 40.3), (124.3, 39.9)]
YALU = [(124.3, 39.9), (124.9, 40.3), (125.4, 40.6), (126.3, 41.3), (126.9, 41.8), (127.5, 41.7), (128.1, 42.0)]
SIX = [("흥화진", 124.65, 40.25), ("용주", 124.85, 39.95), ("통주", 125.15, 40.05), ("철주", 125.05, 39.75),
       ("귀주", 125.45, 40.0), ("곽주", 125.4, 39.7)]
# the map is inked onto a real-looking hanji scroll on the war-council table (assets/img/table1.png);
# the scroll's paper spans roughly x 640-1345, y 290-840 of the 1920x1080 frame
proj = lambda lon, lat: (round(905 + (lon - 124) * 54, 1), round(318 + (43 - lat) * 54, 1))
coast = [proj(*p) for p in COAST]
yalu = [proj(*p) for p in YALU]
six = [proj(lo, la) for _, lo, la in SIX]
GX, GY = proj(125.0, 40.0)  # zoom target: the 강동 6주 area
files["ink"] = comp("ink", ["myeongjo", "brush", "noto"], f"""        #ink-cam {{
          position: absolute;
          inset: 0;
        }}
        #ink-table {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
        }}
        #ink-host {{
          position: absolute;
          inset: 0;
          mix-blend-mode: multiply;
        }}
        #ink-flicker {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 22% 18%, rgba(255, 170, 80, 0.22) 0%, rgba(255, 170, 80, 0) 45%);
          mix-blend-mode: screen;
        }}
        .ink-w {{
          position: absolute;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          color: rgba(30, 24, 18, 0.88);
          mix-blend-mode: multiply;
        }}
        #ink-y1 {{
          left: 672px;
          top: 330px;
          font-size: 76px;
        }}
        #ink-y2 {{
          left: 676px;
          top: 420px;
          font-size: 26px;
          color: rgba(122, 43, 31, 0.9);
        }}
        #ink-khitan {{
          left: 1120px;
          top: 300px;
          font-size: 26px;
          color: rgba(240, 230, 210, 0.95);
          mix-blend-mode: normal;
        }}
        #ink-goryeo {{
          left: 1020px;
          top: 560px;
          font-size: 26px;
        }}
        #ink-gd {{
          left: 672px;
          top: 470px;
          font-family: "Nanum Brush Script", cursive;
          font-weight: 400;
          font-size: 72px;
          color: rgba(150, 100, 20, 0.95);
        }}
        #ink-gd-sub {{
          left: 676px;
          top: 548px;
          font-size: 20px;
        }}
        #ink-name {{
          left: 676px;
          top: 600px;
          font-size: 36px;
        }}
        #ink-name small {{
          font-size: 18px;
          color: rgba(122, 43, 31, 0.9);
          margin-left: 10px;
        }}
        #ink-note {{
          position: absolute;
          left: 30px;
          top: 24px;
          font-family: "Noto Sans KR", sans-serif;
          font-size: 20px;
          color: rgba(230, 215, 190, 0.7);
        }}
""", """        <div id="ink-cam">
          <img id="ink-table" src="assets/img/table1.png" alt="" />
          <div id="ink-host"></div>
          <div id="ink-y1" class="ink-w">993</div>
          <div id="ink-y2" class="ink-w">고려 성종 12년</div>
          <div id="ink-khitan" class="ink-w">거란</div>
          <div id="ink-goryeo" class="ink-w">고려</div>
          <div id="ink-gd" class="ink-w">강동 6주</div>
          <div id="ink-gd-sub" class="ink-w">압록강까지, 280리의 땅</div>
          <div id="ink-name" class="ink-w">서희<small>徐熙 · 942–998</small></div>
          <div id="ink-flicker"></div>
        </div>
        <div id="ink-note">개념도 · 실제 경계와 다를 수 있음</div>
""", f"""        const W = {W}, H = {H};
        const COAST = {json.dumps(coast)}, YALU = {json.dumps(yalu)}, SIX = {json.dumps(six)};
        const PAPER = [650, 300, 1335, 832];   // ink stays on the paper
        const clamp = (v) => Math.max(0, Math.min(1, v));
        const prog = (t, a, b) => clamp((t - a) / (b - a));
        const ease = (x) => 1 - Math.pow(1 - x, 3);
        let P = null;
        new p5(function (p) {{
          p.setup = function () {{
            p.createCanvas(W, H).parent(document.getElementById("ink-host"));
            p.pixelDensity(1);
            p.noLoop();
            P = p;
          }};
          p.draw = function () {{}};
        }});
        function path(pts, upto) {{
          const n = Math.max(1, Math.floor((pts.length - 1) * upto));
          const ctx = P.drawingContext;
          ctx.beginPath();
          ctx.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i <= n; i++) ctx.lineTo(pts[i][0], pts[i][1]);
          return ctx;
        }}
        function render(t) {{
          if (!P) return;
          P.clear();
          P.randomSeed(9);
          P.noiseSeed(9);
          const ctx = P.drawingContext;
          ctx.save();
          ctx.beginPath();
          ctx.rect(PAPER[0], PAPER[1], PAPER[2] - PAPER[0], PAPER[3] - PAPER[1]);
          ctx.clip();
          // coastline brushed in with a dry ink brush
          const c = ease(prog(t, 0.4, 3.0));
          ctx.lineJoin = "round";
          ctx.lineCap = "round";
          for (let k = 0; k < 4; k++) {{
            ctx.save();
            ctx.translate((P.noise(k) - 0.5) * 2.4, (P.noise(k + 9) - 0.5) * 2.4);
            path(COAST, c);
            ctx.strokeStyle = `rgba(28,22,16,${{0.5 - k * 0.1}})`;
            ctx.lineWidth = 3.4 - k * 0.7;
            ctx.stroke();
            ctx.restore();
          }}
          if (c >= 1) {{
            path(COAST, 1);
            ctx.closePath();
            ctx.fillStyle = "rgba(120,90,50,0.10)";
            ctx.fill();
          }}
          // Khitan ink soaking into the paper from the north edge
          const k = ease(prog(t, 2.6, 8.0)) * (1 - prog(t, 25.6, 27.6));
          if (k > 0) {{
            for (let i = 0; i < 60; i++) {{
              const bx = 960 + P.noise(i * 0.3) * 380, by = 300 + P.noise(i * 0.3, 5) * 40;
              const r = (30 + P.noise(i, 2) * 80) * k;
              const g = ctx.createRadialGradient(bx, by + 40 * k, 0, bx, by + 40 * k, r);
              g.addColorStop(0, `rgba(15,12,10,${{0.6 * k}})`);
              g.addColorStop(0.7, `rgba(15,12,10,${{0.25 * k}})`);
              g.addColorStop(1, "rgba(15,12,10,0)");
              ctx.fillStyle = g;
              ctx.fillRect(bx - r, by + 40 * k - r, r * 2, r * 2);
            }}
            for (let a = 0; a < 3; a++) {{
              const ax = 1010 + a * 70, len = 50 + 80 * prog(t, 4 + a * 0.4, 8);
              ctx.strokeStyle = `rgba(140,30,20,${{0.85 * k}})`;
              ctx.lineWidth = 5;
              ctx.beginPath();
              ctx.moveTo(ax, 360);
              ctx.lineTo(ax + 10, 360 + len);
              ctx.moveTo(ax + 10 - 11, 360 + len - 15);
              ctx.lineTo(ax + 10, 360 + len);
              ctx.lineTo(ax + 10 + 13, 360 + len - 12);
              ctx.stroke();
            }}
          }}
          ctx.restore();
          // 강동 6주 in gold leaf along the Yalu, the six fortresses pressed in like seals
          const y = ease(prog(t, 27.4, 30.0));
          if (y > 0) {{
            ctx.shadowColor = "rgba(255,190,80,0.9)";
            ctx.shadowBlur = 10;
            path(YALU, y);
            ctx.strokeStyle = "#c8902a";
            ctx.lineWidth = 6;
            ctx.stroke();
            ctx.shadowBlur = 0;
            SIX.forEach(([sx, sy], i) => {{
              const s = ease(prog(t, 28.6 + i * 0.25, 29.2 + i * 0.25));
              if (s <= 0) return;
              ctx.fillStyle = "rgba(200,144,42,0.35)";
              ctx.beginPath();
              ctx.arc(sx, sy, 12 * s, 0, Math.PI * 2);
              ctx.fill();
              ctx.fillStyle = "#a8321f";
              ctx.fillRect(sx - 3.5 * s, sy - 3.5 * s, 7 * s, 7 * s);
            }});
          }}
        }}
        const state = {{ t: 0 }};
        tl.to(state, {{ t: 34.5, duration: 34.5, ease: "none", onUpdate: () => render(state.t) }}, 0);
        // candle flicker
        tl.to(state, {{ duration: 34.5, ease: "none", onUpdate: () => {{
          const f = 0.75 + 0.15 * Math.sin(state.t * 7.1) + 0.1 * Math.sin(state.t * 12.7 + 1);
          document.getElementById("ink-flicker").style.opacity = f;
        }} }}, 0);
        // camera: slow push over the table, then a move onto the north-west for 강동 6주
        tl.fromTo("#ink-cam", {{ scale: 1.08 }}, {{ scale: 1.22, duration: 10, ease: "sine.inOut" }}, 0);
        tl.set("#ink-cam", {{ transformOrigin: "{GX}px {GY - 40}px" }}, 0);
        tl.to("#ink-cam", {{ scale: 2.1, x: {960 - GX}, y: {470 - GY}, duration: 3.5, ease: "power2.inOut" }}, 26.0);
""" + pop("#ink-y1", 1.0, 20, 1.2) + pop("#ink-y2", 1.6, 10) + pop("#ink-khitan", 3.4, -10) + pop("#ink-goryeo", 2.4, 10)
    + out("#ink-y1, #ink-y2, #ink-khitan, #ink-goryeo", 9.0) + pop("#ink-gd", 28.0, 10) + pop("#ink-gd-sub", 28.8, 6)
    + pop("#ink-name", 31.0, 6) + pop("#ink-note", 27.5, 0)
    + out("#ink-gd, #ink-gd-sub, #ink-name, #ink-note", 33.6, 0.5))


# ---------------------------------------------------------------- live-action clips (Seedance)
def clip(cid, src, dur, extra_css="", extra_body="", extra_js="", fade_in=0.6, push=(1.0, 1.05)):
    return comp(cid, ["myeongjo"], f'''        #{cid}-fade {{
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
        }}
{extra_css}''', f'''        <div id="{cid}-fade">
          <video id="{cid}-video" src="{src}" data-start="0" data-duration="{dur}" muted playsinline></video>
{extra_body}        </div>
''', f'''        tl.fromTo("#{cid}-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_in}, ease: "none" }}, 0);
        tl.fromTo("#{cid}-video", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {dur}, ease: "none" }}, 0);
{extra_js}''')


files["camp"] = clip("camp", "assets/clips/camp.mp4", 8.4)
files["tent"] = clip("tent", "assets/clips/tent.mp4", 8.4, '''        #tent-q {
          position: absolute;
          left: 0;
          right: 0;
          top: 90px;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 58px;
          color: #f6ead2;
          text-shadow: 0 4px 24px rgba(0, 0, 0, 0.8);
        }
''', '        <div id="tent-q">칼이 아닌 말로, 나라를 지키다</div>\n', pop("#tent-q", 5.6, 20, 1.0), fade_in=0.4)

# ---------------------------------------------------------------- ocean (Canvas 2D) + facts
files["ocean"] = comp("ocean", ["myeongjo", "noto"], f'''        #ocean-cv {{
          position: absolute;
          inset: 0;
        }}
        #ocean-facts {{
          position: absolute;
          left: 120px;
          top: 110px;
        }}
        #ocean-name {{
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 120px;
          line-height: 1.05;
          color: #ffffff;
          text-shadow: 0 0 40px rgba(80, 170, 255, 0.45);
        }}
        #ocean-en {{
          margin-top: 6px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 30px;
          letter-spacing: 14px;
          color: #9fd4ff;
        }}
        .ocean-row {{
          margin-top: 18px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 800;
          font-size: 36px;
          color: #e8f4ff;
        }}
        .ocean-row b {{
          color: {GOLD};
          margin-right: 16px;
        }}
''', '''        <canvas id="ocean-cv" width="1920" height="1080"></canvas>
        <div id="ocean-facts">
          <div id="ocean-name">서희함</div>
          <div id="ocean-en">ROKS SEO HUI</div>
          <div id="ocean-r1" class="ocean-row"><b>장보고-Ⅲ 배치-Ⅱ</b>2번함</div>
          <div id="ocean-r2" class="ocean-row"><b>3,600톤급</b>잠수함</div>
          <div id="ocean-r3" class="ocean-row"><b>2026. 11. 3.</b>진수</div>
        </div>
''', '''        const cv = document.getElementById("ocean-cv"), ctx = cv.getContext("2d");
        const W = 1920, H = 1080;
        const rnd = (i, k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
        function render(t) {
          // ink settles into water: paper tone fades to deep blue in the first 2.5 s
          const m = Math.min(1, t / 2.5);
          const g = ctx.createLinearGradient(0, 0, 0, H);
          g.addColorStop(0, `rgb(${Math.round(239 - 225 * m)},${Math.round(230 - 170 * m)},${Math.round(210 - 100 * m)})`);
          g.addColorStop(1, `rgb(${Math.round(239 - 237 * m)},${Math.round(230 - 218 * m)},${Math.round(210 - 180 * m)})`);
          ctx.fillStyle = g;
          ctx.fillRect(0, 0, W, H);
          // light shafts from the surface, swaying
          ctx.globalCompositeOperation = "lighter";
          for (let i = 0; i < 9; i++) {
            const x = 150 + i * 210 + Math.sin(t * 0.4 + i) * 60, w = 70 + rnd(i, 1) * 120;
            const s = ctx.createLinearGradient(0, 0, 0, H);
            s.addColorStop(0, `rgba(120,200,255,${0.16 * m})`);
            s.addColorStop(1, "rgba(120,200,255,0)");
            ctx.fillStyle = s;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x + w, 0);
            ctx.lineTo(x + w * 2.6 - 300, H);
            ctx.lineTo(x - 300, H);
            ctx.fill();
          }
          // caustic shimmer near the top
          for (let i = 0; i < 26; i++) {
            const x = rnd(i, 2) * W + Math.sin(t * 0.6 + i) * 40, y = rnd(i, 3) * 220;
            const a = (0.04 + 0.03 * Math.sin(t * 1.5 + i)) * m, r = 120 + rnd(i, 10) * 160;
            const cg = ctx.createRadialGradient(x, y, 0, x, y, r);
            cg.addColorStop(0, `rgba(170,230,255,${a})`);
            cg.addColorStop(1, "rgba(170,230,255,0)");
            ctx.fillStyle = cg;
            ctx.fillRect(x - r, y - r, r * 2, r * 2);
          }
          ctx.globalCompositeOperation = "source-over";
          // drifting particles (marine snow), each a pure function of t
          for (let i = 0; i < 220; i++) {
            const x = (rnd(i, 4) * W + t * (8 + rnd(i, 5) * 20)) % W;
            const y = (rnd(i, 6) * H + t * (6 + rnd(i, 7) * 14)) % H;
            ctx.fillStyle = `rgba(200,230,255,${(0.15 + rnd(i, 8) * 0.35) * m})`;
            ctx.beginPath();
            ctx.arc(x, y, 1 + rnd(i, 9) * 2.2, 0, Math.PI * 2);
            ctx.fill();
          }
          // depth vignette
          const v = ctx.createRadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1150);
          v.addColorStop(0, "rgba(0,0,0,0)");
          v.addColorStop(1, `rgba(0,6,16,${0.75 * m})`);
          ctx.fillStyle = v;
          ctx.fillRect(0, 0, W, H);
        }
        const state = { t: 0 };
        tl.to(state, { t: 19, duration: 19, ease: "none", onUpdate: () => render(state.t) }, 0);
''' + pop("#ocean-name", 10.6, 40, 1.0) + pop("#ocean-en", 11.2, 10) + pop("#ocean-r1", 12.0, 20)
    + pop("#ocean-r2", 12.6, 20) + pop("#ocean-r3", 13.2, 20)
    + '        tl.set("#ocean-name, #ocean-en, .ocean-row", { opacity: 0 }, 0);\n')

# ---------------------------------------------------------------- submarine (Blender, alpha)
files["sub"] = comp("sub", [], '''        #sub-box {
          position: absolute;
          left: 0;
          top: 0;
          width: 1920px;
          height: 1080px;
        }
        #sub-video {
          width: 100%;
          height: 100%;
          filter: saturate(0.9) brightness(1.05);
        }
        #sub-haze {
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 55%, rgba(4, 24, 46, 0) 40%, rgba(4, 24, 46, 0.55) 100%);
        }
''', '''        <div id="sub-box">
          <video id="sub-video" src="assets/3d/sub.webm" data-start="0" data-duration="16" muted playsinline></video>
        </div>
        <div id="sub-haze"></div>
''', '''        tl.fromTo("#sub-box", { opacity: 0, x: 220 }, { opacity: 1, x: 0, duration: 2.4, ease: "power2.out" }, 0);
        tl.to("#sub-box", { x: -60, duration: 13.6, ease: "none" }, 2.4);
        tl.to("#sub-box", { y: 190, duration: 2.2, ease: "power2.inOut" }, 7.6);
        tl.to("#sub-box", { opacity: 0, duration: 1.0, ease: "none" }, 15.0);
''')

# ---------------------------------------------------------------- speech (lipsynced)
files["speech"] = clip("speech", "assets/clips/speech-lip.mp4", 15.2, push=(1.0, 1.04), fade_in=0.8)

# ---------------------------------------------------------------- end card
files["end"] = comp("end", ["myeongjo", "noto"], f'''        #end-bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 45%, #0b2a4d 0%, {SEA} 60%, #010a15 100%);
        }}
        #end-line1 {{
          position: absolute;
          left: 0;
          right: 0;
          top: 300px;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 104px;
          color: #ffffff;
        }}
        #end-line1 span {{
          color: {GOLD};
        }}
        #end-rule {{
          position: absolute;
          left: 760px;
          width: 400px;
          top: 470px;
          height: 4px;
          background: {GOLD};
        }}
        #end-line2 {{
          position: absolute;
          left: 0;
          right: 0;
          top: 510px;
          text-align: center;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 40px;
          color: #cfe2f5;
        }}
        #end-from {{
          position: absolute;
          left: 0;
          right: 0;
          top: 660px;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 54px;
          color: #ffffff;
        }}
        #end-logo {{
          position: absolute;
          left: 50%;
          top: 780px;
          margin-left: -130px;
          width: 260px;
          padding: 12px 20px;
          border-radius: 18px;
          background: #ffffff;
        }}
        #end-logo img {{
          display: block;
          width: 100%;
        }}
        #end-ai {{
          position: absolute;
          right: 30px;
          bottom: 22px;
          font-family: "Noto Sans KR", sans-serif;
          font-size: 20px;
          color: #7f97b0;
        }}
''', '''        <div id="end-bg"></div>
        <div id="end-line1"><span>서희함</span>의 진수를 진심으로 축하합니다</div>
        <div id="end-rule"></div>
        <div id="end-line2">천 년의 지혜와 함께, 안전한 항해를 기원합니다</div>
        <div id="end-from">이천시민 일동</div>
        <div id="end-logo"><img src="assets/img/icheon-logo.png" alt="이천시" /></div>
        <div id="end-ai">본 영상은 AI로 제작되었으며 역사 장면은 재연입니다</div>
''', '''        tl.fromTo("#end-bg", { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "none" }, 0);
        tl.fromTo("#end-line1", { opacity: 0, y: 30, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 1.4, ease: "power3.out" }, 0.6);
        tl.fromTo("#end-rule", { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: "power3.inOut" }, 1.6);
''' + pop("#end-line2", 2.2, 16) + pop("#end-from", 3.4, 16) + pop("#end-logo", 4.0, 16) + pop("#end-ai", 4.0, 0)
    + out("#end-bg, #end-line1, #end-rule, #end-line2, #end-from, #end-logo, #end-ai", 10.2, 1.0))

# ---------------------------------------------------------------- captions
caps = [(s, s + d, c) for _, s, d, c in LINES if c] + [(52.0 + a, 52.0 + b, c) for a, b, c in SPEECH]
files["caps"] = comp("caps", ["noto"], '''        .caps-line {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 46px;
          text-align: center;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 40px;
          color: #ffffff;
          opacity: 0;
        }
        .caps-line span {
          display: inline-block;
          padding: 8px 26px;
          border-radius: 12px;
          background: rgba(0, 0, 0, 0.55);
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
    <script src="p5.min.js"></script>
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
    <!-- 서희함 진수 축하 영상. Clips: Magnific Seedance 2.5 (+ veed lipsync); submarine: Meshy 7.1
         rendered in Blender Cycles; map: p5.js; sea: Canvas 2D; score: Lyria 3 Pro. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html"
        data-start="0" data-duration="{DUR}" data-track-index="5" data-width="{W}" data-height="{H}"></div>
      <audio id="soundtrack" src="assets/audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="6"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
with open("work/lines.json", "w") as fh:
    json.dump([[f, s, d] for f, s, d, _ in LINES], fh)
print("ok")
