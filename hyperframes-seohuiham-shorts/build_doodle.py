# ⑤ 실사 + 손그림 — cinematic stills (Seo Hui on the cliff, the submarine under the sea, surfacing
# at sunrise) with marker doodles drawn on top (Canvas 2D, redrawn from the GSAP clock) and
# handwritten notes in Gaegu.
import json
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

YEL = "#ffe36e"
# photos: id, file, object-position x%, start, end
PH = [("ph1", "cliff.png", 57, 0, 6.6), ("ph2", "sub-side.png", 57, 6.4, HIT + 0.1), ("ph3", "sub-surface.png", 37, HIT, DUR)]
css = f'''        .ph {{
          position: absolute;
          inset: 0;
          width: 1080px;
          height: 1920px;
          object-fit: cover;
          opacity: 0;
        }}
        #cv {{
          position: absolute;
          left: 0;
          top: 0;
        }}
        .note {{
          position: absolute;
          font-family: "Gaegu", cursive;
          font-weight: 700;
          line-height: 1.05;
          color: #ffffff;
          text-shadow: 0 3px 0 rgba(0, 0, 0, 0.55), 0 0 22px rgba(0, 0, 0, 0.55);
          clip-path: inset(0 100% 0 0);
          white-space: nowrap;
        }}
        #shade {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.45) 0%, rgba(0, 0, 0, 0) 30%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.6) 100%);
        }}
        #flash {{
          position: absolute;
          inset: 0;
          background: #ffffff;
          opacity: 0;
        }}
        #sign {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1420px;
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 26px;
          opacity: 0;
        }}
        #sign img {{
          height: 100px;
          filter: drop-shadow(0 3px 10px rgba(0, 0, 0, 0.5));
        }}
        #sign div {{
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 50px;
          color: #ffffff;
          text-shadow: 0 3px 12px rgba(0, 0, 0, 0.6);
        }}
        #sign i {{
          width: 3px;
          height: 76px;
          background: {YEL};
        }}
'''
NOTES = [  # id, html, x, y, size, colour, start
    ("n1", "이 분이 서희!", 50, 110, 120, YEL, 1.1),
    ("n2", "993년, 칼 대신 말로<br />나라를 지킨 외교관", 70, 1450, 82, "#ffffff", 2.6),
    ("n3", "1,000년 뒤…", 80, 230, 120, "#ffffff", 6.9),
    ("n4", "이름 물려받음!", 360, 1240, 116, YEL, 8.2),
    ("n5", "서희함", 200, 240, 250, YEL, HIT + 0.3),
    ("n6", "진수 축하해요!", 180, 520, 130, "#ffffff", HIT + 1.6),
    ("n7", "2026. 11. 3.", 330, 680, 76, "#ffffff", HIT + 2.6),
]
body = "".join(f'        <img id="{i}" class="ph" src="assets/{f}" alt="" style="object-position:{p}% 50%" />\n' for i, f, p, _, _ in PH)
body += '        <div id="shade"></div>\n        <canvas id="cv" width="1080" height="1920"></canvas>\n'
body += "".join(f'        <div id="{i}" class="note" style="left:{x}px;top:{y}px;font-size:{s}px;color:{c}">{h}</div>\n' for i, h, x, y, s, c, _ in NOTES)
body += '        <div id="sign"><img src="assets/icheon-logo-dark.png" alt="이천시" /><i></i><div>경기도 이천시</div></div>\n        <div id="flash"></div>\n'

# strokes: list of (kind, params, start, dur, colour, width)
STROKES = [
    ("loop", [540, 470, 200, 220, 1.15, -2.2], 0.6, 0.9, YEL, 12),
    ("arrow", [[250, 250], [230, 330], [330, 360]], 1.4, 0.5, YEL, 10),
    ("under", [[80, 1640], [880, 1625]], 3.4, 0.5, "#ffffff", 9),
    ("arrow", [[600, 1240], [640, 980], [700, 760]], 8.6, 0.5, YEL, 11),
    ("loop", [700, 640, 180, 130, 1.1, -1.4], 7.6, 0.8, "#ffffff", 10),
    ("under", [[200, 520], [800, 500]], HIT + 0.9, 0.35, YEL, 13),
    ("under", [[220, 545], [780, 530]], HIT + 1.15, 0.35, YEL, 9),
    ("star", [120, 300, 50], HIT + 1.0, 0.4, "#ffffff", 8),
    ("star", [930, 260, 60], HIT + 1.3, 0.4, YEL, 8),
    ("heart", [890, 1200, 70], HIT + 2.2, 0.6, "#ff8a8a", 10),
    ("spark", [540, 900, 240], HIT + 0.2, 0.6, "#ffffff", 7),
]
js = ""
for i, _, _, s, e in PH:
    js += f'        tl.fromTo("#{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: {0.05 if s else 0.4}, ease: "none" }}, {s});\n'
    js += f'        tl.fromTo("#{i}", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {round(e - s, 2)}, ease: "none" }}, {s});\n'
    if e < DUR:
        js += f'        tl.set("#{i}", {{ opacity: 0 }}, {e});\n'
js += f'        tl.to("#flash", {{ keyframes: [{{ opacity: 0.9, duration: 0.04 }}, {{ opacity: 0, duration: 0.45 }}] }}, {HIT - 0.04});\n'
for i, _, _, _, _, _, a in NOTES:
    js += f'        tl.to("#{i}", {{ clipPath: "inset(0 0% 0 0)", duration: 0.55, ease: "power1.inOut" }}, {round(a, 2)});\n'
js += out("#n1, #n2", 6.3, 0.2) + out("#n3, #n4", HIT - 0.05, 0.1)
js += '        tl.fromTo("#n5", { scale: 1.4, rotation: -6 }, { scale: 1, rotation: -3, duration: 0.5, ease: "back.out(2)" }, ' + str(round(HIT + 0.3, 2)) + ');\n'
js += '        tl.fromTo("#sign", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 14.2);\n'
js += out("#n5, #n6, #n7, #sign, #cv", 20.2, 0.7)
js += '''        const cv = document.getElementById("cv"), ctx = cv.getContext("2d");
        const STROKES = __S__;
        const clamp = (v) => Math.max(0, Math.min(1, v));
        const jit = (i, k) => Math.sin(i * 12.9898 + k * 78.233) * 2.2;
        function pts(kind, p) {
          const o = [];
          if (kind === "loop") {
            const [cx, cy, rx, ry, turns, a0] = p, n = Math.round(90 * turns);
            for (let i = 0; i <= n; i++) { const a = a0 + (i / 90) * Math.PI * 2; o.push([cx + Math.cos(a) * rx * (1 + 0.04 * Math.sin(i * 0.3)), cy + Math.sin(a) * ry]); }
          } else if (kind === "arrow") {
            const [a, b, c] = p;
            for (let i = 0; i <= 40; i++) { const u = i / 40; o.push([(1 - u) * (1 - u) * a[0] + 2 * (1 - u) * u * b[0] + u * u * c[0], (1 - u) * (1 - u) * a[1] + 2 * (1 - u) * u * b[1] + u * u * c[1]]); }
          } else if (kind === "under") {
            const [a, b] = p;
            for (let i = 0; i <= 30; i++) { const u = i / 30; o.push([a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u + Math.sin(u * 9) * 3]); }
          } else if (kind === "star") {
            const [cx, cy, r] = p;
            for (let i = 0; i <= 10; i++) { const a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r * 0.45 : r; o.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
          } else if (kind === "heart") {
            const [cx, cy, r] = p;
            for (let i = 0; i <= 60; i++) { const t = (i / 60) * Math.PI * 2; o.push([cx + r * 0.06 * 16 * Math.pow(Math.sin(t), 3), cy - r * 0.06 * (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t))]); }
          }
          return o;
        }
        function render(t) {
          ctx.clearRect(0, 0, 1080, 1920);
          ctx.lineCap = "round";
          ctx.lineJoin = "round";
          ctx.shadowColor = "rgba(0,0,0,0.45)";
          ctx.shadowBlur = 8;
          ctx.shadowOffsetY = 3;
          STROKES.forEach(([kind, p, s, d, col, w], k) => {
            const e = clamp((t - s) / d);
            if (e <= 0) return;
            // each photo's doodles leave with the photo
            const life = s < 6.4 ? 6.4 : s < 10 ? 10.0 : 99;
            if (t >= life) return;
            ctx.strokeStyle = col;
            ctx.lineWidth = w;
            if (kind === "spark") {
              const [cx, cy, r] = p;
              for (let i = 0; i < 12; i++) {
                const a = (i / 12) * Math.PI * 2, r0 = r * (0.55 + 0.45 * e), r1 = r0 + 60 * (1 - e * 0.5);
                ctx.globalAlpha = 1 - clamp((t - s - d) / 0.8);
                ctx.beginPath();
                ctx.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0);
                ctx.lineTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1);
                ctx.stroke();
              }
              ctx.globalAlpha = 1;
              return;
            }
            const q = pts(kind, p), n = Math.max(1, Math.floor((q.length - 1) * e));
            for (let pass = 0; pass < 2; pass++) {
              ctx.globalAlpha = pass ? 0.55 : 1;
              ctx.beginPath();
              ctx.moveTo(q[0][0] + jit(0, k + pass), q[0][1] + jit(1, k + pass));
              for (let i = 1; i <= n; i++) ctx.lineTo(q[i][0] + jit(i, k + pass), q[i][1] + jit(i + 7, k + pass));
              ctx.stroke();
            }
            ctx.globalAlpha = 1;
            if (kind === "arrow" && e >= 1) {
              const [x1, y1] = q[q.length - 1], [x0, y0] = q[q.length - 5], a = Math.atan2(y1 - y0, x1 - x0);
              ctx.beginPath();
              ctx.moveTo(x1 - Math.cos(a - 0.5) * 40, y1 - Math.sin(a - 0.5) * 40);
              ctx.lineTo(x1, y1);
              ctx.lineTo(x1 - Math.cos(a + 0.5) * 40, y1 - Math.sin(a + 0.5) * 40);
              ctx.stroke();
            }
          });
        }
        const state = { t: 0 };
        tl.to(state, { t: 21, duration: 21, ease: "none", onUpdate: () => render(state.t) }, 0);
'''.replace("__S__", json.dumps(STROKES))

d = setup("doodle")
write(d, {"doodle": comp("doodle", ["pre", "gaegu"], css, body, js)},
      index("서희함 · 실사+손그림", "⑤ photo + doodles short. Stills: Magnific; doodles drawn on canvas; score: Lyria 3 Pro cut.", [("doodle", 0, DUR)]))
print("ok")
