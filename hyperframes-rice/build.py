# Build the Icheon rice festival dance reel (1080x1920). Cuts and captions land on the music's bars.
# `python3 build.py b` builds variant B: a plain-rice crowd (only Babari in costume) and the
# "1년 준비" line; the default (A) has the costumed crowd and the "88번 손길" line.
import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
GOLD = "#f2c46b"
RED = "#e0483a"
RANGES = (("latin", "U+0000-00FF, U+2190-21FF"), ("korean", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"))
DISPLAY_FACES = "".join(f'''        @font-face {{
          font-family: "Black Han Sans";
          font-weight: 400;
          src: url("fonts/black-han-sans-{sub}-400-normal.woff2") format("woff2");
          unicode-range: {rng};
        }}
''' for sub, rng in RANGES)
D = '"Black Han Sans", sans-serif'
VARIANT = sys.argv[1] if len(sys.argv) > 1 else "a"
SUFFIX = "-b" if VARIANT == "b" else ""
W, H = 1080, 1920
BEAT = 0.46875  # 128 BPM (music3.mp3)
FIRST = 0.0  # kick on the first sample; the drop lands on bar 8 (15.0s)
LEN = round(FIRST + 4 * BEAT * 16, 3)  # bar 16 = 30.0, where the track ends


def bar(n):
    return round(FIRST + 4 * BEAT * n, 3)


def comp(cid, css, body, anims):
    if "Black Han Sans" in css:
        css = DISPLAY_FACES + css
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
        }}
{css}      </style>
      <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{anims}        window.__timelines["{cid}"] = tl;
      </script>
    </template>
  </body>
</html>
'''


def clip(cid, src, dur, punch):
    # punch: list of beat times (scene-local) for a quick zoom-in hit
    hits = "".join(f'        tl.to("#{cid}-frame", {{ keyframes: [{{ scale: 1.06, duration: 0.08, ease: "power2.out" }}, {{ scale: 1, duration: 0.12 }}] }}, {t});\n' for t in punch)
    return comp(cid, f'''        #{cid}-frame {{
          position: absolute;
          inset: 0;
          background: #000;
        }}
        #{cid}-video {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }}
''', f'''        <div id="{cid}-frame">
          <video id="{cid}-video" src="assets/clips/{src}" data-start="0" data-duration="{dur}" muted playsinline></video>
        </div>
''', hits)


files = {}
b = bar
files["clip1"] = clip("clip1", f"leader-lip{SUFFIX}.mp4", b(4), [])
files["clip2"] = clip("clip2", f"crowd{SUFFIX}.mp4", round(b(8) - b(4), 3), [round(4 * BEAT * k, 3) for k in range(0, 4)])
files["clip3"] = clip("clip3", "closeup-lip.mp4", round(b(12) - b(8), 3), [])  # thumbs-up lands near the end

# Meme captions in the top safe zone
CAPS = [
    (0.0, 4.0, "인삼 군무 보셨죠?", "이번엔|이천 쌀 차례"),
    (4.0, b(4), "", "햅쌀 정예부대 집합!"),
    (b(4), b(6), "", "한 톨도 안 틀리는|칼군무"),
    (b(6), b(8), "연습이요?", "꼬박 1년 준비했습니다" if VARIANT == "b" else "88번 손이 갔습니다"),
    (b(8), round(b(8) + 3.9, 3), "", "이천 햅쌀 가마솥밥"),
    (round(b(8) + 3.9, 3), b(12), "", "이천 원에 드실래요?"),
]
cap_html = ""
cap_anims = ""
for i, (a, e, small, big) in enumerate(CAPS, 1):
    small_html = f'            <div class="caps-small">{small}</div>\n' if small else ""
    big_html = "".join(f'            <div class="caps-big">{line}</div>\n' for line in big.split("|"))
    cap_html += f'''          <div id="caps-c{i}" class="caps-group">
{small_html}{big_html}
          </div>
'''
    cap_anims += f'''        tl.fromTo("#caps-c{i}", {{ opacity: 0, scale: 1.35 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power4.out" }}, {a});
        tl.to("#caps-c{i}", {{ opacity: 0, duration: 0.08, ease: "none" }}, {round(e - 0.08, 3)});
'''
files["caps"] = comp("caps", f'''        .caps-group {{
          position: absolute;
          left: 60px;
          right: 60px;
          top: 300px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          opacity: 0;
        }}
        .caps-small {{
          font-size: 54px;
          font-weight: 800;
          color: #ffffff;
          -webkit-text-stroke: 8px #000;
          paint-order: stroke fill;
        }}
        .caps-big {{
          margin-top: 6px;
          font-family: {D};
          font-size: 104px;
          line-height: 1.15;
          color: {GOLD};
          -webkit-text-stroke: 14px #000;
          paint-order: stroke fill;
        }}
''', cap_html, cap_anims)

# End card over a blurred last frame
PROGS = ["가마솥밥 이천명 이천원", "무지개 가래떡 뽑기", "돌아온 명인전", "이천첨단드론대전"]
chips = "".join(f'            <div class="end-chip">{p}</div>\n' for p in PROGS)
files["end"] = comp("end", f'''        #end-bg {{
          position: absolute;
          inset: -40px;
          width: calc(100% + 80px);
          height: calc(100% + 80px);
          object-fit: cover;
          filter: blur(18px) brightness(0.35);
        }}
        #end-wrap {{
          position: absolute;
          left: 70px;
          right: 70px;
          top: 300px;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          color: #ffffff;
        }}
        #end-kicker {{
          font-size: 46px;
          font-weight: 800;
          color: {GOLD};
        }}
        .end-title {{
          font-family: {D};
          font-size: 118px;
          line-height: 1.1;
        }}
        #end-title1 {{
          margin-top: 18px;
        }}
        #end-title2 {{
          color: {GOLD};
        }}
        #end-date {{
          margin-top: 44px;
          padding: 18px 44px;
          border-radius: 999px;
          background: {RED};
          font-family: {D};
          font-size: 70px;
        }}
        #end-place {{
          margin-top: 26px;
          font-size: 42px;
          font-weight: 800;
          line-height: 1.4;
        }}
        #end-chips {{
          margin-top: 40px;
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 16px;
        }}
        .end-chip {{
          padding: 12px 28px;
          border-radius: 18px;
          background: rgba(242, 196, 107, 0.95);
          color: #1c1408;
          font-size: 40px;
          font-weight: 800;
        }}
        #end-note {{
          position: absolute;
          left: 0;
          right: 0;
          bottom: 330px;
          text-align: center;
          font-size: 26px;
          font-weight: 500;
          color: rgba(255, 255, 255, 0.7);
        }}
''', f'''        <img id="end-bg" src="assets/end-frame.jpg" alt="" />
        <div id="end-wrap">
          <div id="end-kicker">갓 지은 햅쌀밥은 축제에서</div>
          <div id="end-title1" class="end-title">제25회 이천</div>
          <div id="end-title2" class="end-title">쌀문화축제</div>
          <div id="end-date">10.14(수) ~ 10.18(일)</div>
          <div id="end-place">서울동경기인삼농협<br-none></br-none></div>
          <div id="end-chips">
{chips}          </div>
        </div>
        <div id="end-note">※ 이 영상은 AI로 생성한 영상입니다</div>
''', f'''        tl.fromTo("#end-bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "none" }}, 0);
        tl.fromTo("#end-kicker", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 0.1);
        tl.fromTo(".end-title", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "power4.out", stagger: {BEAT} }}, {BEAT});
        tl.fromTo("#end-date", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {3 * BEAT});
        tl.fromTo("#end-place", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {4 * BEAT});
        tl.fromTo(".end-chip", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "back.out(2)", stagger: {BEAT / 2} }}, {5 * BEAT});
        tl.fromTo("#end-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {8 * BEAT});
''')
files["end"] = files["end"].replace('<div id="end-place">서울동경기인삼농협<br-none></br-none></div>', '<div id="end-place">이천 복하천 수변공원 일원</div>')

for k, v in files.items():
    open(f"compositions/{k}.html", "w").write(v)

slots = [("clip1", 0, b(4), 0), ("clip2", b(4), b(8) - b(4), 1), ("clip3", b(8), b(12) - b(8), 0),
         ("end", b(12), LEN - b(12), 1), ("caps", 0, b(12), 2)]
hosts = "".join(f'''      <div id="{s}" data-composition-id="{s}" data-composition-src="compositions/{s}.html"
        data-start="{round(a, 3)}" data-duration="{round(d, 3)}" data-track-index="{t}" data-width="{W}" data-height="{H}"></div>
''' for s, a, d, t in slots)
ff = ""
for w in (500, 800):
    for sub, rng in RANGES:
        ff += f'''      @font-face {{
        font-family: "Noto Sans KR";
        font-weight: {w};
        src: url("fonts/noto-sans-kr-{sub}-{w}-normal.woff2") format("woff2");
        unicode-range: {rng};
      }}
'''
open("index.html", "w").write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>이천 쌀 군무 릴스</title>
    <script src="gsap.min.js"></script>
    <style>
{ff}      * {{
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
        font-family: "Noto Sans KR", sans-serif;
      }}
    </style>
  </head>
  <body>
    <!-- Clips: Magnific Seedance 2.5 (3D Babari rice-grain characters). Voices: ElevenLabs via Magnific. Music: Magnific ElevenLabs music, original track. -->
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{LEN}"
      data-width="{W}"
      data-height="{H}"
    >
{hosts}      <audio id="soundtrack" src="assets/audio/mix{SUFFIX}.mp3" data-start="0" data-duration="{round(LEN - 0.1, 2)}" data-track-index="3"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
print("bars:", [b(i) for i in range(13)])
