# ⑥ 종이 콜라주 — torn-paper sea and sky, Seo Hui and the submarine as cut-out stickers,
# masking-tape labels; at the hit a torn banner 서희함 stamps down and paper confetti falls.
# Lettering: Do Hyeon (titles), Jua (labels).
import random
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

rnd = random.Random(7)


def torn(top_jag=True, bottom_jag=False, n=28, amp=2.2):
    """clip-path polygon (percent) with a ragged torn edge"""
    pts = []
    for i in range(n + 1):
        x = i * 100 / n
        pts.append(f"{x:.1f}% {rnd.uniform(0, amp) if top_jag else 0:.1f}%")
    for i in range(n, -1, -1):
        x = i * 100 / n
        pts.append(f"{x:.1f}% {100 - rnd.uniform(0, amp) if bottom_jag else 100:.1f}%")
    return "polygon(" + ", ".join(pts) + ")"


def wave_path(n=5, amp=3.2):
    """rolling paper wave: n crests, slightly uneven like hand-cut paper"""
    import math
    pts, ph = [], rnd.uniform(0, 6.28)
    for i in range(121):
        x = i * 100 / 120
        y = amp + amp * math.sin(ph + x / 100 * n * 2 * math.pi) + rnd.uniform(-0.25, 0.25)
        pts.append(f"{x:.2f}% {y:.2f}%")
    return "polygon(" + ", ".join(pts) + ", 100% 100%, 0% 100%)"


STICKER = ("drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 5px 0 #fff) "
           "drop-shadow(0 -5px 0 #fff) drop-shadow(0 14px 18px rgba(0,0,0,0.35))")
WAVES = [("w1", "#2f6f9a", 1180), ("w2", "#1f4f78", 1330), ("w3", "#123553", 1500)]
CONF = ["#e94f37", "#f6c344", "#3aa0a8", "#ffffff", "#e8a0b4"]
css = f'''        #sky {{
          position: absolute;
          inset: 0;
          background: #f3e7cf;
        }}
        #fibre {{
          position: absolute;
          inset: 0;
          background-image: radial-gradient(rgba(120, 90, 50, 0.08) 1px, transparent 1.4px);
          background-size: 9px 9px;
        }}
        #sun {{
          position: absolute;
          left: 640px;
          top: 300px;
          width: 300px;
          height: 300px;
          border-radius: 50%;
          background: #f4a640;
          filter: drop-shadow(0 10px 14px rgba(120, 70, 20, 0.3));
          clip-path: {torn(True, True, 40, 3)};
        }}
        .wave {{
          position: absolute;
          left: -60px;
          width: 1200px;
          height: 900px;
          filter: drop-shadow(0 -8px 10px rgba(0, 0, 0, 0.25));
        }}
        .paper {{
          position: absolute;
          padding: 18px 40px 22px;
          background: #fffaf0;
          box-shadow: 0 10px 18px rgba(0, 0, 0, 0.25);
          font-family: "Do Hyeon", sans-serif;
          color: #1d2b3a;
          white-space: nowrap;
        }}
        .tape {{
          position: absolute;
          width: 150px;
          height: 46px;
          background: rgba(246, 195, 68, 0.75);
          top: -22px;
          left: 50%;
          margin-left: -75px;
          transform: rotate(-4deg);
        }}
        .lab {{
          font-family: "Jua", sans-serif;
        }}
        #seohui {{
          position: absolute;
          left: 80px;
          top: 420px;
          height: 800px;
          filter: {STICKER};
        }}
        #sub {{
          position: absolute;
          left: 120px;
          top: 1180px;
          width: 1000px;
          filter: {STICKER};
        }}
        .cf {{
          position: absolute;
          width: 34px;
          height: 22px;
        }}
        #sign {{
          position: absolute;
          left: 50%;
          top: 1390px;
          margin-left: -330px;
          width: 660px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 24px;
          padding: 22px 0;
          background: #fffaf0;
          box-shadow: 0 10px 18px rgba(0, 0, 0, 0.3);
          opacity: 0;
        }}
        #sign img {{
          height: 110px;
        }}
        #sign div {{
          font-family: "Do Hyeon", sans-serif;
          font-size: 62px;
          color: #1d2b3a;
        }}
'''
body = '''        <div id="sky"></div>
        <div id="fibre"></div>
        <div id="sun"></div>
        <img id="seohui" src="assets/seohui-cut.png" alt="" />
'''
body += "".join(f'        <div id="{w}" class="wave" style="top:{top}px;background:{c};clip-path:{wave_path()}"></div>\n'
                for w, c, top in WAVES[:1])
body += '        <img id="sub" src="assets/sub-cut.png" alt="" />\n'
body += "".join(f'        <div id="{w}" class="wave" style="top:{top}px;background:{c};clip-path:{wave_path()}"></div>\n'
                for w, c, top in WAVES[1:])
body += f'''        <div id="t993" class="paper" style="left:90px;top:200px;font-size:150px;transform:rotate(-3deg)"><i class="tape"></i>993년</div>
        <div id="tname" class="paper lab" style="left:580px;top:560px;font-size:62px;transform:rotate(4deg)"><i class="tape"></i>고려의 외교관<br /><span style="font-family:'Do Hyeon';font-size:120px;color:#b5371f">서희</span></div>
        <div id="tsay" class="paper lab" style="left:560px;top:900px;font-size:66px;background:#1d2b3a;color:#fffaf0;transform:rotate(-5deg)">“칼 대신 말로!”</div>
        <div id="tlater" class="paper lab" style="left:120px;top:240px;font-size:96px;transform:rotate(2deg)"><i class="tape"></i>1,000년 뒤</div>
        <div id="tban" class="paper" style="left:70px;right:70px;top:240px;text-align:center;font-size:250px;color:#b5371f;clip-path:{torn(True, True, 30, 3)};transform:rotate(-2deg)">서희함</div>
        <div id="tcon" class="paper lab" style="left:150px;top:600px;font-size:88px;background:{GOLD};transform:rotate(2deg)"><i class="tape"></i>진수를 축하합니다!</div>
        <div id="tdate" class="paper lab" style="left:640px;top:780px;font-size:54px;transform:rotate(-4deg)">2026. 11. 3.</div>
        <div id="sign"><img src="assets/icheon-logo.png" alt="이천시" /><div>경기도 이천시</div></div>
'''
for k in range(46):
    x, y0, rot = rnd.uniform(20, 1040), rnd.uniform(-600, -40), rnd.uniform(0, 360)
    body += f'        <div id="cf{k}" class="cf" style="left:{x:.0f}px;top:{y0:.0f}px;background:{CONF[k % len(CONF)]};transform:rotate({rot:.0f}deg)"></div>\n'

js = '        tl.fromTo("#sky, #fibre", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "none" }, 0);\n'
js += "".join(f'        tl.fromTo("#{w}", {{ y: 700 }}, {{ y: 0, duration: 0.8, ease: "back.out(1.4)" }}, {0.2 + i * 0.15});\n'
              f'        tl.to("#{w}", {{ x: {(-1) ** i * 30}, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: 8 }}, {1.0 + i * 0.15});\n'
              for i, (w, _, _) in enumerate(WAVES))
js += '        tl.fromTo("#sun", { y: 500, rotation: -20 }, { y: 0, rotation: 0, duration: 1.2, ease: "power3.out" }, 0.3);\n'
js += '        tl.fromTo("#t993", { opacity: 0, scale: 1.6, rotation: -12 }, { opacity: 1, scale: 1, rotation: -3, duration: 0.35, ease: "back.out(2)" }, 0.6);\n'
js += '        tl.fromTo("#seohui", { y: 900, rotation: -8 }, { y: 0, rotation: -2, duration: 0.8, ease: "back.out(1.6)" }, 1.8);\n'
js += '        tl.fromTo("#tname", { opacity: 0, scale: 0.4, rotation: 20 }, { opacity: 1, scale: 1, rotation: 4, duration: 0.4, ease: "back.out(2)" }, 2.6);\n'
js += '        tl.fromTo("#tsay", { opacity: 0, x: 200 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(2)" }, 3.6);\n'
js += '        tl.to("#seohui", { y: -10, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, 2.6);\n'
js += '        tl.to("#seohui, #tname, #tsay, #t993", { x: -1100, rotation: -15, duration: 0.6, ease: "power3.in" }, 6.0);\n'
js += '        tl.fromTo("#tlater", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 6.7);\n'
js += '        tl.fromTo("#sub", { x: 1200 }, { x: 0, duration: 1.4, ease: "power3.out" }, 7.2);\n'
js += '        tl.to("#sub", { y: -26, rotation: -1.5, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: 9 }, 8.6);\n'
js += out("#tlater", HIT - 0.2, 0.2)
js += '        tl.set("#t993, #tname, #tsay, #tlater, #tban, #tcon, #tdate, #sign", { opacity: 0 }, 0);\n'
js += f'        tl.fromTo("#tban", {{ opacity: 0, scale: 2.2, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -2, duration: 0.3, ease: "power4.in" }}, {HIT - 0.25});\n'
js += f'        tl.to("#sub", {{ y: -260, duration: 1.0, ease: "back.out(1.6)" }}, {HIT + 0.1});\n'
js += f'        tl.fromTo("#tcon", {{ opacity: 0, x: -300, rotation: -10 }}, {{ opacity: 1, x: 0, rotation: 2, duration: 0.5, ease: "back.out(2)" }}, {HIT + 1.0});\n'
js += f'        tl.fromTo("#tdate", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }}, {HIT + 1.8});\n'
js += f'        tl.fromTo("#sign", {{ opacity: 0, y: 200, rotation: 6 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.7, ease: "back.out(1.6)" }}, {HIT + 3.6});\n'
for k in range(46):
    js += (f'        tl.to("#cf{k}", {{ y: {rnd.uniform(1900, 2600):.0f}, x: {rnd.uniform(-160, 160):.0f}, rotation: {rnd.uniform(360, 1080):.0f}, '
           f'duration: {rnd.uniform(2.6, 4.2):.2f}, ease: "power1.in" }}, {HIT + rnd.uniform(0, 0.9):.2f});\n')
js += out("#tban, #tcon, #tdate, #sign, #sub", 20.2, 0.7)

d = setup("paper")
write(d, {"paper": comp("paper", ["dohyeon", "jua"], css, body, js)},
      index("서희함 · 종이 콜라주", "⑥ paper collage short. Cut-outs: Magnific background removal; score: Lyria 3 Pro cut.", [("paper", 0, DUR)], bg="#f3e7cf"))
print("ok")
