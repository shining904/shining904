# ⑤ Photo + doodles: marker loops, arrows, steam and stars are brushed over a real-looking
# food photo by p5 (redrawn from the GSAP clock), with handwritten notes stuck to the dishes.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import comp, index
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B0, BEAT = 0.2, 0.706
def b(k): return round(B0 + BEAT * k, 3)
T = [0, b(2), b(6), b(10), b(14), b(18), 15]
css = '''        #dd-cam { position: absolute; inset: 0; transform-origin: 0 0; }
        #dd-photo { position: absolute; inset: 0; width: 1080px; height: 1920px; }
        #dd-cv { position: absolute; left: 0; top: 0; }
        .dd-note { position: absolute; font-family: "Nanum Brush Script", cursive; line-height: 1; color: #ffffff;
          text-shadow: 0 3px 0 rgba(0,0,0,0.55), 0 0 18px rgba(0,0,0,0.6); clip-path: inset(0 100% 0 0); white-space: nowrap; }
'''
NOTES = [  # id, text, x, y, size, color, start
    ("dd-title", "이천 쌀밥 한 상", 140, 150, 170, "#ffffff", 0.15),
    ("dd-n1", "갓 지은 이천쌀!", 560, 340, 104, "#ffe066", T[1] + 0.9),
    ("dd-n2", "김치 필수!", 110, 455, 96, "#ffffff", T[2] + 0.1),
    ("dd-n3", "보글보글~", 760, 560, 88, "#ffffff", T[2] + 1.3),
    ("dd-n4", "밥 한 숟갈에 행복", 150, 1610, 120, "#ffffff", T[3] + 0.2),
    ("dd-end", "이천에서, 밥 먹고 가요", 90, 160, 118, "#ffe066", T[5] + 0.1),
]
body = '''        <div id="dd-cam">
          <img id="dd-photo" src="assets/food.jpg" alt="" />
          <div id="dd-cv"></div>
''' + "".join(f'          <div id="{i}" class="dd-note" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c}">{t}</div>\n' for i, t, x, y, s, c, _ in NOTES) + "        </div>\n"
js = r'''        (function () {
          const W = 1080, H = 1920;
          const T = __T__;
          const clamp = (v) => Math.max(0, Math.min(1, v));
          const prog = (t, a, b) => clamp((t - a) / (b - a));
          function loop(cx, cy, rx, ry, turns, start) {
            const pts = [];
            const n = Math.round(110 * turns);
            for (let i = 0; i <= n; i++) {
              const a = start + (i / 110) * Math.PI * 2, wob = 1 + 0.05 * Math.sin(i * 0.21);
              pts.push([cx + Math.cos(a) * rx * wob * (1 + i * 0.0006), cy + Math.sin(a) * ry * wob]);
            }
            return pts;
          }
          function curve(p0, p1, p2, n) {
            const pts = [];
            for (let i = 0; i <= n; i++) {
              const u = i / n;
              pts.push([(1 - u) * (1 - u) * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0], (1 - u) * (1 - u) * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]]);
            }
            return pts;
          }
          function arrowHead(tip, from, len) {
            const a = Math.atan2(tip[1] - from[1], tip[0] - from[0]);
            return [[[tip[0] - Math.cos(a - 0.5) * len, tip[1] - Math.sin(a - 0.5) * len], tip], [[tip[0] - Math.cos(a + 0.5) * len, tip[1] - Math.sin(a + 0.5) * len], tip]];
          }
          function star(cx, cy, r) {
            const pts = [];
            for (let i = 0; i <= 10; i++) {
              const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.45 : r;
              pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
            }
            return pts;
          }
          function heart(cx, cy, s) {
            const pts = [];
            for (let i = 0; i <= 60; i++) {
              const a = (i / 60) * Math.PI * 2;
              pts.push([cx + s * 16 * Math.pow(Math.sin(a), 3), cy - s * (13 * Math.cos(a) - 5 * Math.cos(2 * a) - 2 * Math.cos(3 * a) - Math.cos(4 * a))]);
            }
            return pts;
          }
          function dens(pts, step) {
            const out = [];
            for (let i = 0; i < pts.length - 1; i++) {
              const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
              const n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / step));
              for (let k = 0; k < n; k++) out.push([x0 + ((x1 - x0) * k) / n, y0 + ((y1 - y0) * k) / n]);
            }
            out.push(pts[pts.length - 1]);
            return out;
          }
          const YEL = [255, 214, 64], WHT = [255, 255, 255], RED = [240, 72, 60];
          const arrow1 = curve([860, 460], [900, 700], [680, 840], 50);
          const D = [
            // [path, color, width, start, end]
            [dens(curve([150, 330], [560, 380], [960, 320], 40), 6), YEL, 16, 0.6, 1.4],
            [loop(552, 960, 230, 150, 1.25, -0.4), YEL, 18, T[1] + 0.1, T[1] + 0.9],
            [arrow1, YEL, 14, T[1] + 1.1, T[1] + 1.6],
            ...arrowHead([680, 840], arrow1[46], 40).map((s) => [dens(s, 4), YEL, 14, T[1] + 1.6, T[1] + 1.75]),
            [loop(246, 776, 150, 140, 1.15, 3.6), RED, 14, T[2] + 0.1, T[2] + 0.8],
            [dens([[952, 742], [950, 742]], 1), WHT, 1, 99, 99],
            [loop(920, 760, 36, 30, 1, 0), WHT, 8, T[2] + 1.0, T[2] + 1.3],
            [loop(990, 800, 24, 20, 1, 0), WHT, 8, T[2] + 1.2, T[2] + 1.5],
            [loop(880, 820, 18, 15, 1, 0), WHT, 8, T[2] + 1.35, T[2] + 1.6],
            [dens(star(330, 1150, 46), 4), YEL, 10, T[3] + 0.6, T[3] + 1.0],
            [dens(star(800, 1150, 40), 4), YEL, 10, T[3] + 0.9, T[3] + 1.3],
            [dens(star(560, 700, 34), 4), YEL, 10, T[3] + 1.2, T[3] + 1.5],
            [heart(1000, 1640, 3.2), RED, 12, T[3] + 1.2, T[3] + 1.8],
            ...[0, 1, 2, 3, 4].map((k) => [dens(star(260 + k * 140, 1760, 52), 4), YEL, 12, T[4] + 0.15 + k * 0.22, T[4] + 0.45 + k * 0.22]),
          ];
          let P = null;
          new p5(function (p) {
            p.setup = function () {
              p.createCanvas(W, H).parent(document.getElementById("dd-cv"));
              p.pixelDensity(1);
              p.noLoop();
              p.clear();
              P = p;
            };
            p.draw = function () {};
          });
          function marker(pts, amt, w, col, seed) {
            const n = Math.floor((pts.length - 1) * amt);
            if (n < 1) return;
            for (let b = 0; b < 3; b++) {
              for (let i = 0; i < n; i++) {
                const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
                const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy) || 1;
                const off = (P.noise(i * 0.02, b * 5 + seed) - 0.5) * w * 0.5;
                P.stroke(col[0], col[1], col[2], 235);
                P.strokeWeight(w * (0.55 + 0.15 * b));
                P.line(x0 - (dy / len) * off, y0 + (dx / len) * off, x1 - (dy / len) * off, y1 + (dx / len) * off);
              }
            }
          }
          function render(t) {
            if (!P) return;
            P.noiseSeed(3);
            P.clear();
            P.strokeCap(P.ROUND);
            // steam squiggles rising above the rice
            const st = prog(t, T[1] + 0.3, T[1] + 0.8) * (1 - prog(t, T[4], T[4] + 0.5));
            if (st > 0) {
              for (let k = 0; k < 3; k++) {
                const x0 = 480 + k * 70, rise = ((t * 60 + k * 40) % 120);
                const pts = [];
                for (let i = 0; i <= 30; i++) pts.push([x0 + Math.sin(i * 0.4 + t * 3 + k) * 14, 860 - rise - i * 5]);
                P.drawingContext.globalAlpha = st * (1 - rise / 140);
                marker(pts, 1, 8, WHT, 20 + k);
                P.drawingContext.globalAlpha = 1;
              }
            }
            D.forEach(([pts, col, w, a, e], k) => marker(pts, prog(t, a, e), w, col, k));
          }
          const state = { t: 0 };
          const tl = gsap.timeline({ paused: true });
          tl.to(state, { t: 15, duration: 15, ease: "none", onUpdate: () => render(state.t) }, 0);
          // keep the photo covering the frame: scale >= 1 and the offset clamped to the photo edges
          const cam = (cx, cy, s) => ({ x: Math.min(0, Math.max(W - W * s, 540 - cx * s)), y: Math.min(0, Math.max(H - H * s, 960 - cy * s)), scale: s });
          tl.fromTo("#dd-cam", cam(540, 960, 1.0), { ...cam(552, 930, 1.15), duration: T[2] - 0.2, ease: "sine.inOut" }, 0.2);
          tl.to("#dd-cam", { ...cam(560, 800, 1.1), duration: 1.2, ease: "sine.inOut" }, T[2]);
          tl.to("#dd-cam", { ...cam(540, 1400, 1.08), duration: 1.4, ease: "sine.inOut" }, T[3]);
          tl.to("#dd-cam", { ...cam(540, 960, 1.0), duration: 1.6, ease: "sine.inOut" }, T[5]);
__NOTES__          tl.to("#dd-title", { opacity: 0, duration: 0.4 }, T[5]);
          window.__timelines["doodle"] = tl;
          render(0);
        })();
'''
notes_js = "".join(f'          tl.fromTo("#{i}", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: {round(0.09 * len(t), 2)}, ease: "none" }}, {round(st, 3)});\n' for i, t, x, y, s, c, st in NOTES)
js = js.replace("__T__", str(T)).replace("__NOTES__", notes_js)
open("compositions/doodle.html", "w").write(comp("doodle", ["brush"], css, body, js))
open("index.html", "w").write(index("이천 쌀밥 낙서", "doodle", 15, "Photo + doodle test: marker doodles are brushed by p5 over a generated food photo (Magnific), redrawn from the GSAP clock. Music: Magnific Google Lyria, original track.", "#2a1b12", ("gsap.min.js", "p5.min.js")))
