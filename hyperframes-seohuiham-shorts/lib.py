# Shared helpers for the five 서희함 shorts (1080x1920, 21 s). Each style lives in its own
# HyperFrames project folder (kinetic/, data/, map/, doodle/, paper/) that links shared/
# fonts and assets. Common beats: story of Seo Hui 0-10 s, the score's hit at 10.05 s =
# "서희함", celebration and sign-off 10-21 s.
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H, DUR, HIT = 1080, 1920, 21, 10.05
GOLD = "#e3b25a"

_PRE = {200: "ExtraLight", 300: "Light", 500: "Medium", 700: "Bold", 800: "ExtraBold", 900: "Black"}


def _fontsource(name, family, weight):
    css = open(os.path.join(ROOT, "shared/fonts", f"{name}-{weight}.css")).read()
    out = ""
    for block in re.findall(r"@font-face \{.*?\}", css, re.S):
        src = re.search(r"url\(\./files/([^)]+\.woff2)\)", block).group(1)
        rng = re.search(r"unicode-range: ([^;]+);", block).group(1)
        out += f'''        @font-face {{
          font-family: "{family}";
          font-weight: {weight};
          src: url("fonts/{src}") format("woff2");
          unicode-range: {rng};
        }}
'''
    return out


def faces(*names):
    out = ""
    for n in names:
        if n == "pre":
            out += "".join(f'''        @font-face {{
          font-family: "Pretendard";
          font-weight: {w};
          src: url("fonts/Pretendard-{f}.woff2") format("woff2");
        }}
''' for w, f in _PRE.items())
        elif n == "gaegu":
            out += _fontsource("gaegu", "Gaegu", 700)
        elif n == "dohyeon":
            out += _fontsource("do-hyeon", "Do Hyeon", 400)
        elif n == "gowun":
            out += _fontsource("gowun-dodum", "Gowun Dodum", 400)
        elif n == "jua":
            out += _fontsource("jua", "Jua", 400)
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


def index(title, comment, layers, bg="#000", p5=False):
    """layers: [(cid, start, dur)] stacked bottom to top; music on the last track"""
    tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i}" data-width="{W}" data-height="{H}"></div>
''' for i, (c, s, d) in enumerate(layers))
    p5tag = '    <script src="p5.min.js"></script>\n' if p5 else ""
    return f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>{title}</title>
    <script src="gsap.min.js"></script>
{p5tag}    <style>
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <audio id="soundtrack" src="assets/music.mp3" data-start="0" data-duration="{DUR}" data-track-index="{len(layers)}"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''


def setup(style):
    """create/refresh the project folder for one style and return its path"""
    d = os.path.join(ROOT, style)
    os.makedirs(os.path.join(d, "compositions"), exist_ok=True)
    for name, target in (("fonts", "../shared/fonts"), ("assets", "../shared/assets"),
                         ("gsap.min.js", "../shared/gsap.min.js"), ("p5.min.js", "../shared/p5.min.js"),
                         ("node_modules", "../../hyperframes-kra-film/node_modules")):
        p = os.path.join(d, name)
        if not os.path.lexists(p):
            os.symlink(target, p)
    open(os.path.join(d, "package.json"), "w").write(
        '{\n  "name": "seohuiham-' + style + '",\n  "private": true,\n  "type": "module",\n'
        '  "devDependencies": {\n    "hyperframes": "0.8.82"\n  }\n}\n')
    open(os.path.join(d, "hyperframes.json"), "w").write(
        '{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n'
        '  "paths": { "blocks": "compositions", "assets": "assets" },\n  "media": { "autoProxy": true }\n}\n')
    return d


def write(d, files, html):
    for k, v in files.items():
        open(os.path.join(d, "compositions", f"{k}.html"), "w").write(v)
    open(os.path.join(d, "index.html"), "w").write(html)


def pop(sel, a, y=40, dur=0.6, ease="power3.out"):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "{ease}" }}, {a});\n'


def out(sel, a, dur=0.4):
    return f'        tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {a});\n'
