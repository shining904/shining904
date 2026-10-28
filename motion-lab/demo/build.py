# motion-lab demo: "흙과 불이 빚은 시간 — 이천" (15 s, 1080x1920).
# Four layers, each from a different tool, stacked in one HyperFrames timeline:
#   kiln  Canvas 2D   kiln-glow background + film grain, redrawn every frame
#   ink   p5.js       gold ink ensō brushed in, embers rising, brush underline
#   jar   Blender     Meshy 3D white-porcelain jar, Cycles render with alpha (assets/3d/jar.webm)
#   type  HTML/GSAP   kinetic typography, title, seal
# Run: python3 build.py   (then npx hyperframes check / render)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from common import comp as _comp  # noqa: E402


def comp(cid, fonts, css, body, js):
    # common.comp leaves the timeline to us: create it, then register it under the comp id
    return _comp(cid, fonts, css, body, "        const tl = gsap.timeline({ paused: true });\n" + js
                 + f'        window.__timelines["{cid}"] = tl;\n')

DUR = 15
GOLD = "#e9b75f"
files = {}

# ---------------------------------------------------------------- kiln (Canvas 2D)
files["kiln"] = comp("kiln", [], '''        #kiln-cv {
          position: absolute;
          inset: 0;
        }
''', '''        <canvas id="kiln-cv" width="1080" height="1920"></canvas>
''', '''        const cv = document.getElementById("kiln-cv"), ctx = cv.getContext("2d");
        const W = 1080, H = 1920;
        // tiny seeded hash so every frame's grain is the same on every render (seek-safe)
        const hash = (n) => { n = (n << 13) ^ n; return 1 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824; };
        const grain = document.createElement("canvas");
        grain.width = 270; grain.height = 480;
        const g = grain.getContext("2d"), gimg = g.createImageData(270, 480);
        function render(t) {
          const up = Math.min(1, t / 1.6);                 // glow fades in
          const breath = 0.85 + 0.15 * Math.sin(t * 2.1) + 0.05 * Math.sin(t * 7.3);
          ctx.fillStyle = "#120c09";
          ctx.fillRect(0, 0, W, H);
          // kiln mouth glow from below, breathing like a fire
          let rg = ctx.createRadialGradient(540, 2050, 80, 540, 1900, 1300 * breath);
          rg.addColorStop(0, `rgba(255,150,60,${0.85 * up})`);
          rg.addColorStop(0.35, `rgba(196,74,26,${0.45 * up})`);
          rg.addColorStop(1, "rgba(18,12,9,0)");
          ctx.fillStyle = rg;
          ctx.fillRect(0, 0, W, H);
          // cool halo behind the jar
          rg = ctx.createRadialGradient(540, 860, 40, 540, 860, 620);
          rg.addColorStop(0, `rgba(255,236,205,${0.16 * up})`);
          rg.addColorStop(1, "rgba(255,236,205,0)");
          ctx.fillStyle = rg;
          ctx.fillRect(0, 0, W, H);
          // grain: new pattern every 2 frames, upscaled
          const f = Math.floor(t * 15);
          for (let i = 0; i < gimg.data.length; i += 4) {
            const v = 128 + hash(i * 7 + f * 104729) * 70;
            gimg.data[i] = gimg.data[i + 1] = gimg.data[i + 2] = v;
            gimg.data[i + 3] = 22;
          }
          g.putImageData(gimg, 0, 0);
          ctx.imageSmoothingEnabled = false;
          ctx.drawImage(grain, 0, 0, W, H);
          // vignette
          rg = ctx.createRadialGradient(540, 900, 500, 540, 900, 1250);
          rg.addColorStop(0, "rgba(0,0,0,0)");
          rg.addColorStop(1, "rgba(0,0,0,0.6)");
          ctx.fillStyle = rg;
          ctx.fillRect(0, 0, W, H);
        }
        const state = { t: 0 };
        tl.to(state, { t: 15, duration: 15, ease: "none", onUpdate: () => render(state.t) }, 0);
''')

# ---------------------------------------------------------------- ink (p5.js)
files["ink"] = comp("ink", [], '''        #ink-host {
          position: absolute;
          inset: 0;
        }
''', '''        <div id="ink-host"></div>
''', '''        const W = 1080, H = 1920, CX = 540, CY = 880, R = 390;
        const clamp = (v) => Math.max(0, Math.min(1, v));
        const prog = (t, a, b) => clamp((t - a) / (b - a));
        const ease = (x) => 1 - Math.pow(1 - x, 3);
        let P = null;
        new p5(function (p) {
          p.setup = function () {
            p.createCanvas(W, H).parent(document.getElementById("ink-host"));
            p.pixelDensity(1);
            p.noLoop();
            P = p;
          };
          p.draw = function () {};
        });
        // ensō: one brush loop with a gap, pressure fading at the tail
        const ENSO = [];
        for (let i = 0; i <= 520; i++) {
          const a = -Math.PI * 0.62 + (i / 520) * Math.PI * 1.86;
          const wob = 1 + 0.012 * Math.sin(i * 0.055) + 0.006 * Math.sin(i * 0.185);
          ENSO.push([CX + Math.cos(a) * R * wob, CY + Math.sin(a) * R * wob * 1.02]);
        }
        const UNDER = [];
        for (let i = 0; i <= 90; i++) UNDER.push([300 + i * 5.4, 1470 + Math.sin(i * 0.09) * 10 - i * 0.25]);
        // dry brush: 9 bristles, each a continuous path broken into short runs so pressure and
        // ink can change along the stroke (separate tiny segments read as beads, not ink)
        function brush(pts, amt, w, col, alpha, seed) {
          const n = Math.floor((pts.length - 1) * amt), ctx = P.drawingContext, RUN = 6;
          ctx.lineCap = "round";
          ctx.lineJoin = "round";
          for (let b = 0; b < 9; b++) {
            const lane = (b - 4) / 4;
            for (let i0 = 0; i0 < n; i0 += RUN) {
              const u = i0 / (pts.length - 1);
              if (P.noise(i0 * 0.05, b * 13 + seed) < 0.12 + 0.35 * u * Math.abs(lane)) continue;  // dry gaps
              const press = Math.sin(Math.PI * Math.min(1, u * 1.05 + 0.05)) * (0.75 + 0.25 * P.noise(i0 * 0.03, seed));
              ctx.beginPath();
              for (let i = i0; i <= Math.min(n, i0 + RUN); i++) {
                const [x0, y0] = pts[Math.max(0, i - 1)], [x1, y1] = pts[Math.min(pts.length - 1, i + 1)];
                const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy) || 1;
                const off = lane * w * 0.5 * press + (P.noise(i * 0.02, b * 5 + seed) - 0.5) * w * 0.18;
                const x = pts[i][0] - (dy / len) * off, y = pts[i][1] + (dx / len) * off;
                if (i === i0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
              }
              const a = alpha * (0.55 + 0.45 * P.noise(i0 * 0.04, b + seed)) / 255;
              ctx.strokeStyle = `rgba(${col[0]},${col[1]},${col[2]},${a})`;
              ctx.lineWidth = Math.max(1, w * 0.2 * (0.6 + press));
              ctx.stroke();
            }
          }
        }
        // embers: each has a fixed seed, so its position is a pure function of time
        const EMB = [];
        for (let i = 0; i < 140; i++) {
          const r = (k) => { const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
          EMB.push({ x: r(1) * W, born: 1.2 + r(2) * 13, speed: 120 + r(3) * 260, sway: 20 + r(4) * 50, size: 2 + r(5) * 5, ph: r(6) * 6.28, life: 2.5 + r(7) * 3 });
        }
        function render(t) {
          if (!P) return;
          P.clear();
          P.randomSeed(3);
          P.noiseSeed(3);
          const ctx = P.drawingContext;
          // ensō
          const e = ease(prog(t, 0.3, 2.4)), fade = 1 - 0.55 * prog(t, 9.0, 10.0);
          if (e > 0) {
            ctx.shadowColor = "rgba(233,183,95,0.6)";
            ctx.shadowBlur = 18;
            brush(ENSO, e, 30, [233, 183, 95], 210 * fade, 7);
            ctx.shadowBlur = 0;
          }
          // underline brushed under the title
          const u = ease(prog(t, 10.2, 11.0));
          if (u > 0) brush(UNDER, u, 16, [233, 183, 95], 230, 21);
          // embers rising, brighter after the title lands
          const boost = 1 + 0.8 * prog(t, 10.0, 11.0);
          P.noStroke();
          for (const m of EMB) {
            const age = t - m.born;
            if (age < 0 || age > m.life) continue;
            const k = age / m.life, y = 1950 - age * m.speed;
            const x = m.x + Math.sin(age * 1.7 + m.ph) * m.sway;
            const a = Math.sin(Math.PI * k) * 255 * Math.min(1, boost);
            ctx.shadowColor = "rgba(255,150,60,0.9)";
            ctx.shadowBlur = 12;
            P.fill(255, 170 + 60 * (1 - k), 90, a);
            P.circle(x, y, m.size * boost * (1 - 0.5 * k));
          }
          ctx.shadowBlur = 0;
        }
        const state = { t: 0 };
        tl.to(state, { t: 15, duration: 15, ease: "none", onUpdate: () => render(state.t) }, 0);
''')

# ---------------------------------------------------------------- jar (Blender render with alpha)
files["jar"] = comp("jar", [], '''        #jar-box {
          position: absolute;
          left: 130px;
          top: 450px;
          width: 820px;
          height: 820px;
        }
        #jar-video {
          width: 100%;
          height: 100%;
          -webkit-mask-image: radial-gradient(ellipse 48% 50% at 50% 52%, #000 62%, transparent 100%);
          mask-image: radial-gradient(ellipse 48% 50% at 50% 52%, #000 62%, transparent 100%);
        }
''', '''        <div id="jar-box">
          <video id="jar-video" src="assets/3d/jar.webm" data-start="0" data-duration="12.6" muted playsinline></video>
        </div>
''', '''        tl.fromTo("#jar-box", { opacity: 0, y: 80, scale: 0.92 }, { opacity: 1, y: 0, scale: 1, duration: 1.4, ease: "power3.out" }, 0);
        tl.to("#jar-box", { y: -40, scale: 0.94, duration: 1.6, ease: "power2.inOut" }, 7.0);
''')

# ---------------------------------------------------------------- type (kinetic typography)
L1, L2 = "흙과 불이", "빚어낸 하얀 시간"
spans = lambda s, c: "".join(f'<span class="{c}">{ch if ch != " " else "&nbsp;"}</span>' for ch in s)
files["type"] = comp("type", ["myeongjo", "brush", "noto"], f'''        .type-line {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          color: #f6ead6;
        }}
        #type-l1 {{
          top: 250px;
          font-size: 96px;
        }}
        #type-l2 {{
          top: 372px;
          font-size: 64px;
          color: {GOLD};
        }}
        .type-c1,
        .type-c2 {{
          display: inline-block;
        }}
        #type-title {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1225px;
          text-align: center;
          font-family: "Nanum Brush Script", cursive;
          font-size: 300px;
          line-height: 1;
          color: {GOLD};
          text-shadow: 0 0 40px rgba(233, 140, 60, 0.45);
        }}
        #type-seal {{
          position: absolute;
          left: 760px;
          top: 1270px;
          width: 120px;
          height: 120px;
          border: 6px solid #d8432c;
          border-radius: 14px;
          color: #d8432c;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 46px;
          line-height: 52px;
          text-align: center;
          padding-top: 4px;
        }}
        #type-sub {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1510px;
          text-align: center;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 34px;
          letter-spacing: 12px;
          color: #e8d8bf;
        }}
''', f'''        <div id="type-l1" class="type-line">{spans(L1, "type-c1")}</div>
        <div id="type-l2" class="type-line">{spans(L2, "type-c2")}</div>
        <div id="type-title">이천</div>
        <div id="type-seal">利<br />川</div>
        <div id="type-sub">ICHEON · 도자기의 도시</div>
''', '''        tl.fromTo(".type-c1", { opacity: 0, y: 40, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out", stagger: 0.09 }, 0.8);
        tl.fromTo(".type-c2", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power2.out", stagger: 0.05 }, 1.9);
        tl.to("#type-l1, #type-l2", { opacity: 0, y: -30, duration: 0.6, ease: "power2.in" }, 8.8);
        tl.fromTo("#type-title", { clipPath: "inset(0 100% 0 0)", opacity: 1 }, { clipPath: "inset(0 0% 0 0)", duration: 1.0, ease: "power2.inOut" }, 9.6);
        tl.fromTo("#type-seal", { opacity: 0, scale: 2.4, rotation: -16 }, { opacity: 1, scale: 1, rotation: -6, duration: 0.2, ease: "power4.in" }, 10.7);
        tl.fromTo("#type-sub", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, 11.1);
''')

for k, v in files.items():
    with open(f"compositions/{k}.html", "w") as fh:
        fh.write(v)

LAYERS = [("kiln", 0, DUR, 0), ("ink", 0, DUR, 1), ("jar", 2.4, 12.6, 2), ("type", 0, DUR, 3)]
tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i}" data-width="1080" data-height="1920"></div>
''' for c, s, d, i in LAYERS)
audio = ('      <audio id="soundtrack" src="assets/audio/music.mp3" data-start="0" data-duration="15" data-track-index="4"></audio>\n'
         if os.path.exists("assets/audio/music.mp3") else "")
with open("index.html", "w") as fh:
    fh.write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>흙과 불이 빚은 시간</title>
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
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: #120c09;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #120c09;
      }}
    </style>
  </head>
  <body>
    <!-- motion-lab demo. 3D jar: Meshy 7.1 (via Magnific) rendered in Blender Cycles with alpha. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{tracks}{audio}    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
print("ok")
