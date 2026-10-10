# ④ Map trip: an illustrated (not to scale) Icheon map; the camera flies stop to stop
# while a marker drives the dashed route and a card names each place.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import comp, index
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B0, BEAT = 0.28, 0.5714
def b(k): return round(B0 + BEAT * k, 3)
T = [0, b(3), b(8), b(12), b(17), b(21), 15]
# approximate relative positions (map space 1080 x 1920)
STOPS = [
    ("예스파크", "이천도자예술마을", "공방 골목에서 도자기 구경", 520, 640, "#c0563b"),
    ("설봉공원", "설봉산 아래 호수공원", "단풍 따라 호숫가 산책", 455, 905, "#d98a1c"),
    ("복하천 수변공원", "10.14~10.18 이천쌀문화축제", "가마솥밥 한 그릇", 640, 1060, "#2f7fb5"),
    ("덕평공룡수목원", "마장면", "공룡과 숲길 가족 나들이", 250, 1250, "#3f8a4a"),
]
LEGS = [
    "M520 640 C 560 720, 430 800, 455 905",
    "M455 905 C 480 980, 600 980, 640 1060",
    "M640 1060 C 560 1180, 380 1150, 250 1250",
]
css = '''        #root { background: #e9e2d0; font-family: "Noto Sans KR", sans-serif; }
        #map-cam { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
        #map-svg { position: absolute; left: 0; top: 0; }
        .map-pin { position: absolute; width: 64px; height: 64px; margin: -64px 0 0 -32px; }
        .map-pin svg { width: 64px; height: 64px; }
        .map-plabel { position: absolute; transform: translate(-50%, -128px); padding: 6px 16px; border-radius: 999px; background: #ffffff; font-size: 26px; font-weight: 800; color: #2b2b2b; white-space: nowrap; box-shadow: 0 6px 14px rgba(0,0,0,0.15); opacity: 0; }
        #map-car { position: absolute; width: 54px; height: 54px; margin: -27px 0 0 -27px; border-radius: 50%; background: #e0483a; border: 6px solid #ffffff; box-shadow: 0 8px 18px rgba(0,0,0,0.3); }
        #map-title { position: absolute; left: 0; right: 0; top: 220px; text-align: center; }
        #map-title b { display: block; font-family: "Black Han Sans", sans-serif; font-weight: 400; font-size: 120px; color: #23324f; line-height: 1.1; }
        #map-title span { font-size: 44px; font-weight: 800; color: #c0563b; letter-spacing: 4px; }
        .map-card { position: absolute; left: 70px; right: 70px; top: 1420px; padding: 34px 40px; border-radius: 34px; background: #ffffff; box-shadow: 0 24px 50px rgba(35, 50, 79, 0.25); opacity: 0; }
        .map-card .no { display: inline-block; padding: 6px 22px; border-radius: 999px; color: #ffffff; font-size: 30px; font-weight: 800; }
        .map-card .name { margin-top: 12px; font-family: "Black Han Sans", sans-serif; font-size: 88px; line-height: 1.05; color: #23324f; }
        .map-card .sub { margin-top: 8px; font-size: 38px; font-weight: 800; color: #5b5b5b; }
        .map-card .desc { margin-top: 6px; font-size: 40px; font-weight: 800; color: #23324f; }
        #map-end { position: absolute; left: 0; right: 0; top: 1500px; text-align: center; opacity: 0; }
        #map-end b { display: block; font-family: "Black Han Sans", sans-serif; font-weight: 400; font-size: 100px; color: #23324f; }
        #map-note { position: absolute; left: 0; right: 0; top: 1800px; text-align: center; font-size: 26px; font-weight: 500; color: #6d6656; opacity: 0; }
'''
trees = ""
import math
for i in range(70):
    x = 140 + (i * 137) % 800
    y = 520 + (i * 211) % 900
    if any(abs(x - sx) < 60 and abs(y - sy) < 60 for _, _, _, sx, sy, _ in STOPS):
        continue
    col = ["#d9822b", "#c4512d", "#e6b33a", "#8f6b2f"][i % 4]
    trees += f'<circle cx="{x}" cy="{y}" r="{12 + (i * 7) % 10}" fill="{col}" opacity="0.85" />'
svg = f'''          <svg id="map-svg" width="1080" height="1920" viewBox="0 0 1080 1920">
            <path id="map-land" d="M170 470 C 320 380, 600 420, 760 470 C 900 520, 960 660, 930 820 C 990 980, 950 1150, 860 1260 C 780 1400, 600 1450, 430 1420 C 280 1400, 140 1340, 120 1200 C 90 1040, 130 900, 110 760 C 100 620, 110 530, 170 470 Z" fill="#f6efdc" stroke="#9c8f6e" stroke-width="6" stroke-dasharray="3000" stroke-dashoffset="3000" />
            <path id="map-river" d="M930 860 C 820 900, 760 1000, 660 1040 C 560 1080, 470 1100, 380 1180 C 300 1240, 200 1260, 120 1300" fill="none" stroke="#7fb7d9" stroke-width="22" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200" />
            <text x="780" y="960" font-size="26" font-weight="800" fill="#1f5577" font-family="Noto Sans KR">복하천</text>
            <g id="map-mtn" fill="#a7b38a" stroke="#6f7d55" stroke-width="4">
              <path d="M330 860 L390 760 L450 860 Z" /><path d="M380 860 L430 790 L480 860 Z" />
              <path d="M700 620 L750 540 L800 620 Z" /><path d="M200 1000 L250 930 L300 1000 Z" />
            </g>
            <text x="300" y="900" font-size="24" font-weight="800" fill="#5d6a45" font-family="Noto Sans KR">설봉산</text>
            <g id="map-trees">{trees}</g>
            {''.join(f'<path class="map-leg" id="map-leg{i}" d="{d}" fill="none" stroke="#e0483a" stroke-width="10" stroke-linecap="round" stroke-dasharray="1 0" />' for i, d in enumerate(LEGS))}
          </svg>
'''
pins = "".join(f'''          <div class="map-pin" id="map-pin{i}" style="left:{x}px;top:{y}px"><svg viewBox="0 0 64 64"><path d="M32 62 C 32 62, 8 36, 8 22 A 24 24 0 0 1 56 22 C 56 36, 32 62, 32 62 Z" fill="{c}" stroke="#ffffff" stroke-width="4"/><circle cx="32" cy="22" r="9" fill="#ffffff"/></svg></div>
          <div class="map-plabel" id="map-plabel{i}" style="left:{x}px;top:{y}px">{n}</div>
''' for i, (n, s, d, x, y, c) in enumerate(STOPS))
cards = "".join(f'''        <div class="map-card" id="map-card{i}"><span class="no" style="background:{c}">{i + 1}번째 코스</span><div class="name">{n}</div><div class="sub">{s}</div><div class="desc">{d}</div></div>
''' for i, (n, s, d, x, y, c) in enumerate(STOPS))
body = f'''        <div id="map-cam">
{svg}{pins}          <div id="map-car" style="left:{STOPS[0][3]}px;top:{STOPS[0][4]}px"></div>
        </div>
        <div id="map-title"><b>이천 가을<br />여행 코스</b><span>ICHEON AUTUMN TRIP</span></div>
{cards}        <div id="map-end"><b>하루 코스로 딱!</b></div>
        <div id="map-note">※ 실제 축척과 다른 약도입니다</div>
'''
def cam(px, py, s):
    return f"x: {round(540 - px * s, 1)}, y: {round(820 - py * s, 1)}, scale: {s}"
js = "        const tl = gsap.timeline({ paused: true });\n"
js += '''        const legs = [0, 1, 2].map((i) => document.getElementById("map-leg" + i));
        const lens = legs.map((p) => p.getTotalLength());
        legs.forEach((p, i) => { p.style.strokeDasharray = "18 14"; });
        const car = document.getElementById("map-car");
        // reveal each leg with a mask-like dash: draw progress via dashoffset on a solid copy is heavy, so clip with stroke-dasharray on the dashed path
        function placeCar(i, u) {
          const pt = legs[i].getPointAtLength(lens[i] * u);
          car.style.left = pt.x + "px";
          car.style.top = pt.y + "px";
        }
        const legState = [0, 1, 2].map(() => ({ u: 0 }));
        function drawLeg(i) {
          const u = legState[i].u, L = lens[i];
          legs[i].style.strokeDasharray = u >= 1 ? "18 14" : `${L * u} ${L}`;
          if (u > 0) placeCar(i, u);
        }
'''
js += f'        tl.to("#map-land", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 1.4, ease: "power2.inOut" }}, 0.1);\n'
js += f'        tl.to("#map-river", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 1.2, ease: "power2.out" }}, 0.6);\n'
js += f'        tl.fromTo("#map-mtn path, #map-trees circle", {{ scale: 0, transformOrigin: "50% 100%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.012 }}, 0.5);\n'
js += f'        tl.fromTo("#map-title", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 0.15);\n'
js += f'        tl.to("#map-title", {{ opacity: 0, y: -60, duration: 0.3 }}, {round(T[1] - 0.2, 3)});\n'
js += f'        tl.fromTo(".map-pin", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "bounce.out", stagger: 0.12 }}, 1.0);\n'
js += f'        tl.to(".map-plabel", {{ opacity: 1, duration: 0.3 }}, {round(T[5] + 0.8, 3)});\n'
js += f'        tl.fromTo("#map-car", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)" }}, {T[1]});\n'
js += f'        tl.fromTo("#map-cam", {{ x: 0, y: 0, scale: 1 }}, {{ {cam(STOPS[0][3], STOPS[0][4], 1.9)}, duration: 0.9, ease: "power2.inOut" }}, {round(T[1] - 0.3, 3)});\n'
for i in range(4):
    a, e = T[i + 1], T[i + 2]
    if i > 0:
        js += f'        tl.to(legState[{i - 1}], {{ u: 1, duration: 1.0, ease: "power1.inOut", onUpdate: () => drawLeg({i - 1}) }}, {a});\n'
        js += f'        tl.to("#map-cam", {{ {cam(STOPS[i][3], STOPS[i][4], 1.9)}, duration: 1.0, ease: "power1.inOut" }}, {a});\n'
    js += f'        tl.fromTo("#map-card{i}", {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {round(a + (0.9 if i else 0.4), 3)});\n'
    js += f'        tl.to("#map-pin{i}", {{ scale: 1.5, duration: 0.25, yoyo: true, repeat: 1, transformOrigin: "50% 100%" }}, {round(a + (0.9 if i else 0.4), 3)});\n'
    js += f'        tl.to("#map-card{i}", {{ opacity: 0, y: 60, duration: 0.25 }}, {round(e - 0.25, 3)});\n'
js += f'        tl.to("#map-cam", {{ x: 0, y: -60, scale: 1, duration: 1.0, ease: "power2.inOut" }}, {T[5]});\n'
js += f'        tl.fromTo("#map-end", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {round(T[5] + 0.9, 3)});\n'
js += f'        tl.fromTo("#map-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {round(T[5] + 1.2, 3)});\n'
js += '        legState.forEach((s, i) => drawLeg(i));\n'
js += '        window.__timelines["map"] = tl;\n'
open("compositions/map.html", "w").write(comp("map", ["bhs", "noto"], css, body, js))
open("index.html", "w").write(index("이천 가을 여행 지도", "map", 15, "Map trip test: illustrated, not-to-scale map; stops change on beats of the 105 BPM bed. Music: Magnific Google Lyria, original track.", "#e9e2d0"))
