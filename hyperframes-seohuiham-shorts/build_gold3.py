# ①++ 금빛 한 줄 v3 (37.5 s) — gold2 with a brighter score, the submarine in natural colour
# (no gold tint), a launch-ceremony clip in the finale, and Seo Hui (Icheon's AI ambassador)
# voicing the message: congratulating with the citizens of Icheon and cheering the safe voyage.
# Based on 금빛 한 줄 확장판 — one gold line, no cuts: horizon → the sea of 993 → Seo Hui, Icheon's
# AI ambassador → the submarine → underline of
# 서희함 at the score's hit → the real sunrise horizon, "서희함의 안전한 항해를 응원합니다".
# Adds gold particle bursts at each morph, drifting motes, film grain, a light leak and a slow push-in.
import json
import math
import lib
from lib import GOLD, comp, index, setup, write, out

DUR, HIT = 37.5, 24.1          # score: goldC.mp3 delayed 0.75 s so its hit (23.35 s) lands at 24.1 s
lib.DUR = DUR
C = json.load(open("shared/assets/contours.json"))
N = 420


def flat(x0, x1, y):
    half = N // 2
    a = [[round(x0 + (x1 - x0) * i / (half - 1), 1), y] for i in range(half)]
    return a + [[p[0], y + 0.6] for p in reversed(a)]


def wave(y, amp, crests, x0=-40, x1=1120):
    half = N // 2
    a = [[round(x0 + (x1 - x0) * i / (half - 1), 1), round(y + amp * math.sin(i / (half - 1) * crests * 2 * math.pi), 1)] for i in range(half)]
    return a + [[p[0], p[1] + 0.6] for p in reversed(a)]


SHAPES = {"h0": flat(80, 1000, 1000), "wave": wave(1040, 50, 3), "seohui": [[round(540 + (x - 540) * 0.88, 1), round(500 + (y - 560) * 0.88, 1)] for x, y in C["seohui"]],
          "sub": C["sub"], "under": flat(250, 830, 770), "h1": flat(-40, 1120, 812)}
MORPHS = [(4.6, 6.2, "h0", "wave"), (12.2, 13.7, "wave", "seohui"),
          (17.6, 19.0, "seohui", "sub"), (HIT + 0.05, HIT + 0.9, "sub", "under"), (29.4, 30.6, "under", "h1")]
LINE_OUT = 30.4

css = f'''        #bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 45%, #17140f 0%, #050505 75%);
        }}
        #deep {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 30%, #0f2a45 0%, #04101d 80%);
          opacity: 0;
        }}
        #cam {{
          position: absolute;
          inset: 0;
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
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.72) 0%, rgba(0, 0, 0, 0.4) 34%, rgba(0, 0, 0, 0) 52%, rgba(0, 0, 0, 0) 62%, rgba(0, 0, 0, 0.65) 85%);
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
        #cv, #grain {{
          position: absolute;
          left: 0;
          top: 0;
        }}
        #grain {{
          width: 1080px;
          height: 1920px;
          opacity: 0.09;
          mix-blend-mode: overlay;
        }}
        #leak {{
          position: absolute;
          left: -500px;
          top: -300px;
          width: 1300px;
          height: 1300px;
          border-radius: 50%;
          background: radial-gradient(circle, rgba(255, 170, 80, 0.32) 0%, rgba(255, 120, 40, 0.12) 40%, rgba(0, 0, 0, 0) 70%);
          mix-blend-mode: screen;
          opacity: 0;
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
          letter-spacing: 6px;
          color: #f0cf8a;
        }}
        .gold {{
          background: linear-gradient(105deg, rgba(255, 255, 255, 0) 40%, rgba(255, 252, 238, 0.95) 50%, rgba(255, 255, 255, 0) 60%) 120% 0 / 300% 100% no-repeat,
            linear-gradient(180deg, #fff4d6 0%, {GOLD} 50%, #a3711f 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }}
        #amb {{
          position: absolute;
          left: 0;
          right: 0;
          top: 160px;
          text-align: center;
          opacity: 0;
        }}
        #amb-pill {{
          display: inline-block;
          padding: 14px 44px;
          border: 2px solid {GOLD};
          border-radius: 60px;
          background: rgba(10, 8, 4, 0.55);
          font-family: "Pretendard", sans-serif;
          font-weight: 500;
          font-size: 58px;
          font-weight: 700;
          letter-spacing: 3px;
          color: #ffe6a8;
        }}
        #amb-name {{
          margin-top: 10px;
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          font-size: 170px;
          letter-spacing: -2px;
          color: #f3ead8;
        }}
        .co {{
          position: absolute;
          width: 0;
          height: 0;
        }}
        .co i {{
          position: absolute;
          left: -9px;
          top: -9px;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: #fff6dc;
          box-shadow: 0 0 16px 4px rgba(255, 200, 110, 0.8);
        }}
        .co u {{
          position: absolute;
          left: -1px;
          top: 0;
          width: 2px;
          background: linear-gradient(180deg, #ffe6a8, {GOLD});
          transform-origin: 50% 0;
        }}
        .co div {{
          position: absolute;
          width: 400px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          white-space: nowrap;
        }}
        .co b {{
          display: block;
          font-weight: 800;
          font-size: 56px;
          color: #f3ead8;
        }}
        .co span {{
          font-weight: 500;
          font-size: 34px;
          letter-spacing: 2px;
          color: #f0cf8a;
        }}
        #ai-note {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1462px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 500;
          font-size: 28px;
          color: rgba(255, 255, 255, 0.82);
          text-shadow: 0 1px 6px rgba(0, 0, 0, 0.9);
          white-space: nowrap;
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
          top: 1290px;
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 26px;
          opacity: 0;
        }}
        #sign img {{
          height: 150px;
        }}
'''
body = f'''        <div id="bg"></div>
        <div id="deep"></div>
        <video id="v-side" class="foot" src="assets/sub-side.mp4" data-start="25.0" data-duration="5.6" muted playsinline style="object-position:55% 50%"></video>
        <video id="v-surf" class="foot" src="assets/sub-surface.mp4" data-start="29.4" data-duration="3.2" muted playsinline style="object-position:37% 50%"></video>
        <video id="v-launch-a" class="foot" src="assets/launch.mp4" data-start="31.6" data-media-start="0" data-duration="2.9" muted playsinline></video>
        <video id="v-launch-b" class="foot" src="assets/launch.mp4" data-start="34.3" data-media-start="5.0" data-duration="3.04" muted playsinline></video>
        <div id="vig"></div>
        <div id="endshade"></div>
        <div id="cam">
          <img id="fill-seohui" class="fill" src="assets/seohui-cut.png" alt="" style="left:276px;top:500px;width:528px;height:774px" />
          <img id="fill-sub" class="fill" src="assets/sub-cut.png" alt="" style="left:60px;top:820px;width:960px;height:400px;filter:brightness(0.92) contrast(1.05)" />
          <canvas id="cv" width="1080" height="1920"></canvas>
        </div>
        <div id="leak"></div>
        <canvas id="grain" width="270" height="480"></canvas>
        <div id="t0" class="t thin" style="top:640px;font-size:92px">천 년을 건너온 이름, <b style="font-weight:900">서희</b></div>
        <div id="t1" class="t thin" style="top:520px;font-size:230px;color:{GOLD}">993</div>
        <div id="t1b" class="t cap" style="top:780px;font-size:46px">고려, 거란의 침입</div>
        <div id="t2" class="t thin" style="top:1240px;font-size:80px">칼 대신, <b style="font-weight:900">지혜로</b></div>
        <div id="t2b" class="t" style="top:1350px;font-size:58px;font-weight:300">나라를 지켜낸 서희의 외교 담판</div>
        <div id="amb"><div id="amb-pill">이천시 AI 홍보대사</div><div id="amb-name">서희</div></div>
        <div id="t3" class="t" style="top:1305px;font-size:60px;line-height:1.3;font-weight:300">이천시민들과 함께<br /><b style="font-weight:800">서희함의 진수를 축하합니다</b></div>
        <div id="t4" class="t thin" style="top:420px;font-size:80px">서희의 이름, <b style="font-weight:900">바다로</b></div>
        <div id="co1" class="co" style="left:330px;top:1060px"><i></i><u style="height:230px"></u><div style="left:-210px;top:240px"><b>장보고-Ⅲ 배치-Ⅱ</b><span>2번함</span></div></div>
        <div id="co2" class="co" style="left:800px;top:1040px"><i></i><u style="height:250px"></u><div style="left:-200px;top:260px"><b>3,600톤급</b><span>잠수함</span></div></div>
        <div id="title" class="t" style="top:470px;font-size:260px;font-weight:900;letter-spacing:-4px"><span class="gold">서</span><span class="gold">희</span><span class="gold">함</span></div>
        <div id="d1" class="t thin" style="top:230px;font-size:84px;letter-spacing:8px">2026. 11. 3.</div>
        <div id="d2" class="t" style="top:350px;font-size:116px;font-weight:800;text-shadow:0 3px 18px rgba(0,0,0,0.6)">진수를 축하합니다</div>
        <div id="d3" class="t" style="top:1050px;font-size:80px;line-height:1.28;font-weight:400;text-shadow:0 2px 18px rgba(0,0,0,0.9)"><b style="font-weight:800;color:#ffe6a8">서희함</b>의 안전한 항해를<br /><b style="font-weight:800">응원합니다</b></div>
        <div id="sign"><img src="assets/icheon-logo-dark.png" alt="이천시" /></div>
        <div id="ai-note">이 영상은 AI로 제작되어 실제와 다를 수 있습니다</div>
        <div id="flash"></div>
'''
js = '''        const cv = document.getElementById("cv"), ctx = cv.getContext("2d");
        const gv = document.getElementById("grain"), gx = gv.getContext("2d"), gimg = gx.createImageData(270, 480);
        const S = __SHAPES__, M = __MORPHS__, N = __N__, HIT = __HIT__, OUT = __OUT__;
        const clamp = (v) => Math.max(0, Math.min(1, v));
        const io = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
        const hash = (n) => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
        function shapeAt(t) {
          let cur = S[M[0][2]];
          for (const [a, b, f, g] of M) {
            if (t < a) break;
            if (t >= b) { cur = S[g]; continue; }
            const u = io((t - a) / (b - a)), A = S[f], B = S[g];
            return A.map((p, i) => [p[0] + (B[i][0] - p[0]) * u + Math.sin(i * 0.09 + t * 6) * 22 * Math.sin(Math.PI * u),
                                    p[1] + (B[i][1] - p[1]) * u + Math.cos(i * 0.07 + t * 5) * 22 * Math.sin(Math.PI * u)]);
          }
          return cur;
        }
        // bursts: sparks thrown off the new shape as each morph lands (bigger at the hit)
        const BURSTS = M.map(([a, b, f, g]) => [b, g, b > HIT && b < HIT + 1 ? 2.2 : 1]);
        BURSTS.push([HIT, "sub", 3]);
        function sparks(t) {
          ctx.shadowColor = "rgba(255,200,110,0.9)";
          BURSTS.forEach(([t0, key, power], bi) => {
            const age = t - t0;
            if (age < 0 || age > 1.8) return;
            const P = S[key], count = Math.round(70 * power);
            for (let j = 0; j < count; j++) {
              const r1 = hash(bi * 997 + j), r2 = hash(bi * 131 + j * 7), r3 = hash(bi * 53 + j * 13);
              const p = P[Math.floor(r1 * N)], ang = r2 * Math.PI * 2, sp = (60 + r3 * 260) * Math.sqrt(power);
              const e = 1 - Math.pow(1 - age / 1.8, 3);
              const x = p[0] + Math.cos(ang) * sp * e, y = p[1] + Math.sin(ang) * sp * e + 40 * age * age;
              ctx.globalAlpha = (1 - age / 1.8) * (0.5 + 0.5 * r3);
              ctx.shadowBlur = 14;
              ctx.fillStyle = r1 > 0.7 ? "#fff6dc" : "#f2c675";
              ctx.beginPath();
              ctx.arc(x, y, 1.5 + r2 * 3, 0, Math.PI * 2);
              ctx.fill();
            }
          });
        }
        function motes(t) {
          ctx.shadowBlur = 8;
          for (let j = 0; j < 70; j++) {
            const r1 = hash(j + 0.5), r2 = hash(j * 3.3), r3 = hash(j * 7.7);
            const y = 1920 - (((r2 * 1920 + t * (14 + r3 * 30)) % 2100)) + 90;
            const x = r1 * 1080 + Math.sin(t * 0.4 + j) * 26;
            ctx.globalAlpha = (0.12 + 0.3 * r3) * (0.6 + 0.4 * Math.sin(t * 1.3 + j));
            ctx.fillStyle = "#f2c675";
            ctx.beginPath();
            ctx.arc(x, y, 1 + r3 * 2.2, 0, Math.PI * 2);
            ctx.fill();
          }
        }
        function line(t) {
          const fade = 1 - clamp((t - OUT) / 1.0);
          if (fade <= 0) return;
          const P = shapeAt(t);
          const half = t < 2.6;
          const n = Math.max(2, Math.floor((N / 2) * (half ? io(clamp((t - 0.3) / 2.1)) : 1)));
          const g = ctx.createLinearGradient(0, 0, 1080, 0);
          g.addColorStop(0, "#9c6c22");
          g.addColorStop(0.5, "#ffe6a8");
          g.addColorStop(1, "#b8862f");
          const boost = 1 + 1.5 * Math.exp(-Math.max(0, t - HIT) * 2.5) * (t >= HIT ? 1 : 0);
          ctx.lineJoin = "round";
          ctx.lineCap = "round";
          ctx.shadowColor = "rgba(255,200,110,0.9)";
          for (const [w, al, blur] of [[12, 0.16, 34], [3.4, 1, 12]]) {
            ctx.globalAlpha = al * fade;
            ctx.shadowBlur = blur * boost;
            ctx.strokeStyle = g;
            ctx.lineWidth = w * (w > 4 ? boost : 1);
            ctx.beginPath();
            ctx.moveTo(P[0][0], P[0][1]);
            for (let i = 1; i < (half ? n : N); i++) ctx.lineTo(P[i][0], P[i][1]);
            if (!half) ctx.closePath();
            ctx.stroke();
          }
          ctx.globalAlpha = fade;
          ctx.shadowBlur = 28;
          ctx.fillStyle = "#fff6dc";
          for (const off of half ? [0] : [0, 0.5]) {
            const k = half ? n - 1 : Math.floor(((t * 0.3 + off) % 1) * N);
            ctx.beginPath();
            ctx.arc(P[k][0], P[k][1], 6, 0, Math.PI * 2);
            ctx.fill();
          }
        }
        function grain(t) {
          const f = Math.floor(t * 30), d = gimg.data;
          for (let i = 0; i < 270 * 480; i++) {
            const v = hash(i * 0.013 + f * 17.31) * 255;
            d[i * 4] = d[i * 4 + 1] = d[i * 4 + 2] = v;
            d[i * 4 + 3] = 255;
          }
          gx.putImageData(gimg, 0, 0);
        }
        function shock(t) {
          const age = t - HIT;
          if (age < 0 || age > 1.4) return;
          ctx.shadowColor = "rgba(255,210,130,1)";
          for (const [lag, w] of [[0, 6], [0.12, 2.5]]) {
            const u = clamp((age - lag) / 1.2);
            if (u <= 0) continue;
            ctx.globalAlpha = (1 - u) * 0.9;
            ctx.strokeStyle = "#ffe6a8";
            ctx.lineWidth = w * (1 - u) + 1;
            ctx.shadowBlur = 30;
            ctx.beginPath();
            ctx.ellipse(540, 1000, 60 + u * 900, 30 + u * 420, 0, 0, Math.PI * 2);
            ctx.stroke();
          }
        }
        function render(t) {
          ctx.clearRect(0, 0, 1080, 1920);
          shock(t);
          motes(t);
          line(t);
          sparks(t);
          ctx.globalAlpha = 1;
          ctx.shadowBlur = 0;
          grain(t);
        }
        const state = { t: 0 };
        tl.to(state, { t: __DUR__, duration: __DUR__, ease: "none", onUpdate: () => render(state.t) }, 0);
'''
for k, v in {"__SHAPES__": json.dumps(SHAPES), "__MORPHS__": json.dumps(MORPHS), "__N__": str(N),
             "__HIT__": str(HIT), "__OUT__": str(LINE_OUT), "__DUR__": str(DUR)}.items():
    js = js.replace(k, v)


def fade(sel, a, to, dur):
    return f'        tl.to("{sel}", {{ opacity: {to}, duration: {dur}, ease: "power1.inOut" }}, {a});\n'


def rise(sel, a, dur=0.9):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: 26, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: {dur}, ease: "power3.out" }}, {a});\n'


# slow push-in on the line world, released at the hit
js += '        tl.fromTo("#cam", { scale: 1.0 }, { scale: 1.06, duration: 24.0, ease: "none" }, 0);\n'
js += f'        tl.to("#cam", {{ scale: 1.0, duration: 0.8, ease: "power3.out" }}, {HIT});\n'
js += '        tl.to("#leak", { keyframes: [{ opacity: 1, x: 300, duration: 4 }, { opacity: 0, x: 700, duration: 4 }], ease: "sine.inOut" }, 1.0);\n'
js += '        tl.to("#leak", { keyframes: [{ opacity: 1, x: 500, y: 600, duration: 2.5 }, { opacity: 0, x: 900, y: 800, duration: 3 }], ease: "sine.inOut" }, 13.4);\n'
js += f'        tl.to("#leak", {{ keyframes: [{{ opacity: 1, x: 200, y: 200, duration: 1.0 }}, {{ opacity: 0, x: 600, y: 300, duration: 3 }}], ease: "sine.inOut" }}, {HIT});\n'
# 0–4.6 horizon
js += '        tl.fromTo("#ai-note", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "none" }, 0.3);\n'
js += rise("#t0", 0.6, 1.2) + out("#t0", 4.2, 0.5)
# 4.6–12.2 the sea of 993
js += rise("#t1", 6.6, 1.1) + rise("#t1b", 7.2) + rise("#t2", 8.4) + rise("#t2b", 9.0) + out("#t1, #t1b, #t2, #t2b", 11.8, 0.5)
# 12.2–17.4 Seo Hui, AI ambassador
js += fade("#fill-seohui", 13.4, 0.92, 0.9) + '        tl.fromTo("#fill-seohui", { scale: 1.04 }, { scale: 1, duration: 4.0, ease: "none" }, 13.4);\n'
js += '        tl.fromTo("#amb", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }, 13.8);\n'
js += rise("#t3", 13.8) + fade("#fill-seohui", 17.3, 0, 0.5) + out("#amb, #t3", 17.3, 0.5)
# 17.4–24.1 the submarine
js += fade("#deep", 17.2, 1, 2.0)
js += rise("#t4", 19.4) + fade("#fill-sub", 19.0, 0.9, 1.0)
for k, a in ((1, 20.4), (2, 21.2)):
    js += f'        tl.fromTo("#co{k} i", {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(3)" }}, {a});\n'
    js += f'        tl.fromTo("#co{k} u", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power2.out" }}, {a + 0.2});\n'
    js += f'        tl.fromTo("#co{k} div", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {a + 0.55});\n'
js += '        tl.set(".co i", { scale: 0 }, 0);\n        tl.set(".co u", { scaleY: 0 }, 0);\n'
js += out("#co1, #co2", HIT - 0.4, 0.3)
js += '        tl.fromTo("#fill-sub", { y: 0 }, { y: -18, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 2 }, 19.6);\n'
js += out("#t4", HIT - 0.4, 0.3)
# the hit
js += f'        tl.to("#flash", {{ keyframes: [{{ opacity: 1, duration: 0.06 }}, {{ opacity: 0, duration: 1.0 }}] }}, {HIT - 0.06});\n'
js += f'        tl.fromTo("#title span", {{ opacity: 0, y: 60, scale: 1.3, filter: "blur(16px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power4.out", stagger: 0.12 }}, {HIT});\n'
js += f'        tl.set("#title", {{ opacity: 1 }}, {HIT});\n'
js += f'        tl.fromTo("#title span", {{ backgroundPosition: "120% 0, 0 0" }}, {{ backgroundPosition: "-20% 0, 0 0", duration: 1.4, ease: "power2.inOut", stagger: 0.08, immediateRender: false }}, {HIT + 0.7});\n'
js += f'        tl.fromTo("#title span", {{ backgroundPosition: "120% 0, 0 0" }}, {{ backgroundPosition: "-20% 0, 0 0", duration: 1.4, ease: "power2.inOut", stagger: 0.08, immediateRender: false }}, {HIT + 2.9});\n'
js += f'        tl.to("#fill-sub", {{ y: 160, scale: 1.12, filter: "brightness(1) contrast(1)", duration: 1.2, ease: "power2.inOut" }}, {HIT + 0.1});\n'
js += fade("#v-side", 25.0, 0.55, 1.2) + fade("#fill-sub", 25.4, 0, 1.0)
js += '        tl.fromTo("#v-side", { scale: 1.12 }, { scale: 1.0, duration: 5.6, ease: "none" }, 25.0);\n'
js += out("#title", 29.0, 0.6)
# 29.4– sunrise: date, congratulations, safe voyage, sign
js += fade("#v-surf", 29.4, 1, 1.4) + '        tl.fromTo("#v-surf", { scale: 1.0 }, { scale: 1.08, duration: 8.1, ease: "none" }, 29.4);\n'
js += fade("#v-launch-a", 31.6, 1, 0.9) + '        tl.fromTo("#v-launch-a", { scale: 1.0 }, { scale: 1.04, duration: 2.9, ease: "none" }, 31.6);\n'
js += fade("#v-launch-b", 34.3, 1, 0.5) + '        tl.fromTo("#v-launch-b", { scale: 1.02 }, { scale: 1.06, duration: 3.04, ease: "none" }, 34.3);\n'
js += fade("#endshade", 29.8, 1, 1.2) + rise("#d1", 30.4) + rise("#d2", 31.0, 1.0)
js += rise("#d3", 32.6, 1.1)
js += '        tl.fromTo("#sign", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }, 33.8);\n'
js += out("#d1, #d2, #d3, #sign", 36.5, 0.8) + fade("#v-launch-b", 36.6, 0.0, 0.7)

d = setup("gold3")
html = index("서희함 · 금빛 한 줄 확장판", "①+ extended one-take gold line short. Silhouettes traced from Magnific cut-outs; footage Seedance; score Lyria 3 Pro.",
             [("gold3", 0, DUR)], bg="#050505").replace("assets/music.mp3", "assets/music-gold3-mix.mp3")
write(d, {"gold3": comp("gold3", ["pre"], css, body, js)}, html)
print("ok")
