# Title page for "기도후원자 영상편지": warm light, drifting glow particles, serif title.
# `python3 build.py 16x9` (default, 1920x1080) or `python3 build.py 9x16` (1080x1920).
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FMT = sys.argv[1] if len(sys.argv) > 1 else "16x9"
W, H = (1920, 1080) if FMT == "16x9" else (1080, 1920)
V = W < H
TITLE_SIZE = 96 if V else 120
faces = ""
for fam, w, f, rng in [("Nanum Myeongjo", 800, "nanum-myeongjo-latin-800-normal", "U+0000-00FF"),
                       ("Nanum Myeongjo", 800, "nanum-myeongjo-korean-800-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"),
                       ("Noto Sans KR", 500, "noto-sans-kr-latin-500-normal", "U+0000-00FF"),
                       ("Noto Sans KR", 500, "noto-sans-kr-korean-500-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")]:
    faces += f'''        @font-face {{
          font-family: "{fam}";
          font-weight: {w};
          src: url("fonts/{f}.woff2") format("woff2");
          unicode-range: {rng};
        }}
'''
dots = "".join(f'        <div class="lt-dot" style="left:{(i * 197) % W}px;top:{(i * 331) % H}px;width:{6 + i % 4 * 4}px;height:{6 + i % 4 * 4}px"></div>\n' for i in range(26))
comp = f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{faces}        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          background: radial-gradient(ellipse at 50% 40%, #fff6e6 0%, #f3dfc0 55%, #d9b88e 100%);
        }}
        #lt-glow {{
          position: absolute;
          left: 50%;
          top: 40%;
          width: {int(W * 0.9)}px;
          height: {int(W * 0.9)}px;
          margin: -{int(W * 0.45)}px 0 0 -{int(W * 0.45)}px;
          border-radius: 50%;
          background: radial-gradient(circle, rgba(255, 255, 255, 0.85) 0%, rgba(255, 244, 220, 0) 60%);
        }}
        .lt-dot {{
          position: absolute;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.9);
          box-shadow: 0 0 14px 4px rgba(255, 236, 190, 0.8);
        }}
        #lt-wrap {{
          position: absolute;
          left: 0;
          right: 0;
          top: 50%;
          transform: translateY(-50%);
          text-align: center;
        }}
        #lt-kicker {{
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: {34 if V else 38}px;
          letter-spacing: 10px;
          color: #8a6a44;
        }}
        #lt-line {{
          width: {360 if V else 420}px;
          height: 3px;
          margin: 34px auto;
          background: #b08a5a;
          transform-origin: center;
        }}
        #lt-title {{
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: {TITLE_SIZE}px;
          line-height: 1.3;
          color: #4a3423;
        }}
        #lt-sub {{
          margin-top: 34px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: {40 if V else 44}px;
          color: #7a5b3c;
        }}
      </style>
      <div id="root" data-composition-id="title" data-width="{W}" data-height="{H}">
        <div id="lt-glow"></div>
{dots}        <div id="lt-wrap">
          <div id="lt-kicker">A LETTER OF THANKS</div>
          <div id="lt-line"></div>
          <div id="lt-title">{"기도후원자<br />영상편지" if V else "기도후원자 영상편지"}</div>
          <div id="lt-sub">기도로 함께해 주신 분들께</div>
        </div>
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
        tl.fromTo("#lt-glow", {{ scale: 0.7, opacity: 0.4 }}, {{ scale: 1.1, opacity: 1, duration: 5, ease: "sine.out" }}, 0);
        tl.fromTo(".lt-dot", {{ opacity: 0, y: 30 }}, {{ opacity: 0.9, y: -60, duration: 5, ease: "none", stagger: 0.04 }}, 0);
        tl.fromTo("#lt-kicker", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power2.out" }}, 0.3);
        tl.fromTo("#lt-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.9, ease: "power2.inOut" }}, 0.6);
        tl.fromTo("#lt-title", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 1.2, ease: "power2.out" }}, 0.9);
        tl.fromTo("#lt-sub", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, 1.8);
        tl.to("#lt-wrap", {{ opacity: 0, duration: 0.6, ease: "power1.in" }}, 4.4);
        window.__timelines["title"] = tl;
      </script>
    </template>
  </body>
</html>
'''
open("compositions/title.html", "w").write(comp)
open("index.html", "w").write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>기도후원자 영상편지</title>
    <script src="gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #f3dfc0; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #f3dfc0; }}
    </style>
  </head>
  <body>
    <!-- Title page only; the received clips get appended after it with ffmpeg. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="5" data-width="{W}" data-height="{H}">
      <div id="title" data-composition-id="title" data-composition-src="compositions/title.html"
        data-start="0" data-duration="5" data-track-index="0" data-width="{W}" data-height="{H}"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
