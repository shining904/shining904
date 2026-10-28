# ② 키네틱 타이포 — words slam in on the drum build; at the hit the name 서희함 becomes a window
# onto the submarine footage (knockout text). Pretendard Black throughout.
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

NAVY, RED = "#0b1d3a", "#d4412f"
css = f'''        .g {{
          position: absolute;
          inset: 0;
          opacity: 0;
        }}
        .wd {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          line-height: 1;
          letter-spacing: -4px;
          opacity: 0;
        }}
        .sm {{
          font-weight: 700;
          letter-spacing: 0;
        }}
        .vid {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }}
        .ko {{
          position: absolute;
          inset: 0;
          background: #000;
          mix-blend-mode: multiply;
        }}
        .ko .wd {{
          color: #ffffff;
        }}
        .bar {{
          position: absolute;
          left: 90px;
          right: 90px;
          height: 14px;
          transform-origin: 0 50%;
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
          top: 1330px;
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 30px;
          opacity: 0;
        }}
        #sign img {{
          height: 120px;
        }}
        #sign div {{
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 58px;
          color: #ffffff;
        }}
        #sign i {{
          width: 3px;
          height: 90px;
          background: {GOLD};
        }}
'''
G = [  # id, start, end, background, words [(t, text, size, top, colour, extra)]
    ("g0", 0.0, 2.0, "#000", [(0.25, "993", 360, 660, GOLD, ""), (1.2, "년", 150, 1060, "#ffffff", "")]),
    ("g1", 2.0, 4.0, "#f4efe6", [(2.1, "칼", 520, 520, NAVY, ""), (3.0, "대신", 230, 1120, RED, "")]),
    ("g2", 4.0, 6.0, NAVY, [(4.1, "지혜로", 300, 700, "#ffffff", ""), (4.9, "나라를 지킨", 110, 1060, GOLD, "font-weight:800")]),
]
body, js = "", ""
for gid, s, e, bg, words in G:
    body += f'        <div id="{gid}" class="g" style="background:{bg}">\n'
    body += f'          <div id="{gid}-bar" class="bar" style="top:{1500 if gid != "g1" else 380}px;background:{GOLD}"></div>\n'
    for k, (t, txt, size, top, col, extra) in enumerate(words):
        body += f'          <div id="{gid}w{k}" class="wd" style="top:{top}px;font-size:{size}px;color:{col};{extra}">{txt}</div>\n'
    body += "        </div>\n"
    js += f'        tl.set("#{gid}", {{ opacity: 1 }}, {s});\n        tl.set("#{gid}", {{ opacity: 0 }}, {e});\n'
    js += f'        tl.fromTo("#{gid}", {{ scale: 1 }}, {{ scale: 1.06, duration: {e - s}, ease: "none" }}, {s});\n'
    js += f'        tl.fromTo("#{gid}-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {e - s - 0.2}, ease: "power2.inOut" }}, {s + 0.1});\n'
    for k, (t, *_r) in enumerate(words):
        js += f'        tl.fromTo("#{gid}w{k}", {{ opacity: 0, scale: 2.6 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {t});\n'
        js += f'        tl.to("#{gid}w{k}", {{ x: 12, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }}, {round(t + 0.18, 2)});\n'
    js += f'        tl.to("#flash", {{ keyframes: [{{ opacity: 0.6, duration: 0.03 }}, {{ opacity: 0, duration: 0.14 }}] }}, {e});\n'

# 6-10: "서희" as a window onto the cliff footage, then the build-up words
body += '''        <div id="g3" class="g">
          <video id="v-cliff" class="vid" src="assets/cliff.mp4" data-start="6" data-duration="4.1" muted playsinline></video>
          <div class="ko">
            <div id="g3w0" class="wd" style="top:560px;font-size:420px">서희</div>
          </div>
          <div id="g3w1" class="wd sm" style="top:1080px;font-size:72px;color:#ffffff">고려의 외교관</div>
          <div id="g3w2" class="wd" style="top:1240px;font-size:120px;color:''' + GOLD + '''">그 이름이,</div>
        </div>
'''
js += '        tl.set("#g3", { opacity: 1 }, 6.0);\n        tl.set("#g3", { opacity: 0 }, ' + str(HIT) + ');\n'
js += '        tl.fromTo("#g3w0", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 6.05);\n'
js += '        tl.to("#g3w0", { scale: 1.25, duration: 3.5, ease: "power1.in" }, 6.55);\n'
js += pop("#g3w1", 7.0, 30, 0.4) + pop("#g3w2", 8.6, 30, 0.35)

# hit: 서희함 knockout over the approaching submarine, then 2026.11.3 and the close
body += f'''        <div id="g4" class="g">
          <video id="v-front" class="vid" src="assets/sub-side.mp4" data-start="{HIT}" data-duration="4.0" muted playsinline style="filter:brightness(1.25)"></video>
          <div class="ko">
            <div id="g4w0" class="wd" style="top:600px;font-size:330px;letter-spacing:-10px">서희함</div>
          </div>
          <div id="g4w1" class="wd" style="top:600px;font-size:330px;letter-spacing:-10px;color:transparent;-webkit-text-stroke:3px {GOLD}">서희함</div>
        </div>
        <div id="g5" class="g">
          <video id="v-side" class="vid" src="assets/sub-surface.mp4" data-start="14.05" data-duration="6.95" muted playsinline style="filter:brightness(0.55)"></video>
          <div id="g5w0" class="wd sm" style="top:330px;font-size:84px;color:#ffffff">2026. 11. 3.</div>
          <div id="g5w1" class="wd" style="top:450px;font-size:250px;color:{GOLD}">진수</div>
          <div id="g5w2" class="wd sm" style="top:820px;font-size:92px;color:#ffffff">축하합니다</div>
          <div id="g5w3" class="wd sm" style="top:960px;font-size:46px;color:#d6e6f5;font-weight:500">천 년의 지혜, 바다를 지키다</div>
          <div id="sign"><img src="assets/icheon-logo-dark.png" alt="이천시" /><i></i><div>경기도 이천시</div></div>
        </div>
        <div id="flash"></div>
'''
js += f'        tl.to("#flash", {{ keyframes: [{{ opacity: 1, duration: 0.04 }}, {{ opacity: 0, duration: 0.5 }}] }}, {HIT - 0.04});\n'
js += f'        tl.set("#g4", {{ opacity: 1 }}, {HIT});\n        tl.set("#g4", {{ opacity: 0 }}, 14.05);\n'
js += f'        tl.fromTo("#g4w0, #g4w1", {{ opacity: 1, scale: 1.9 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power4.out" }}, {HIT});\n'
js += '        tl.to("#g4w0, #g4w1", { scale: 1.12, duration: 3.2, ease: "none" }, 10.4);\n'
js += '        tl.to("#g4w0, #g4w1", { scale: 9, duration: 0.45, ease: "power3.in" }, 13.6);\n'
js += '        tl.set("#g5", { opacity: 1 }, 14.05);\n'
js += '        tl.fromTo("#g5w0", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.3, ease: "power4.out" }, 14.2);\n'
js += '        tl.fromTo("#g5w1", { opacity: 0, scale: 2.6 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, 14.6);\n'
js += pop("#g5w2", 15.6, 40, 0.4) + pop("#g5w3", 16.3, 20, 0.6)
js += '        tl.fromTo("#sign", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 17.0);\n'
js += out("#g5w0, #g5w1, #g5w2, #g5w3, #sign", 20.2, 0.7)

d = setup("kinetic")
write(d, {"type": comp("type", ["pre"], css, body, js)},
      index("서희함 · 키네틱 타이포", "② kinetic typography short. Footage: Magnific Seedance; score: Lyria 3 Pro cut.", [("type", 0, DUR)]))
print("ok")
