# ③ 데이터 스토리 — the story told in numbers: 993 → 1,033 years → 3,600 t → 89 m → 2026.11.3.
# Clean editorial infographics (Pretendard) on deep navy, the submarine render drawn to scale.
from lib import GOLD, HIT, DUR, comp, index, setup, write, pop, out

INK, SKY = "#071a33", "#7cc7ff"
css = f'''        #bg {{
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse at 50% 30%, #12345f 0%, {INK} 70%);
        }}
        #grid {{
          position: absolute;
          inset: 0;
          background-image: linear-gradient(rgba(124, 199, 255, 0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(124, 199, 255, 0.07) 1px, transparent 1px);
          background-size: 60px 60px;
        }}
        .card {{
          position: absolute;
          left: 90px;
          right: 90px;
          opacity: 0;
        }}
        .tag {{
          display: inline-block;
          padding: 8px 20px;
          border: 2px solid {SKY};
          border-radius: 999px;
          font-family: "Pretendard", sans-serif;
          font-weight: 700;
          font-size: 30px;
          color: {SKY};
          letter-spacing: 2px;
        }}
        .num {{
          margin-top: 18px;
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          font-size: 250px;
          line-height: 1;
          color: #ffffff;
          letter-spacing: -6px;
          white-space: nowrap;
        }}
        .num small {{
          font-size: 90px;
          font-weight: 800;
          margin-left: 10px;
          letter-spacing: 0;
          color: {GOLD};
        }}
        .cap {{
          margin-top: 18px;
          font-family: "Pretendard", sans-serif;
          font-weight: 500;
          font-size: 46px;
          line-height: 1.4;
          color: #d8e6f5;
        }}
        .cap b {{
          font-weight: 800;
          color: #ffffff;
        }}
        #tl-line {{
          position: absolute;
          left: 140px;
          right: 140px;
          top: 1320px;
          height: 6px;
          background: rgba(124, 199, 255, 0.35);
          transform-origin: 0 50%;
          opacity: 0;
        }}
        #tl-fill {{
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 100%;
          background: {GOLD};
          transform-origin: 0 50%;
        }}
        .tl-pt {{
          position: absolute;
          top: 1290px;
          width: 66px;
          height: 66px;
          margin-left: -33px;
          border-radius: 50%;
          background: {INK};
          border: 6px solid {GOLD};
          opacity: 0;
        }}
        .tl-lab {{
          position: absolute;
          top: 1380px;
          width: 300px;
          margin-left: -150px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 44px;
          color: #ffffff;
          opacity: 0;
        }}
        .tl-lab span {{
          display: block;
          font-weight: 500;
          font-size: 30px;
          color: {SKY};
        }}
        #sub {{
          position: absolute;
          left: 90px;
          width: 900px;
          top: 1230px;
          opacity: 0;
        }}
        #ruler {{
          position: absolute;
          left: 90px;
          width: 900px;
          top: 1630px;
          height: 40px;
          border-left: 4px solid {GOLD};
          border-right: 4px solid {GOLD};
          opacity: 0;
        }}
        #ruler i {{
          position: absolute;
          left: 0;
          right: 0;
          top: 18px;
          height: 4px;
          background: {GOLD};
          transform-origin: 50% 50%;
        }}
        #ruler b {{
          position: absolute;
          left: 0;
          right: 0;
          top: 50px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 48px;
          color: {GOLD};
        }}
        #hit {{
          position: absolute;
          inset: 0;
          background: #ffffff;
          opacity: 0;
        }}
        #name {{
          position: absolute;
          left: 0;
          right: 0;
          top: 330px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 900;
          font-size: 260px;
          letter-spacing: -8px;
          color: #ffffff;
          opacity: 0;
        }}
        #name-en {{
          position: absolute;
          left: 0;
          right: 0;
          top: 660px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 700;
          font-size: 36px;
          letter-spacing: 22px;
          color: {SKY};
          opacity: 0;
        }}
        #congr {{
          position: absolute;
          left: 0;
          right: 0;
          top: 780px;
          text-align: center;
          font-family: "Pretendard", sans-serif;
          font-weight: 800;
          font-size: 76px;
          line-height: 1.3;
          color: #ffffff;
          opacity: 0;
        }}
        #congr span {{
          color: {GOLD};
        }}
        #sign {{
          position: absolute;
          left: 0;
          right: 0;
          top: 1430px;
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
          color: #ffffff;
        }}
        #sign i {{
          width: 3px;
          height: 76px;
          background: {GOLD};
        }}
        #src {{
          position: absolute;
          left: 90px;
          right: 90px;
          bottom: 40px;
          font-family: "Pretendard", sans-serif;
          font-weight: 500;
          font-size: 22px;
          color: rgba(216, 230, 245, 0.55);
          opacity: 0;
        }}
'''
body = '''        <div id="bg"></div>
        <div id="grid"></div>
        <div id="c1" class="card" style="top:380px">
          <div class="tag">YEAR</div>
          <div class="num"><span id="n1">0</span><small>년</small></div>
          <div class="cap">거란의 대군 앞에서<br /><b>서희</b>는 칼 대신 말로 나라를 지켰다</div>
        </div>
        <div id="c2" class="card" style="top:380px">
          <div class="tag">YEARS LATER</div>
          <div class="num"><span id="n2">0</span><small>년 뒤</small></div>
          <div class="cap">그 이름이<br /><b>바다를 지키는 잠수함</b>이 된다</div>
        </div>
        <div id="tl-line"><div id="tl-fill"></div></div>
        <div id="p1" class="tl-pt" style="left:200px"></div>
        <div id="p2" class="tl-pt" style="left:880px"></div>
        <div id="l1" class="tl-lab" style="left:200px">993<span>강동 6주 담판</span></div>
        <div id="l2" class="tl-lab" style="left:880px">2026<span>서희함 진수</span></div>
        <div id="c3" class="card" style="top:380px">
          <div class="tag">DISPLACEMENT</div>
          <div class="num"><span id="n3">0</span><small>톤급</small></div>
          <div class="cap">장보고-Ⅲ 배치-Ⅱ <b>2번함</b></div>
        </div>
        <img id="sub" src="assets/sub-render.png" alt="" />
        <div id="ruler"><i></i><b>길이 약 89m</b></div>
        <div id="hit"></div>
        <div id="name">서희함</div>
        <div id="name-en">ROKS SEO HUI</div>
        <div id="congr"><span>2026. 11. 3.</span><br />진수를 축하합니다</div>
        <div id="sign"><img src="assets/icheon-logo-dark.png" alt="이천시" /><i></i><div>경기도 이천시</div></div>
        <div id="src">수치: 해군·언론 보도 기준(3,600톤급, 길이 약 89m) · 잠수함 이미지는 3D 연출</div>
'''


def count(sel, target, a, dur, fmt="Math.round(v)"):
    return (f'        {{ const o = {{ v: 0 }}; tl.to(o, {{ v: {target}, duration: {dur}, ease: "power2.out", '
            f'onUpdate: () => {{ const v = o.v; document.querySelector("{sel}").textContent = {fmt}; }} }}, {a}); }}\n')


js = pop("#c1", 0.2, 60, 0.6) + count("#n1", 993, 0.3, 1.4) + out("#c1", 3.0, 0.3)
js += pop("#c2", 3.3, 60, 0.5) + count("#n2", 1033, 3.4, 1.4, 'Math.round(v).toLocaleString("en-US")')
js += '        tl.set("#tl-line", { opacity: 1 }, 3.6);\n'
js += '        tl.fromTo("#tl-fill", { scaleX: 0 }, { scaleX: 1, duration: 2.0, ease: "power2.inOut" }, 3.8);\n'
js += pop("#p1, #l1", 3.7, 20, 0.4) + pop("#p2, #l2", 5.6, 20, 0.4)
js += out("#c2, #tl-line, #p1, #p2, #l1, #l2", 6.6, 0.3)
js += pop("#c3", 6.9, 60, 0.5) + count("#n3", 3600, 7.0, 1.6, 'Math.round(v).toLocaleString("en-US")')
js += '        tl.fromTo("#sub", { opacity: 0, x: 300 }, { opacity: 1, x: 0, duration: 1.0, ease: "power3.out" }, 7.2);\n'
js += '        tl.set("#ruler", { opacity: 1 }, 8.2);\n'
js += '        tl.fromTo("#ruler i", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power3.out" }, 8.2);\n'
js += pop("#ruler b", 8.6, 10, 0.4) + pop("#src", 7.2, 0, 0.6)
js += out("#c3, #ruler, #src", HIT - 0.15, 0.15)
# hit: white flash, the name lands, the submarine slides up under it
js += f'        tl.to("#hit", {{ keyframes: [{{ opacity: 1, duration: 0.05 }}, {{ opacity: 0, duration: 0.6 }}] }}, {HIT - 0.05});\n'
js += f'        tl.fromTo("#name", {{ opacity: 0, scale: 1.8 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power4.out" }}, {HIT});\n'
js += f'        tl.to("#sub", {{ top: 980, duration: 1.2, ease: "power3.inOut" }}, {HIT + 0.2});\n'.replace("top: 980", "y: -250")
js += pop("#name-en", 10.8, 10, 0.5) + pop("#congr", 12.0, 30, 0.7)
js += '        tl.fromTo("#sign", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 14.0);\n'
js += '        tl.fromTo("#sub", { scale: 1 }, { scale: 1.06, duration: 9, ease: "none" }, 12.0);\n'
js += out("#name, #name-en, #congr, #sign, #sub", 20.2, 0.7)

d = setup("data")
write(d, {"data": comp("data", ["pre"], css, body, js)},
      index("서희함 · 데이터 스토리", "③ data story short. Submarine: Meshy 7.1 model rendered in Blender; score: Lyria 3 Pro cut.", [("data", 0, DUR)]))
print("ok")
