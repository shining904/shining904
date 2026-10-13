# 장호원 경마공원 유치 시안 (60 s, 1920x1080).
# Generates index.html and compositions/*.html. Run: python3 build.py
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, DUR = 1920, 1080, 60

NAVY, GOLD, CREAM = "#0b1a33", "#f2c25c", "#fff6e3"
FONTS = [("Black Han Sans", 400, "black-han-sans-latin-400-normal", "U+0000-00FF, U+2190-21FF"),
         ("Black Han Sans", 400, "black-han-sans-korean-400-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")]
FONTS += [("Noto Sans KR", w, f"noto-sans-kr-{s}-{w}-normal", r) for w in (500, 800)
          for s, r in (("latin", "U+0000-00FF, U+2190-21FF"), ("korean", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"))]
FACES = "".join(f'''        @font-face {{
          font-family: "{f}";
          font-weight: {w};
          src: url("fonts/{n}.woff2") format("woff2");
          unicode-range: {r};
        }}
''' for f, w, n, r in FONTS)

# scene id, start, duration, track
SCENES = [("dawn", 0, 6.8), ("race", 6.6, 6.8), ("zone", 13.2, 10.3), ("map", 23.3, 12.7),
          ("plain", 35.8, 6.8), ("sign", 42.4, 6.0), ("gain", 48.2, 5.6), ("end", 53.6, 6.4)]
# narration: start, caption (speech lengths measured from the TTS files)
NARR = [(1.0, "대한민국 경마의 다음 출발선은, 어디일까요?", 3.5),
        (7.2, "과천 경마공원 이전. 그 답을, 이천이 준비했습니다.", 4.8),
        (13.8, "이천은 이미 말산업특구. 470여 두의 말과 말 전문 동물병원이 있는 도시입니다.", 6.75),
        (23.8, "그리고, 이천이 고른 자리. 장호원.", 3.6),
        (28.0, "국도 세 개 노선과 감곡IC, 중부내륙선 감곡장호원역이 가까워 어디서든 빠르게 닿습니다.", 7.4),
        (36.2, "청미천의 너른 들, 햇사레 복숭아의 고장이 새로운 무대가 됩니다.", 4.6),
        (42.8, "장호원 주민 4천여 명이, 먼저 서명했습니다.", 3.7),
        (54.2, "준비된 이천. 출발선은, 장호원.", 3.2)]


def comp(cid, css, body, js):
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{FACES}        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          font-family: "Noto Sans KR", sans-serif;
        }}
{css}      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{js}        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
'''


def count(sel, target, a, dur, fmt):
    return (f'        {{ const o = {{ v: 0 }}; tl.to(o, {{ v: {target}, duration: {dur}, ease: "power2.out", '
            f'onUpdate: () => {{ const v = o.v; document.querySelector("{sel}").textContent = {fmt}; }} }}, {a}); }}\n')


COMMA = 'Math.round(v).toLocaleString("en-US")'
FADE_IN = '        tl.fromTo("#{p}-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "none" }}, 0);\n'
VIDEO_CSS = '''        #{p}-fade {{
          position: absolute;
          inset: 0;
          background: #000;
        }}
        #{p}-video {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }}
        #{p}-shade {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(5, 12, 26, 0.15) 0%, rgba(5, 12, 26, 0.35) 55%, rgba(5, 12, 26, 0.85) 100%);
        }}
'''
HEAD_CSS = f'''        .head {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Black Han Sans", sans-serif;
          color: #ffffff;
          text-shadow: 0 6px 30px rgba(0, 0, 0, 0.55);
        }}
        .tag {{
          position: absolute;
          left: 50%;
          transform: translateX(-50%);
          padding: 10px 30px;
          border: 3px solid {GOLD};
          border-radius: 999px;
          font-size: 38px;
          font-weight: 800;
          color: {GOLD};
          background: rgba(11, 26, 51, 0.7);
          white-space: nowrap;
        }}
        .gold {{
          color: {GOLD};
        }}
'''


def video_scene(p, src, dur, extra_css, extra_body, extra_js, scale=(1.0, 1.08)):
    css = VIDEO_CSS.format(p=p) + HEAD_CSS + extra_css
    body = f'''        <div id="{p}-fade">
          <video id="{p}-video" src="{src}" data-start="0" data-duration="{dur}" muted playsinline></video>
          <div id="{p}-shade"></div>
{extra_body}        </div>
'''
    js = FADE_IN.format(p=p)
    js += f'        tl.fromTo("#{p}-video", {{ scale: {scale[0]} }}, {{ scale: {scale[1]}, duration: {dur}, ease: "none" }}, 0);\n'
    return comp(p, css, body, js + extra_js)


def pop(sel, a, y=40, dur=0.6):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "power3.out" }}, {a});\n'


def slam(sel, a):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power4.out" }}, {a});\n'


files = {}

# 1. dawn — the question
files["dawn"] = video_scene("dawn", "assets/clips/dawn-graded.mp4", 6.8, '''        #dawn-q1 {
          top: 300px;
          font-size: 64px;
        }
        #dawn-q2 {
          top: 390px;
          font-size: 150px;
        }
''', '''          <div id="dawn-q1" class="head">대한민국 경마의 다음</div>
          <div id="dawn-q2" class="head"><span class="gold">출발선</span>은 어디인가</div>
''', pop("#dawn-q1", 1.0) + slam("#dawn-q2", 2.3) +
    '        tl.to("#dawn-q1, #dawn-q2", { opacity: 0, duration: 0.4, ease: "none" }, 6.2);\n')

# 2. race — relocation + Icheon prepared
files["race"] = video_scene("race", "assets/clips/race.mp4", 6.8, '''        #race-tag {
          top: 260px;
        }
        #race-h {
          top: 340px;
          font-size: 170px;
        }
''', '''          <div id="race-tag" class="tag">과천 경마공원 이전</div>
          <div id="race-h" class="head">그 답, <span class="gold">이천</span></div>
''', pop("#race-tag", 0.5, 20) + slam("#race-h", 2.9) +
    '        tl.to("#race-tag, #race-h", { opacity: 0, duration: 0.4, ease: "none" }, 6.2);\n')

# 3. zone — horse-industry special zone stats over the farm clip
cards = [("zone-c1", "470", "여 두", "사육 중인 말"), ("zone-c2", "26", "개", "말 사육 농가"),
         ("zone-c3", "5,600", "여 마리", "말 전문 동물병원 연간 진료")]
card_html = "".join(f'''          <div id="{i}" class="zone-card">
            <div class="zone-num"><span id="{i}-n">0</span><small>{u}</small></div>
            <div class="zone-lab">{lab}</div>
          </div>
''' for i, _, u, lab in cards)
zone_js = pop("#zone-tag", 0.4, 20) + slam("#zone-h", 0.9)
for k, (i, n, _, _) in enumerate(cards):
    a = 2.6 + k * 1.3
    zone_js += pop(f"#{i}", a, 60, 0.7) + count(f"#{i}-n", n.replace(",", ""), a, 1.4, COMMA)
zone_js += slam("#zone-badge", 7.0)
files["zone"] = video_scene("zone", "assets/clips/farm.mp4", 10.3, f'''        #zone-shade {{
          background: linear-gradient(180deg, rgba(11, 26, 51, 0.82) 0%, rgba(11, 26, 51, 0.7) 60%, rgba(5, 12, 26, 0.92) 100%);
        }}
        #zone-tag {{
          top: 120px;
        }}
        #zone-h {{
          top: 200px;
          font-size: 120px;
        }}
        #zone-cards {{
          position: absolute;
          top: 430px;
          left: 0;
          right: 0;
          display: flex;
          justify-content: center;
          gap: 56px;
        }}
        .zone-card {{
          width: 480px;
          padding: 34px 0 30px;
          border-radius: 28px;
          background: rgba(255, 246, 227, 0.08);
          border: 2px solid rgba(242, 194, 92, 0.55);
          text-align: center;
        }}
        .zone-num {{
          font-family: "Black Han Sans", sans-serif;
          font-size: 118px;
          line-height: 1.1;
          color: {GOLD};
        }}
        .zone-num small {{
          font-size: 48px;
          margin-left: 6px;
        }}
        .zone-lab {{
          margin-top: 8px;
          font-size: 36px;
          font-weight: 500;
          color: {CREAM};
        }}
        #zone-badge {{
          top: 760px;
          font-size: 40px;
          color: {NAVY};
          background: {GOLD};
        }}
''', f'''          <div id="zone-tag" class="tag">경기도 이천시</div>
          <div id="zone-h" class="head">이미 <span class="gold">말산업특구</span></div>
          <div id="zone-cards">
{card_html}          </div>
          <div id="zone-badge" class="tag">전국 말의 약 10%가 이천에</div>
''', zone_js, scale=(1.05, 1.12))

# 4. map — Icheon concept map, zoom into Jangho-won, roads/IC/rail draw on
JX, JY = 1330, 760  # Jangho-won on the concept map
ICHEON = ("M 760 170 C 880 140, 1010 180, 1080 250 C 1170 320, 1240 330, 1300 420 C 1350 500, 1420 560, 1460 650 "
          "C 1500 740, 1460 830, 1380 870 C 1290 910, 1200 880, 1130 860 C 1040 830, 960 880, 880 860 "
          "C 790 840, 740 760, 680 700 C 610 630, 560 560, 580 470 C 600 380, 640 300, 690 230 C 710 200, 730 180, 760 170 Z")
JANGHO = (f"M 1250 640 C 1320 610, 1420 620, 1460 680 C 1480 750, 1450 820, 1380 860 C 1320 890, 1250 870, 1220 820 "
          f"C 1190 760, 1200 680, 1250 640 Z")
ROADS = [("map-r3", "M 900 300 C 1050 450, 1200 620, 1330 760 C 1420 860, 1520 960, 1600 1060", "3"),
         ("map-r37", "M 1700 520 C 1580 600, 1450 690, 1330 760 C 1230 820, 1120 900, 1020 1060", "37"),
         ("map-r38", "M 620 820 C 820 790, 1050 770, 1330 760 C 1500 755, 1680 770, 1900 800", "38")]
RAIL = "M 1560 120 C 1520 320, 1480 520, 1420 700 C 1390 800, 1370 900, 1350 1080"
map_svg = f'''          <svg id="map-svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
            <g id="map-world">
              <path id="map-land" d="{ICHEON}" fill="#16294a" stroke="{GOLD}" stroke-width="5" />
              <path id="map-jh" d="{JANGHO}" fill="{GOLD}" fill-opacity="0.85" />
              <path id="map-river" d="M 1180 1080 C 1230 960, 1300 880, 1360 830 C 1420 790, 1500 760, 1620 700" fill="none" stroke="#6fb3e0" stroke-width="10" stroke-linecap="round" />
{"".join(f'              <path id="{i}" class="map-road" d="{d}" fill="none" stroke="#ffffff" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0" />' + chr(10) for i, d, _ in ROADS)}              <path id="map-rail" d="{RAIL}" fill="none" stroke="#ff7a59" stroke-width="9" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" opacity="0" />
            </g>
          </svg>
'''
map_body = map_svg + f'''          <div id="map-l-icheon" class="map-lab">이천시</div>
          <div id="map-l-yeoju" class="map-near">여주</div>
          <div id="map-l-anseong" class="map-near">안성</div>
          <div id="map-l-eumseong" class="map-near">충북 음성</div>
          <div id="map-pin"><div id="map-ring"></div><div id="map-dot"></div></div>
          <div id="map-l-jh" class="map-big">장호원읍</div>
          <div id="map-chips">
            <div id="map-c1" class="map-chip"><b>국도</b> 3 · 37 · 38호선</div>
            <div id="map-c2" class="map-chip"><b>감곡IC</b> 약 4.5km</div>
            <div id="map-c3" class="map-chip rail"><b>중부내륙선</b> 감곡장호원역 인접</div>
          </div>
          <div id="map-note">개념도 · 실제 위치·거리와 다를 수 있음</div>
'''
map_js = '        tl.fromTo("#map-land", { opacity: 0, scale: 0.9, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.8, ease: "power3.out" }, 0.1);\n'
map_js += pop("#map-l-icheon", 0.5, 20) + pop("#map-l-yeoju, #map-l-anseong, #map-l-eumseong", 0.8, 10)
map_js += '        tl.fromTo("#map-jh", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "none" }, 1.4);\n'
map_js += slam("#map-pin", 1.5) + slam("#map-l-jh", 1.8)
map_js += '        tl.fromTo("#map-ring", { scale: 0.4, opacity: 0.9 }, { scale: 2.2, opacity: 0, duration: 1.2, ease: "power1.out", repeat: 9 }, 1.6);\n'
# zoom: labels outside Jangho-won fade, world scales around Jangho-won and slides it left of centre
map_js += '        tl.to("#map-l-icheon, #map-l-yeoju, #map-l-anseong", { opacity: 0, duration: 0.4, ease: "none" }, 4.0);\n'
map_js += f'        tl.to("#map-world", {{ scale: 1.9, x: {760 - JX}, y: {540 - JY}, svgOrigin: "{JX} {JY}", duration: 1.4, ease: "power3.inOut" }}, 4.0);\n'
map_js += f'        tl.to("#map-pin", {{ x: {760 - JX}, y: {540 - JY}, duration: 1.4, ease: "power3.inOut" }}, 4.0);\n'
map_js += f'        tl.to("#map-l-jh", {{ x: {520 - (JX - 160)}, y: {610 - (JY + 40)}, duration: 1.4, ease: "power3.inOut" }}, 4.0);\n'
map_js += f'        tl.to("#map-l-eumseong", {{ x: -620, y: -100, duration: 1.4, ease: "power3.inOut" }}, 4.0);\n'
map_js += '        tl.to("#map-river", { opacity: 0.6, duration: 0.3, ease: "none" }, 4.0);\n'
for k, (i, _, _) in enumerate(ROADS):
    map_js += f'        tl.to("#{i}", {{ strokeDashoffset: 0, duration: 1.0, ease: "power2.inOut" }}, {5.0 + k * 0.35});\n'
    map_js += f'        tl.set("#{i}", {{ opacity: 1 }}, {5.0 + k * 0.35});\n'
map_js += pop("#map-c1", 5.4, 30)
map_js += pop("#map-c2", 6.9, 30)
map_js += '        tl.set("#map-rail", { opacity: 1 }, 8.1);\n        tl.to("#map-rail", { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }, 8.1);\n'
map_js += pop("#map-c3", 8.6, 30) + pop("#map-note", 5.4, 0)
files["map"] = comp("map", f'''        #map-bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(circle at 60% 55%, #1a3563 0%, {NAVY} 60%, #060e1d 100%);
        }}
        #map-svg {{
          position: absolute;
          inset: 0;
        }}
        .map-lab {{
          position: absolute;
          left: 860px;
          top: 440px;
          font-family: "Black Han Sans", sans-serif;
          font-size: 84px;
          color: #ffffff;
        }}
        .map-near {{
          position: absolute;
          font-size: 34px;
          font-weight: 500;
          color: #b9c6dd;
        }}
        #map-l-yeoju {{
          left: 1560px;
          top: 420px;
        }}
        #map-l-anseong {{
          left: 560px;
          top: 930px;
        }}
        #map-l-eumseong {{
          left: 1500px;
          top: 920px;
        }}
        #map-pin {{
          position: absolute;
          left: {JX}px;
          top: {JY}px;
          width: 0;
          height: 0;
        }}
        #map-dot,
        #map-ring {{
          position: absolute;
          left: -22px;
          top: -22px;
          width: 44px;
          height: 44px;
          border-radius: 50%;
        }}
        #map-dot {{
          background: #ffffff;
          border: 8px solid #e0483a;
        }}
        #map-ring {{
          border: 6px solid #ffffff;
        }}
        .map-big {{
          position: absolute;
          left: {JX - 160}px;
          top: {JY + 40}px;
          font-family: "Black Han Sans", sans-serif;
          font-size: 96px;
          color: #ffffff;
          text-shadow: 0 6px 24px rgba(0, 0, 0, 0.6);
        }}
        #map-chips {{
          position: absolute;
          left: 1180px;
          top: 300px;
          display: flex;
          flex-direction: column;
          gap: 28px;
        }}
        .map-chip {{
          padding: 22px 36px;
          border-radius: 22px;
          background: rgba(255, 246, 227, 0.96);
          color: {NAVY};
          font-size: 44px;
          font-weight: 500;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
        }}
        .map-chip b {{
          font-weight: 800;
          color: #b23a2c;
          margin-right: 10px;
        }}
        .map-chip.rail b {{
          color: #c2410c;
        }}
        #map-note {{
          position: absolute;
          right: 40px;
          top: 36px;
          font-size: 24px;
          color: #b9c6dd;
        }}
''', '          <div id="map-bg"></div>\n' + map_body, map_js)

# 5. plain — Cheongmi stream plain + Haetsare peaches (generated still, Ken Burns)
files["plain"] = comp("plain", VIDEO_CSS.format(p="plain").replace("#plain-video", "#plain-img") + HEAD_CSS + '''        #plain-tag {
          top: 150px;
        }
        #plain-h {
          top: 230px;
          font-size: 116px;
        }
''', '''        <div id="plain-fade">
          <img id="plain-img" src="assets/plain.jpg" alt="" />
          <div id="plain-shade"></div>
          <div id="plain-tag" class="tag">장호원읍</div>
          <div id="plain-h" class="head">청미천의 너른 들,<br /><span class="gold">햇사레 복숭아</span>의 고장</div>
        </div>
''', FADE_IN.format(p="plain") +
    '        tl.fromTo("#plain-img", { scale: 1.15, x: 60 }, { scale: 1.0, x: 0, duration: 6.8, ease: "none" }, 0);\n' +
    pop("#plain-tag", 0.5, 20) + pop("#plain-h", 0.9, 50, 0.8))
files["plain"] = files["plain"].replace('''          background: linear-gradient(180deg, rgba(5, 12, 26, 0.15) 0%''', '''          background: linear-gradient(180deg, rgba(5, 12, 26, 0.6) 0%''')

# 6. sign — 4,000 signatures: 400 dots (1 dot = 10 residents) rain into a grid
COLS, ROWS, GAP = 40, 10, 34
gx0 = (W - (COLS - 1) * GAP) // 2
sign_js = pop("#sign-tag", 0.3, 20)
sign_js += '''        (function () {
          let s = 7;
          const rnd = () => ((s = (s * 16807) %% 2147483647) / 2147483647);
          const host = document.querySelector("#sign-dots");
          for (let i = 0; i < %d; i++) {
            const d = document.createElement("div");
            d.className = "sign-dot";
            d.style.left = (%d + (i %% %d) * %d) + "px";
            d.style.top = (Math.floor(i / %d) * %d) + "px";
            host.appendChild(d);
            tl.fromTo(d, { opacity: 0, x: (rnd() - 0.5) * 900, y: -500 - rnd() * 400 },
              { opacity: 1, x: 0, y: 0, duration: 0.9, ease: "power3.out" }, 0.6 + rnd() * 2.2);
          }
        })();
''' % (COLS * ROWS, gx0 - 9, COLS, GAP, COLS, GAP)
sign_js += slam("#sign-num", 1.2) + count("#sign-n", 4000, 1.2, 2.4, COMMA)
sign_js += pop("#sign-chip", 3.3, 30) + pop("#sign-legend", 3.0, 0)
files["sign"] = comp("sign", f'''        #sign-bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(circle at 50% 40%, #1a3563 0%, {NAVY} 65%, #060e1d 100%);
        }}
{HEAD_CSS}        #sign-tag {{
          top: 90px;
        }}
        #sign-num {{
          top: 170px;
          font-size: 200px;
          color: {GOLD};
        }}
        #sign-num small {{
          font-size: 90px;
          color: #ffffff;
        }}
        #sign-dots {{
          position: absolute;
          left: 0;
          top: 520px;
          width: {W}px;
          height: 360px;
        }}
        .sign-dot {{
          position: absolute;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: {GOLD};
        }}
        #sign-legend {{
          position: absolute;
          right: 160px;
          top: 470px;
          font-size: 26px;
          color: #b9c6dd;
        }}
        #sign-chip {{
          top: 880px;
        }}
''', f'''          <div id="sign-bg"></div>
          <div id="sign-tag" class="tag">장호원읍 1차 유치 서명</div>
          <div id="sign-num" class="head"><span id="sign-n">0</span><small>여 명</small></div>
          <div id="sign-legend">● 1 = 주민 10명</div>
          <div id="sign-dots"></div>
          <div id="sign-chip" class="tag">주민 추진위원회 구성 · 시민이 먼저 움직였다</div>
''', sign_js)

# 7. gain — expected benefits over the aerial render
gains = [("gain-g1", 490, "억 원", "연간 세입 효과"), ("gain-g2", 3000, "명", "근무 인력 이전"),
         ("gain-g3", 200, "만 명+", "연간 방문객")]
gain_html = "".join(f'''            <div id="{i}" class="gain-card">
              <div class="gain-num"><span id="{i}-n">0</span><small>{u}</small></div>
              <div class="gain-lab">{lab}</div>
            </div>
''' for i, _, u, lab in gains)
gain_js = pop("#gain-tag", 0.2, 20)
for k, (i, n, _, _) in enumerate(gains):
    a = 0.5 + k * 0.7
    gain_js += pop(f"#{i}", a, 60, 0.6) + count(f"#{i}-n", n, a, 1.2, COMMA)
gain_js += pop("#gain-note", 2.4, 0)
files["gain"] = video_scene("gain", "assets/clips/aerial.mp4", 5.6, f'''        #gain-shade {{
          background: linear-gradient(180deg, rgba(5, 12, 26, 0.55) 0%, rgba(5, 12, 26, 0.75) 100%);
        }}
        #gain-tag {{
          top: 200px;
        }}
        #gain-cards {{
          position: absolute;
          top: 340px;
          left: 0;
          right: 0;
          display: flex;
          justify-content: center;
          gap: 48px;
        }}
        .gain-card {{
          width: 500px;
          padding: 40px 0 34px;
          border-radius: 28px;
          background: rgba(11, 26, 51, 0.78);
          border: 2px solid {GOLD};
          text-align: center;
        }}
        .gain-num {{
          font-family: "Black Han Sans", sans-serif;
          font-size: 120px;
          line-height: 1.1;
          color: {GOLD};
        }}
        .gain-num small {{
          font-size: 50px;
          margin-left: 6px;
        }}
        .gain-lab {{
          margin-top: 8px;
          font-size: 40px;
          font-weight: 500;
          color: #ffffff;
        }}
        #gain-note {{
          position: absolute;
          left: 0;
          right: 0;
          top: 700px;
          text-align: center;
          font-size: 30px;
          color: #dfe6f2;
        }}
''', f'''          <div id="gain-tag" class="tag">경마공원이 오면, 이천은</div>
          <div id="gain-cards">
{gain_html}          </div>
          <div id="gain-note">※ 이천시 추산 (과천 경마공원 규모 운영 기준)</div>
''', gain_js)

# 8. end — slogan + Icheon logo
end_js = FADE_IN.format(p="end")
end_js += '        tl.fromTo("#end-img", { scale: 1.0 }, { scale: 1.1, duration: 6.4, ease: "none" }, 0);\n'
end_js += pop("#end-s1", 0.6, 40, 0.7) + slam("#end-s2", 1.6)
end_js += '        tl.fromTo("#end-line", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power3.inOut" }, 2.2);\n'
end_js += pop("#end-sub", 2.6, 20) + pop("#end-logo", 3.0, 20) + pop("#end-ai", 3.0, 0)
files["end"] = comp("end", VIDEO_CSS.format(p="end").replace("#end-video", "#end-img") + HEAD_CSS + f'''        #end-shade {{
          background: radial-gradient(ellipse at 50% 45%, rgba(5, 12, 26, 0.45) 0%, rgba(5, 12, 26, 0.88) 75%);
        }}
        #end-s1 {{
          top: 190px;
          font-size: 110px;
        }}
        #end-s2 {{
          top: 320px;
          font-size: 190px;
          color: {GOLD};
        }}
        #end-line {{
          position: absolute;
          left: 660px;
          width: 600px;
          top: 575px;
          height: 6px;
          background: {GOLD};
          transform-origin: 50% 50%;
        }}
        #end-sub {{
          top: 610px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 800;
          font-size: 46px;
        }}
        #end-logo {{
          position: absolute;
          left: 50%;
          top: 720px;
          margin-left: -150px;
          width: 300px;
          padding: 14px 24px;
          border-radius: 20px;
          background: #ffffff;
        }}
        #end-logo img {{
          display: block;
          width: 100%;
        }}
        #end-ai {{
          position: absolute;
          right: 36px;
          bottom: 150px;
          font-size: 22px;
          color: #b9c6dd;
        }}
''', '''        <div id="end-fade">
          <img id="end-img" src="assets/aerial-end.jpg" alt="" />
          <div id="end-shade"></div>
          <div id="end-s1" class="head">준비된 이천,</div>
          <div id="end-s2" class="head">출발선은 장호원</div>
          <div id="end-line"></div>
          <div id="end-sub" class="head">한국마사회 경마공원, 이천 장호원으로</div>
          <div id="end-logo"><img src="assets/icheon-logo.png" alt="이천시" /></div>
          <div id="end-ai">AI 생성 영상·이미지 포함 · 조감도는 상상도</div>
        </div>
''', end_js)

# captions — narration subtitles at the bottom
caps_body = '          <div id="caps-bar"></div>\n' + "".join(
    f'          <div id="caps-c{k}" class="caps-line">{t}</div>\n' for k, (_, t, _) in enumerate(NARR))
caps_js = ""
for k, (s, _, d) in enumerate(NARR):
    caps_js += f'        tl.fromTo("#caps-c{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "none" }}, {s});\n'
    caps_js += f'        tl.to("#caps-c{k}", {{ opacity: 0, duration: 0.2, ease: "none" }}, {round(s + d + 0.3, 2)});\n'
files["caps"] = comp("caps", '''        #caps-bar {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          height: 170px;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.75) 100%);
        }
        .caps-line {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 44px;
          text-align: center;
          font-size: 42px;
          font-weight: 500;
          color: #ffffff;
          text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
          opacity: 0;
        }
''', caps_body, caps_js)

for k, v in files.items():
    with open(f"compositions/{k}.html", "w") as fh:
        fh.write(v)

tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i % 2}" data-width="{W}" data-height="{H}"></div>
''' for i, (c, s, d) in enumerate(SCENES))
with open("index.html", "w") as fh:
    fh.write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>준비된 이천, 출발선은 장호원</title>
    <script src="gsap.min.js"></script>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: {W}px;
        height: {H}px;
        overflow: hidden;
        background: #000;
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #000;
      }}
    </style>
  </head>
  <body>
    <!-- 장호원 경마공원 유치 시안. Clips reused from hyperframes-kra-film (Magnific Seedance);
         plain.jpg, narration and score generated with Magnific. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html"
        data-start="0" data-duration="{DUR}" data-track-index="2" data-width="{W}" data-height="{H}"></div>
      <audio id="soundtrack" src="assets/audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
print("ok")
