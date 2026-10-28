# 16:9 (1920x1080) edition of the v4 gold short (mayor interview in the gold circle, hand-signed
# letter finale). It reuses build_gold4.py and re-lays it out: shapes re-fitted to the wide frame,
# the interview circle on the right with the mayor's name and words in a left column, everything
# else centred, and the 16:9 sunrise footage instead of the vertical launch clip in the finale.
# Same switches as build_gold4.py: MAYOR=<file>, GREEN=1.
import re
import lib

src = open("build_gold4.py").read()


def sub(a, b, count=1):
    global src
    assert src.count(a) == count, (src.count(a), a[:80])
    src = src.replace(a, b)


def restyle(el_id, style):
    """replace the inline style of the element with this id"""
    global src
    pat = re.compile(r'(id="' + el_id + r'"[^>]*?style=")[^"]*(")')
    assert len(pat.findall(src)) == 1, el_id
    src = pat.sub(lambda m: m.group(1) + style + m.group(2), src)


# frame size
sub("lib.DUR = DUR", "lib.DUR = DUR\nlib.W, lib.H = 1920, 1080")
sub("WIN = (540, 860, 360)", "WIN = (1300, 540, 360)")
# shapes: re-fit to the wide frame (the interview circle is already built from WIN)
sub('SHAPES = {"h0"', '''def fit(pts, s, cx, cy, ox, oy):
    return [[round((x - cx) * s + ox, 1), round((y - cy) * s + oy, 1)] for x, y in pts]


SHAPES = {"h0"''')
sub('LINE_OUT = 30.4', '''LINE_OUT = 30.4
SHAPES.update({"h0": flat(360, 1560, 560), "wave": wave(620, 44, 4, -40, 1960),
               "sub": fit(SHAPES["sub"], 1.0, 0, 1020, 420, 600), "under": flat(660, 1260, 545), "h1": flat(-40, 1960, 457)})''')
sub('''          width: 1080px;
          height: 1920px;''', '''          width: 1920px;
          height: 1080px;''')
sub('<canvas id="cv" width="1080" height="1920"></canvas>', '<canvas id="cv" width="1920" height="1080"></canvas>')
sub('<canvas id="grain" width="270" height="480"></canvas>', '<canvas id="grain" width="480" height="270"></canvas>')
# no vertical launch clip in 16:9: the sunrise footage carries the finale
sub('data-start="29.4" data-duration="3.2"', 'data-start="29.4" data-duration="8.1"')
src = re.sub(r'        <video id="v-launch-[ab]"[^\n]*\n', "", src)
src = re.sub(r"js \+= fade\(\"#v-launch-[ab]\"[^\n]*\n", "", src)
sub('fade("#v-launch-b", 36.6, 0.0, 0.7)', 'fade("#v-surf", 36.6, 0.0, 0.7)')
sub('.replace("assets/music.mp3"', '.replace("<title>서희함 · 금빛 한 줄 확장판</title>", "<title>서희함 · 금빛 한 줄 16:9</title>").replace("assets/music.mp3"')
sub('setup("gold4-green" if GREEN else "gold4")', 'setup("gold4-wide-green" if GREEN else "gold4-wide")')
sub('[("gold4", 0, DUR)]', '[("gold4wide", 0, DUR)]')
sub('{"gold4": comp("gold4"', '{"gold4wide": comp("gold4wide"')
# canvas maths
for a, b in [("createImageData(270, 480)", "createImageData(480, 270)"), ("i < 270 * 480", "i < 480 * 270"),
             ("const y = 1920 - (((r2 * 1920 + t * (14 + r3 * 30)) % 2100)) + 90;", "const y = 1080 - (((r2 * 1080 + t * (14 + r3 * 30)) % 1260)) + 90;"),
             ("const x = r1 * 1080 + Math.sin", "const x = r1 * 1920 + Math.sin"),
             ("ctx.createLinearGradient(0, 0, 1080, 0)", "ctx.createLinearGradient(0, 0, 1920, 0)"),
             ("ctx.ellipse(540, 1000, 60 + u * 900, 30 + u * 420", "ctx.ellipse(960, 560, 60 + u * 1100, 30 + u * 420"),
             ("ctx.clearRect(0, 0, 1080, 1920)", "ctx.clearRect(0, 0, 1920, 1080)")]:
    sub(a, b)
# text layout
LEFT = "left:140px;right:auto;text-align:left;"
restyle("t0", "top:400px;font-size:84px")
restyle("t1", "top:130px;font-size:200px;color:{GOLD}")
restyle("t1b", "top:370px;font-size:40px")
restyle("t2", "top:720px;font-size:76px")
restyle("t2b", "top:830px;font-size:52px;font-weight:300")
restyle("t3", LEFT + "top:600px;font-size:56px;line-height:1.35;font-weight:300;text-shadow:0 2px 12px rgba(0,0,0,0.8)")
restyle("t4", "top:130px;font-size:84px")
restyle("title", "top:240px;font-size:240px;font-weight:900;letter-spacing:-4px")
restyle("d2", "top:250px;font-size:104px;font-weight:800;text-shadow:0 3px 18px rgba(0,0,0,0.6)")
sub('</span>의<br />진수를 축하합니다</div>', '</span>의 진수를 축하합니다</div>')
restyle("fill-sub", "left:480px;top:400px;width:960px;height:400px;filter:brightness(0.92) contrast(1.05)")
restyle("co1", "left:750px;top:640px")
restyle("co2", "left:1220px;top:620px")
sub('<u style="height:230px"></u><div style="left:-210px;top:240px">', '<u style="height:150px"></u><div style="left:-210px;top:160px">')
sub('<u style="height:250px"></u><div style="left:-200px;top:260px">', '<u style="height:170px"></u><div style="left:-200px;top:180px">')
# id-level overrides appended after the base css
sub("\nbody = f'''", '''
css += """        #mname {
          left: 140px;
          right: auto;
          top: 330px;
          text-align: left;
        }
        #letter {
          right: 240px;
          top: 730px;
        }
        #ai-note {
          top: 1032px;
          font-size: 24px;
        }
"""
body = f\'\'\'''')
exec(compile(src, "build_gold4.py (wide)", "exec"))
