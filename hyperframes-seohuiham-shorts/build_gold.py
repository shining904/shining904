# ① 금빛 한 줄 (one-take) — a single gold line carries the whole film without a cut:
# horizon → Seo Hui's silhouette → waves → the submarine's silhouette → underline of 서희함 →
# the horizon of the sunrise footage. Black and champagne gold, Pretendard light/black contrast.
import json
import math
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

C = json.load(open("shared/assets/contours.json"))
N = 420


def flat(x0, x1, y):
    """a straight line drawn as a thin closed loop, so it can morph into closed silhouettes"""
    half = N // 2
    a = [[round(x0 + (x1 - x0) * i / (half - 1), 1), y] for i in range(half)]
    return a + [[p[0], y + 0.6] for p in reversed(a)]


def wave(y, amp, crests, x0=-40, x1=1120):
    half = N // 2
    a = [[round(x0 + (x1 - x0) * i / (half - 1), 1), round(y + amp * math.sin(i / (half - 1) * crests * 2 * math.pi), 1)] for i in range(half)]
    return a + [[p[0], p[1] + 0.6] for p in reversed(a)]


SHAPES = {"h0": flat(80, 1000, 1000), "seohui": C["seohui"], "wave": wave(1060, 46, 3), "sub": C["sub"],
          "under": flat(290, 790, 770), "h1": flat(-40, 1120, 812)}
# morphs: (start, end, from, to)
MORPHS = [(2.4, 3.9, "h0", "seohui"), (6.0, 7.3, "seohui", "wave"), (8.1, 9.6, "wave", "sub"),
          (HIT + 0.05, HIT + 0.9, "sub", "under"), (15.4, 16.6, "under", "h1")]

css = f'''        #bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 45%, #15130f 0%, #050505 75%);
        }}
        #deep {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 30%, #0f2a45 0%, #04101d 80%);
          opacity: 0;
        }}
        .foot {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
          opacity: 0;
        }}
        #endshade {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0.35) 32%, rgba(0, 0, 0, 0) 50%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.65) 85%);
          opacity: 0;
        }}
        #vig {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 45%, rgba(0, 0, 0, 0) 35%, rgba(0, 0, 0, 0.75) 100%);
        }}
        .fill {{
          position: absolute;
          object-fit: contain;
          opacity: 0;
          filter: grayscale(1) sepia(0.55) saturate(1.3) brightness(0.95) contrast(1.1);
        }}
        #cv {{
          position: absolute;
          left: 0;
          top: 0;
        }}
        .t {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          color: #f3ead8;
          opacity: 0;
          white-space: nowrap;
        }}
        .thin {{
          font-weight: 200;
        }}
        .cap {{
          font-weight: 500;
          letter-spacing: 12px;
          color: #f0cf8a;
        }}
        .gold {{
          background: linear-gradient(180deg, #fff4d6 0%, {GOLD} 50%, #a3711f 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }}
        #flash {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 40%, rgba(255, 238, 200, 1) 0%, rgba(255, 238, 200, 0) 65%);
          opacity: 0;
        }}
        #sign {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1400px;
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 26px;
          opacity: 0;
        }}
        #sign img {{
          height: 100px;
        }}
        #sign div {{
          font-family: "Pretendard", sans-serif;
          font-weight: 300;
          font-size: 50px;
          letter-spacing: 6px;
          color: #ffffff;
        }}
        #sign i {{
          width: 2px;
          height: 76px;
          background: {GOLD};
        }}
'''
body = f'''        <div id="bg"></div>
        <div id="deep"></div>
        <video id="v-side" class="foot" src="assets/sub-side.mp4" data-start="11.2" data-duration="5.6" muted playsinline style="object-position:55% 50%"></video>
        <video id="v-surf" class="foot" src="assets/sub-surface.mp4" data-start="15.6" data-duration="5.4" muted playsinline style="object-position:37% 50%"></video>
        <div id="vig"></div>
        <div id="endshade"></div>
        <img id="fill-seohui" class="fill" src="assets/seohui-cut.png" alt="" style="left:240px;top:560px;width:600px;height:880px" />
        <img id="fill-sub" class="fill" src="assets/sub-cut.png" alt="" style="left:60px;top:820px;width:960px;height:400px" />
        <canvas id="cv" width="1080" height="1920"></canvas>
        <div id="t1" class="t thin" style="top:640px;font-size:210px;color:{GOLD}">993</div>
        <div id="t1b" class="t cap" style="top:880px;font-size:36px">GORYEO · THE KHITAN INVASION</div>
        <div id="t2" class="t thin" style="top:1500px;font-size:84px">칼 대신, <b style="font-weight:900">지혜로</b></div>
        <div id="t2b" class="t cap" style="top:1620px;font-size:32px">고려의 외교관 서희</div>
        <div id="t3" class="t thin" style="top:640px;font-size:92px">그리고 <b style="font-weight:900">천 년</b></div>
        <div id="t4" class="t cap" style="top:1300px;font-size:36px">THE NAME RETURNS TO THE SEA</div>
        <div id="title" class="t gold" style="top:500px;font-size:250px;font-weight:900;letter-spacing:-4px">서희함</div>
        <div id="title-en" class="t cap" style="top:810px;font-size:44px">ROKS SEO HUI</div>
        <div id="d1" class="t thin" style="top:300px;font-size:70px;letter-spacing:8px">2026. 11. 3.</div>
        <div id="d2" class="t" style="top:400px;font-size:96px;font-weight:800">진수를 축하합니다</div>
        <div id="sign"><img src="assets/icheon-logo-dark.png" alt="이천시" /><i></i><div>경기도 이천시</div></div>
        <div id="flash"></div>
'''
js = '''        const cv = document.getElementById("cv"), ctx = cv.getContext("2d");
        const S = __SHAPES__, M = __MORPHS__, N = __N__;
        const clamp = (v) => Math.max(0, Math.min(1, v));
        const io = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
        function shapeAt(t) {
          let cur = S[M[0][2]];
          for (const [a, b, f, g] of M) {
            if (t < a) break;
            if (t >= b) { cur = S[g]; continue; }
            const u = io((t - a) / (b - a)), A = S[f], B = S[g];
            // a soft wave ripples along the line while it travels between shapes
            return A.map((p, i) => [p[0] + (B[i][0] - p[0]) * u + Math.sin(i * 0.09 + t * 6) * 18 * Math.sin(Math.PI * u),
                                    p[1] + (B[i][1] - p[1]) * u + Math.cos(i * 0.07 + t * 5) * 18 * Math.sin(Math.PI * u)]);
          }
          return cur;
        }
        function render(t) {
          ctx.clearRect(0, 0, 1080, 1920);
          const fade = 1 - clamp((t - 16.4) / 1.2);   // the line hands over to the real horizon
          if (fade <= 0) return;
          const P = shapeAt(t);
          const draw = t < 2.4 ? io(clamp((t - 0.3) / 1.9)) : 1;   // first stroke drawn on
          const n = Math.max(2, Math.floor(N / 2 * draw));
          const half = t < 2.4;
          const g = ctx.createLinearGradient(0, 0, 1080, 0);
          g.addColorStop(0, "#9c6c22");
          g.addColorStop(0.5, "#ffe6a8");
          g.addColorStop(1, "#b8862f");
          ctx.lineJoin = "round";
          ctx.lineCap = "round";
          for (const [w, a, blur] of [[10, 0.18, 30], [3.2, 1, 12]]) {
            ctx.globalAlpha = a * fade;
            ctx.shadowColor = "rgba(255,200,110,0.9)";
            ctx.shadowBlur = blur;
            ctx.strokeStyle = g;
            ctx.lineWidth = w;
            ctx.beginPath();
            ctx.moveTo(P[0][0], P[0][1]);
            const end = half ? n : N;
            for (let i = 1; i < end; i++) ctx.lineTo(P[i][0], P[i][1]);
            if (!half) ctx.closePath();
            ctx.stroke();
          }
          // a bright spark riding the line
          const k = half ? n - 1 : Math.floor(((t * 0.35) % 1) * N);
          ctx.globalAlpha = fade;
          ctx.shadowBlur = 28;
          ctx.fillStyle = "#fff6dc";
          ctx.beginPath();
          ctx.arc(P[k][0], P[k][1], 6, 0, Math.PI * 2);
          ctx.fill();
          ctx.globalAlpha = 1;
          ctx.shadowBlur = 0;
        }
        const state = { t: 0 };
        tl.to(state, { t: 21, duration: 21, ease: "none", onUpdate: () => render(state.t) }, 0);
'''.replace("__SHAPES__", json.dumps(SHAPES)).replace("__MORPHS__", json.dumps(MORPHS)).replace("__N__", str(N))


def fade(sel, a, to, dur):
    return f'        tl.to("{sel}", {{ opacity: {to}, duration: {dur}, ease: "power1.inOut" }}, {a});\n'


def rise(sel, a, dur=0.9):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: 26, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: {dur}, ease: "power3.out" }}, {a});\n'


js += rise("#t1", 0.7, 1.2) + rise("#t1b", 1.3) + out("#t1, #t1b", 2.3, 0.5)
js += fade("#fill-seohui", 3.5, 0.9, 0.8) + '        tl.fromTo("#fill-seohui", { scale: 1.04 }, { scale: 1, duration: 2.5, ease: "none" }, 3.5);\n'
js += rise("#t2", 4.1) + rise("#t2b", 4.7) + fade("#fill-seohui", 5.7, 0, 0.5) + out("#t2, #t2b", 5.8, 0.5)
js += fade("#deep", 6.2, 1, 2.0) + rise("#t3", 6.8) + out("#t3", 8.6, 0.5)
js += fade("#fill-sub", 9.2, 0.9, 0.8) + rise("#t4", 9.0, 0.7) + out("#t4", HIT - 0.3, 0.3)
# the hit
js += f'        tl.to("#flash", {{ keyframes: [{{ opacity: 1, duration: 0.06 }}, {{ opacity: 0, duration: 0.9 }}] }}, {HIT - 0.06});\n'
js += f'        tl.fromTo("#title", {{ opacity: 0, scale: 1.25, filter: "blur(18px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.7, ease: "power4.out" }}, {HIT});\n'
js += rise("#title-en", HIT + 0.9, 0.8)
js += f'        tl.to("#fill-sub", {{ y: 160, scale: 1.12, filter: "grayscale(0) sepia(0) saturate(1) brightness(1) contrast(1)", duration: 1.2, ease: "power2.inOut" }}, {HIT + 0.1});\n'
js += fade("#v-side", 11.2, 0.55, 1.2) + fade("#fill-sub", 11.6, 0, 1.0)
js += '        tl.fromTo("#v-side", { scale: 1.12 }, { scale: 1.0, duration: 5.6, ease: "none" }, 11.2);\n'
js += out("#title, #title-en", 15.2, 0.6)
js += fade("#v-surf", 15.6, 1, 1.4) + '        tl.fromTo("#v-surf", { scale: 1.0 }, { scale: 1.08, duration: 5.4, ease: "none" }, 15.6);\n'
js += fade("#endshade", 16.0, 1, 1.2) + rise("#d1", 16.6) + rise("#d2", 17.2, 1.0)
js += '        tl.fromTo("#sign", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, 18.0);\n'
js += out("#d1, #d2, #sign", 20.2, 0.7) + fade("#v-surf", 20.3, 0.0, 0.7)

d = setup("gold")
write(d, {"gold": comp("gold", ["pre"], css, body, js)},
      index("서희함 · 금빛 한 줄", "① one-take gold line short. Silhouettes traced from Magnific cut-outs; footage Seedance; score Lyria 3 Pro cut.", [("gold", 0, DUR)], bg="#050505"))
print("ok")
