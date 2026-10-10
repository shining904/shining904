# ⑥ Paper collage: four seasons of Icheon as cut-paper layers; each new season slides up
# with a torn top edge, pieces pop in like stop-motion, then a kraft-paper title card.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import comp, index
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B0, BEAT = 0.45, 0.5217
def b(k): return round(B0 + BEAT * k, 3)
T = [0, b(6), b(12), b(18), b(24), 15]

def torn(seed, amp=22, step=28):
    # polygon for a full-height panel whose top edge is torn
    pts, x, i = [], 0, 0
    while x <= 1080:
        j = ((seed * 131 + i * 977) % 41) / 40.0
        pts.append(f"{x}px {round(amp * j)}px")
        x += step; i += 1
    pts += ["1080px 2000px", "0px 2000px"]
    return "polygon(" + ", ".join(pts) + ")"

def wave_strip(y, h, col, seed, amp=26):
    d = f"M0 {y}"
    for x in range(0, 1081, 60):
        d += f" Q {x + 30} {y - amp * (1 if (x // 60 + seed) % 2 else -0.4)} {x + 60} {y}"
    d += f" L1080 {y + h} L0 {y + h} Z"
    return f'<path class="pp-piece" d="{d}" fill="{col}" filter="url(#pp-shadow)" />'

def circle(cx, cy, r, col, cls=""):
    return f'<circle class="pp-piece {cls}" cx="{cx}" cy="{cy}" r="{r}" fill="{col}" filter="url(#pp-shadow)" />'

DEFS = '''<defs>
  <filter id="pp-shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#3a2a12" flood-opacity="0.35"/></filter>
</defs>'''

seasons = []
# 봄: 산수유 branch with yellow clusters
spring = [wave_strip(1500, 500, "#9cc46a", 1), wave_strip(1620, 400, "#7aa94e", 2),
          '<path class="pp-piece" d="M60 760 C 300 700, 520 820, 760 720 C 860 680, 960 700, 1040 660 L1040 690 C 960 730, 860 712, 762 752 C 520 852, 300 732, 60 792 Z" fill="#7a5233" filter="url(#pp-shadow)"/>',
          '<path class="pp-piece" d="M380 770 C 420 880, 500 960, 600 1020 L590 1040 C 490 980, 400 900, 360 780 Z" fill="#7a5233" filter="url(#pp-shadow)"/>']
for k, (x, y) in enumerate([(160, 720), (300, 700), (460, 770), (620, 740), (800, 700), (940, 680), (520, 960), (430, 880), (700, 760)]):
    for m in range(5):
        a = m * 1.256 + k
        spring.append(circle(round(x + math.cos(a) * 26), round(y + math.sin(a) * 26), 20, "#ffd23f" if m % 2 else "#f2b705"))
seasons.append(("#f6edc6", spring, "봄", "노란 산수유 마을", "#a87400"))
# 여름: sun, clouds, layered paddies
summer = [circle(820, 520, 120, "#ffb347"),
          '<path class="pp-piece" d="M120 640 a70 70 0 0 1 120 -40 a90 90 0 0 1 170 20 a60 60 0 0 1 40 100 H130 a55 55 0 0 1 -10 -80 Z" fill="#ffffff" filter="url(#pp-shadow)"/>',
          '<path class="pp-piece" d="M600 780 a60 60 0 0 1 100 -30 a80 80 0 0 1 150 20 a50 50 0 0 1 30 80 H610 a45 45 0 0 1 -10 -70 Z" fill="#ffffff" filter="url(#pp-shadow)"/>',
          wave_strip(1050, 900, "#8fd07a", 0, 30), wave_strip(1250, 700, "#5fb35a", 1, 30), wave_strip(1450, 500, "#3f9a4a", 0, 30), wave_strip(1650, 300, "#2f7f3c", 1, 30)]
seasons.append(("#bfe6ef", summer, "여름", "초록 물결 논", "#2f7f3c"))
# 가을: golden field, vase, red leaves
autumn = [wave_strip(1300, 700, "#e2a93b", 0, 24), wave_strip(1480, 500, "#c98a24", 1, 24),
          '<path class="pp-piece" d="M540 760 C 500 760, 500 790, 520 800 C 400 860, 380 1000, 430 1120 C 470 1220, 490 1280, 470 1320 L610 1320 C 590 1280, 610 1220, 650 1120 C 700 1000, 680 860, 560 800 C 580 790, 580 760, 540 760 Z" fill="#7fb3a0" filter="url(#pp-shadow)"/>',
          '<path class="pp-piece" d="M470 960 C 520 930, 560 990, 610 950" fill="none" stroke="#f4efe2" stroke-width="10" stroke-linecap="round"/>']
for k in range(12):
    x, y = 120 + (k * 173) % 860, 520 + (k * 97) % 380
    autumn.append(f'<path class="pp-piece pp-leaf" d="M{x} {y} q 30 -40 60 0 q -30 40 -60 0 Z" fill="{["#d9482b", "#e9772a", "#b8322a"][k % 3]}" filter="url(#pp-shadow)" transform="rotate({(k * 37) % 90 - 45} {x + 30} {y})"/>')
seasons.append(("#f6d8a8", autumn, "가을", "황금 들판과 도자기", "#b8322a"))
# 겨울: snowy mountains, falling snow
winter = ['<path class="pp-piece" d="M-40 1500 L300 860 L520 1180 L700 900 L1120 1500 Z" fill="#9fb3c8" filter="url(#pp-shadow)"/>',
          '<path class="pp-piece" d="M300 860 L380 1010 L340 990 L300 1040 L260 990 L220 1010 Z" fill="#ffffff"/>',
          '<path class="pp-piece" d="M700 900 L790 1040 L740 1020 L700 1070 L660 1020 L610 1040 Z" fill="#ffffff"/>',
          wave_strip(1450, 600, "#ffffff", 0, 30), wave_strip(1620, 400, "#e8eef5", 1, 30)]
for k in range(26):
    winter.append(circle(60 + (k * 211) % 980, 420 + (k * 137) % 900, 10 + k % 3 * 4, "#ffffff", "pp-snow"))
seasons.append(("#d9e4ef", winter, "겨울", "하얀 설봉산", "#36506e"))

css = '''        #root { background: #e9dcc2; font-family: "Noto Sans KR", sans-serif; }
        .pp-panel { position: absolute; left: 0; top: 0; width: 1080px; height: 1990px; }
        .pp-panel svg { position: absolute; left: 0; top: 0; }
        .pp-label { position: absolute; left: 90px; top: 210px; padding: 26px 46px 30px; background: #fffdf6;
          box-shadow: 0 10px 22px rgba(58, 42, 18, 0.3); transform: rotate(-3deg); }
        .pp-label b { display: block; font-family: "Black Han Sans", sans-serif; font-weight: 400; font-size: 150px; line-height: 1; }
        .pp-label span { display: block; margin-top: 10px; font-size: 52px; font-weight: 800; color: #3b3326; }
        .pp-tape { position: absolute; width: 170px; height: 50px; background: rgba(255, 240, 190, 0.85); }
        #pp-end { position: absolute; inset: 0; background: #c9a77a; }
        #pp-end-card { position: absolute; left: 110px; right: 110px; top: 620px; padding: 70px 40px 80px; background: #fffdf6;
          box-shadow: 0 18px 40px rgba(58, 42, 18, 0.35); text-align: center; transform: rotate(2deg); }
        #pp-end-card b { display: block; font-family: "Black Han Sans", sans-serif; font-weight: 400; font-size: 120px; line-height: 1.15; color: #3b3326; }
        #pp-end-card span { display: block; margin-top: 24px; font-size: 46px; font-weight: 800; color: #b8322a; letter-spacing: 4px; }
        .pp-dot { position: absolute; width: 120px; height: 120px; border-radius: 50%; }
        #pp-grain { position: absolute; inset: 0; pointer-events: none; opacity: 0.35; mix-blend-mode: multiply; }
'''
body = ""
for i, (bg, pieces, s1, s2, col) in enumerate(seasons):
    clip = "" if i == 0 else f"clip-path:{torn(i)};"
    body += f'''        <div class="pp-panel" id="pp-s{i}" style="background:{bg};{clip}">
          <svg width="1080" height="1990" viewBox="0 0 1080 1990">{DEFS}{"".join(pieces)}</svg>
          <div class="pp-label" id="pp-label{i}"><b style="color:{col}">{s1}</b><span>{s2}</span>
            <div class="pp-tape" style="left:-40px;top:-20px;transform:rotate(-20deg)"></div><div class="pp-tape" style="right:-40px;top:-16px;transform:rotate(18deg)"></div></div>
        </div>
'''
body += f'''        <div id="pp-end" style="clip-path:{torn(9, 30, 36)}">
          <div class="pp-dot" style="left:120px;top:300px;background:#f2b705"></div>
          <div class="pp-dot" style="left:840px;top:340px;background:#3f9a4a"></div>
          <div class="pp-dot" style="left:150px;top:1450px;background:#d9482b"></div>
          <div class="pp-dot" style="left:820px;top:1480px;background:#9fb3c8"></div>
          <div id="pp-end-card"><b>사계절이<br />아름다운 이천</b><span>ICHEON · FOUR SEASONS</span>
            <div class="pp-tape" style="left:40px;top:-24px;transform:rotate(-12deg)"></div><div class="pp-tape" style="right:40px;top:-24px;transform:rotate(10deg)"></div></div>
        </div>
        <svg id="pp-grain" width="1080" height="1920"><filter id="pp-noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.55 0"/></filter><rect width="1080" height="1920" filter="url(#pp-noise)"/></svg>
'''
js = "        const tl = gsap.timeline({ paused: true });\n"
for i in range(4):
    a = T[i]
    if i:
        js += f'        tl.fromTo("#pp-s{i}", {{ y: 1990 }}, {{ y: -40, duration: 0.55, ease: "power3.out" }}, {round(a - 0.3, 3)});\n'
        js += f'        tl.set("#pp-s{i - 1}", {{ opacity: 0 }}, {round(a + 0.3, 3)});\n'
    else:
        js += '        tl.set("#pp-s0", { y: -40 }, 0);\n'
    js += f'        tl.fromTo("#pp-s{i} .pp-piece", {{ scale: 0, transformOrigin: "50% 50%", transformBox: "fill-box" }}, {{ scale: 1, duration: 0.22, ease: "back.out(2.2)", stagger: {0.012 if i == 0 else 0.05} }}, {round(a + 0.2, 3)});\n'
    js += f'        tl.fromTo("#pp-label{i}", {{ opacity: 0, scale: 1.6, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.25, ease: "power4.out" }}, {round(a + 0.5, 3)});\n'
    # stop-motion jitter on the whole layer
    js += f'        tl.to("#pp-s{i} svg", {{ rotation: 0.6, y: 4, duration: {BEAT / 2:.3f}, ease: "steps(1)", yoyo: true, repeat: 9, transformOrigin: "50% 50%" }}, {round(a + 0.6, 3)});\n'
js += f'        tl.fromTo(".pp-leaf", {{ y: -60 }}, {{ y: 80, duration: 3, ease: "none", stagger: 0.05 }}, {T[2]});\n'
js += f'        tl.fromTo(".pp-snow", {{ y: -100 }}, {{ y: 220, duration: 3, ease: "none", stagger: 0.03 }}, {T[3]});\n'
js += f'        tl.fromTo("#pp-end", {{ y: 1990 }}, {{ y: 0, duration: 0.55, ease: "power3.out" }}, {round(T[4] - 0.3, 3)});\n'
js += f'        tl.set("#pp-s3", {{ opacity: 0 }}, {round(T[4] + 0.3, 3)});\n'
js += f'        tl.fromTo(".pp-dot", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2.5)", stagger: 0.12 }}, {round(T[4] + 0.2, 3)});\n'
js += f'        tl.fromTo("#pp-end-card", {{ opacity: 0, scale: 1.5, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: 2, duration: 0.3, ease: "power4.out" }}, {round(T[4] + 0.4, 3)});\n'
js += '        window.__timelines["paper"] = tl;\n'
open("compositions/paper.html", "w").write(comp("paper", ["bhs", "noto"], css, body, js))
open("index.html", "w").write(index("이천의 사계 종이 콜라주", "paper", 15, "Paper-collage test: cut-paper seasons slide up with torn edges on beats of the 115 BPM bed. Music: Magnific Google Lyria, original track.", "#e9dcc2"))
