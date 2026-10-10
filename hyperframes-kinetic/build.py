# ② Kinetic typography: word groups slam in on the 120 BPM beat; each group flips the palette.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import comp, index
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B0, BEAT = 0.44, 0.5
def b(k): return round(B0 + BEAT * k, 3)
# group: (start beat, end beat, bg, color, [(beat, text, size, top, extra css)])
G = [
    (0, 4, "#111111", "#ffffff", [(0, "이천은", 150, 640, ""), (2, "어떤", 150, 820, ""), (3, "곳일까?", 210, 990, "color:#f2c14e")]),
    (4, 8, "#f2c14e", "#1b1408", [(4, "밥이", 150, 560, ""), (5, "맛있는", 150, 740, ""), (6, "쌀의 도시", 220, 930, "")]),
    (8, 12, "#7fb3a0", "#10261f", [(8, "흙이", 150, 560, ""), (9, "빚은", 150, 740, ""), (10, "도자기의 도시", 180, 930, "color:#ffffff")]),
    (12, 16, "#0d1b3e", "#5fe3f0", [(12, "첨단이", 150, 560, "color:#ffffff"), (13, "달리는", 150, 740, "color:#ffffff"), (14, "반도체의 도시", 180, 930, "text-shadow:-8px 0 #ff2e7e, 8px 0 #5fe3f0;color:#ffffff")]),
    (16, 22, "#ffffff", "#111111", [(16, "그리고", 130, 520, ""), (17, "이 모든 걸", 150, 690, ""), (18, "만드는", 150, 870, ""), (20, "사람들", 250, 1060, "color:#e0483a")]),
    (22, 30, "#111111", "#ffffff", [(22, "이천", 460, 560, ""), (24, "I C H E O N", 90, 1100, "color:#f2c14e;letter-spacing:6px"), (26, "오늘도, 이천에서", 96, 1280, "font-family:'Noto Sans KR';font-weight:800")]),
]
css = '''        .kt-group {
          position: absolute;
          inset: 0;
          opacity: 0;
        }
        .kt-word {
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Black Han Sans", sans-serif;
          line-height: 1;
          opacity: 0;
        }
        #kt-flash {
          position: absolute;
          inset: 0;
          background: #ffffff;
          opacity: 0;
        }
        .kt-bar {
          position: absolute;
          left: 0;
          height: 26px;
          width: 100%;
          transform-origin: left center;
        }
'''
body, js = "", "        const tl = gsap.timeline({ paused: true });\n"
for gi, (s, e, bg, col, words) in enumerate(G):
    body += f'        <div id="kt-g{gi}" class="kt-group" style="background:{bg};color:{col}">\n'
    body += f'          <div class="kt-bar" id="kt-bar{gi}" style="top:{420 if gi % 2 else 1500}px;background:{col};opacity:0.18"></div>\n'
    for wi, (k, txt, size, top, extra) in enumerate(words):
        body += f'          <div id="kt-g{gi}w{wi}" class="kt-word" style="top:{top}px;font-size:{size}px;{extra}">{txt}</div>\n'
    body += "        </div>\n"
    js += f'        tl.set("#kt-g{gi}", {{ opacity: 1 }}, {b(s) if gi else 0});\n'
    if gi < len(G) - 1:
        js += f'        tl.set("#kt-g{gi}", {{ opacity: 0 }}, {b(e)});\n'
        js += f'        tl.to("#kt-flash", {{ keyframes: [{{ opacity: 0.7, duration: 0.03 }}, {{ opacity: 0, duration: 0.12 }}] }}, {b(e)});\n'
    js += f'        tl.fromTo("#kt-g{gi}", {{ scale: 1 }}, {{ scale: 1.07, duration: {round(b(e) - b(s), 3)}, ease: "none" }}, {b(s)});\n'
    js += f'        tl.fromTo("#kt-bar{gi}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {round(b(e) - b(s), 3)}, ease: "none" }}, {b(s)});\n'
    for wi, (k, *_ ) in enumerate(words):
        last = wi == len(words) - 1
        js += f'        tl.fromTo("#kt-g{gi}w{wi}", {{ opacity: 0, scale: {3.2 if last else 2.2}, y: {-40 if wi % 2 else 40} }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "power4.out" }}, {b(k)});\n'
        if last:
            js += f'        tl.to("#kt-g{gi}w{wi}", {{ x: 14, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }}, {round(b(k) + 0.14, 3)});\n'
# outro: split the giant word apart a little and hold
js += f'        tl.to("#kt-g5w0", {{ scale: 1.12, y: -40, duration: 2.0, ease: "power2.out" }}, {b(23)});\n'
js += '        window.__timelines["type"] = tl;\n'
body += '        <div id="kt-flash"></div>\n'
open("compositions/type.html", "w").write(comp("type", ["bhs", "noto"], css, body, js))
open("index.html", "w").write(index("이천 키네틱 타이포", "type", 15, "Kinetic typography test: word groups land on beats of the 120 BPM bed (first beat 0.44 s). Music: Magnific Google Lyria, original track.", "#111"))
