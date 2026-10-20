# 2026 이천펫축제 홍보 릴스 — "개우 도전 1일차" (배우 도전 1일차 밈 패러디), 30 s, 1080x1920.
# Generates index.html and compositions/*.html. Run: python3 build.py
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, DUR = 1080, 1920, 30
RED, YEL = "#ff4d4d", "#ffd83d"
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

# id, clip, start, duration, day label, situation, stars
DAYS = [("d1", "day1", 0.0, 7.4, "개우 도전 1일차", "상황: 산책이 취소됐다", 1),
        ("d2", "day2", 7.4, 7.2, "개우 도전 2일차", "상황: 고양이가 내 방석을 차지했다", 3),
        ("d3", "day3", 14.6, 7.4, "개우 도전 3일차", "상황: “목욕하자”", 4)]
END_START, END_DUR = 22.0, 8.0


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


def pop(sel, a, y=40, dur=0.5, ease="back.out(1.8)"):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "{ease}" }}, {a});\n'


def stamp(sel, a):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, scale: 2.2, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.35, ease: "power4.out" }}, {a});\n'


MEME_CSS = f'''        .meme-top {{
          position: absolute;
          left: 0;
          right: 0;
          top: 150px;
          text-align: center;
        }}
        .meme-day {{
          display: inline-block;
          font-family: "Black Han Sans", sans-serif;
          font-size: 118px;
          line-height: 1.1;
          color: #ffffff;
          -webkit-text-stroke: 14px #111111;
          paint-order: stroke fill;
        }}
        .meme-sit {{
          display: inline-block;
          margin-top: 22px;
          padding: 14px 34px;
          border-radius: 18px;
          background: #111111;
          color: {YEL};
          font-size: 50px;
          font-weight: 800;
        }}
        .meme-rate {{
          position: absolute;
          left: 50%;
          bottom: 260px;
          margin-left: -330px;
          width: 660px;
          padding: 18px 0;
          border-radius: 24px;
          background: rgba(17, 17, 17, 0.82);
          text-align: center;
          color: #ffffff;
          font-size: 48px;
          font-weight: 800;
        }}
        .meme-rate b {{
          font-family: "Black Han Sans", sans-serif;
          font-weight: 400;
          color: {YEL};
          letter-spacing: 4px;
        }}
'''


def video_layer(p, clip, dur):
    css = f'''        #{p}-video {{
          position: absolute;
          inset: 0;
          width: 100%;
          height: 100%;
          object-fit: cover;
        }}
        #{p}-shade {{
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          height: 640px;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.35) 0%, rgba(0, 0, 0, 0) 100%);
        }}
'''
    body = f'''        <video id="{p}-video" src="assets/clips/{clip}.mp4" data-start="0" data-duration="{dur}" muted playsinline></video>
        <div id="{p}-shade"></div>
'''
    return css, body


files = {}
for p, clip, s, d, day, sit, stars in DAYS:
    vcss, vbody = video_layer(p, clip, d)
    star = "★" * stars + "☆" * (5 - stars)
    extra = ""
    js = pop(f"#{p}-day", 0.15, -40) + pop(f"#{p}-sit", 0.55, 20, 0.4, "power3.out")
    if p == "d1":
        js += stamp(f"#{p}-rate", 5.4)
    elif p == "d2":
        js += stamp(f"#{p}-rate", 5.6)
    else:
        extra = '        <div id="d3-peek" class="meme-tag">(실눈 확인 중)</div>\n'
        js += stamp("#d3-peek", 4.6) + stamp(f"#{p}-rate", 5.6)
    files[p] = comp(p, vcss + MEME_CSS + f'''        .meme-tag {{
          position: absolute;
          left: 90px;
          top: 1080px;
          padding: 10px 26px;
          border-radius: 14px;
          background: {YEL};
          color: #111111;
          font-size: 46px;
          font-weight: 800;
        }}
''', vbody + f'''        <div class="meme-top">
          <div id="{p}-day" class="meme-day">{day}</div><br />
          <div id="{p}-sit" class="meme-sit">{sit}</div>
        </div>
{extra}        <div id="{p}-rate" class="meme-rate">연기력 <b>{star}</b></div>
''', js)

# ending — stage clip + festival card
vcss, vbody = video_layer("end", "stage", END_DUR)
CHIPS = ["멍냥이 장기자랑", "캣통령 토크콘서트", "댕댕이 가을운동회", "펫워크 산책교실"]
chips = "".join(f'            <div class="end-chip">{c}</div>\n' for c in CHIPS)
end_js = '        tl.fromTo("#end-video", { scale: 1.3, y: -250 }, { scale: 1.34, y: -250, duration: 8, ease: "none" }, 0);\n'
end_js += stamp("#end-rate", 0.1)
end_js += pop("#end-q", 0.9, -30) + pop("#end-card", 4.3, 120, 0.7, "power3.out")
end_js += pop("#end-date", 4.8, 20) + pop("#end-place", 5.1, 20)
end_js += '        tl.fromTo(".end-chip", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.12 }, 5.4);\n'
end_js += pop("#end-foot", 6.0, 0)
files["end"] = comp("end", vcss + MEME_CSS + f'''        #end-rate {{
          top: 130px;
          bottom: auto;
        }}
        #end-q {{
          position: absolute;
          left: 0;
          right: 0;
          top: 250px;
          text-align: center;
          font-family: "Black Han Sans", sans-serif;
          font-size: 96px;
          line-height: 1.15;
          color: #ffffff;
          -webkit-text-stroke: 12px #111111;
          paint-order: stroke fill;
        }}
        #end-q span {{
          color: {YEL};
        }}
        #end-card {{
          position: absolute;
          left: 60px;
          right: 60px;
          bottom: 60px;
          padding: 34px 40px 30px;
          border-radius: 40px;
          background: rgba(255, 255, 255, 0.95);
          text-align: center;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        }}
        #end-title {{
          font-family: "Black Han Sans", sans-serif;
          font-size: 92px;
          line-height: 1.1;
          color: #222222;
        }}
        #end-title small {{
          display: block;
          font-size: 44px;
          color: #c2410c;
        }}
        #end-date {{
          display: inline-block;
          margin-top: 18px;
          padding: 10px 36px;
          border-radius: 999px;
          background: {RED};
          color: #ffffff;
          font-size: 50px;
          font-weight: 800;
        }}
        #end-place {{
          margin-top: 14px;
          font-size: 40px;
          font-weight: 800;
          color: #222222;
        }}
        #end-chips {{
          margin-top: 22px;
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 12px;
        }}
        .end-chip {{
          padding: 10px 22px;
          border-radius: 999px;
          background: #fff1c2;
          border: 3px solid #f2b705;
          color: #4a3500;
          font-size: 34px;
          font-weight: 800;
        }}
        #end-foot {{
          margin-top: 18px;
          font-size: 28px;
          color: #555555;
        }}
''', vbody + f'''        <div id="end-rate" class="meme-rate">연기력 <b>★★★★★</b> ?!</div>
        <div id="end-q">연기력 검증은<br /><span>여기서!</span></div>
        <div id="end-card">
          <div id="end-title"><small>멍냥이 장기자랑 출전 대기 중</small>2026 이천펫축제</div>
          <div id="end-date">10.24(토) ~ 25(일)</div>
          <div id="end-place">이천도자예술마을(예스파크) 일원</div>
          <div id="end-chips">
{chips}          </div>
          <div id="end-foot">개막 10.24(토) 오후 2시 · 이천시 · AI 생성 영상</div>
        </div>
''', end_js)

for k, v in files.items():
    with open(f"compositions/{k}.html", "w") as fh:
        fh.write(v)

scenes = [(p, s, d) for p, _, s, d, *_ in DAYS] + [("end", END_START, END_DUR)]
tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i % 2}" data-width="{W}" data-height="{H}"></div>
''' for i, (c, s, d) in enumerate(scenes))
with open("index.html", "w") as fh:
    fh.write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>개우 도전 1일차</title>
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
    <!-- 2026 이천펫축제 릴스. Clips: Magnific Seedance 2.5; music Lyria; narration ElevenLabs (Jiwoo). -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <audio id="soundtrack" src="assets/audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="2"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
print("ok")
