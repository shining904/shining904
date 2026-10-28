# ④ 지도 여행 — follow the name across the map: 이천 (서희's family seat) → 압록강 강동 6주 (993)
# → 거제 (서희함 launch, 2026). Flat cartographic style, Gowun Dodum lettering.
import json
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

COAST = [(124.3, 39.9), (124.7, 39.6), (125.1, 39.5), (125.4, 39.0), (125.1, 38.7), (125.3, 38.3), (124.8, 38.0),
         (125.6, 37.7), (126.1, 37.7), (126.6, 37.5), (126.8, 37.0), (126.5, 36.6), (126.5, 36.0), (126.7, 35.5),
         (126.4, 34.8), (126.6, 34.4), (127.4, 34.6), (128.0, 34.8), (128.6, 34.9), (129.1, 35.1), (129.4, 35.5),
         (129.5, 36.0), (129.4, 36.6), (129.3, 37.1), (128.9, 37.7), (128.5, 38.3), (128.3, 38.6), (127.8, 39.1),
         (127.5, 39.3), (127.6, 39.8), (128.3, 40.0), (128.9, 40.5), (129.7, 40.9), (129.8, 41.4), (130.2, 42.0),
         (130.7, 42.3), (130.0, 42.9), (129.3, 42.4), (128.9, 42.0), (128.1, 42.0), (127.5, 41.7), (126.9, 41.8),
         (126.3, 41.3), (125.4, 40.6), (124.9, 40.3), (124.3, 39.9)]
P = lambda lon, lat: (round(70 + (lon - 124) * 138, 1), round(330 + (43 - lat) * 138, 1))
coast = " ".join(f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(P(*c) for c in COAST)) + " Z"
yalu = " ".join(f"{'M' if i == 0 else 'L'} {x} {y}" for i, (x, y) in enumerate(P(*c) for c in COAST[-7:]))
ICN, GDG, GJE = P(127.44, 37.27), P(125.05, 40.0), P(128.62, 34.88)
JEJU = P(126.55, 33.38)
route1 = f"M {ICN[0]} {ICN[1]} Q {ICN[0] - 120} {ICN[1] - 300} {GDG[0]} {GDG[1]}"
route2 = f"M {GDG[0]} {GDG[1]} Q {GDG[0] + 560} {GDG[1] + 380} {GJE[0]} {GJE[1]}"
SEA, LAND, LINE = "#cfe2e8", "#f6efe0", "#8c7b5b"

css = f'''        #cam {{
          position: absolute;
          left: 0;
          top: 0;
          width: 1080px;
          height: 1920px;
          transform-origin: 0 0;
        }}
        #sea {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, #e2eef1 0%, {SEA} 60%, #b7d3dc 100%);
        }}
        #waves {{
          position: absolute;
          inset: 0;
          background-image: repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.35) 0 2px, transparent 2px 46px);
        }}
        svg {{
          position: absolute;
          left: 0;
          top: 0;
        }}
        .pin {{
          position: absolute;
          width: 0;
          height: 0;
        }}
        .pin i {{
          position: absolute;
          left: -16px;
          top: -16px;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: #c83e2c;
          border: 6px solid #ffffff;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }}
        .bub {{
          position: absolute;
          width: 420px;
          padding: 18px 24px;
          border-radius: 26px;
          background: #ffffff;
          box-shadow: 0 10px 30px rgba(40, 60, 70, 0.25);
          font-family: "Gowun Dodum", sans-serif;
          color: #2d2a24;
          word-break: keep-all;
        }}
        .bub b {{
          display: block;
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 30px;
          color: #c83e2c;
        }}
        .bub div {{
          font-size: 40px;
          line-height: 1.25;
        }}
        .bub img {{
          float: right;
          width: 110px;
          height: 110px;
          margin-left: 12px;
          border-radius: 50%;
          object-fit: cover;
          object-position: 50% 20%;
          background: #e8dcc4;
        }}
        #hdr {{
          position: absolute;
          left: 70px;
          right: 70px;
          top: 110px;
          font-family: "Gowun Dodum", sans-serif;
          color: #1f3442;
        }}
        #hdr-1 {{
          font-size: 44px;
        }}
        #hdr-2 {{
          margin-top: 6px;
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          font-size: 110px;
          letter-spacing: -3px;
        }}
        #fin {{
          position: absolute;
          left: 0;
          right: 0;
          top: 100px;
          text-align: center;
          opacity: 0;
        }}
        #fin-name {{
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          font-size: 200px;
          letter-spacing: -6px;
          color: #12324a;
        }}
        #fin-sub {{
          font-family: "Gowun Dodum", sans-serif;
          font-size: 50px;
          color: #12324a;
        }}
        #sign {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1470px;
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
          font-weight: 800;
          font-size: 50px;
          color: #12324a;
        }}
        #sign i {{
          width: 3px;
          height: 76px;
          background: #c83e2c;
        }}
        #note {{
          position: absolute;
          right: 40px;
          bottom: 30px;
          font-family: "Gowun Dodum", sans-serif;
          font-size: 22px;
          color: #3c5260;
        }}
'''
body = f'''        <div id="sea"></div>
        <div id="waves"></div>
        <div id="cam">
          <svg width="1080" height="1920" viewBox="0 0 1080 1920">
            <path id="land" d="{coast}" fill="{LAND}" stroke="{LINE}" stroke-width="4" stroke-linejoin="round" />
            <ellipse cx="{JEJU[0]}" cy="{JEJU[1]}" rx="44" ry="18" fill="{LAND}" stroke="{LINE}" stroke-width="3" />
            <path id="yalu" d="{yalu}" fill="none" stroke="#5aa7c9" stroke-width="8" stroke-linecap="round" />
            <path id="r1" d="{route1}" fill="none" stroke="#c83e2c" stroke-width="9" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" pathLength="1" />
            <path id="r2" d="{route2}" fill="none" stroke="#c83e2c" stroke-width="9" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1" pathLength="1" />
            <path id="glow" d="{route1} {route2[route2.index('Q') - 1:]}" fill="none" stroke="{GOLD}" stroke-width="16" stroke-linecap="round" opacity="0" />
          </svg>
          <div id="pin1" class="pin" style="left:{ICN[0]}px;top:{ICN[1]}px"><i></i></div>
          <div id="pin2" class="pin" style="left:{GDG[0]}px;top:{GDG[1]}px"><i></i></div>
          <div id="pin3" class="pin" style="left:{GJE[0]}px;top:{GJE[1]}px"><i></i></div>
        </div>
        <div id="b1" class="bub" style="left:570px;top:820px;width:470px"><img src="assets/face-cut.png" alt="" /><b>이천</b><div>서희의 고향,<br />이천 서씨의 본관</div></div>
        <div id="b2" class="bub" style="left:360px;top:840px"><b>993 · 압록강</b><div>칼 대신 말로<br />강동 6주를 얻다</div></div>
        <div id="b3" class="bub" style="left:290px;top:830px;width:470px"><img src="assets/sub-cut.png" alt="" style="object-fit:contain;background:#dbeef5;border-radius:16px" /><b>2026 · 거제</b><div>서희함<br />진수</div></div>
        <div id="hdr"><div id="hdr-1">천 년을 건너온 이름</div><div id="hdr-2">서희의 길</div></div>
        <div id="fin"><div id="fin-name">서희함</div><div id="fin-sub">진수를 진심으로 축하합니다</div></div>
        <div id="sign"><img src="assets/icheon-logo-key.png" alt="이천시" /><i></i><div>경기도 이천시</div></div>
        <div id="note">개념도 · 실제 위치·경계와 다를 수 있음</div>
'''


def cam(a, dur, cx, cy, s, ease="power2.inOut"):
    """move the camera so map point (cx, cy) sits at screen (540, 1000) at scale s"""
    return f'        tl.to("#cam", {{ x: {round(540 - cx * s)}, y: {round(1000 - cy * s)}, scale: {s}, duration: {dur}, ease: "{ease}" }}, {a});\n'


js = f'        tl.set("#cam", {{ x: {round(540 - ICN[0] * 2.2)}, y: {round(1000 - ICN[1] * 2.2)}, scale: 2.2 }}, 0);\n'
js += pop("#hdr", 0.2, 30, 0.7)
js += '        tl.fromTo("#pin1 i", { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(3)" }, 0.6);\n'
js += pop("#b1", 0.9, 20, 0.5)
js += cam(2.6, 1.6, (ICN[0] + GDG[0]) / 2, (ICN[1] + GDG[1]) / 2, 1.5)
js += '        tl.to("#r1", { strokeDashoffset: 0, duration: 1.8, ease: "power1.inOut" }, 2.8);\n'
js += out("#b1", 2.7, 0.3)
js += cam(4.3, 1.0, GDG[0] + 120, GDG[1], 1.9)
js += '        tl.fromTo("#pin2 i", { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(3)" }, 4.5);\n'
js += pop("#b2", 4.7, 20, 0.5)
js += out("#b2", 6.4, 0.3)
js += cam(6.4, 2.0, (GDG[0] + GJE[0]) / 2 + 80, (GDG[1] + GJE[1]) / 2, 1.25)
js += '        tl.to("#r2", { strokeDashoffset: 0, duration: 2.2, ease: "power1.inOut" }, 6.5);\n'
js += cam(8.5, 1.0, GJE[0] - 150, GJE[1], 1.8)
js += '        tl.fromTo("#pin3 i", { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(3)" }, 8.7);\n'
js += pop("#b3", 8.9, 20, 0.5) + out("#hdr", 8.6, 0.4)
# hit: pull back to the whole route, it glows gold, the name lands
js += out("#b3", HIT - 0.1, 0.2)
js += cam(HIT, 1.1, 540, 1010, 1.0, "power3.out")
js += f'        tl.to("#glow", {{ opacity: 0.9, duration: 0.4, ease: "none" }}, {HIT + 0.3});\n'
js += f'        tl.fromTo("#fin", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power4.out" }}, {HIT + 0.5});\n'
js += '        tl.fromTo("#sign", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 13.5);\n'
js += out("#fin, #sign, #cam, #note", 20.2, 0.7)

d = setup("map")
write(d, {"map": comp("map", ["pre", "gowun"], css, body, js)},
      index("서희함 · 지도 여행", "④ map journey short. Map is a concept sketch from approximate coordinates; score: Lyria 3 Pro cut.", [("map", 0, DUR)], bg=SEA))
print("ok")
