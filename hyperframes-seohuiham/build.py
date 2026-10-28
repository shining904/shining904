# 서희함 진수 축하 영상 — 웅장한 버전 「천 년의 지혜, 바다를 지키다」 (1920x1080, 73 s).
# Focus on the two heroes: Seo Hui and the submarine. Cut to the Lyria trailer score (epic.mp3):
#   0-7    open      Seedance    pre-dawn sea, narration 1 set as kinetic type
#   7-15   cliff     Seedance    Seo Hui on the dawn cliff, crane shot, name card
#   15-23  front     Seedance    the submarine emerges head-on from the deep, narration 3
#   23-31  side      Seedance    the submarine glides under the sunlit surface
#   31-47  title     Seedance    slowed approaching hull; 서·희·함 slam in syllable by syllable on
#                                   the score's big hit (36 s), light sweep, motto
#   46-62  speech    Seedance+lipsync  Seo Hui's congratulation
#   61-73  finale    Seedance    the submarine surfaces at sunrise, closing card
# The earlier, history-led cut lives in build_v1.py. Run: python3 build.py
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, DUR = 1920, 1080, 73
GOLD = "#e3b25a"
FONTS = {
    "myeongjo": [("Nanum Myeongjo", 800, "nanum-myeongjo-latin-800-normal", "U+0000-00FF"),
                 ("Nanum Myeongjo", 800, "nanum-myeongjo-korean-800-normal", "U+1100-11FF, U+3130-318F, U+AC00-D7AF, U+4E00-9FFF")],
    "noto": [("Noto Sans KR", w, f"noto-sans-kr-{s}-{w}-normal", r) for w in (500, 800)
             for s, r in (("latin", "U+0000-00FF, U+2160-216F"), ("korean", "U+1100-11FF, U+3130-318F, U+AC00-D7AF"))],
}


def faces(*names):
    return "".join(f'''        @font-face {{
          font-family: "{f}";
          font-weight: {w};
          src: url("fonts/{n}.woff2") format("woff2");
          unicode-range: {r};
        }}
''' for k in names for f, w, n, r in FONTS[k])


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


def pop(sel, a, y=30, dur=0.9, ease="power3.out"):
    return f'        tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {dur}, ease: "{ease}" }}, {a});\n'


def out(sel, a, dur=0.6):
    return f'        tl.to("{sel}", {{ opacity: 0, duration: {dur}, ease: "power1.in" }}, {a});\n'


def reveal(sel, a, dur=1.2):
    """letters fade up out of a blur, like a film title"""
    return (f'        tl.fromTo("{sel}", {{ opacity: 0, scale: 1.12, filter: "blur(14px)" }}, '
            f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: {dur}, ease: "power2.out" }}, {a});\n')


TITLE_CSS = f'''        .ttl {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          color: #f7efe0;
          text-shadow: 0 6px 40px rgba(0, 0, 0, 0.7);
        }}
        .gold {{
          background: linear-gradient(180deg, #fff3cf 0%, {GOLD} 45%, #9a6a1c 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          text-shadow: none;
          filter: drop-shadow(0 4px 24px rgba(0, 0, 0, 0.6));
        }}
'''


def clip(cid, src, dur, extra_css="", extra_body="", extra_js="", fade_in=0.8, push=(1.0, 1.06), grade=""):
    return comp(cid, ["myeongjo", "noto"], f'''        #{cid}-fade {{
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
          {grade}
        }}
        #{cid}-bars {{
          position: absolute;
          inset: 0;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.55) 0%, rgba(0, 0, 0, 0) 18%, rgba(0, 0, 0, 0) 78%, rgba(0, 0, 0, 0.6) 100%);
        }}
{TITLE_CSS}{extra_css}''', f'''        <div id="{cid}-fade">
          <video id="{cid}-video" src="{src}" data-start="0" data-duration="{dur}" muted playsinline></video>
          <div id="{cid}-bars"></div>
{extra_body}        </div>
''', f'''        tl.fromTo("#{cid}-fade", {{ opacity: 0 }}, {{ opacity: 1, duration: {fade_in}, ease: "none" }}, 0);
        tl.fromTo("#{cid}-video", {{ scale: {push[0]} }}, {{ scale: {push[1]}, duration: {dur}, ease: "none" }}, 0);
{extra_js}''')


SCENES = [("open", 0, 7.6, 0), ("cliff", 7.0, 8.4, 1), ("front", 15.0, 8.4, 2), ("side", 23.0, 8.4, 3),
          ("title", 31.0, 15.9, 4), ("speech", 46.4, 14.6, 5), ("finale", 60.6, 12.4, 6)]
LINES = [("e1.mp3", 1.6, 4.68, "천 년 전, 칼 대신 지혜로 나라를 지킨 사람이 있었습니다."),
         ("e2.mp3", 9.6, 2.1, "고려의 외교관, 서희."),
         ("e3.mp3", 17.2, 2.86, "이제 그 이름이, 바다를 지킵니다."),
         ("s2.mp3", 46.5, 14.6, None)]
SPEECH = [(0.0, 1.15, "서희함 장병 여러분."), (1.73, 5.55, "천 년 전 저는 칼 대신 지혜로 이 땅을 지켰습니다."),
          (6.14, 9.74, "이제 제 이름이 바다 깊은 곳에서 나라를 지킵니다."),
          (10.21, 14.6, "이천시민들과 함께, 서희함의 안전한 항해를 응원합니다.")]
files = {}

# ---------------------------------------------------------------- kinetic helpers
KIN_CSS = f'''        .kin {{
          position: absolute;
          left: 0;
          right: 0;
          text-align: center;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          color: #f7efe0;
          text-shadow: 0 4px 30px rgba(0, 0, 0, 0.75);
          white-space: nowrap;
        }}
        .kin .w {{
          display: inline-block;
        }}
        .rule {{
          position: absolute;
          height: 2px;
          background: linear-gradient(90deg, rgba(227, 178, 90, 0) 0%, {GOLD} 50%, rgba(227, 178, 90, 0) 100%);
          transform-origin: 50% 50%;
        }}
        .hud {{
          position: absolute;
          font-family: "Noto Sans KR", sans-serif;
          color: #e9f4ff;
          text-shadow: 0 2px 12px rgba(0, 0, 0, 0.8);
        }}
'''


def words(text, cls="w"):
    return "".join(f'<span class="{cls}">{w}</span>' + ("&nbsp;" if i < len(text.split()) - 1 else "")
                   for i, w in enumerate(text.split()))


def stagger_in(sel, a, each=0.12, dur=0.9):
    """words rise out of a soft blur one after another"""
    return (f'        tl.fromTo("{sel}", {{ opacity: 0, y: 40, filter: "blur(12px)" }}, '
            f'{{ opacity: 1, y: 0, filter: "blur(0px)", duration: {dur}, ease: "power3.out", stagger: {each} }}, {a});\n')


def rule_in(sel, a, dur=1.0):
    return f'        tl.fromTo("{sel}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {dur}, ease: "power3.inOut" }}, {a});\n'


# ---------------------------------------------------------------- open: pre-dawn sea + kinetic lines
files["open"] = clip("open", "assets/clips/sea-open.mp4", 7.6, KIN_CSS + '''        #open-l1 {
          top: 330px;
          font-size: 64px;
          color: #d9c9ab;
          letter-spacing: 18px;
        }
        #open-l2 {
          top: 430px;
          font-size: 110px;
        }
        #open-l3 {
          top: 590px;
          font-size: 64px;
        }
        #open-r1 {
          left: 660px;
          width: 600px;
          top: 560px;
        }
        #open-dark {
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0.2) 0%, rgba(0, 0, 0, 0.65) 100%);
        }
        #open-white {
          position: absolute;
          inset: 0;
          background: #fff3dc;
          opacity: 0;
        }
''', f'''          <div id="open-dark"></div>
          <div id="open-l1" class="kin">천 년 전</div>
          <div id="open-l2" class="kin">{words("칼 대신 지혜로", "w o2")}</div>
          <div id="open-r1" class="rule"></div>
          <div id="open-l3" class="kin">{words("나라를 지킨 사람이 있었다", "w o3")}</div>
          <div id="open-white"></div>
''', '        tl.fromTo("#open-l1", { opacity: 0, letterSpacing: "40px" }, { opacity: 1, letterSpacing: "18px", duration: 1.6, ease: "power2.out" }, 0.8);\n'.replace('letterSpacing: "40px"', 'scale: 1.15').replace('letterSpacing: "18px"', 'scale: 1')
    + stagger_in(".o2", 2.4, 0.18, 1.0) + rule_in("#open-r1", 3.4, 1.2) + stagger_in(".o3", 4.0, 0.14, 0.9)
    + '        tl.to("#open-white", { opacity: 1, duration: 0.6, ease: "power2.in" }, 7.0);\n',
    fade_in=1.6, push=(1.0, 1.08), grade="filter: brightness(0.85) contrast(1.05);")

# ---------------------------------------------------------------- cliff: Seo Hui, kinetic name card
files["cliff"] = clip("cliff", "assets/clips/cliff.mp4", 8.4, KIN_CSS + f'''        #cliff-han {{
          position: absolute;
          left: 60px;
          top: 520px;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 330px;
          color: rgba(255, 236, 200, 0.1);
          -webkit-text-stroke: 2px rgba(255, 236, 200, 0.55);
          white-space: nowrap;
        }}
        #cliff-name {{
          left: 150px;
          right: auto;
          top: 650px;
          text-align: left;
          font-size: 150px;
        }}
        #cliff-r {{
          left: 150px;
          width: 520px;
          top: 840px;
          transform-origin: 0 50%;
          background: linear-gradient(90deg, {GOLD} 0%, rgba(227, 178, 90, 0) 100%);
        }}
        #cliff-sub {{
          left: 154px;
          top: 862px;
          font-size: 32px;
          font-weight: 500;
          letter-spacing: 8px;
        }}
''', '''          <div id="cliff-han">徐熙</div>
          <div id="cliff-name" class="ttl gold">서희</div>
          <div id="cliff-r" class="rule"></div>
          <div id="cliff-sub" class="hud">고려의 외교관 · 942–998</div>
''', '        tl.fromTo("#cliff-han", { opacity: 0, x: -120 }, { opacity: 1, x: 40, duration: 6.0, ease: "power1.out" }, 1.6);\n'
    + reveal("#cliff-name", 2.4, 1.4) + '        tl.fromTo("#cliff-r", { scaleX: 0 }, { scaleX: 1, duration: 1.0, ease: "power3.inOut" }, 3.2);\n'
    + pop("#cliff-sub", 3.6, 10) + out("#cliff-han, #cliff-name, #cliff-r, #cliff-sub", 7.2, 0.8),
    fade_in=0.4, push=(1.04, 1.0))

# ---------------------------------------------------------------- front: kinetic line over the approaching hull
files["front"] = clip("front", "assets/clips/sub-front.mp4", 8.4, KIN_CSS + '''        #front-l1 {
          top: 360px;
          font-size: 70px;
          color: #cfe6ff;
        }
        #front-l2 {
          top: 470px;
          font-size: 140px;
        }
        #front-r {
          left: 610px;
          width: 700px;
          top: 650px;
        }
''', f'''          <div id="front-l1" class="kin">{words("이제 그 이름이,", "w f1")}</div>
          <div id="front-l2" class="kin">{words("바다를 지킵니다", "w f2")}</div>
          <div id="front-r" class="rule"></div>
''', stagger_in(".f1", 2.0, 0.12, 0.8) + stagger_in(".f2", 3.0, 0.2, 1.0) + rule_in("#front-r", 3.8, 1.2)
    + out("#front-l1, #front-l2, #front-r", 7.4, 0.8), fade_in=0.4, push=(1.0, 1.08))

# ---------------------------------------------------------------- side: HUD callouts on the hull
files["side"] = clip("side", "assets/clips/sub-side.mp4", 8.4, KIN_CSS + f'''        .call {{
          position: absolute;
          border-left: 2px solid {GOLD};
          padding-left: 18px;
        }}
        .call b {{
          display: block;
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 64px;
          color: #ffffff;
        }}
        .call span {{
          font-size: 26px;
          letter-spacing: 6px;
          color: #bfe0ff;
        }}
        .dot {{
          position: absolute;
          width: 16px;
          height: 16px;
          margin: -8px 0 0 -8px;
          border-radius: 50%;
          border: 2px solid {GOLD};
          box-shadow: 0 0 14px {GOLD};
        }}
        #side-c1 {{
          left: 1180px;
          top: 150px;
        }}
        #side-c2 {{
          left: 260px;
          top: 760px;
        }}
        #side-c3 {{
          left: 1250px;
          top: 760px;
        }}
''', '''          <div id="side-d1" class="dot" style="left:1060px;top:300px"></div>
          <div id="side-c1" class="call hud"><b><span id="side-ton">0</span>톤급</b><span>DISPLACEMENT</span></div>
          <div id="side-c2" class="call hud"><b>장보고-Ⅲ 배치-Ⅱ</b><span>2번함 · 2026. 11. 3. 진수</span></div>
          <div id="side-c3" class="call hud"><b>국산화율 약 80%</b><span>K-SUBMARINE</span></div>
''', '        tl.fromTo("#side-d1", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, 1.0);\n'
    + '        tl.fromTo(".call", { opacity: 0, x: -40, clipPath: "inset(0 100% 0 0)" }, { opacity: 1, x: 0, clipPath: "inset(0 0% 0 0)", duration: 0.9, ease: "power3.out", stagger: 1.1 }, 1.3);\n'
    + '        { const o = { v: 0 }; tl.to(o, { v: 3600, duration: 1.6, ease: "power2.out", onUpdate: () => { document.querySelector("#side-ton").textContent = Math.round(o.v).toLocaleString("en-US"); } }, 1.3); }\n'
    + out(".call, #side-d1", 7.5, 0.6), fade_in=0.5, push=(1.0, 1.05))

# ---------------------------------------------------------------- title: letters slam over the slowed hull
files["title"] = clip("title", "assets/clips/title-bg.mp4", 15.9, KIN_CSS + f'''        #title-dim {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 42%, rgba(2, 14, 28, 0.35) 0%, rgba(2, 10, 20, 0.85) 100%);
        }}
        #title-flash {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 42%, rgba(255, 240, 205, 0.9) 0%, rgba(255, 240, 205, 0) 55%);
          mix-blend-mode: screen;
          opacity: 0;
        }}
        #title-name {{
          top: 250px;
          font-size: 250px;
          letter-spacing: 40px;
          padding-left: 40px;
        }}
        #title-name .c {{
          display: inline-block;
        }}
        #title-sweep {{
          position: absolute;
          left: 0;
          top: 250px;
          width: 1920px;
          height: 300px;
          background: linear-gradient(100deg, rgba(255, 255, 255, 0) 40%, rgba(255, 248, 225, 0.55) 50%, rgba(255, 255, 255, 0) 60%);
          mix-blend-mode: overlay;
        }}
        #title-r1 {{
          left: 560px;
          width: 800px;
          top: 560px;
        }}
        #title-en {{
          top: 585px;
          font-size: 34px;
          font-weight: 500;
          letter-spacing: 28px;
          color: #cfe6ff;
          left: 0;
          right: 0;
          text-align: center;
        }}
        #title-motto {{
          top: 690px;
          font-size: 66px;
        }}
''', '''          <div id="title-dim"></div>
          <div id="title-name" class="kin gold"><span class="c">서</span><span class="c">희</span><span class="c">함</span></div>
          <div id="title-sweep"></div>
          <div id="title-r1" class="rule"></div>
          <div id="title-en" class="hud">ROKS SEO HUI</div>
          <div id="title-motto" class="kin">천 년의 지혜, 바다를 지키다</div>
          <div id="title-flash"></div>
''', '        tl.set("#title-name .c", { opacity: 0 }, 0);\n'
    # each syllable slams on a beat leading into the score's big hit at ~5.3 s
    + "".join(f'        tl.fromTo("#title-name .c:nth-child({k + 1})", {{ opacity: 0, scale: 2.4, filter: "blur(16px)" }}, '
              f'{{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "power4.in" }}, {a});\n'
              for k, a in enumerate((3.7, 4.4, 5.05)))
    + '        tl.fromTo("#title-flash", { opacity: 0 }, { opacity: 1, duration: 0.07, ease: "none" }, 5.3);\n'
    + '        tl.to("#title-flash", { opacity: 0, duration: 1.3, ease: "power2.out" }, 5.37);\n'
    + '        tl.fromTo("#title-sweep", { x: -1400 }, { x: 1400, duration: 1.6, ease: "power2.inOut" }, 5.6);\n'
    + '        tl.fromTo("#title-name", { scale: 1 }, { scale: 1.05, duration: 9, ease: "none" }, 5.4);\n'
    + rule_in("#title-r1", 6.0, 1.2) + pop("#title-en", 6.6, 10) + stagger_in("#title-motto", 8.4, 0, 1.4)
    + out("#title-name, #title-r1, #title-en, #title-motto, #title-sweep", 14.6, 1.0),
    fade_in=1.2, push=(1.0, 1.04))

# ---------------------------------------------------------------- speech (lipsynced, new solemn voice)
files["speech"] = clip("speech", "assets/clips/speech-lip.mp4", 14.6, fade_in=1.0, push=(1.0, 1.04))

# ---------------------------------------------------------------- finale: kinetic close + logo
files["finale"] = clip("finale", "assets/clips/sub-surface.mp4", 12.4, KIN_CSS + '''        #fin-shade {
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          height: 680px;
          background: linear-gradient(180deg, rgba(0, 0, 0, 0.75) 0%, rgba(0, 0, 0, 0.6) 70%, rgba(0, 0, 0, 0) 100%);
        }
        #fin-shade2 {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 0;
          height: 460px;
          background: linear-gradient(0deg, rgba(0, 0, 0, 0.75) 0%, rgba(0, 0, 0, 0) 100%);
        }
        #fin-1 {
          top: 170px;
          font-size: 74px;
          color: #e9dcc4;
        }
        #fin-2 {
          top: 270px;
          font-size: 116px;
        }
        #fin-r {
          left: 610px;
          width: 700px;
          top: 430px;
        }
        #fin-3 {
          top: 455px;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 32px;
          letter-spacing: 6px;
        }
        #fin-sign {
          position: absolute;
          left: 0;
          right: 0;
          top: 800px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 34px;
        }
        #fin-logo {
          height: 130px;
          filter: drop-shadow(0 4px 18px rgba(0, 0, 0, 0.6));
        }
        #fin-from {
          font-family: "Nanum Myeongjo", serif;
          font-weight: 800;
          font-size: 54px;
          color: #ffffff;
          text-shadow: 0 4px 20px rgba(0, 0, 0, 0.7);
          letter-spacing: 6px;
        }
        #fin-bar {
          width: 2px;
          height: 90px;
          background: rgba(227, 178, 90, 0.9);
        }
        #fin-ai {
          position: absolute;
          right: 26px;
          bottom: 16px;
          font-family: "Noto Sans KR", sans-serif;
          font-size: 18px;
          color: rgba(255, 255, 255, 0.6);
        }
        #fin-black {
          position: absolute;
          inset: 0;
          background: #000;
          opacity: 0;
        }
''', f'''          <div id="fin-shade"></div>
          <div id="fin-shade2"></div>
          <div id="fin-1" class="kin">{words("서희함의 진수를", "w g1")}</div>
          <div id="fin-2" class="kin gold">{words("진심으로 축하합니다", "w g2")}</div>
          <div id="fin-r" class="rule"></div>
          <div id="fin-3" class="kin">천 년의 지혜와 함께, 안전한 항해를 기원합니다</div>
          <div id="fin-sign"><img id="fin-logo" src="assets/img/icheon-logo-dark.png" alt="이천시" /><div id="fin-bar"></div><div id="fin-from">경기도 이천시</div></div>
          <div id="fin-ai">본 영상은 AI로 제작되었으며 일부 장면은 연출입니다</div>
          <div id="fin-black"></div>
''', '        tl.fromTo("#fin-shade, #fin-shade2", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "none" }, 0.8);\n'
    + stagger_in(".g1", 1.2, 0.15, 0.9) + stagger_in(".g2", 2.0, 0.2, 1.1) + rule_in("#fin-r", 3.0, 1.2)
    + pop("#fin-3", 3.5, 10) + '        tl.fromTo("#fin-sign", { opacity: 0, y: 24, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 1.4, ease: "power3.out" }, 5.0);\n'
    + pop("#fin-ai", 5.4, 0) + '        tl.to("#fin-black", { opacity: 1, duration: 1.4, ease: "none" }, 10.2);\n',
    fade_in=1.0, push=(1.0, 1.06))


# ---------------------------------------------------------------- captions
caps = [(46.5 + a, 46.5 + b, c) for a, b, c in SPEECH]
files["caps"] = comp("caps", ["noto"], '''        .caps-line {
          position: absolute;
          left: 0;
          right: 0;
          bottom: 40px;
          text-align: center;
          font-family: "Noto Sans KR", sans-serif;
          font-weight: 500;
          font-size: 38px;
          color: #ffffff;
          opacity: 0;
        }
        .caps-line span {
          display: inline-block;
          padding: 8px 26px;
          border-radius: 12px;
          background: rgba(0, 0, 0, 0.5);
        }
''', "".join(f'        <div id="caps-c{k}" class="caps-line"><span>{c}</span></div>\n' for k, (_, _, c) in enumerate(caps)),
    "".join(f'        tl.fromTo("#caps-c{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "none" }}, {round(a, 2)});\n'
            f'        tl.to("#caps-c{k}", {{ opacity: 0, duration: 0.25, ease: "none" }}, {round(b + 0.25, 2)});\n'
            for k, (a, b, _) in enumerate(caps)))

for k, v in files.items():
    with open(f"compositions/{k}.html", "w") as fh:
        fh.write(v)

tracks = "".join(f'''      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html"
        data-start="{s}" data-duration="{d}" data-track-index="{i}" data-width="{W}" data-height="{H}"></div>
''' for c, s, d, i in SCENES)
with open("index.html", "w") as fh:
    fh.write(f'''<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>천 년의 지혜, 바다를 지키다</title>
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
    <!-- 서희함 진수 축하 영상 (웅장한 버전). Clips: Magnific Seedance 2.5 (+ veed lipsync); title-scene
         submarine: Meshy 7.1 rendered in Blender Cycles; sea and sonar: Canvas 2D; score: Lyria 3 Pro. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
{tracks}      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html"
        data-start="0" data-duration="{DUR}" data-track-index="7" data-width="{W}" data-height="{H}"></div>
      <audio id="soundtrack" src="assets/audio/mix.mp3" data-start="0" data-duration="{DUR}" data-track-index="8"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
os.makedirs("work", exist_ok=True)
with open("work/lines.json", "w") as fh:
    json.dump([[f, s, d] for f, s, d, _ in LINES], fh)
print("ok")
