# Shared helpers for the style-test reels (1080x1920 HyperFrames projects).
FONTS = {
    "bhs": [("Black Han Sans", 400, "black-han-sans-latin-400-normal", "U+0000-00FF, U+2190-21FF"),
            ("Black Han Sans", 400, "black-han-sans-korean-400-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")],
    "noto": [("Noto Sans KR", w, f"noto-sans-kr-{sub}-{w}-normal", rng) for w in (500, 800)
             for sub, rng in (("latin", "U+0000-00FF, U+2190-21FF"), ("korean", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"))],
    "brush": [("Nanum Brush Script", 400, "nanum-brush-script-latin-400-normal", "U+0000-00FF"),
              ("Nanum Brush Script", 400, "nanum-brush-script-korean-400-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")],
    "myeongjo": [("Nanum Myeongjo", 800, "nanum-myeongjo-latin-800-normal", "U+0000-00FF"),
                 ("Nanum Myeongjo", 800, "nanum-myeongjo-korean-800-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF")],
}


def faces(*names):
    out = ""
    for n in names:
        for fam, w, f, rng in FONTS[n]:
            out += f'''        @font-face {{
          font-family: "{fam}";
          font-weight: {w};
          src: url("fonts/{f}.woff2") format("woff2");
          unicode-range: {rng};
        }}
'''
    return out


def comp(cid, fonts, css, body, js):
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
{faces(*fonts)}        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
        }}
{css}      </style>
      <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}      </div>
      <script>
{js}      </script>
    </template>
  </body>
</html>
'''


def index(title, cid, dur, comment, bg="#000", scripts=("gsap.min.js",)):
    tags = "".join(f'    <script src="{s}"></script>\n' for s in scripts)
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>{title}</title>
{tags}    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      html,
      body {{
        width: 1080px;
        height: 1920px;
        overflow: hidden;
        background: {bg};
      }}
      #root {{
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: {bg};
      }}
    </style>
  </head>
  <body>
    <!-- {comment} -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="0" data-duration="{dur}" data-track-index="0" data-width="1080" data-height="1920"></div>
      <audio id="soundtrack" src="assets/audio/music.mp3" data-start="0" data-duration="{dur}" data-track-index="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
